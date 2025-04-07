import streamlit as st

#Configure the Streamlit page with a custom page title
st.set_page_config(page_title="KG-QA Chatbot", page_icon=":earth_asia::book:", layout="wide")

import time
from sparql_handler import process_question_and_get_sparql_data 
from logger import setup_logger 
from streamlit_option_menu import option_menu
import json

logger=setup_logger()


header = st.container()

def streamlit_ui():
    with st.sidebar: 
        choice = option_menu( menu_title= 'KG-QA',
                             options = ['Home','Architecture of Chatbot'],
                             icons = ['house-fill','columns-gap'],
                             menu_icon = "diagram-3-fill",
                             default_index=0,)

    if choice == 'Home':
        with header:
            st.title('🌍 📖 Knowledge Graph Question Answering Chatbot')
            st.write("Got a question? Ask away, and I'll fetch the answer from the mighty DBpedia knowledge graph")
         # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []
        if "current_entites_relationships" not in st.session_state:
            st.session_state.current_entites_relationships = None
        if "current_sparql_query" not in st.session_state:
            st.session_state.current_sparql_query = None
        if "current_sparql_response" not in st.session_state:
            st.session_state.current_sparql_response = None

        # Display chat messages from history on app rerun
        for message in st.session_state.messages: 
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        # Create expanders in sidebar
        with st.sidebar.expander("See Enities and Relationships Here"):
            entity_relationship_placeholder = st.code("No Entities/Relatioships\navailabe yet", language='json')
        with st.sidebar.expander("See Generated SPARQL Query Here"):
            response_placeholder = st.code("No SPARQL query available yet", language="sparql")
        with st.sidebar.expander("See Response given by Knowledge Graph"):
            raw_sparql_response_placeholder = st.markdown("No Response available yet", unsafe_allow_html=True)

        if prompt := st.chat_input("Enter your question here..."):  #this line will check if the prompt is empty or not
            # Display user message in chat message container
            with st.chat_message("user"):
                st.markdown(prompt)
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})

            # Start the timer to measure response time
            start_time = time.time()

            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                with st.spinner('Fetching the answer...'):
                    response = process_question_and_get_sparql_data(prompt)   
        
            # Calculate the time taken for the response
            end_time = time.time()
            time_taken = end_time - start_time  # Time in seconds

            # Display assistant response with the time taken for the request
            message_placeholder.markdown(response)
             # Create a placeholder for dynamically updating the time taken
            time_placeholder = st.empty()

            # Update time dynamically in the placeholder
            time_placeholder.markdown(f"**Time Taken for Response**: {time_taken:.2f} seconds")
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            #To display Entites , Relationships and SPARQL query in realtime
            if "current_entites_relationships" in st.session_state and st.session_state.current_entites_relationships:
                formatted_json = json.dumps(st.session_state.current_entites_relationships, indent=4)
                entity_relationship_placeholder.code(formatted_json, language="json")
            else:
                entity_relationship_placeholder.write("No Entities/Relatioships\navailabe yet")

            if "current_sparql_query" in st.session_state and st.session_state.current_sparql_query:
                response_placeholder.code(st.session_state.current_sparql_query, language="sparql")
            else:
                response_placeholder.write("No SPARQL query available yet")

            if "current_sparql_response" in st.session_state and st.session_state.current_sparql_response:
                if st.session_state.current_sparql_response == "No Response available yet":
                    raw_sparql_response_placeholder.write("No Response available yet")
                else:
                    formatted_links = "\n".join([f"[{url}]({url})" for url in st.session_state.current_sparql_response])
                    raw_sparql_response_placeholder.markdown(formatted_links, unsafe_allow_html=True)
            
            else:
                raw_sparql_response_placeholder.write("No Response available yet")  

    elif choice == 'Architecture of Chatbot': 
        st.title("Architecture of Chatbot")
        st.image('assets/flow_diagram.png', caption='The flow diagram above illustrates the architecture and the workflow of the KG-QA-Chatbot. It shows how the chatbot processes the input query, fetches relevant data from DBpedia, and generates an appropriate response using a language model.', use_container_width=True)
        
streamlit_ui()