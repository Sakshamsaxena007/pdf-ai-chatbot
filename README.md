# PDF AI Chatbot

An AI-powered chatbot that allows users to upload PDF documents and ask questions about their content.

## Features

* PDF Upload (up to 50 MB)
* Document Chunking
* Vector Search using ChromaDB
* LLM-powered Question Answering
* Source Page Attribution
* Chat History Support

## Tech Stack

* Python
* Streamlit
* LangChain
* ChromaDB
* Groq LLM
* HuggingFace Embeddings

## Run Locally

pip install -r requirements.txt

streamlit run app.py

## Architecture

PDF → Text Extraction → Chunking → Embeddings → ChromaDB → Retrieval → Groq LLM → Answer + Sources

## Prepared by
Saksham Saxena
