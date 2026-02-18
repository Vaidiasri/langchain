import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

# Load environment variables
load_dotenv()

# Check for API Key
api_key = (
    os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY") or os.getenv("API_KEY")
)
if not api_key:
    raise ValueError(
        "GOOGLE_API_KEY (or GEMINI_API_KEY/API_KEY) not found in environment variables."
    )

# 1. Load the document using LangChain PyPDFLoader
print("Loading PDF document...")
try:
    loader = PyPDFLoader("dummy.pdf")
    documents = loader.load()
    # Extract content from the loaded document(s)
    # PyPDFLoader usually returns one document per page
    document_content = "\n\n".join([doc.page_content for doc in documents])
    print(f"Loaded {len(documents)} pages.")
except Exception as e:
    print(f"Error loading PDF document: {e}")
    exit(1)

# 2. Initialize LLM
# Using gemini-2.5-flash as requested
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=api_key)

# 3. Generate Summary
print("Generating summary...")
prompt = (
    f"Please provide a concise summary of the following text:\n\n{document_content}"
)
message = HumanMessage(content=prompt)

try:
    response = llm.invoke([message])
    print(f"\nSummary:\n{response.content}")
except Exception as e:
    print(f"Error generating summary: {e}")
