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

## 🌐 Overview

KG-QA-Chatbot is designed to understand user queries, fetch data from DBpedia using SPARQL, and generate informative responses through an LLM. The chatbot supports a wide range of factual questions and is accessible via a Streamlit-based interface.
<img width="822" alt="image" src="https://github.com/user-attachments/assets/54afa102-2c36-44bb-8e42-58f6e9b05406" />

---

## 🔁 Flow Diagram

<img width="789" alt="image" src="https://github.com/user-attachments/assets/d241cb45-c682-4d43-b222-d893333bbfbd" />


The diagram outlines the end-to-end workflow: from user input to SPARQL querying, and final response generation using an LLM.

---


## 🧱 Project Structure
LLM-KG-Chatbot/ ├── src/ │ ├── init.py │ ├── main.py │ ├── logger.py │ ├── prompt_template.py │ ├── prompts.py │ ├── sparql_handler.py │ ├── helper.py │ └── config.py ├── .streamlit/ │ └── secrets.toml ├── requirements.txt ├── README.md


---

##  Installation Instructions

### Prerequisites

- Python 3.8+
- Git
- pip

###  Step 1: Clone the Repository

```bash
git clone https://github.com/vigmallya/LLM-KG-Chatbot.git
cd LLM-KG-Chatbot
Step 2: Create a Virtual Environment
Windows:

python -m venv venv
.\venv\Scripts\activate
Linux/Mac:

python3 -m venv venv
source venv/bin/activate**
### Step 3: Install Dependencies
pip install -r requirements.txt
### Step 4: Setup API Key and Base URL
Edit the secrets.toml file in .streamlit/:

[API]
MODEL_API_KEY = "YOUR_API_KEY"
MODEL_END_POINT = "YOUR_BASE_URL"
Replace with your actual API credentials.

### Step 5: Run the Chatbot
streamlit run src/main.py

Navigate to the local URL (usually http://localhost:8501) and start chatting!
