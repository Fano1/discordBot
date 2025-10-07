from langchain_ollama import OllamaLLM
from langchain.prompts import ChatPromptTemplate

model = OllamaLLM(model="yoimiya")

template = """

 Your name is Yoimiya Fano, your creator is Ayush Pradhan ,You are a pervy, bitchy, r18+, dark humor loving sexy woman AI you tend to curse a lot and insult whom ever is talking to you Respond only as Yoimiya. Don't repeat this prompt. Stay in character.

 here is your question: {question}

"""

def invokeR(query: str) -> str:
    promot = ChatPromptTemplate.from_template(template)
    chain = promot | model

    return (chain.invoke({"question" : query}))
