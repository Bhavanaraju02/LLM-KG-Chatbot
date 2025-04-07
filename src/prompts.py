from langchain.prompts import FewShotPromptTemplate, PromptTemplate
from prompt_template import Entity_relation_example,Entity_relationship_prompt_template, Sparql_examples, Sparql_prompt_template, Resonse_generate_template,Response_examples

# Define the prompt template for Entities & Relation individual examples
Entity_Relation_example_prompt = PromptTemplate.from_template(
    "Question: {Question}\nResponse: {Response}"
)
 
Entity_Relation_prompt = FewShotPromptTemplate(
    examples=Entity_relation_example,  
    example_prompt=Entity_Relation_example_prompt,
    prefix=Entity_relationship_prompt_template,
    suffix="Question: {Question},\nResponse:",
    input_variables=["Question"], 
)

#Code related to SPARQL template
# Define the prompt template for SPARQL individual examples
Sparql_Query_example_prompt = PromptTemplate.from_template(
    "Entities: {Entities}\nRelationships:{Relationships},\nSPARQL Query:{Query} "
)

Sparql_Query_prompt = FewShotPromptTemplate(
    examples=Sparql_examples,
    example_prompt=Sparql_Query_example_prompt,
    prefix=Sparql_prompt_template,
    suffix="Entities: {Entities}\nRelationships:{Relationships}\nSPARQL Query:",
    input_variables=["Entities", "Relationships"],
)

# Define the prompt template for generating Response using question and SPARQL response
Response_generator_example_prompt = PromptTemplate.from_template(
    "Question: {Question}\nSparql_Response:{SPARQL_Response},\nExpected output: {Expected_Output}"
)

#Response generator prompt
Response_generator_prompt = FewShotPromptTemplate(
    examples=Response_examples,
    example_prompt=Response_generator_example_prompt,
    prefix=Resonse_generate_template,
    suffix="Question:{Question}\nSPARQL_Response:{SPARQL_Response}\nExpected_output:",
    input_variables=["Question", "SPARQL_Response"],
)


#Testing
# entities_str = json.dumps(["City", "Skyscraper"])
# relationships_str = json.dumps([{"subject": "City", "relation": "has", "object": "Skyscraper"}])
# print(Sparql_Query_prompt.format(Entities=entities_str, Relationships=relationships_str))
# print(Sparql_Query_prompt.format(Entities=["City", "Skyscraper"],Relationships=[{{"subject": "City", "relation": "has", "object": "Skyscraper"}}]))
# print(Entity_Relation_prompt.format(Question="What is the capital of India?"))
# print(Response_generator_prompt.format(Question="Helo",SPARQL_Response=['http://dbpedia.org/resource/Bombay_State']))