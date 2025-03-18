import uuid
from langchain.vectorstores import Chroma
from langchain.storage import InMemoryStore
from langchain.schema.document import Document
from langchain.embeddings import OpenAIEmbeddings
from langchain.retrievers.multi_vector import MultiVectorRetriever

def setup_retriever():
    vectorstore = Chroma(collection_name="multi_modal_rag", embedding_function=OpenAIEmbeddings())
    store = InMemoryStore()
    retriever = MultiVectorRetriever(
        vectorstore=vectorstore,
        docstore=store,
        id_key="doc_id",
    )
    return retriever

def load_into_retriever(retriever, elements, summaries):
    ids = [str(uuid.uuid4()) for _ in elements]
    summary_docs = [Document(page_content=summary, metadata={"doc_id": ids[i]}) for i, summary in enumerate(summaries)]
    retriever.vectorstore.add_documents(summary_docs)
    retriever.docstore.mset(list(zip(ids, elements)))