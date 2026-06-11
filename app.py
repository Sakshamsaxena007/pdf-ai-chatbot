import os
import tempfile
import streamlit as st
from pdf_loader import load_pdf
from vector_store import create_vector_store
from chatbot import get_answer

st.set_page_config(
    page_title="PDF AI Chatbot",
    page_icon="📄",
    layout="wide"
)

st.markdown("""
<style>
body { font-family: 'Segoe UI', sans-serif; }
.header {
    background: linear-gradient(135deg, #667eea, #764ba2);
    padding: 30px;
    border-radius: 15px;
    text-align: center;
    color: white;
    margin-bottom: 25px;
}
.header h1 { font-size: 2.5em; margin: 0; }
.header p { font-size: 1.1em; margin: 8px 0 0 0; opacity: 0.9; }
.source-box {
    background: #f0f7ff;
    border-left: 4px solid #667eea;
    padding: 10px 15px;
    border-radius: 6px;
    margin-top: 8px;
    font-size: 0.85em;
    color: #444;
}
.success-box {
    background: #f0fff4;
    border-left: 4px solid #48bb78;
    padding: 12px 18px;
    border-radius: 8px;
    margin-bottom: 20px;
    color: #276749;
    font-weight: 500;
}
.empty-state {
    text-align: center;
    padding: 80px 20px;
    color: #aaa;
}
.empty-state h2 { font-size: 1.8em; }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header">
    <h1>📄 PDF AI Chatbot</h1>
    <p>Upload any PDF and get instant AI-powered answers with page references</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("## 📂 Upload PDF")
    uploaded_file = st.file_uploader(
        "Choose a PDF file (max 50MB)",
        type="pdf"
    )
    st.markdown("---")
    st.markdown("### 💡 How It Works")
    st.markdown("**1.** 📤 Upload your PDF")
    st.markdown("**2.** 💬 Type your question")
    st.markdown("**3.** 🤖 Get AI answer")
    st.markdown("**4.** 📌 See source pages")
    st.markdown("---")
    st.markdown("### ⚙️ Powered By")
    st.markdown("🔹 Google Gemini AI")
    st.markdown("🔹 ChromaDB Vector Store")
    st.markdown("🔹 LangChain Framework")

# Main Content
if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    with st.spinner("⏳ Processing your PDF..."):
        pages = load_pdf(tmp_path)
        vector_store = create_vector_store(pages)

    st.markdown(f"""
    <div class="success-box">
        ✅ <strong>{uploaded_file.name}</strong> uploaded successfully!
        &nbsp;|&nbsp; 📄 <strong>{len(pages)}</strong> pages ready
    </div>
    """, unsafe_allow_html=True)

    # Initialize chat
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Show chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            if msg["role"] == "assistant" and "sources" in msg:
                st.markdown("**📌 Sources:**")
                for src in msg["sources"]:
                    st.markdown(
                        f'<div class="source-box">📄 <strong>Page {src["page"]}:</strong> {src["excerpt"]}</div>',
                        unsafe_allow_html=True
                    )

    # Chat input
    question = st.chat_input("💬 Ask anything about your PDF...")

    if question:
        with st.chat_message("user"):
            st.write(question)
        st.session_state.messages.append({
            "role": "user",
            "content": question
        })

        with st.chat_message("assistant"):
            with st.spinner("🤔 Thinking..."):
                result = get_answer(question, vector_store)
                answer = result["result"]
                sources = result["source_documents"]

            st.write(answer)

            source_list = []
            if sources:
                st.markdown("**📌 Sources:**")
                for doc in sources:
                    excerpt = doc.page_content[:200] + "..."
                    page_num = doc.metadata.get("page", "?")
                    source_list.append({
                        "page": page_num,
                        "excerpt": excerpt
                    })
                    st.markdown(
                        f'<div class="source-box">📄 <strong>Page {page_num}:</strong> {excerpt}</div>',
                        unsafe_allow_html=True
                    )

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer,
            "sources": source_list
        })

    os.unlink(tmp_path)

else:
    st.markdown("""
    <div class="empty-state">
        <h2>👈 Upload a PDF to get started!</h2>
        <p>Ask questions, get answers, see exact page sources</p>
    </div>
    """, unsafe_allow_html=True)
