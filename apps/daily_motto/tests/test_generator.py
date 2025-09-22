import sys
from dotenv import load_dotenv
from litellm import completion
import os

prompt = "Generate a short motivational reminder (max 3 lines) for work and fitness, calm and reflective, 70% mindset / 30% practical."

# Load the .env file from one folder up
dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path)

api_key = os.getenv('GROQ_API_KEY')
if api_key is None:
    print("Upozornění: GROQ_API_KEY nebyl nalezen v souboru .env nebo proměnných prostředí.")
    sys.exit()

os.environ['GROQ_API_KEY'] = api_key
print("Groq API klíč úspěšně načten a nastaven.")

groq_LLMs_dict = {
    "gemma2": "groq/gemma2-9b-it",
    "gpt120b": "groq/openai/gpt-oss-120b",
    "gpt20b": "groq/openai/gpt-oss-20b",
    "compound_mini": "groq/groq/compound-mini",
    "llama33versatile": "groq/llama-3.3-70b-versatile",
    "llama31instant": "groq/llama-3.1-8b-instant"
}
response = completion(
    model=groq_LLMs_dict["llama31instant"],
    messages=[
        {"role": "user", "content": prompt}
    ],
)

print("Generated Reminder:\n", response.choices[0].message.content)
