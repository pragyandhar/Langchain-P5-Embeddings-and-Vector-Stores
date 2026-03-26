from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

def build_vectorstore(chunks):
    print("\nGenerating embeddings and building vector store...")
    
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    vectorstore = FAISS.from_documents(chunks, embeddings)

    print(f"Vector store built with {len(chunks)} chunks")
    return vectorstore

def build_retriever(vectorstore, k=3):
    retriever = vectorstore.as_retriever(search_kwargs={"k": k})
    
    print(f"Retriever ready — will fetch top {k} chunks per query")
    return retriever
