# Import required libraries
import os  # For environment variable access
from dotenv import load_dotenv  # Load environment variables from .env file
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
)  # Google Gemini LLM integration
import argparse  # Command-line argument parsing

# Import message types for chat history
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Simple CLI chat bot (Gemini via LangChain)."
    )
    p.add_argument("--model", default="gemini-2.5-flash", help="Gemini model name")
    p.add_argument(
        "--temperature", type=float, default=0.7, help="Sampling temperature"
    )
    p.add_argument(
        "--system",
        default="You are a helpful assistant.",
        help="System instruction (role prompt)",
    )
    p.add_argument(
        "--list-models",
        action="store_true",
        help="List available models for your API key and exit",
    )
    return p


def main() -> int:
    """Main function to run the CLI chat bot.

    Returns:
        int: Exit code (0 for success)
    """
    # Load environment variables from .env file
    load_dotenv()

    # Parse command-line arguments
    args = build_arg_parser().parse_args()

    # Retrieve API key from environment variables
    # Priority: GOOGLE_API_KEY > GEMINI_API_KEY > API_KEY
    api_key = (
        os.getenv("GOOGLE_API_KEY")
        or os.getenv("GEMINI_API_KEY")
        or os.getenv("API_KEY")
    )

    # Ensure API key is present before proceeding
    if not api_key:
        raise SystemExit(
            "Missing API key. Set GOOGLE_API_KEY (recommended) or GEMINI_API_KEY (or API_KEY) in .env or your environment."
        )

    # Handle --list-models flag: display available models and exit
    if args.list_models:
        from google import genai

        # Create a Google GenAI client to fetch available models
        client = genai.Client(api_key=api_key)
        print("Available models:\n")

        # List all models accessible with the current API key
        for m in client.models.list():
            name = getattr(m, "name", None) or str(m)
            print(f"- {name}")
        return 0

    # Initialize the Gemini chat model with specified parameters
    llm = ChatGoogleGenerativeAI(
        model=args.model,
        temperature=args.temperature,
        api_key=api_key,
    )

    # Start the interactive chat loop
    print("CLI Chat Bot (Gemini). Type /exit to quit, /reset to clear history.\n")

    # Initialize conversation history with system message
    # This maintains context across multiple turns
    history: list = [SystemMessage(content=args.system)]

    # Main chat loop - runs until user exits
    while True:
        try:
            # Get user input
            user_text = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            # Handle Ctrl+C or Ctrl+D gracefully
            print("\nBye.")
            return 0

        # Skip empty inputs
        if not user_text:
            continue

        # Handle exit commands
        if user_text.lower() in {"/exit", "/quit"}:
            print("Bye.")
            return 0

        # Handle reset command - clears conversation history
        if user_text.lower() == "/reset":
            history = [SystemMessage(content=args.system)]
            print("(history cleared)")
            continue

        # Add user message to conversation history
        history.append(HumanMessage(content=user_text))

        try:
            # Send the entire conversation history to the model
            response = llm.invoke(history)
        except Exception as e:
            msg = str(e)

            # Handle model name format error (missing "models/" prefix)
            # Some models require the "models/" prefix in their name
            if (
                "NOT_FOUND" in msg
                and "models/" in msg
                and not args.model.startswith("models/")
            ):
                try:
                    # Retry with "models/" prefix
                    llm = ChatGoogleGenerativeAI(
                        model=f"models/{args.model}",
                        temperature=args.temperature,
                        api_key=api_key,
                    )
                    response = llm.invoke(history)
                except Exception as e2:
                    # If retry fails, display error and continue
                    print(f"[error] {e2}")
                    history.pop()  # Remove failed user message
                    continue
            else:
                # Handle other errors (network issues, rate limits, etc.)
                print(f"[error] {e}")
                # Remove the last user message to avoid duplicating context on retry
                history.pop()
                continue

        # Add AI response to history for conversational context
        # This allows the model to remember previous exchanges
        history.append(AIMessage(content=response.content))

        # Display the AI's response to the user
        print(response.content)


if __name__ == "__main__":
    raise SystemExit(main())
