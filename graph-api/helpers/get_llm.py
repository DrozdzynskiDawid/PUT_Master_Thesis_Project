import os
from langchain_groq import ChatGroq

def get_llm():
    llm = ChatGroq(
        temperature=0,
        model_name=os.getenv("MODEL_NAME"),
        api_key=os.getenv("GROQ_API_KEY")
    )

    return llm