from openai import OpenAI
from dotenv import load_dotenv
from llm.client import ai_call

result = ai_call(
    "gpt-5-mini",
    "Explain in one sentence what debate is."
    )

print(result)

