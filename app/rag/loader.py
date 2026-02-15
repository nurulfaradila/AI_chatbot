from pathlib import Path
from typing import List

from langchain.schema import Document
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


class DocumentLoader:
    
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
    
    def load_documents(self, documents_path: str) -> List[Document]:
        documents = []
        docs_dir = Path(documents_path)
        
        if not docs_dir.exists():
            raise ValueError(f"Documents directory not found: {documents_path}")
        
        for pdf_file in docs_dir.glob("*.pdf"):
            print(f"Loading PDF: {pdf_file.name}")
            loader = PyPDFLoader(str(pdf_file))
            docs = loader.load()
            documents.extend(docs)
        
        for txt_file in docs_dir.glob("*.txt"):
            print(f"Loading TXT: {txt_file.name}")
            loader = TextLoader(str(txt_file), encoding="utf-8")
            docs = loader.load()
            documents.extend(docs)
        
        if not documents:
            raise ValueError(f"No PDF or TXT files found in {documents_path}")
        
        print(f"Loaded {len(documents)} document(s)")
        return documents
    
    def split_documents(self, documents: List[Document]) -> List[Document]:
        chunks = self.text_splitter.split_documents(documents)
        print(f"Split into {len(chunks)} chunks")
        return chunks
    
    def load_and_split(self, documents_path: str) -> List[Document]:
        documents = self.load_documents(documents_path)
        chunks = self.split_documents(documents)
        return chunks
