from openai import OpenAI
from dotenv import load_dotenv

# Use project-local .env values even if the base/system environment has the same variable names.
load_dotenv(override=True)
client = OpenAI()
    
def ai_call(ai_model,prompt):
    response = client.responses.create(
        model = ai_model,
        input = prompt
    )

    return response.output_text


