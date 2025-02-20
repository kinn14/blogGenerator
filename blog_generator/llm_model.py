import os
from langchain_openai.chat_models import ChatOpenAI
from langchain_groq.chat_models import ChatGroq
import config


class Llm:

    def __init__(self, model_type: str, model_name: str = None) -> None:
        self.model_type = model_type # currently accepting OpenAI or Groq
        self.model_name = model_name

        if self.model_type.lower() == 'openai':
            self.llm_model = ChatOpenAI(temperature=0)

        elif self.model_type.lower() == 'groq':
            model_name = self.model_name
            self.llm_model = ChatGroq(model=self.model_name)
        
    def get_llm_model(self):
        return self.llm_model