from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

from app.rag.llm import LocalLLM
from app.rag.retriever import DocumentRetriever


class RAGChain:
    
    PROMPT_TEMPLATE = """You are a helpful AI assistant. Use the following pieces of context to answer the question at the end.

If you cannot find the answer in the provided context, you MUST respond with:
"I don't have enough information in the provided documents."

Do NOT make up information or use knowledge outside the provided context.

Context:
{context}

Question: {question}

Answer:"""
    
    def __init__(self, llm: LocalLLM, retriever: DocumentRetriever):
        self.llm = llm
        self.retriever = retriever
        
        self.prompt = PromptTemplate(
            template=self.PROMPT_TEMPLATE,
            input_variables=["context", "question"]
        )
        
        print("Creating RAG chain...")
        self.chain = RetrievalQA.from_chain_type(
            llm=llm.get_llm(),
            chain_type="stuff",
            retriever=retriever.get_retriever_interface(),
            return_source_documents=True,
            chain_type_kwargs={"prompt": self.prompt}
        )
        print("RAG chain created successfully")
    
    def query(self, question: str) -> dict:
        print(f"\nProcessing query: {question}")
        
        response = self.chain.invoke({"query": question})
        
        answer = response.get("result", "")
        sources = response.get("source_documents", [])
        
        print(f"Generated answer: {answer[:100]}...")
        print(f"Used {len(sources)} source document(s)")
        
        return {
            "answer": answer,
            "sources": sources
        }
