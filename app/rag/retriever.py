from typing import List

from langchain.schema import Document

from app.rag.vector_store import VectorStore


class DocumentRetriever:
    
    def __init__(self, vector_store: VectorStore, k: int = 4):
        self.vector_store = vector_store
        self.k = k
    
    def retrieve(self, query: str) -> List[Document]:
        print(f"Retrieving top {self.k} documents for query: {query[:100]}...")
        
        documents = self.vector_store.similarity_search(query, k=self.k)
        
        print(f"Retrieved {len(documents)} documents")
        
        for i, doc in enumerate(documents, 1):
            source = doc.metadata.get('source', 'unknown')
            print(f"  [{i}] Source: {source}")
        
        return documents
    
    def get_retriever_interface(self):
        return self.vector_store.get_retriever(k=self.k)
