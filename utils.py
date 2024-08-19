import logging
import pandas as pd
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter

def load_documents(file_path):
    logging.info(f"Loading documents from {file_path}")
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    logging.info(f"Loaded {len(documents)} documents")
    return documents

def split_documents(documents, chunk_size=1000, chunk_overlap=0):
    logging.info(f"Splitting documents into chunks with chunk_size={chunk_size} and chunk_overlap={chunk_overlap}")
    text_splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    texts = text_splitter.split_documents(documents)
    logging.info(f"Split into {len(texts)} chunks")
    return texts
