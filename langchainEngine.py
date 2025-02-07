from langchain.agents import load_tools, initialize_agent
from langchain.llms import OpenAI
from langchain.agents import AgentType
from langchain.tools import 

# 初始化LLM
llm = OpenAI(temperature=0)

# 加载工具，这里是使用SerpAPI进行搜索
tools = load_tools(["serpapi"], llm=llm)

# 初始化Agent
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)