import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableBranch
from langchain_core.output_parsers import StrOutputParser

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

# ---------------------------------------------------------
# Step 1: Sentiment Classification Chain
# ---------------------------------------------------------
classifier_prompt = PromptTemplate.from_template(
    """
    Classify the sentiment of the following text as strictly 'POSITIVE', 'NEGATIVE', or 'NEUTRAL'.
    Output ONLY one word. Do not add punctuation or explanation.

    Text: {text}
    
    Sentiment:
    """
)

# Using StrOutputParser to get clean string output
classifier_chain = classifier_prompt | llm | StrOutputParser()


# ---------------------------------------------------------
# Step 2: Define Response Chains for Each Sentiment
# ---------------------------------------------------------

# Positive Chain
positive_prompt = PromptTemplate.from_template(
    """
    You are a friendly customer service representative.
    Write a short, enthusiastic thank you note to a customer who gave this positive feedback:
    "{text}"
    """
)
positive_chain = positive_prompt | llm | StrOutputParser()

# Negative Chain
negative_prompt = PromptTemplate.from_template(
    """
    You are a professional and empathetic customer service representative.
    Write a short, sincere apology and offer support to a customer who gave this negative feedback:
    "{text}"
    """
)
negative_chain = negative_prompt | llm | StrOutputParser()

# Neutral Chain
neutral_prompt = PromptTemplate.from_template(
    """
    You are a polite customer service representative.
    Write a short, standard acknowledgment for this neutral feedback:
    "{text}"
    """
)
neutral_chain = neutral_prompt | llm | StrOutputParser()


# ---------------------------------------------------------
# Step 3: Branching Logic (Routing)
# ---------------------------------------------------------

# Define the routing logic based on the classifier output
branch = RunnableBranch(
    (lambda x: "POSITIVE" in x["sentiment"].upper(), positive_chain),
    (lambda x: "NEGATIVE" in x["sentiment"].upper(), negative_chain),
    neutral_chain,  # Default branch (Neutral)
)

# ---------------------------------------------------------
# Step 4: Combined Chain
# ---------------------------------------------------------

# The full chain:
# 1. Classify sentiment
# 2. Pass original text AND sentiment to the branch
# 3. Branch executes appropriate chain
full_chain = {"sentiment": classifier_chain, "text": lambda x: x["text"]} | branch


# ---------------------------------------------------------
# Example Usage
# ---------------------------------------------------------
import time

if __name__ == "__main__":
    examples = [
        "I absolutely love this product! It's amazing.",
        "This is the worst service I have ever received. Terrible.",
        " The package arrived on time.",
    ]

    print("=" * 60)
    print("Conditional Chain: Sentiment Analysis -> Specific Response")
    print("=" * 60)

    for i, text in enumerate(examples):
        print(f"\nProcessing example {i+1}/{len(examples)}...")
        print(f"Input: '{text}'")

        try:
            # Determine sentiment first just for display purposes (the chain does this internally too)
            sentiment_check = classifier_chain.invoke({"text": text}).strip().upper()
            print(f"Detected Sentiment: {sentiment_check}")

            # Run the full chain
            response = full_chain.invoke({"text": text})
            print(f"Response:\n{response.strip()}")
            print("-" * 60)

            # Add delay to respect rate limits (5 RPM = 1 request every 12s)
            # We are making 2 calls per iteration (classifier + response), so we need significant padding
            if i < len(examples) - 1:
                print("Waiting 15s to respect API rate limits...")
                time.sleep(15)

        except Exception as e:
            print(f"Error processing example: {e}")
            break
