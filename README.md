# AI Agent

A collection of small, runnable LangChain agent scripts that build up in complexity. Each script is a self-contained example showing a different capability.

## Features

- **Basic agent** — a plain chat agent with no tools.
- **Tool-using agent** — adds a prebuilt web-search tool (`DuckDuckGoSearchRun`) and a custom `word_count` tool.
- **Memory** — keeps conversation context across calls using a `thread_id`.
- **Fallback model** — tries one provider and automatically falls back to another if it fails.

## Requirements

- Python 3.9+
- A [Groq](https://console.groq.com) API key (see setup below). The fallback script also needs a Gemini API key, used only if Groq is unavailable.

## Setup

1. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

   The scripts that use tools, memory, or fallback also need these extras:

   ```bash
   pip install langchain-community langgraph langchain-google-genai
   ```

2. **Create a `.env` file** in the project root with your API keys:

   ```env
   GROQ_API_KEY=your_groq_api_key_here
   # only needed for agent_with_fallback.py
   GOOGLE_API_KEY=your_gemini_api_key_here
   ```

   `.env` is git-ignored, so your keys stay out of version control.

3. **Run any script**

   ```bash
   python agent.py
   python agent_with_tools.py
   python agent_with_memory.py
   python agent_with_fallback.py
   ```

## Scripts

### `agent.py` — Basic agent

The simplest example. Creates an agent with the `openai/gpt-oss-120b` model and asks it a question. No tools, no memory.

### `agent_with_tools.py` — Tool-using agent

Gives the agent two tools:

| Tool | Description |
| --- | --- |
| `search` | `DuckDuckGoSearchRun` — prebuilt web search, no API key needed. |
| `word_count` | A custom tool written with the `@tool` decorator that counts words in a string. |

The prompt asks the agent to search the web and then report the word count of its own answer.

### `agent_with_memory.py` — Memory

Uses an in-memory checkpointer (`InMemorySaver`) so the agent remembers earlier turns. A `thread_id` in the config labels the conversation:

- Same `thread_id` → same memory.
- Different `thread_id` → separate conversation.

The example tells the agent a name, then asks it to recall that name in the next turn.

### `agent_with_fallback.py` — Fallback model

A `get_model()` function tries **Groq** first and calls `model.invoke("ping")` to confirm it actually works. If Groq errors or is rate-limited, it falls back to **Gemini** (`gemini-2.5-flash`) and tells you which provider it ended up using.

## Notes

- The model in each script is `openai/gpt-oss-120b`; `agent_with_tools.py`'s comment also mentions `openai/gpt-oss-20b` as a smaller/faster alternative.
- All scripts print the agent's reply to stdout.
- `.env`, `__pycache__/`, `*.pyc`, and virtualenv folders are git-ignored.

## License

MIT
