import os
from dotenv import load_dotenv
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_groq import ChatGroq  
from langchain_core.documents import Document

load_dotenv()
# inicjalizacja LLM
llm = ChatGroq(
    temperature=0,
    model_name="openai/gpt-oss-120b",
    api_key=os.getenv("GROQ_API_KEY")
)

# ontologia
schema = {
    "allowed_nodes": ["Task", "Method", "Metric", "Material", "OtherScientificTerm", "Generic"],
    "allowed_relationships": ["USED-FOR", "FEATURE-OF", "PART-OF", "COMPARE", "HYPONYM-OF", "EVALUATE-FOR"]
}
llm_transformer = LLMGraphTransformer(
    llm=llm,
    allowed_nodes=schema["allowed_nodes"],
    allowed_relationships=schema["allowed_relationships"]
)

# Przykładowy tekst z Scierc
text_from_scierc = "English is shown to be trans-context-free on the basis of coordinations of the respectively type that involve strictly syntactic cross-serial agreement . The agreement in question involves number in nouns and reflexive pronouns and is syntactic rather than semantic in nature because grammatical number in English , like grammatical gender in languages such as French , is partly arbitrary . The formal proof , which makes crucial use of the Interchange Lemma of Ogden et al. , is so constructed as to be valid even if English is presumed to contain grammatical sentences in which respectively operates across a pair of coordinate phrases one of whose members has fewer conjuncts than the other ; it thus goes through whatever the facts may be regarding constructions with unequal numbers of conjuncts in the scope of respectively , whereas other arguments have foundered on this problem ."
documents = [Document(page_content=text_from_scierc)]

try:
    print("Wysyłanie zapytania do Groq...")
    graph_documents = llm_transformer.convert_to_graph_documents(documents)

    print("\n--- WYNIKI ---")
    if graph_documents:
        print(f"Nodes ({len(graph_documents[0].nodes)}):\n {graph_documents[0].nodes}")
        print(f"\nRelationships ({len(graph_documents[0].relationships)}):")
        for rel in graph_documents[0].relationships:
            print(f"  {rel.source.id} --[{rel.type}]--> {rel.target.id}")
    else:
        print("Nie znaleziono relacji.")
        
except Exception as e:
    print(f"Wystąpił błąd: {e}")