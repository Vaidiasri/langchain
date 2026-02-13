# Import required libraries
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict
from pydantic import BaseModel, Field

# Load environment variables
load_dotenv()


# Method 1: Using TypedDict for structured output
class PersonInfoDict(TypedDict):
    """Dictionary structure for person information"""

    name: str
    age: int
    occupation: str
    hobbies: list[str]


# Method 2: Using Pydantic BaseModel (recommended for validation)
class PersonInfo(BaseModel):
    """Person information with validation"""

    name: str = Field(description="The person's full name")
    age: int = Field(description="The person's age in years", ge=0, le=150)
    occupation: str = Field(description="The person's current occupation")
    hobbies: list[str] = Field(description="List of the person's hobbies")


def example_with_typeddict():
    """Example using TypedDict for structured output"""
    print("=" * 60)
    print("Example 1: Using TypedDict")
    print("=" * 60)

    # Get API key
    api_key = (
        os.getenv("GOOGLE_API_KEY")
        or os.getenv("GEMINI_API_KEY")
        or os.getenv("API_KEY")
    )

    if not api_key:
        raise SystemExit("Missing API key")

    # Initialize the model
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.7,
        api_key=api_key,
    )

    # Create structured output model using TypedDict
    structured_llm = llm.with_structured_output(PersonInfoDict)

    # Invoke with a prompt
    prompt = (
        "Tell me about a fictional software engineer named Alice who is 28 years old"
    )
    result = structured_llm.invoke(prompt)

    print(f"\nPrompt: {prompt}\n")
    print(f"Result type: {type(result)}")
    print(f"Result: {result}\n")

    # Access as dictionary
    print(f"Name: {result['name']}")
    print(f"Age: {result['age']}")
    print(f"Occupation: {result['occupation']}")
    print(f"Hobbies: {', '.join(result['hobbies'])}")


def example_with_pydantic():
    """Example using Pydantic BaseModel for structured output"""
    print("\n" + "=" * 60)
    print("Example 2: Using Pydantic BaseModel (Recommended)")
    print("=" * 60)

    # Get API key
    api_key = (
        os.getenv("GOOGLE_API_KEY")
        or os.getenv("GEMINI_API_KEY")
        or os.getenv("API_KEY")
    )

    if not api_key:
        raise SystemExit("Missing API key")

    # Initialize the model
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.7,
        api_key=api_key,
    )

    # Create structured output model using Pydantic
    structured_llm = llm.with_structured_output(PersonInfo)

    # Invoke with a prompt
    prompt = "Tell me about a fictional data scientist named Bob who is 35 years old"
    result = structured_llm.invoke(prompt)

    print(f"\nPrompt: {prompt}\n")
    print(f"Result type: {type(result)}")
    print(f"Result: {result}\n")

    # Access as object attributes
    print(f"Name: {result.name}")
    print(f"Age: {result.age}")
    print(f"Occupation: {result.occupation}")
    print(f"Hobbies: {', '.join(result.hobbies)}")

    # Convert to dictionary if needed
    result_dict = result.model_dump()
    print(f"\nAs dictionary: {result_dict}")


def example_with_raw_dict_schema():
    """Example using raw dictionary schema"""
    print("\n" + "=" * 60)
    print("Example 3: Using Raw Dictionary Schema")
    print("=" * 60)

    # Get API key
    api_key = (
        os.getenv("GOOGLE_API_KEY")
        or os.getenv("GEMINI_API_KEY")
        or os.getenv("API_KEY")
    )

    if not api_key:
        raise SystemExit("Missing API key")

    # Initialize the model
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.7,
        api_key=api_key,
    )

    # Define schema as a dictionary (JSON Schema format)
    schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string", "description": "The person's full name"},
            "age": {"type": "integer", "description": "The person's age"},
            "occupation": {"type": "string", "description": "Current occupation"},
            "hobbies": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of hobbies",
            },
        },
        "required": ["name", "age", "occupation", "hobbies"],
    }

    # Create structured output model using raw schema
    structured_llm = llm.with_structured_output(schema)

    # Invoke with a prompt
    prompt = "Tell me about a fictional teacher named Carol who is 42 years old"
    result = structured_llm.invoke(prompt)

    print(f"\nPrompt: {prompt}\n")
    print(f"Result type: {type(result)}")
    print(f"Result: {result}\n")

    # Access as dictionary
    print(f"Name: {result['name']}")
    print(f"Age: {result['age']}")
    print(f"Occupation: {result['occupation']}")
    print(f"Hobbies: {', '.join(result['hobbies'])}")


def main():
    """Run all examples"""
    try:
        # Example 1: TypedDict
        example_with_typeddict()

        # Example 2: Pydantic (Recommended)
        example_with_pydantic()

        # Example 3: Raw dictionary schema
        example_with_raw_dict_schema()

    except Exception as e:
        print(f"\n[Error] {e}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
