import os

os.environ["OPENAI_API_KEY"] = "sk-..."
os.environ["GROQ_API_KEY"] = "sk-..."
os.environ["LANGCHAIN_API_KEY"] = "sk-..."
os.environ["LANGCHAIN_TRACING_V2"] = "true"

OUTPUT_PATH = "./content/"
PDF_FILE = OUTPUT_PATH + 'attention.pdf'