from langchain_community.llms import Ollama


class LocalLLM:
    
    def __init__(
        self,
        model: str = "llama3",
        base_url: str = "http://localhost:11434",
        temperature: float = 0.1
    ):
        self.model = model
        self.base_url = base_url
        self.temperature = temperature
        
        print(f"Initializing Ollama LLM with model: {model}")
        
        self.llm = Ollama(
            model=model,
            base_url=base_url,
            temperature=temperature
        )
        
        print("Ollama LLM initialized successfully")
    
    def get_llm(self):
        return self.llm
    
    def invoke(self, prompt: str) -> str:
        return self.llm.invoke(prompt)
