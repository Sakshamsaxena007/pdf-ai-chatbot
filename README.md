# *PDF AI Chatbot*

## Overview

A Retrieval-Augmented Generation (RAG) chatbot that allows users to upload PDF documents and ask questions about their content.

The application extracts text from PDFs, creates embeddings, stores them in ChromaDB, retrieves relevant information, and generates answers using Groq LLM.

---

## Features

- PDF Upload
- Text Extraction
- Chunking
- Embeddings
- ChromaDB Vector Database
- Question Answering
- Source Page Citation
- Chat History

---

## Architecture

PDF
↓
Text Extraction
↓
Chunking
↓
Embeddings
↓
ChromaDB
↓
Retriever
↓
Groq LLM
↓
Answer + Sources

---

## Chunking Strategy

- Chunk Size: 1000
- Chunk Overlap: 200

---

## Embedding Model

sentence-transformers/all-MiniLM-L6-v2

---

## Retrieval Strategy

Top 3 most relevant chunks are retrieved using semantic similarity search.

---

## LLM

Groq LLM

---

## Installation

pip install -r requirements.txt

streamlit run app.py

---

## Prepared By

Saksham Saxena
