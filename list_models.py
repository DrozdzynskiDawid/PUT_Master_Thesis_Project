import google.generativeai as genai
import os
import sys
from dotenv import load_dotenv

# Put your API key in a .env file in the same directory as this script as follows:
# GOOGLE_API_KEY="your_api_key_here"
load_dotenv() 
API_KEY = os.environ.get("GOOGLE_API_KEY")

try:
    genai.configure(api_key=API_KEY)
    for model in genai.list_models():
        print(f"- {model.display_name} ({model.name})")

except Exception as e:
    print(f"Error occured: {e}", file=sys.stderr)
    print("\nPlease check that your API key is correct and that you have an internet connection.", file=sys.stderr)