from openai import OpenAI
import os

# Option 1: Using environment variable
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Option 2: Directly pass the key (not recommended for production)
client = OpenAI(api_key="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")

MODEL = "gpt-4o-mini"
