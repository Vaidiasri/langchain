import sys

try:
    import langchain

    print(f"LangChain version: {langchain.__version__}")
    print(f"LangChain file: {langchain.__file__}")
    print(f"LangChain dir: {dir(langchain)}")
except ImportError as e:
    print(f"Error importing langchain: {e}")

try:
    import langchain.chains

    print("Successfully imported langchain.chains")
except ImportError as e:
    print(f"Error importing langchain.chains: {e}")

try:
    from langchain.chains.summarize import load_summarize_chain

    print("Successfully imported load_summarize_chain")
except ImportError as e:
    print(f"Error importing load_summarize_chain: {e}")

import site

print(f"Site packages: {site.getsitepackages()}")
