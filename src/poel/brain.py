from openai import AsyncOpenAI
from .config import MODEL, MAX_OUTPUT_TOKENS
from .identity import POEL_INSTRUCTIONS

client = AsyncOpenAI()

async def think(input_items: list) -> str:
    """
    Pensa usando Responses API (async).
    """
    response = await client.responses.create(
        model=MODEL,
        instructions=POEL_INSTRUCTIONS,
        input=input_items,
        max_output_tokens=MAX_OUTPUT_TOKENS,
    )
    return response.output_text.strip()
