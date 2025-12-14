import time
import re
import structlog
from openai import OpenAI
from pydantic import BaseModel, ValidationError
from .config import MODEL, MAX_OUTPUT_TOKENS

client = OpenAI()
logger = structlog.get_logger()

class PoelOutput(BaseModel):
    thought: str
    response: str
    confidence: float

def strip_markdown(text: str) -> str:
    """Strips markdown formatting from a string."""
    text = text.strip()
    match = re.search(r"```(json)?\n(.*)\n```", text, re.DOTALL)
    if match:
        return match.group(2).strip()
    return text

def think(input_items: list) -> PoelOutput:
    start_time = time.time()

    messages = input_items

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        max_tokens=MAX_OUTPUT_TOKENS,
    )

    latency = time.time() - start_time
    raw_response = response.choices[0].message.content.strip()
    cleaned_response = strip_markdown(raw_response)

    logger.info(
        "poel.think",
        latency=latency,
        tokens=response.usage.total_tokens,
        model=MODEL
    )

    try:
        return PoelOutput.parse_raw(cleaned_response)
    except ValidationError as e:
        logger.error("poel.think.validation_error", error=e)
        return PoelOutput(
            thought="Failed to parse the response from the LLM.",
            response="I'm having trouble formatting my thoughts. Please try again.",
            confidence=0.0
        )
