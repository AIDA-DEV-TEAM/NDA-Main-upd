from dotenv import load_dotenv
import os

load_dotenv()

required_vars = ["AZURE_OPENAI_ENDPOINT", "AZURE_OPENAI_API_KEY", "OPENAI_API_VERSION"]

print("Environment Variable Check:")
for var in required_vars:
    value = os.getenv(var)
    if value:
        print(f"{var}: Present (Length: {len(value)})")
    else:
        print(f"{var}: MISSING")
