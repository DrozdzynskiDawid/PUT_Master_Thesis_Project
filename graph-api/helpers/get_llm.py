import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

def get_llm():
    load_dotenv()
    llm = ChatGroq(
        temperature=0,
        model_name=os.getenv("MODEL_NAME"),
        api_key=os.getenv("GROQ_API_KEY")
    )

    return llm