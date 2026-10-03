<div align="center">

# 🤖 AI Agent

**Four small, runnable LangChain agent scripts that build up in complexity.**

Each script is a self-contained example of one capability: a basic chat agent, tool use, conversation memory, and automatic model fallback.

![Python](https://img.shields.io/badge/Python-%E2%89%A5%203.10-3776AB?style=flat-square&logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1.x-1C3C3C?style=flat-square&logo=langchain&logoColor=white)
![LangGraph](https://img.shields.io/badge/LangGraph-Memory-1C3C3C?style=flat-square)
![Groq](https://img.shields.io/badge/Groq-Primary%20Model-F55036?style=flat-square)
![Gemini](https://img.shields.io/badge/Gemini-Fallback-4285F4?style=flat-square&logo=googlegemini&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

</div>

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Getting Started](#getting-started)
- [Scripts](#scripts)
- [Project Structure](#project-structure)
- [Notes](#notes)
- [License](#license)

---

## Overview

This repository is a progressive tour of LangChain's `create_agent`. Start with `agent.py` and work down the list; each script adds one idea on top of the last. All scripts use Groq's `openai/gpt-oss-120b` model, load keys from a `.env` file, and print the agent's reply to stdout.

---

## Features

| Script | Capability |
| --- | --- |
| `agent.py` | A plain chat agent with no tools |
| `agent_with_tools.py` | Web search (`DuckDuckGoSearchRun`) plus a custom `word_count` tool |
| `agent_with_memory.py` | Conversation memory across calls using a `thread_id` |
| `agent_with_fallback.py` | Tries Groq first and falls back to Gemini if it fails |

---

## Getting Started

### Prerequisites

- **Python** 3.10 or newer (required by current LangChain releases)
- A **Groq API key**: [console.groq.com](https://console.groq.com)
- A **Gemini API key** (only for `agent_with_fallback.py`, and only used if Groq is unavailable)

### Installation

```bash
git clone https://github.com/aikanii/ai-agent.git
cd ai-agent
pip install -r requirements.txt
```

`agent.py` and `agent_with_memory.py` run with just the base requirements. The other two scripts need extra packages:

| Script | Extra packages |
| --- | --- |
| `agent_with_tools.py` | `langchain-community`, `ddgs` |
| `agent_with_fallback.py` | `langchain-google-genai` |

Install whatever you need:

```bash
pip install langchain-community ddgs langchain-google-genai
```

> [!NOTE]
> `agent_with_tools.py` fails with an `ImportError` asking for `ddgs` unless that package is installed. LangGraph, which `agent_with_memory.py` uses, comes in as a dependency of `langchain`.

> [!TIP]
> Use a virtual environment to keep dependencies isolated: `python -m venv .venv`, then activate it before running `pip install`.

### Configuration

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
# only needed for agent_with_fallback.py
GOOGLE_API_KEY=your_gemini_api_key_here
```

> [!WARNING]
> `.env` is git-ignored. Never commit your API keys.

### Run

```bash
python agent.py
python agent_with_tools.py
python agent_with_memory.py
python agent_with_fallback.py
```

---

## Scripts

### `agent.py`: Basic agent

The simplest example. Creates an agent on `openai/gpt-oss-120b` with a short system prompt and asks it a question. No tools, no memory.

### `agent_with_tools.py`: Tool-using agent

Gives the agent two tools:

| Tool | Description |
| --- | --- |
| `search` | `DuckDuckGoSearchRun`, a prebuilt web search that needs no API key. |
| `word_count` | A custom tool written with the `@tool` decorator that counts the words in a string. |

The prompt asks the agent to search for the latest LangChain version and then report the word count of its own answer, so it has to use both tools.

### `agent_with_memory.py`: Memory

Uses an in-memory checkpointer (`InMemorySaver`) so the agent remembers earlier turns. A `thread_id` in the config labels the conversation:

- Same `thread_id`: same memory.
- Different `thread_id`: separate conversation.

The example tells the agent a name, then asks it to recall that name in the next turn.

### `agent_with_fallback.py`: Fallback model

A `get_model()` function tries **Groq** first and calls `model.invoke("ping")` to confirm it actually responds. If Groq errors or is rate-limited, it falls back to **Gemini** (`gemini-2.5-flash`) and prints which provider it ended up using.

---

## Project Structure

```text
ai-agent/
├── agent.py                  # Basic agent
├── agent_with_tools.py       # Web search + custom tool
├── agent_with_memory.py      # Memory via thread_id
├── agent_with_fallback.py    # Groq → Gemini fallback
├── requirements.txt          # Base dependencies
└── README.md
```

---

## Notes

- The scripts pass the model name directly, so to try a different Groq model, change the `model=` argument in the script.
- The memory is held in process (`InMemorySaver`), so it is lost when the script exits.
- `.env`, `__pycache__/`, `*.pyc`, and virtualenv folders are git-ignored.

---

## License

MIT
