import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("models/gemini-2.5-flash")


def test_gemini():
    response = model.generate_content(
        "Say hello in one sentence"
    )
    return response.text
if __name__ == "__main__":
    print(test_gemini())