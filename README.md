# LangChain + Google Gemini Examples

This project demonstrates how to use **LangChain** with **Google Gemini** (`langchain_google_genai`) for various use cases, including chatbots, simple chains, and structured outputs.

## 🚀 Setup

1.  **Clone the repository** and navigate to the project folder.
2.  **Create a virtual environment** (recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # on Windows: venv\Scripts\activate
    ```
3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

    > **Note:** If you are using a virtual environment (like `myenv`), make sure to activate it *before* installing dependencies.

4.  **Set your API key**:
    Create a `.env` file in the project root:
    ```bash
    GOOGLE_API_KEY=your_key_here
    ```

## 📚 Examples

### 1. Interactive CLI Chatbot (`main.py`)

A simple terminal-based chat bot that remembers conversation history.

```bash
python main.py
```

**Options:**

- `--model`: Specify model (default: `gemini-2.5-flash`)
- `--temperature`: Set creativity (0.0 to 1.0)
- `--system`: Set system prompt
- `--list-models`: List available models

**Commands:**

- `/exit` or `/quit`: Exit the chat
- `/reset`: Clear conversation history

---

### 2. Simple Chain (`simple_chain.py`)

Demonstrates a basic LangChain pipeline using `PromptTemplate` and Gemini.

```bash
python simple_chain.py
```

_Asks: "What is the capital of France?"_

---

### 3. Structured Output (`structured_output_example.py`)

Comprehensive examples showing how to get **JSON/Dictionary responses** from the LLM.

```bash
python structured_output_example.py
```

**Covers 3 methods:**

1.  **TypedDict**: Simple dictionary structure
2.  **Pydantic BaseModel**: Validated structure (Recommended)
3.  **JSON Schema**: Raw schema definition

---

### 4. Simple Structured Example (`simple_dict_example.py`)

A practical example of generating a movie review in a specific dictionary format.

```bash
python simple_dict_example.py
```

---

### 5. Sequential Chain (`sequential_chain.py`)

Demonstrates how to chain multiple LLM calls together using LCEL (LangChain Expression Language).
Input -> Translate to French -> Translate to Spanish -> Output.

```bash
python sequential_chain.py
```

_Example: English "Hello" -> French "Bonjour" -> Spanish "Hola"_

### 6. Parallel Chain (`parallel_chain.py`)

Demonstrates how to run multiple chains **simultaneously** using `RunnableParallel`.
Input -> [Make Notes] + [Make Quiz] -> Combined Output.

```bash
python parallel_chain.py
```

_Example: Input text -> Returns dictionary with "notes" and "quiz"._

### 7. Conditional Chain (`conditional_chain.py`)

Demonstrates how to route requests to different chains based on logic (Sentiment Analysis) using `RunnableBranch`.
Input -> [Sentiment Classifier] -> [Positive/Negative/Neutral] Branch -> Specific Response.

```bash
python conditional_chain.py
```

_Example: "I love this!" routes to Positive Chain -> "Thank you note"._

### 8. Document Loaders (RAG Basics)

Demonstrates how to load and summarize documents using specific loaders.

**A. Text Document Loader (`text_doc.py`)**
Loads a text file (`dummy_data.txt`) and summarizes it.

```bash
python text_doc.py
```

**B. PDF Document Loader (`pdf_doc.py`)**
First, generate a dummy PDF:
```bash
python generate_pdf.py
```
Then, load and summarize it:
```bash
python pdf_doc.py
```

_Note: Ensure `pypdf` and `reportlab` are installed._


## 📖 Documentation

See [structured_output_guide.md](structured_output_guide.md) for a detailed guide on using structured outputs.
