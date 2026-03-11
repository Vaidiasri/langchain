from langchain_core.tools import tool

# Step 1 & 2: Make a simple python function with type hints
@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers together."""
    # Step 3: (Already added the @tool decorator above)
    return a * b

if __name__ == "__main__":
    # Demonstrate the tool
    print("--- Custom Multiplication Tool ---")
    
    # Test values
    val1, val2 = 5, 10
    
    # Direct calling
    result = multiply.invoke({"a": val1, "b": val2})
    
    print(f"Multiplying {val1} and {val2}...")
    print(f"Result: {result}")
    
    # Tool metadata
    print("\nTool Metadata:")
    print(f"Name: {multiply.name}")
    print(f"Description: {multiply.description}")
    print(f"Args Schema: {multiply.args}")
