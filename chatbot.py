import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

def get_answer(question, vector_store):

    retriever = vector_store.as_retriever(search_kwargs={"k": 3})

    docs = retriever.invoke(question)

    context = "\n\n".join([doc.page_content for doc in docs])

    llm = ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama-3.3-70b-versatile"
    )

    prompt = f"""
Answer the question only from the PDF content below.

PDF Content:
{context}

Question:
{question}

Also mention page numbers if available.
"""

    response = llm.invoke(prompt)

    return {
        "result": response.content,
        "source_documents": docs
    }

# What this does simply to help understand the assessment :-
# Sends our question + relevant PDF chunks to Gemini AI.
# Gemini reads them and gives back an answer also with page numbers.
