import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.schema.runnable import RunnableSequence
from SPARQLWrapper import SPARQLWrapper, JSON, SPARQLExceptions
import json
from logger import setup_logger
from prompts import Entity_Relation_prompt, Sparql_Query_prompt,Response_generator_prompt
from config import MODEL_API_KEY, MODEL_END_POINT
from helper import extract_entity
logger=setup_logger()

llm_connection = ChatOpenAI(
    api_key=MODEL_API_KEY,
    base_url=MODEL_END_POINT,
    model="mistral-large-instruct",
    temperature=0,
)

chain_Entitiy_Relationship = RunnableSequence(
    Entity_Relation_prompt  # Extract Entity and Relationship
    | llm_connection # Call LLM to process the first prompt 
)

def extract_entity_relationship_meaning(question):
    # Extrac entity, relationship and meaning
    try:
        response = chain_Entitiy_Relationship.invoke({"Question": question})
        response_value = response.content.strip().replace("```json", "").replace("```", "").replace("`", "")


        if not response_value:
            logger.warning("Received an empty response from chain_Entitiy_Relationship.")
            return None, "Error: Empty response received."
        
        try:
            response_data = json.loads(response_value)
        except json.JSONDecodeError as e:
            logger.error(f"JSON Decode Error: {e}, Response: {response_value}")
            return None, f"Failed to parse JSON: {e}"

        # Extract Entity, Relationship, and Meaning
        Entities = response_data.get("Entities")
        Relationships = response_data.get("Relationships")
        st.session_state.current_entites_relationships = {"Entities": Entities, "Relationshios": Relationships}

        missing_fields = []
        if not Entities:
            missing_fields.append("Entities")
        if not Relationships:
            missing_fields.append("Relationships")
        if missing_fields:
            missing_fields_str = ', '.join(missing_fields)
            logger.error(f"Missing fields in response data: {missing_fields_str}")
            # return None, f"Error: Missing fields: {missing_fields_str}"
            st.session_state.current_entites_relationships = "No Entities/Relatioships\navailabe yet"
            st.session_state.current_sparql_query = "No SPARQL query available yet"
            st.session_state.current_sparql_response = "No Response available yet"
            return None, f"Could not Find {missing_fields_str}, Please ask the valid Questions"
        logger.info(f"Extracted Entities: {Entities}, Relationships: {Relationships}")
        return Entities, Relationships

    except Exception as e:
        logger.exception("An unexpected error occurred during the extraction process.")
        st.session_state.current_entites_relationships = "No Entities/Relatioships\navailabe yet"
        st.session_state.current_sparql_query = "No SPARQL query available yet"
        st.session_state.current_sparql_response = "No Response available yet"
        return None, f"An unexpected error occurred: {str(e)}"


#Code Related to SPARQL Query Generation
chain_Sparql_Query = RunnableSequence(
    Sparql_Query_prompt
    | llm_connection # Call LLM to generate the Sparql Query
)

chain_response_generator = RunnableSequence(
    Response_generator_prompt
    | llm_connection # Call LLM to generate the Sparql Query
)
def generate_response(question, response):
    st.session_state.current_sparql_response = response
    try:
        final_response_generator = chain_response_generator.invoke({"Question": question, "SPARQL_Response": response})
        if final_response_generator.content and isinstance(final_response_generator.content, str):
            return final_response_generator.content.strip()
        else:
            st.session_state.current_sparql_query = "No SPARQL query available yet"
            st.session_state.current_sparql_response = "No Response available yet"
            return "No valid response received from the LLM."
    except Exception as e:
        st.session_state.current_sparql_query = "No SPARQL query available yet"
        st.session_state.current_sparql_response = "No Response available yet"
        return f"An error occurred while fetching the response: {str(e)}"

def generate_sparql_query(Entities, Relationships,question):
    # Generate SPARQL Query
    try:
        sparql_query_response = chain_Sparql_Query.invoke({"Entities": Entities, "Relationships": Relationships})
        
        if not sparql_query_response.content.strip():
            logger.warning("Empty response received from chain_Sparql_Query.")
            return "Error: No SPARQL query generated."
        
        cleaned_response = sparql_query_response.content.strip().replace("```SPARQL", "").replace("```", "").replace("`", "")
        logger.info(f"Generated SPARQL query: {cleaned_response}")
        st.session_state.current_sparql_query = cleaned_response
    
        # Define the DBpedia endpoint
        endpoint_url = "https://dbpedia.org/sparql"

        # Create a SPARQLWrapper object
        sparql = SPARQLWrapper(endpoint_url)
        sparql.setQuery(cleaned_response)
        sparql.setReturnFormat(JSON)

        try:
            results = sparql.query().convert()
            bindings = results.get("results", {}).get("bindings", [])
            
            if bindings:
                all_results = [binding[list(binding.keys())[0]]["value"] for binding in bindings]
                logger.info(f"Query results: {all_results}")
                
                # entities = [extract_entity(uri) for uri in all_results]
                # return "\n".join(entities)
                final_output = generate_response(question, all_results)
                return final_output
            else:
                logger.info("No relevant data found for the Question.")
                st.session_state.current_sparql_query = "No SPARQL query available yet"
                st.session_state.current_sparql_response = "No Response available yet"
                return "No relevant data found for the Question."
                
        except Exception as e:
            logger.error(f"Error executing SPARQL query: {e}")
            st.session_state.current_sparql_query = "No SPARQL query available yet"
            st.session_state.current_sparql_response = "No Response available yet"
            return f"An issue occurred while querying DBpedia. Please check the query or try again later. Error: {str(e)}"
        
        except SPARQLExceptions.QueryBadFormed as e:
            logger.error(f"SPARQL QueryBadFormed Error: {e}")
            st.session_state.current_sparql_query = "No SPARQL query available yet"
            st.session_state.current_sparql_response = "No Response available yet"
            return None  # Return None if the query is malformed

    except Exception as e:
        logger.error(f"Error generating SPARQL query: {e}")
        st.session_state.current_sparql_query = "No SPARQL query available yet"
        st.session_state.current_sparql_response = "No Response available yet"
        return f"An issue occurred while generating the SPARQL query. Error: {str(e)}"
    

def process_question_and_get_sparql_data(question):
    logger.info("Received the following question:: " + question)
    Entities, Relationship_or_error = extract_entity_relationship_meaning(question)
    
    if not Entities:
        # If error occurs during Entities extraction, return error message
        return Relationship_or_error

    # Generate and return the SPARQL result
    return generate_sparql_query(Entities, Relationship_or_error,question)


# # working questions
# question= "Where was naredra modi was born?"
# question= "Who directed the movie 'The Matrix'?"
# process_question_and_get_sparql_data("Where was naredra modi was born?")


