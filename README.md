# RAG-with-Google-Gemini
An implementation of naive RAG using custom written retriever and indexer without langchain pgvector and retrivers and using Google Gemini API key for LLM and Embedding( Since it's free :) ). This is mainly for educational purposes

# Project Setup

This README provides instructions on how to set up your local environment for this project.

## Overview

The repo consists of the following files:

1. `main.py`: This is the main file that contains the code for indexing the data using `Index` class object and querying the LLM using `Retriever` class object.
2. `retriever.py`: This file contains the code for `Retriever` class the relevant documents based on the query.
3. `index.py`: This file contains the code for `Index` class used for indexing the data.
4. `utils.py`: This file contains utility functions used.
5. `requirements.txt`: This file contains the dependencies required for the project.
6. `.env`: This file contains the environment variables required for the project.

## Clone the Repository
## Create a Virtual Environment

First, you need to create a virtual environment. This can be done using the following command:

```bash
python3 -m venv env
# activate the virtual environment
source env/bin/activate
```

## Install Dependencies

Next, you need to install the dependencies. This can be done using the following command:

```bash
pip install -r requirements.txt
```

In addition to the above dependencies, you also need to install the `en_core_web_sm` language model for spaCy. This can be done using the following command:

```bash
python -m spacy download en_core_web_sm
```

## Set up the environment variables

Create a `.env` file in the root directory of the repo and add the following environment variables:

```bash
GOOGLE_API_KEY=<your_google_api_key>
DB_NAME=<your_database_name>
DB_USER=<your_database_user>
DB_PASSWORD=<your_database_password> # leave empty if no password is set
DB_HOST=<your_database_host>
DB_PORT=<your_database_port>
```

If you don't have an `API_KEY`, you can get one [here](https://aistudio.google.com/app/apikey). Keep your .env file confidential and refrain from making it publicly accessible online. 

## Indexing the data

To index the data, keep your files in a folder named `files`( or any other name you prefer and update the `main.py` file accordingly) in the root directory of the repo and set index_creation to True in the `main.py` file:

```python
index_creation = True
```

Then run the following command:

```bash
python3 main.py
```

## Querying the LLM

To query the LLM, set response_generation to True in the `main.py` file:

```python
response_generation = True
```

Then run the following command:

```bash
python3 main.py
```
