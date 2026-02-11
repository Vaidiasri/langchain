## Simple CLI Chat Bot (LangChain + Gemini)

This project is a minimal **terminal chat bot** using **LangChain** with **Google Gemini** (`langchain_google_genai`).

### Setup

- **Create a virtualenv** (recommended) and install deps
- **Set your API key**

Create a file named `.env` in the project root:

```bash
GOOGLE_API_KEY=your_key_here
```

### Run

```bash
python main.py
```

Optional flags:

```bash
python main.py --model gemini-1.5-flash --temperature 0.7 --system "You are a helpful assistant."
```

If you get a **404 NOT_FOUND** for a model, list what your key can access and pick one:

```bash
python main.py --list-models
python main.py --model gemini-2.0-flash
```

### Commands

- **`/exit`** or **`/quit`**: quit
- **`/reset`**: clear conversation history

