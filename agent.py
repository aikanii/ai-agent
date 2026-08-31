from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_groq import ChatGroq
from langchain_community.tools import DuckDuckGoSearchRun

load_dotenv()

llm = ChatGroq(model="openai/gpt-oss-120b")  # or "openai/gpt-oss-20b" for a smaller/faster option

# tool 1 — web search (prebuilt, free, no key)
search = DuckDuckGoSearchRun()

# tool 2 — a function you wrote yourself
@tool
def word_count(text: str) -> int:
    """Count how many words are in a piece of text."""
    return len(text.split())

# hand both tools to the agent
agent = create_agent(
    model=llm,   # was model=model
    tools=[search, word_count],
    system_prompt="You are a helpful assistant. Use your tools when they help answer accurately.",
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "search for the latest langchain version, then tell me how many words your answer is."}]}
)

print(result["messages"][-1].content)