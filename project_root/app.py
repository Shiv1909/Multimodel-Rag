import streamlit as st
import os
import tempfile
from PyPDF2 import PdfReader
import base64
from pathlib import Path

from extract_data import extract_chunks, get_images_base64
from summarize import summarize_elements, summarize_images
from vector_store import setup_retriever, load_into_retriever
from rag_pipeline import create_rag_chain

st.set_page_config(layout="wide")

def display_pdf(pdf_file):
    base64_pdf = base64.b64encode(pdf_file.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

def process_pdf(pdf_path):
    chunks = extract_chunks(pdf_path)
    texts = [chunk for chunk in chunks if "CompositeElement" in str(type(chunk))]
    tables = [chunk for chunk in chunks if "Table" in str(type(chunk))]
    images = get_images_base64(chunks)
    
    text_summaries = summarize_elements(texts)
    table_summaries = summarize_elements([t.metadata.text_as_html for t in tables])
    image_summaries = summarize_images(images)
    
    retriever = setup_retriever()
    load_into_retriever(retriever, texts, text_summaries)
    load_into_retriever(retriever, tables, table_summaries)
    load_into_retriever(retriever, images, image_summaries)
    
    return create_rag_chain(retriever)

# Initialize session state
if 'rag_chain' not in st.session_state:
    st.session_state.rag_chain = None

st.title("Multimodal RAG System")

# Create two columns
left_col, right_col = st.columns([1, 1])

with left_col:
    st.header("PDF Upload and Preview")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    if uploaded_file is not None:
        display_pdf(uploaded_file)

with right_col:
    st.header("API Keys and Interaction")
    
    # API key inputs
    openai_key = st.text_input("OpenAI API Key", type="password")
    groq_key = st.text_input("Groq API Key", type="password")
    langchain_key = st.text_input("LangChain API Key", type="password")
    
    # Process button
    if st.button("Process PDF"):
        if not all([uploaded_file, openai_key, groq_key, langchain_key]):
            st.error("Please provide all required inputs (PDF and API keys)")
        else:
            # Set API keys
            os.environ["OPENAI_API_KEY"] = openai_key
            os.environ["GROQ_API_KEY"] = groq_key
            os.environ["LANGCHAIN_API_KEY"] = langchain_key
            os.environ["LANGCHAIN_TRACING_V2"] = "true"
            
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                pdf_path = tmp_file.name
            
            with st.spinner("Processing PDF..."):
                st.session_state.rag_chain = process_pdf(pdf_path)
            
            # Clean up temporary file
            Path(pdf_path).unlink()
            st.success("PDF processed successfully!")
    
    # Question input and response
    if st.session_state.rag_chain is not None:
        st.subheader("Ask Questions")
        question = st.text_input("Enter your question")
        
        if st.button("Get Answer"):
            if question:
                with st.spinner("Generating answer..."):
                    response = st.session_state.rag_chain.invoke(question)
                st.write("Answer:", response)
            else:
                st.warning("Please enter a question")