import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
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

# 1. Load the document using LangChain TextLoader
print("Loading document...")
try:
    # Explicitly creating the loader with utf-8 encoding
    loader = TextLoader("dummy_data.txt", encoding="utf-8")
    documents = loader.load()
    # Extract content from the loaded document(s)
    document_content = "\n\n".join([doc.page_content for doc in documents])
except Exception as e:
    # Fallback to try without encoding if utf-8 fails, or report specific error
    print(f"Error loading document with utf-8: {e}")
    try:
        print("Retrying with default encoding...")
        loader = TextLoader("dummy_data.txt")
        documents = loader.load()
        document_content = "\n\n".join([doc.page_content for doc in documents])
    except Exception as e2:
        print(f"Error loading document in fallback: {e2}")
        import traceback

        traceback.print_exc()
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
