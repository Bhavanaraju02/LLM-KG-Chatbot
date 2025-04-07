Entity_relation_example=[
    {
        "Question": "Where was Barack Obama born?",
        "Response": "{{\"Entities\": [\"Barack Obama\", \"Birthplace\"], \"Relationships\": [{{\"subject\": \"Barack Obama\", \"relation\": \"born in\", \"object\": \"Birthplace\"}}]}}"
    },
    {
        "Question": "Who were the predecessors and successors of Angela Merkel as Chancellor of Germany?",
        "Response": "{{\"Entities\": [\"Angela Merkel\", \"Chancellor of Germany\", \"Predecessor\", \"Successor\"], \"Relationships\": [{{\"subject\": \"Angela Merkel\", \"relation\": \"held position\", \"object\": \"Chancellor of Germany\"}}, {{\"subject\": \"Predecessor\", \"relation\": \"preceded\", \"object\": \"Angela Merkel\"}}, {{\"subject\": \"Successor\", \"relation\": \"succeeded\", \"object\": \"Angela Merkel\"}}]}}"
    },
    {
        "Question": "Which countries border Germany, and who is its current president?",
        "Response": "{{\"Entities\": [\"Germany\", \"Bordering Countries\", \"President\"], \"Relationships\": [{{\"subject\": \"Germany\", \"relation\": \"borders\", \"object\": \"Bordering Countries\"}}, {{\"subject\": \"Germany\", \"relation\": \"has president\", \"object\": \"President\"}}]}}"
    }
]

Entity_relationship_prompt_template="""
Instruction:
Extract the entities and relationships present in the given natural language text (NLT) or questions. The extracted information should be structured, making it suitable for further processing i.e knowledge graph SPARQL queries generation.

Guidelines:
Identify entities, which represent real-world objects, people, places, or concepts etc.
Extract relationships that describe how the entities are connected based on the question itself.
Focus only on the question part for extracting entities and relationships, and do not include the answer.
Handle complex queries that may involve multiple entities and relationships.

Provide output in JSON format for structured processing.
Return only the Entites and Relationships without any additional explanations. even the ```json and ``` at the end
Below is the examples:
"""

Sparql_prompt_template="""
Instruction:
Transform the provided entities and relationships into a valid SPARQL query for DBpedia. The generated query should accurately represent the semantic connections between entities and enable effective retrieval of information from the knowledge graph.

Guidelines:
Use the standard DBpedia prefixes (dbo, dbr, rdf, rdfs, etc.)
Create variable names that reflect the entity types (e.g., ?city, ?country)
Apply appropriate filters and constraints based on the relationships
Include ORDER BY, GROUP BY, or LIMIT clauses when the context indicates ranking or limitation
Handle complex relationships that may require multiple triple patterns
Optimize the query for performance and accuracy

Return only the SPARQL query without any additional explanations. even the ```SPARQL and ``` at the end
Below is the examples:
"""

Sparql_examples = [
  {
    "Entities": ["City", "Skyscraper"],
    "Relationships": "[{{\"subject\": \"City\", \"relation\": \"has\", \"object\": \"Skyscraper\"}}]",
    "Query": "PREFIX dbo: <http://dbpedia.org/ontology/> \nSELECT DISTINCT ?city WHERE {{ \n  ?building rdf:type dbo:Skyscraper . \n  ?building dbo:location ?city . \n}} \nGROUP BY ?city \nORDER BY DESC(COUNT(?building)) \nLIMIT 1"
  },
  {
    "Entities": ["Country", "GDP per capita"],
    "Relationships": "[{{\"subject\": \"Country\", \"relation\": \"has\", \"object\": \"GDP per capita\"}},{{\"subject\": \"Countries\", \"relation\": \"compared based on\", \"object\": \"GDP per capita\"}}]",
    "Query": "PREFIX dbo: <http://dbpedia.org/ontology/> \nSELECT DISTINCT ?country1 ?country2 WHERE {{ \n  ?country1 rdf:type dbo:Country . \n  ?country1 dbo:gdpPerCapita ?gdp1 . \n  ?country2 rdf:type dbo:Country . \n  ?country2 dbo:gdpPerCapita ?gdp2 . \n  FILTER (?country1 != ?country2) \n  BIND(ABS(?gdp1 - ?gdp2) AS ?diff) \n}} \nORDER BY ASC(?diff) \nLIMIT 1"
  },
  {
    "Entities": ["Artist", "Grammy Award"],
    "Relationships": "[{{\"subject\": \"Artist\", \"relation\": \"has won\", \"object\": \"Grammy Award\"}}]",
    "Query": "PREFIX dbo: <http://dbpedia.org/ontology/> \nSELECT DISTINCT ?artist WHERE {{ \n  ?artist rdf:type dbo:MusicalArtist . \n  ?artist dbo:award dbr:Grammy_Award . \n}} \nGROUP BY ?artist \nORDER BY DESC(COUNT(?artist)) \nLIMIT 1"
  },
  {
    "Entities": ["Movie (Inception)", "Director"],
    "Relationships": "[{{\"subject\": \"Movie (Inception)\", \"relation\": \"is directed by\", \"object\": \"Director\"}}]",
    "Query": "PREFIX dbo: <http://dbpedia.org/ontology/> \nPREFIX dbr: <http://dbpedia.org/resource/> \nSELECT DISTINCT ?uri WHERE {{ \n  dbr:Inception dbo:director ?uri . \n}}"
  },
  {
    "Entities": ["Mount Everest", "Country"],
    "Relationships": "[{{\"subject\": \"Mount Everest\", \"relation\": \"is located in\", \"object\": \"Country\"}}]",
    "Query": "PREFIX dbo: <http://dbpedia.org/ontology/> \nPREFIX dbr: <http://dbpedia.org/resource/> \nSELECT DISTINCT ?uri WHERE {{ \n  dbr:Mount_Everest dbo:locatedInArea ?uri . \n}}"
  },
  {
    "Entities": ["City", "Population"],
    "Relationships": "[{{\"subject\": \"City\", \"relation\": \"has population\", \"object\": \"Population\"}}]",
    "Query": "PREFIX dbo: <http://dbpedia.org/ontology/> \nSELECT DISTINCT ?city WHERE {{ \n  ?city rdf:type dbo:City . \n  ?city dbo:populationTotal ?population . \n}} \nORDER BY DESC(?population) \nLIMIT 1"
  },
  {
    "Entities": ["Country", "UNESCO World Heritage Sites"],
    "Relationships": "[{{\"subject\": \"Country\", \"relation\": \"has\", \"object\": \"UNESCO World Heritage Sites\"}}]",
    "Query": "PREFIX dbo: <http://dbpedia.org/ontology/> \nSELECT DISTINCT ?country WHERE {{ \n  ?heritage rdf:type dbo:WorldHeritageSite . \n  ?heritage dbo:location ?country . \n}} \nGROUP BY ?country \nORDER BY DESC(COUNT(?heritage)) \nLIMIT 1"
  },
  {
    "Entities": ["Car Brand", "Automobile"],
    "Relationships": "[{{\"subject\": \"Car Brand\", \"relation\": \"manufactures\", \"object\": \"Automobile\"}}]",
    "Query": "PREFIX dbo: <http://dbpedia.org/ontology/> \nSELECT DISTINCT ?brand WHERE {{ \n  ?car rdf:type dbo:Automobile . \n  ?car dbo:manufacturer ?brand . \n}} \nGROUP BY ?brand \nORDER BY DESC(COUNT(?car)) \nLIMIT 1"
  },
  {
    "Entities": ["TV Series", "Seasons"],
    "Relationships": "[{{\"subject\": \"TV Series\", \"relation\": \"has number of\", \"object\": \"Seasons\"}}]",
    "Query": "PREFIX dbo: <http://dbpedia.org/ontology/> \nSELECT DISTINCT ?series WHERE {{ \n  ?series rdf:type dbo:TelevisionShow . \n  ?series dbo:numberOfSeasons ?seasons . \n}} \nORDER BY DESC(?seasons) \nLIMIT 1"
  },
  {
    "Entities": ["Director", "Film"],
    "Relationships": "[{{\"subject\": \"Director\", \"relation\": \"directs\", \"object\": \"Film\"}}]",
    "Query": "PREFIX dbo: <http://dbpedia.org/ontology/> \nSELECT DISTINCT ?director WHERE {{ \n  ?movie rdf:type dbo:Film . \n  ?movie dbo:director ?director . \n}} \nGROUP BY ?director \nORDER BY DESC(COUNT(?movie)) \nLIMIT 1"
  }
]

Response_examples=[
    {
      "Question": "Where was Narendra Modi born?",
      "SPARQL_Response": ["http://dbpedia.org/resource/Bombay_State", "http://dbpedia.org/resource/Vadnagar", "http://dbpedia.org/resource/India"],
      "Expected_Output": "Narendra Modi was born in Vadnagar, which was part of Bombay State, now in India."
    },
    {
      "Question": "Who is the founder of Microsoft?",
      "SPARQL_Response": ["http://dbpedia.org/resource/Bill_Gates", "http://dbpedia.org/resource/Paul_Allen"],
      "Expected_Output": "Microsoft was founded by Bill Gates and Paul Allen."
    },
    {
      "Question": "What is the capital of France?",
      "SPARQL_Response": ["http://dbpedia.org/resource/Paris"],
      "Expected_Output": "The capital of France is Paris."
    },
    {
      "Question": "Who wrote 'Pride and Prejudice'?",
      "SPARQL_Response": ["http://dbpedia.org/resource/Jane_Austen"],
      "Expected_Output": "Pride and Prejudice was written by Jane Austen."
    },
    {
      "Question": "Which rivers flow through Egypt?",
      "SPARQL_Response": ["http://dbpedia.org/resource/Nile"],
      "Expected_Output": "The Nile River flows through Egypt."
    }
  ]
Resonse_generate_template="""
Instruction:
Generate a natural language answer based only strictly on the given question and SPARQL response. Do not add any extra details. Maintain grammatical correctness and readability.
Input Format:
Question: {Question}
SPARQL_Response: {SPARQL_Response}
Expected Output:
A well-formed answer in natural language that directly addresses the question using only the provided response.

Add this line infront of all the answers "Based on the question and the retrieved information from the DBpedia knowledge graph..\n" and start the asnwer in next line
"""