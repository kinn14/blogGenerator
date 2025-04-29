import os
import dotenv
dotenv.load_dotenv()

os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
llm_model_type = 'groq'
llm_model_name = 'meta-llama/llama-4-maverick-17b-128e-instruct'