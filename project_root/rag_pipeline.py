from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

def build_prompt(kwargs):
    context_text = "".join(text.text for text in kwargs["context"]["texts"])
    prompt_content = [{"type": "text", "text": f"Answer based on: {context_text}\nQuestion: {kwargs['question']}"}]

    for image in kwargs["context"]["images"]:
        prompt_content.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image}"}})

    return ChatPromptTemplate.from_messages([HumanMessage(content=prompt_content)])

def create_rag_chain(retriever):
    return (
        {"context": retriever | RunnableLambda(parse_docs), "question": RunnablePassthrough()}
        | RunnableLambda(build_prompt)
        | ChatOpenAI(model="gpt-4o-mini")
        | StrOutputParser()
    )