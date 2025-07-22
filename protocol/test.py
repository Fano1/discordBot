from langchain_ollama import OllamaLLM
from langchain.prompts import ChatPromptTemplate

model = OllamaLLM(model="yoimiya")

template = """


"""

def invokeR(query: str) -> str:
    promot = ChatPromptTemplate.from_template(template)
    chain = promot | model

    return (chain.invoke({"question" : query}))
