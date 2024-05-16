import os
import psycopg2
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from index import Index
from retriever import Retriever

# Load environment variables from .env file
load_dotenv()

# Initialize Google API key and GoogleGenerativeAI objects
api_key = os.getenv('GOOGLE_API_KEY')
llm = ChatGoogleGenerativeAI(model="gemini-pro", api_key=api_key)
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# Connect to PostgreSQL database
conn = psycopg2.connect(
    host=os.getenv('DB_HOST'),
    database=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    port=os.getenv('DB_PORT')
)

# Enable vector extension in PostgreSQL
cur = conn.cursor()
cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
conn.commit()

# Configuration dictionary for indexing and retrieval
cfg = {
    'table': 'rag_testing',
    'chunk_size': 1500,
    'chunk_overlap': 100
}

# Set flags for operations
index_creation = False
response_generation = True

# Perform index creation if flag is set
if index_creation:
    idx = Index(cfg, conn, embeddings)
    idx.create_table()
    idx.insert_dir("files/")

# Perform response generation if flag is set
if response_generation:
    query = input("Enter your query: ")
    retr = Retriever(cfg, conn, embeddings)
    docs = retr.retrieve_docs(query, k=3)
    conn.close()

    # Print retrieved documents and their relevance scores
    for doc in docs:
        print(doc.metadata['title'])
        print(doc.page_content)
        print("Relevance score:", doc.metadata['score'])
        print("-" * 50)

    # Construct context for the generative model
    context = "\n".join([doc.metadata['title'] + "\n" + doc.page_content for doc in docs])
    prompt = f"Query: {query}\nRefer to the additional context only if the query is related to it.\nAdditional context: {context} '\n' If query is not related to context, use your own knowledge.  "

    # Generate response using the generative model
    response = llm.invoke(prompt)
    print(response.content)
