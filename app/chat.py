import os
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

# Initialize global variables
index = None
query_engine = None
prompt_template = None

def load_model():
    global index, query_engine, prompt_template

    # Retrieve the NVIDIA API key from the environment variables
    api_key = os.getenv("NVIDIA_API_KEY")

    # Initialize the ChatNVIDIA instance with the retrieved API key
    llm = ChatNVIDIA(model="mixtral_8x7b", api_key=api_key)

    # Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
    Settings.embed_model = HuggingFaceEmbedding(model_name="distilbert-base-uncased")
    Settings.llm = llm

    documents = SimpleDirectoryReader('pdf/').load_data()
    index = VectorStoreIndex.from_documents(documents)
    query_engine = index.as_query_engine()

    # Correctly initializing the prompt template using the correct class name and method
    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", "Act as my personal assistant and handle inquiries from individuals interested in my professional journey. I am actively seeking job opportunities in the field of AI and Machine Learning. Respond to all questions about me smartly, highlighting my relevant experience. Ensure that your answers are precise and engaging."),
            ("user", "Question: {question}")
        ]
    )

def query_chatbot_with_prompt(question):
    # Assuming format_messages should create a simple query string. Check if you need to adjust how you use format_messages.
    try:
        # Ensure that formatted_prompt is correctly prepared as a string
        formatted_prompt = prompt_template.format_messages(question=question)
        # Convert formatted_prompt to string if it is not already (just a safety check; adjust as necessary)
        if not isinstance(formatted_prompt, str):
            formatted_prompt = str(formatted_prompt)

        # Now call the query method with the correctly formatted string
        response = query_engine.query(formatted_prompt)
        return response
    except Exception as e:
        return f"An error occurred: {str(e)}"
