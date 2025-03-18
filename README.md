# Multimodal RAG System

A powerful Retrieval-Augmented Generation (RAG) system that can process and understand PDFs containing text, tables, and images. Built with LangChain, OpenAI, and Groq, this system provides an interactive Streamlit interface for document analysis and Q&A.

## Features

- 📄 PDF Processing: Extract text, tables, and images from PDF documents
- 🖼️ Multimodal Understanding: Process and analyze different types of content
- 💾 Vector Store: Efficient storage and retrieval of document elements
- 🤖 Multiple LLM Support: Integration with OpenAI and Groq models
- 🌐 Interactive UI: User-friendly Streamlit interface
- 📊 Real-time Preview: PDF preview alongside Q&A interface

## Project Structure

```
project_root/
│
├── config.py                # Environment variables and config settings
├── extract_data.py         # PDF extraction functions
├── summarize.py            # Content summarization logic
├── vector_store.py         # Vector store and retriever management
├── rag_pipeline.py         # RAG pipeline implementation
├── utils.py                # Utility functions
├── main.py                 # CLI execution script
├── app.py                  # Streamlit web application
└── requirements.txt        # Project dependencies
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Shiv1909/Multimodel-Rag.git
cd Multimodel-Rag
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your API keys:
- OpenAI API Key
- Groq API Key
- LangChain API Key

## Usage

### Web Interface (Recommended)

1. Run the Streamlit app:
```bash
streamlit run app.py
```

2. Open your browser and navigate to the displayed URL

3. Use the interface to:
   - Upload a PDF file
   - Enter your API keys
   - Process the document
   - Ask questions about the content

### Command Line Interface

Run the main script directly:
```bash
python main.py
```

## How It Works

1. **Document Processing**
   - PDF parsing and element extraction
   - Separation of text, tables, and images
   - Base64 encoding of images

2. **Content Summarization**
   - Text and table summarization using Groq
   - Image description using OpenAI's GPT-4V

3. **Vector Storage**
   - Creation of embeddings for all content
   - Storage in Chroma vector database
   - Multi-vector retrieval system

4. **RAG Pipeline**
   - Context-aware retrieval
   - Multimodal prompt construction
   - Response generation

## Requirements

- Python 3.8+
- Dependencies listed in requirements.txt
- API keys for:
  - OpenAI
  - Groq
  - LangChain

## Acknowledgments

- LangChain for the core RAG functionality
- OpenAI and Groq for language models
- Streamlit for the web interface
- Unstructured for PDF processing
