from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

def create_vector_store(pages):

    texts = []
    metadatas = []

    for page in pages:
        texts.append(page["text"])
        metadatas.append({"page": page["page"]})

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.create_documents(
        texts,
        metadatas=metadatas
    )

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_store = FAISS.from_documents(
        chunks,
        embeddings
    )
    return vector_store

# What this does simply to help understand the assessment :-
# Breaks the PDF text into small chunks (1000 characters each).
# Converts chunks into numbers so AI can search them.
# Stores everything in ChromaDB (a local database).
