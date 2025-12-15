import httpx
from typing import Optional, Self
from .config import settings
from .schemas import ContextPack
from .exceptions import SechelConnectionError, SechelAPIError


class SechelClient:
    """Cliente HTTP para comunicação com Sechel."""

    def __init__(self, base_url: str = str(settings.SECHEL_API_URL)):
        self.base_url = base_url
        self.enabled = settings.SECHEL_ENABLED
        self._client = httpx.AsyncClient(timeout=10.0)

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._client.aclose()

    async def ingest_turn(
        self,
        session_id: str,
        turn_id: int,
        speaker: str,
        text: str,
        metadata: dict = None,
    ) -> Optional[int]:
        """Envia turno para Sechel consolidar."""
        if not self.enabled:
            return None

        try:
            response = await self._client.post(
                f"{self.base_url}/ingest",
                json={
                    "session_id": session_id,
                    "turn_id": turn_id,
                    "speaker": speaker,
                    "raw_text": text,
                    "metadata": metadata or {},
                },
            )
            response.raise_for_status()
            data = response.json()
            return data.get("wal_id")
        except httpx.HTTPStatusError as e:
            raise SechelAPIError(
                f"Sechel API returned status {e.response.status_code}"
            ) from e
        except httpx.RequestError as e:
            raise SechelConnectionError(f"Could not connect to Sechel: {e}") from e

    async def retrieve_context(
        self, query: str, subject: str = None, filters: dict = None
    ) -> ContextPack:
        """Busca contexto estruturado de Sechel."""
        if not self.enabled:
            return self._empty_context_pack()

        try:
            response = await self._client.post(
                f"{self.base_url}/retrieve",
                json={
                    "query": query,
                    "filters": {
                        **({"subject": subject} if subject else {}),
                        **(filters or {}),
                    },
                },
            )
            response.raise_for_status()
            return ContextPack.model_validate(response.json())
        except httpx.HTTPStatusError as e:
            raise SechelAPIError(
                f"Sechel API returned status {e.response.status_code}"
            ) from e
        except httpx.RequestError as e:
            raise SechelConnectionError(f"Could not connect to Sechel: {e}") from e

    def _empty_context_pack(self) -> ContextPack:
        """Context pack vazio para fallback."""
        return ContextPack(
            canonical_state="", relevant_context="", open_conflicts=[], trace=[]
        )
