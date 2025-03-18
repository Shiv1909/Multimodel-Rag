from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

def summarize_elements(elements, model_name="llama-3.1-8b-instant"):
    prompt = ChatPromptTemplate.from_template("""
        You are an assistant tasked with summarizing tables and text.
        Respond with a concise summary without introductions.
        Content: {element}
    """)
    model = ChatGroq(temperature=0.5, model=model_name)
    summarize_chain = {"element": lambda x: x} | prompt | model | StrOutputParser()
    return summarize_chain.batch(elements, {"max_concurrency": 3})

def summarize_images(images):
    prompt = ChatPromptTemplate.from_messages([
        ("user", [{"type": "text", "text": "Describe the image in detail."},
                   {"type": "image_url", "image_url": {"url": "data:image/jpeg;base64,{image}"}}])
    ])
    chain = prompt | ChatOpenAI(model="gpt-4o-mini") | StrOutputParser()
    return chain.batch(images)