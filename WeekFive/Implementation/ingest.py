import os
import glob
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
MODEL = "gpt-4.1-nano"
DB_NAME = str(Path(__file__).parent.parent / "vector_db")
KNOWLEDGE_BASE = str(Path(__file__).parent.parent / "knowledge-base")

def load_documents():
    folders = glob.glob(str(Path(KNOWLEDGE_BASE) / "*"),recursive=True)
    print(f"Found {len(folders)} folders")
    documents_list = []
    for folder in folders:
        doc_type = os.path.basename(folder)
        loader = DirectoryLoader(folder,glob="**/*.md",loader_cls=TextLoader,loader_kwargs={"encoding":"utf-8"})
        docs = loader.load()
        for doc in docs:
            doc.metadata["doc_type"] = doc_type
            documents_list.append(doc)
    print(f"Total documents loaded: {len(documents_list)}")
    return documents_list

def split_documents(documents):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents)
    print(f"Total chunks: {len(chunks)}")
    return chunks

def embed_documents(chunks):
    
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")   
    if os.path.exists(DB_NAME):
        Chroma(persist_directory=DB_NAME,embedding_function=embeddings).delete_collection()

    vector_store = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory=DB_NAME
    )
    print(f"Total vectors in vector store: {vector_store._collection.count()}")
    collection = vector_store._collection
    count = collection.count()

    sample_embedding = collection.get(limit=1, include=["embeddings"])["embeddings"][0]
    dimensions = len(sample_embedding)
    print(f"There are {count:,} vectors with {dimensions:,} dimensions in the vector store")

def main():
    documents = load_documents()
    print("loaded documents")
    chunks = split_documents(documents)
    print("split documents")
    embed_documents(chunks)
    print("embedded documents")
    print("Ingestion complete")

if __name__ == "__main__":
    main()