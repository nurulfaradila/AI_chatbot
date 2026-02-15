from pathlib import Path
from typing import List, Optional

from langchain.schema import Document
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings


class VectorStore:
    
    def __init__(self, embeddings: HuggingFaceEmbeddings, index_path: str = "data/faiss_index"):
        self.embeddings = embeddings
        self.index_path = index_path
        self.vector_store: Optional[FAISS] = None
    
    def create_index(self, documents: List[Document]) -> FAISS:
        if not documents:
            raise ValueError("Cannot create index from empty document list")
        
        print(f"Creating FAISS index from {len(documents)} documents...")
        
        self.vector_store = FAISS.from_documents(
            documents=documents,
            embedding=self.embeddings
        )
        
        print("FAISS index created successfully")
        return self.vector_store
    
    def save_index(self):
        if self.vector_store is None:
            raise ValueError("No vector store to save. Create or load an index first.")
        
        Path(self.index_path).parent.mkdir(parents=True, exist_ok=True)
        
        print(f"Saving FAISS index to {self.index_path}")
        self.vector_store.save_local(self.index_path)
        print("Index saved successfully")
    
    def load_index(self) -> FAISS:
        if not Path(self.index_path).exists():
            raise ValueError(f"Index not found at {self.index_path}. Create an index first.")
        
        print(f"Loading FAISS index from {self.index_path}")
        
        try:
            self.vector_store = FAISS.load_local(
                self.index_path,
                self.embeddings,
                allow_dangerous_deserialization=True
            )
        except TypeError:
            self.vector_store = FAISS.load_local(
                self.index_path,
                self.embeddings
            )
        
        print("Index loaded successfully")
        return self.vector_store
    
    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        if self.vector_store is None:
            raise ValueError("No vector store available. Create or load an index first.")
        
        results = self.vector_store.similarity_search(query, k=k)
        return results
    
    def get_retriever(self, k: int = 4):
        if self.vector_store is None:
            raise ValueError("No vector store available. Create or load an index first.")
        
        return self.vector_store.as_retriever(search_kwargs={"k": k})
