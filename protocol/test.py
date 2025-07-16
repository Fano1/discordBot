from langchain_ollama import ChatOllama

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor, initialize_agent

from pydantic import BaseModel


class Response(BaseModel): #how a llm should response
    topic: str
    summary: str
    src : list[str]
    tools_Used : list[str]

modelr = "yoimiya"
temp = 0.2
microstatr = 1 # 0 for disable and 2 for perplexity 2.0
microstat_taur = 5.0 # (lower -> )coherence and diverstty , default 5
microstat_etar = 0.1 # generates less bull shit
num_ctxr = 2048 #context window to generate next token
max_predictr = 128 # -1 infinite gen, -2 fill context
repeatLastN = 64 #Sets how far back for the model to look back to prevent repetition. (Default: 64, 0 =disabled, -1 = num_ctx)
repeat_penaltyr = 1.1 
topK = 40
topP = 0.9

llmMain = ChatOllama(
    model = modelr, 
    microstat = microstatr,
    microstat_eta = microstat_etar, 
    microstat_tau = microstat_taur, 
    temperature = temp, 
    num_ctx= num_ctxr, 
    max_predict = max_predictr , 
    repeat_last_n = repeatLastN, 
    repeat_penalty = repeat_penaltyr, 
    top_K = topK, 
    top_P = topP
    )
parser = PydanticOutputParser(pydantic_object= Response)


prompt = ChatPromptTemplate.from_messages([
    ( 
        "system",
         """
        Your name is Yoimiya Fano, a research assistant that will help generate a research paper.
        Answer the research query and use the neccary research tools.
        Wrap the output in this format and provide no other text:
        {format_instructions}

        you generate the response in a json format, you give topic key, summary key, source key and tool used key in this format

        No extra text or explanation. Answer as Yoimiya only."
         """,
    ),
    ("human", "{query}"),
    ("placeholder", "{agent_scratchpad}"),
]).partial(format_instructions= parser.get_format_instructions())


agent = create_tool_calling_agent(
    llm = llmMain,
    prompt= prompt,
    tools = []
)

def response(messagectx):
    agentExe = AgentExecutor(agent= agent, tools=[], verbose=True)
    
    raw_response = agentExe.invoke({"query": messagectx})
    structuredAns = (raw_response.get("output"))
    return str(structuredAns)
