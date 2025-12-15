from openai import AsyncOpenAI
from .config import settings
from .identity import POEL_INSTRUCTIONS
from .utils import async_timed

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)


@async_timed
async def think(input_items: list) -> str:
    """
    Pensa usando Responses API (async).
    """
    response = await client.responses.create(
        model=settings.POEL_MODEL,
        instructions=POEL_INSTRUCTIONS,
        input=input_items,
        max_output_tokens=settings.POEL_MAX_OUTPUT_TOKENS,
    )
    return response.output_text.strip()
