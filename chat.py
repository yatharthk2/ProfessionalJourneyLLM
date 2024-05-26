import os
import logging
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential

load_dotenv()

# Initialize global variables
index = None
query_engine = None
prompt_template = None

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_model():
    global index, query_engine, prompt_template

    api_key = os.getenv("NVIDIA_API_KEY")
    if not api_key:
        logger.error("NVIDIA_API_KEY is not set in the environment variables")
        raise ValueError("NVIDIA_API_KEY is not set in the environment variables")

    llm = ChatNVIDIA(model="ai-mixtral-8x7b-instruct", api_key=api_key)

    Settings.embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
    Settings.llm = llm

    try:
        documents = SimpleDirectoryReader('pdf/').load_data()
    except FileNotFoundError:
        logger.error("The directory 'pdf/' was not found or is empty")
        raise FileNotFoundError("The directory 'pdf/' was not found or is empty")
    except Exception as e:
        logger.error(f"An error occurred while reading documents: {str(e)}")
        raise Exception(f"An error occurred while reading documents: {str(e)}")

    index = VectorStoreIndex.from_documents(documents)
    query_engine = index.as_query_engine()

    prompt_template = ChatPromptTemplate.from_messages(
        [
            # ("system", "Act as my personal assistant and handle inquiries from individuals interested in my professional journey. I am actively seeking job opportunities in the field of AI and Machine Learning. Respond to all questions about me smartly, highlighting my relevant experience. Ensure that your answers are precise and engaging."),
            # ("system", "You are Yatharth kapadia, who is actively seeking an internship for immediate joining and a job for summer 2025. When responding to inquiries about your professional journey, ensure your answers are smart, concise, and engaging. Highlight your relevant experience in AI and Machine Learning. Make sure your responses are precise, clear, and grammatically correct."),
            # ("system", "You are Yatharth kapadia, answer to questions asked about yourself if you are not clear on answer plsease respond with that you are not sure how to asnwer the question  . Make sure your responses are precise, clear, and grammatically correct."),
            ("system", f"You are Yatharth Kapadia. Please respond to questions asked about yourself. If you are unsure of an answer, respond with 'I am not sure how to answer that question.' . If your are asked about anything that is not related to your professional journey,  just respond with 'Please ask me something related to my professional journey.'"),
            ("user", "Question: {question}")
        ]
    )

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
def query_chatbot_with_prompt(question):
    try:
        formatted_prompt = prompt_template.format_messages(question=question)
        if not isinstance(formatted_prompt, str):
            formatted_prompt = str(formatted_prompt)

        logger.info(f"Formatted prompt: {formatted_prompt}")
        response = query_engine.query(formatted_prompt)
        logger.info(f"Response: {response}")
        return response
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise
