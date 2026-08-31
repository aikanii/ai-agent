from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

# define your providers in order of preference — all free
def get_model():
    try:
        # first choice: groq (fastest)
        model = ChatGroq(model="openai/gpt-oss-120b")
        model.invoke("ping")  # quick test that it actually responds
        print("using groq")
        return model
    except Exception as e:
        # groq is down or rate-limited — fall back to gemini
        print(f"groq failed ({e}); falling back to gemini")
        return ChatGoogleGenerativeAI(model="gemini-2.5-flash")

agent = create_agent(
    model=get_model(),
    tools=[],
    system_prompt="You are a helpful assistant. Be concise and accurate.",
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "say hi and tell me which model you are."}]}
)
print(result["messages"][-1].content)