from openai import OpenAI
from .config import MODEL, MAX_OUTPUT_TOKENS
from .identity import POEL_INSTRUCTIONS

client = OpenAI()

def think(input_items: list) -> str:
    response = client.responses.create(
        model=MODEL,
        instructions=POEL_INSTRUCTIONS,
        input=input_items,
        max_output_tokens=MAX_OUTPUT_TOKENS,
    )
    return response.output_text.strip()
