from config import PDF_FILE
from extract_data import extract_chunks, get_images_base64
from summarize import summarize_elements, summarize_images
from vector_store import setup_retriever, load_into_retriever
from rag_pipeline import create_rag_chain

chunks = extract_chunks(PDF_FILE)
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

chain = create_rag_chain(retriever)

response = chain.invoke("What is multihead attention?")
print(response)