import yaml 
from utils.config_loader import load_config 
from langchain_groq import ChatGroq 
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from pydantic import BaseModel, Field
from typing import Literal, List, Dict, Optional, Any
import os 
from dotenv import load_dotenv 
load_dotenv()

class ConfigLoader:
    def __init__(self):
        print(f"Loaded Config")
        self.config = load_config() 
    
    def __getitem__(self, key):
        return self.config[key]

class ModelLoader(BaseModel):
    model_provider: Literal["openai", "groq"] = "openai" 
    config: Optional[ConfigLoader] = Field(default=None, exclude=True) 

    def model_post_init(self, __context: Any) -> None:
        self.config = ConfigLoader() 
    
    class Config: 
        arbitary_types_allowed = True

    def load_llm(self):
        """
        Load and return the LLM model
        """
        print("LLM Loading") 
        print(f"Loading model from provider: {self.model_provider}")
        if self.model_provider == "groq":
            print("Loading LLM from GROQ.............")
            groq_api_key = os.getenv["GROQ_API_KEY"]
            model_name = self.config["llm"]["groq"]["model_name"]
            llm = ChatGroq(model_name = model_name, api_key=groq_api_key)
        elif self.model_provider == "openai":
            print("Loadinng LLM from openai") 
            openai_api_key = os.getenv["OPENAI_API_KEY"] 
            model_name = self.config["llm"]["openai"]["model_name"]
            llm = ChatOpenAI(model_name = model_name, api_key = openai_api_key)
        return llm