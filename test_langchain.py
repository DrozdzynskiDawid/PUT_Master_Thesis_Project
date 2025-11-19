from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_experimental.graph_transformers import LLMGraphTransformer
from dotenv import load_dotenv
from langchain_core.documents import Document

load_dotenv() 


llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
llm_transformer = LLMGraphTransformer(llm=llm)

text = """
Marie Curie, born in 1867, was a Polish and naturalised-French physicist and chemist who conducted pioneering research on radioactivity.
She was the first woman to win a Nobel Prize, the first person to win a Nobel Prize twice, and the only person to win a Nobel Prize in two scientific fields.
Her husband, Pierre Curie, was a co-winner of her first Nobel Prize, making them the first-ever married couple to win the Nobel Prize and launching the Curie family legacy of five Nobel Prizes.
She was, in 1906, the first woman to become a professor at the University of Paris.
"""
documents = [Document(page_content=text)]

graph_documents = llm_transformer.convert_to_graph_documents(documents)

print("--- Wynik ---")
print(f"Nodes:\n{graph_documents[0].nodes}\n")
print(f"Relationships:\n{graph_documents[0].relationships}")