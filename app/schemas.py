from typing import List, Optional
from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    
    question: str = Field(
        ...,
        description="User's question to the chatbot",
        min_length=1,
        example="What is the main topic of the documents?"
    )
    
    k: Optional[int] = Field(
        default=4,
        description="Number of relevant chunks to retrieve",
        ge=1,
        le=10
    )


class SourceDocument(BaseModel):
    
    content: str = Field(..., description="Content of the source chunk")
    source: str = Field(..., description="Source file name")
    page: Optional[int] = Field(None, description="Page number (for PDFs)")


class QueryResponse(BaseModel):
    
    answer: str = Field(..., description="Chatbot's answer")
    sources: List[SourceDocument] = Field(
        default=[],
        description="Source documents used to generate the answer"
    )


class IndexRequest(BaseModel):
    
    documents_path: Optional[str] = Field(
        default="data/documents",
        description="Path to documents directory"
    )


class IndexResponse(BaseModel):
    
    status: str = Field(..., description="Status message")
    num_documents: int = Field(..., description="Number of documents indexed")
    num_chunks: int = Field(..., description="Number of chunks created")


class HealthResponse(BaseModel):
    
    status: str = Field(..., description="Service status")
    model: str = Field(..., description="LLM model name")
    index_loaded: bool = Field(..., description="Whether vector index is loaded")
