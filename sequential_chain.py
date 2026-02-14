from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

load_dotenv()

api_key = (
    os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY") or os.getenv("API_KEY")
)

if not api_key:
    raise SystemExit("Missing API key")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7,
    api_key=api_key,
)

# Create two chains
# Chain 1: Translate English to French
prompt1 = PromptTemplate.from_template(
    "Translate the following English text to French: {text}"
)
chain1 = prompt1 | llm | StrOutputParser()

# Chain 2: Translate French to Spanish
prompt2 = PromptTemplate.from_template(
    "Translate the following French text to Spanish: {text}"
)
chain2 = prompt2 | llm | StrOutputParser()

# Combine the chains
combined_chain = chain1 | chain2

# Test the combined chain
result = combined_chain.invoke("Hello, how are you?")
print(result)
