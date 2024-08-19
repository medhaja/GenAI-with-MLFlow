import logging
from langchain_openai import OpenAIEmbeddings, OpenAI
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from config import OPENAI_API_KEY

def create_embeddings():
    logging.info("Creating embeddings with OpenAIEmbeddings")
    return OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

def create_faiss_index(texts, embeddings):
    logging.info("Creating FAISS index from documents")
    return FAISS.from_documents(texts, embeddings)

def create_qa_chain(docsearch):
    logging.info("Creating QA chain with RetrievalQA")
    return RetrievalQA.from_chain_type(
        llm=OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY),
        chain_type="stuff",
        retriever=docsearch.as_retriever(),
        return_source_documents=True,
    )
