import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
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

# Define prompts
notes_prompt = PromptTemplate.from_template(
    """
    You are an expert note-taker. 
    Read the following text and create concise, bulleted study notes.
    Focus on key concepts and definitions.

    Text:
    {context}
    
    Notes:
    """
)

quiz_prompt = PromptTemplate.from_template(
    """
    You are a teacher creating a quiz.
    Read the following text and create a 3-question multiple-choice quiz.
    Include the correct answer for each question.

    Text:
    {context}
    
    Quiz:
    """
)

# Create chains for each branch
# Branch 1: Generate Notes
notes_chain = notes_prompt | llm | StrOutputParser()

# Branch 2: Generate Quiz
quiz_chain = quiz_prompt | llm | StrOutputParser()

# Combine chains in parallel
# The input dictionary key "context" is passed to both chains
parallel_chain = RunnableParallel(notes=notes_chain, quiz=quiz_chain)

# Example Usage
if __name__ == "__main__":
    sample_text = """
    Photosynthesis is the process by which green plants and some other organisms use sunlight to synthesize foods with the aid of chlorophyll. 
    Photosynthesis in plants generally involves the green pigment chlorophyll and generates oxygen as a byproduct. 
    The process takes place in chloroplasts. The overall reaction is: 
    6CO2 + 6H2O + light energy -> C6H12O6 + 6O2.
    This means carbon dioxide and water are converted into glucose (sugar) and oxygen.
    """

    print(f"Input Text:\n{sample_text}\n")
    print("=" * 60)
    print("Generating Notes and Quiz in parallel...")
    print("=" * 60)

    result = parallel_chain.invoke({"context": sample_text})

    print("\nSTUDY NOTES:")
    print("-" * 20)
    print(result["notes"])

    print("\n\n QUIZ:")
    print("-" * 20)
    print(result["quiz"])
