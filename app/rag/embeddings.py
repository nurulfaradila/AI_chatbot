from langchain_community.embeddings import HuggingFaceEmbeddings


class EmbeddingsModel:
    
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model_name = model_name
        
        print(f"Loading embeddings model: {model_name}")
        self.embeddings = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        print("Embeddings model loaded successfully")
    
    def get_embeddings(self):
        return self.embeddings
    
    def embed_query(self, text: str) -> list:
        return self.embeddings.embed_query(text)
    
    def embed_documents(self, texts: list) -> list:
        return self.embeddings.embed_documents(texts)
