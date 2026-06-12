# ReAct-style Autonomous Agent (Groq + Tavily)

A minimal Python example of a ReAct-style autonomous agent that uses the Groq client for model completions and a small set of callable tools implemented in `tools.py`.

## Overview

- `agent.py` implements a simple loop:
  - Loads the system prompt from `System Prompt.md`.
  - Sends user + system messages to Groq's chat completions API.
  - Reads any `tool_calls` returned by the model and dispatches them to the implementations in `tools.py`.
  - Appends tool outputs back into the conversation and continues until the model signals `stop` or a max iteration limit.

## Features

- ReAct-style reasoning + tool invocation loop
- Tool schemas declared in `tools.TOOL_SCHEMAS`
- Built-in tool implementations: file read/write/edit, shell command execution, web search (via Tavily), and directory listing
- Small, easy-to-extend codebase for experimentation

## Requirements

- Python 3.8+ (3.10+ recommended)
- The project uses these Python packages (install with pip):

```
pip install groq tavily python-dotenv
```

Note: check the respective package documentation for exact installation names and authentication steps (Groq/Tavily may require API keys or additional setup).

## Setup

1. Create a virtual environment and activate it:

```
python -m venv .venv
.venv\Scripts\activate    # Windows
source .venv/bin/activate # macOS / Linux
```

2. Install dependencies:

```
pip install -r requirements.txt  # if you create one
# or
pip install groq tavily python-dotenv
```

3. Add environment variables (create a `.env` file in the project root):

```
TAVILY_API_KEY=your_tavily_api_key_here
# If Groq requires an API key, add it according to Groq docs (e.g. GROQ_API_KEY=...)
```

## Usage

Run the agent and type a prompt when asked:

```
python agent.py
Enter prompt: Summarize the repository
```

The agent will print model reasoning and will execute any model-specified tool calls (see warnings below).

## Important files

- [agent.py](agent.py) — Main driver that runs the conversation loop and dispatches tool calls.
- [tools.py](tools.py) — Tool schemas (`TOOL_SCHEMAS`) and implementations (`read_file`, `write_file`, `edit_file`, `shell_command`, `web_search`, `list_directory`). The dispatch function is `execute_tool_call`.
- [System Prompt.md](System Prompt.md) — The system prompt used by the agent to set behavior and role.

## Extending the agent

- To add a new tool:
  1. Add a tool schema to `TOOL_SCHEMAS` in `tools.py`.
  2. Implement the callable Python function in `tools.py`.
  3. Add the function to the `available_function` mapping so `execute_tool_call` can dispatch to it.

## Security & Safety

- `tools.py` exposes a `shell_command` tool that runs arbitrary shell commands. Do not run untrusted prompts with this agent.
- Review and audit the tool implementations before giving the agent access to sensitive systems or production data.

## Troubleshooting

- If you see import errors, confirm dependencies are installed and your virtual environment is active.
- If web-based tools fail, ensure the required API keys are present in `.env` and correctly loaded.

## Contributing

Contributions are welcome. Open issues or PRs to add features, tests, or documentation.

## License

No license is included by default — add a LICENSE file if you want to specify terms.

---

If you'd like, I can also:
- generate a `requirements.txt` listing the detected imports
- add a small `.gitignore` and basic `README` badge
- run a quick sanity check (static) on imports

Tell me which of the above you'd like next.
