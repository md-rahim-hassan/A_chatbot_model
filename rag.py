import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


def process_document(file_path):
  if file_path.endswith('.pdf'):
    loader = PyPDFLoader(file_path)
  else:
    loader = TextLoader(file_path)

  docs = loader.load()

  text_splitter = RecursiveCharacterTextSplitter(
      chunk_size=500, chunk_overlap=50
  )
  chunks = text_splitter.split_documents(docs)

  embeddings = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')
  vector_store = Chroma.from_documents(
      chunks, embeddings, persist_directory='./chroma_db'
  )

  return vector_store.as_retriever(search_kwargs={'k': 3})