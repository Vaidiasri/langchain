import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

# Load environment variables
load_dotenv()

# Get API key
api_key = (
    os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY") or os.getenv("API_KEY")
)

if not api_key:
    raise SystemExit("Missing API key")

# Initialize the model (Gemini 2.5 Flash)
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7, api_key=api_key)

# Create a prompt template
prompt = PromptTemplate.from_template("What is the capital of {country}?")

# Create a chain
# Using the pipe operator to chain prompt and llm together
chain = prompt | llm

# Run the chain
result = chain.invoke({"country": "France"})
print(result.content)
