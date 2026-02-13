# Simple example: Using structured output with dict type in LangChain
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field

# Load environment variables
load_dotenv()

# Get API key
api_key = (
    os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY") or os.getenv("API_KEY")
)

if not api_key:
    raise SystemExit("Missing API key")


# Define your output structure using Pydantic
class MovieReview(BaseModel):
    """Structure for movie review"""

    title: str = Field(description="Movie title")
    rating: float = Field(description="Rating from 0-10", ge=0, le=10)
    genre: str = Field(description="Movie genre")
    summary: str = Field(description="Brief summary")
    pros: list[str] = Field(description="List of positive aspects")
    cons: list[str] = Field(description="List of negative aspects")


# Initialize the model
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7,
    api_key=api_key,
)

# Create structured output version
structured_llm = llm.with_structured_output(MovieReview)

# Get structured response
print("Asking LLM to review a movie in structured format...\n")
result = structured_llm.invoke("Review the movie 'The Matrix' from 1999")

# Access as object attributes
print(f"Title: {result.title}")
print(f"Rating: {result.rating}/10")
print(f"Genre: {result.genre}")
print(f"\nSummary: {result.summary}")
print(f"\nPros:")
for pro in result.pros:
    print(f"  ✓ {pro}")
print(f"\nCons:")
for con in result.cons:
    print(f"  ✗ {con}")

# Convert to dictionary
print("\n" + "=" * 60)
print("As dictionary:")
print("=" * 60)
result_dict = result.model_dump()
print(result_dict)

# Access dictionary values
print(f"\nAccessing dict values:")
print(f"Title from dict: {result_dict['title']}")
print(f"Rating from dict: {result_dict['rating']}")
