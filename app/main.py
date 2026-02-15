from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.schemas import (
    QueryRequest,
    QueryResponse,
    SourceDocument,
    IndexRequest,
    IndexResponse,
    HealthResponse
)
from app.rag.loader import DocumentLoader
from app.rag.embeddings import EmbeddingsModel
from app.rag.vector_store import VectorStore
from app.rag.retriever import DocumentRetriever
from app.rag.llm import LocalLLM
from app.rag.chain import RAGChain


embeddings_model = None
vector_store = None
retriever = None
llm = None
rag_chain = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global embeddings_model, vector_store, retriever, llm, rag_chain
    
    print("=" * 60)
    print("Initializing RAG Chatbot...")
    print("=" * 60)
    
    try:
        embeddings_model = EmbeddingsModel()
        
        vector_store = VectorStore(embeddings_model.get_embeddings())
        
        try:
            vector_store.load_index()
            print("Loaded existing FAISS index")
        except ValueError:
            print("No existing index found. Please use /index endpoint to create one.")
        
        retriever = DocumentRetriever(vector_store, k=4)
        
        llm = LocalLLM(model="phi", temperature=0.1)
        
        rag_chain = RAGChain(llm, retriever)
        
        print("=" * 60)
        print("RAG Chatbot initialized successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"Error during initialization: {e}")
        print("Some features may not work until you fix the issue.")
    
    yield
    
    print("Shutting down RAG Chatbot...")


app = FastAPI(
    title="RAG Chatbot API",
    description="Retrieval-Augmented Generation chatbot using local models",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    return FileResponse("static/index.html")


@app.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="healthy",
        model=llm.model if llm else "not initialized",
        index_loaded=vector_store.vector_store is not None if vector_store else False
    )


@app.post("/index", response_model=IndexResponse)
async def create_index(request: IndexRequest):
    global vector_store, retriever, rag_chain
    
    if not embeddings_model:
        raise HTTPException(status_code=500, detail="Embeddings model not initialized")
    
    documents_path = request.documents_path
    
    if not Path(documents_path).exists():
        raise HTTPException(
            status_code=404,
            detail=f"Documents directory not found: {documents_path}"
        )
    
    try:
        loader = DocumentLoader(chunk_size=500, chunk_overlap=50)
        chunks = loader.load_and_split(documents_path)
        
        if not chunks:
            raise HTTPException(
                status_code=400,
                detail="No documents found in the specified directory"
            )
        
        vector_store.create_index(chunks)
        
        vector_store.save_index()
        
        retriever = DocumentRetriever(vector_store, k=4)
        rag_chain = RAGChain(llm, retriever)
        
        num_documents = len(set(doc.metadata.get('source', '') for doc in chunks))
        
        return IndexResponse(
            status="Index created successfully",
            num_documents=num_documents,
            num_chunks=len(chunks)
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating index: {str(e)}")


@app.post("/query", response_model=QueryResponse)
async def query_chatbot(request: QueryRequest):
    if not rag_chain:
        raise HTTPException(
            status_code=500,
            detail="RAG chain not initialized. Please create an index first using /index endpoint."
        )
    
    if not vector_store or not vector_store.vector_store:
        raise HTTPException(
            status_code=400,
            detail="No index loaded. Please create an index first using /index endpoint."
        )
    
    try:
        if request.k:
            retriever.k = request.k
        
        result = rag_chain.query(request.question)
        
        sources = []
        for doc in result.get("sources", []):
            source_doc = SourceDocument(
                content=doc.page_content,
                source=doc.metadata.get("source", "unknown"),
                page=doc.metadata.get("page", None)
            )
            sources.append(source_doc)
        
        return QueryResponse(
            answer=result.get("answer", ""),
            sources=sources
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
