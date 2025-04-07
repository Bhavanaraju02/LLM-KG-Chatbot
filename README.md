# LLM-KG-Chatbot

The **KG-QA-Chatbot** project combines a Large Language Model (LLM) with a Knowledge Graph (KG) to build an interactive chatbot capable of answering natural language queries using structured knowledge from **DBpedia**.

---

## 📌 Table of Contents

- [Overview](#overview)
- [Flow Diagram](#flow-diagram)
- [Team Members](#team-members)
- [Project Structure](#project-structure)
- [Installation Instructions](#installation-instructions)
  - [Prerequisites](#prerequisites)
  - [Step 1: Clone the Repository](#step-1-clone-the-repository)
  - [Step 2: Create a Virtual Environment](#step-2-create-a-virtual-environment)
  - [Step 3: Install Dependencies](#step-3-install-dependencies)
  - [Step 4: Setup API Key and Base URL](#step-4-setup-api-key-and-base-url)
  - [Step 5: Run the Chatbot](#step-5-run-the-chatbot)
- [Example Questions](#example-questions)
- [Acknowledgments](#acknowledgments)
- [Contribution Guidelines](#contribution-guidelines)

---

##  Overview

KG-QA-Chatbot is designed to understand user queries, fetch data from DBpedia using SPARQL, and generate informative responses through an LLM. The chatbot supports a wide range of factual questions and is accessible via a Streamlit-based interface.
<img width="822" alt="image" src="https://github.com/user-attachments/assets/54afa102-2c36-44bb-8e42-58f6e9b05406" />

---

## Flow Diagram

<img width="789" alt="image" src="https://github.com/user-attachments/assets/d241cb45-c682-4d43-b222-d893333bbfbd" />


The diagram outlines the end-to-end workflow: from user input to SPARQL querying, and final response generation using an LLM.

---
## Team Members

- **Vignesh Mallya** - `4001498`
- **Bhavana Raju** - `4000149`
- **Shree Shaangavi N** - `4000243`

---


##  Project Structure
LLM-KG-Chatbot/
├── src/                          # Contains all the source code files for the project
│   ├── __init__.py                # Marks the folder as a Python package (if needed)
│   ├── main.py                    # Main execution script for running the chatbot or app
│   ├── logger.py                  # Contains logging functionality for tracking events and errors
│   ├── prompt_template.py        # Holds templates for generating prompts to the language model
│   ├── prompts.py                 # Defines the actual prompts used in the interaction with the model
│   ├── sparql_handler.py          # Handles querying and interacting with the SPARQL endpoint (for knowledge graph queries)
│   ├── helper.py                  # Includes helper functions used throughout the project
│   └── config.py                  # Configuration file for project settings and variables
├── .streamlit/                    # Folder for Streamlit-specific configurations
│   └── secrets.toml               # Stores sensitive information like API keys and credentials
├── requirements.txt               # Lists the external libraries and dependencies required to run the project
├── README.md                      # Provides an overview of the project, installation instructions, and usage details


---

##  Installation Instructions

### Prerequisites


---

##  Installation Instructions

### Prerequisites
1. Python 3.8+
2. Git
3. pip


### Step 1: Clone the Repository

```bash
git clone https://github.com/vigmallya/LLM-KG-Chatbot.git
cd LLM-KG-Chatbot
```

### Step 2: Create a Virtual Environment

It is recommended to use a virtual environment to manage dependencies.

#### For Windows:

```bash
python -m venv venv
.\venv\Scripts\activate
```

#### For Linux/Mac:

```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Set Up API Key and Base URL

1. Navigate to the `.streamlit` directory.
2. Open or create the `secrets.toml` file.
3. Add the following configuration:

```toml
[API]
MODEL_API_KEY = "YOUR_API_KEY"
MODEL_END_POINT = "YOUR_BASE_URL"
```

> Replace `YOUR_API_KEY` and `YOUR_BASE_URL` with your actual credentials.

---

##  Run the Chatbot

Once setup is complete, run the chatbot using:

```bash
streamlit run src/main.py
```

Visit the URL displayed in your terminal (usually `http://localhost:8501`) to start chatting!

---

##  Example Questions for Testing

Here are some example questions to test the chatbot’s capabilities:

### Easy
- What is the currency of Japan?
- What is the capital city of Brazil?
- Who painted the Mona Lisa?
- Who wrote Romeo and Juliet?

### Moderate
- Where was Narendra Modi born? / Where was Albert Einstein born?
- How tall is the Eiffel Tower in meters?
- Who directed the movie "The Matrix"?
- What is the maximum depth of the Pacific Ocean in meters?
- How old was Albert Einstein when he died?

### Challenging
- How many official languages does Singapore have? / Switzerland?
- What is the route end of the Birmingham and Oxford Junction Railway?
- Where can one find Dzogchen Ponlop Rinpoche?
- Which car brand has manufactured the most models?

---

##  Acknowledgments

### Educational Resources
- Idea for Flow of the Chatbot
- Setting up UI

---

##  Contribution Guidelines

We welcome contributions! To contribute:

1. **Fork** this repository.
2. **Create** a new feature branch.
3. **Commit** your changes.
4. **Push** to your feature branch.
5. **Open a pull request** with a clear description of the changes.

---



