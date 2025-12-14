import httpx
from typing import Optional, Dict
from .config import SECHEL_API_URL, SECHEL_ENABLED

class SechelClient:
    """Cliente HTTP para comunicação com Sechel."""

    def __init__(self, base_url: str = SECHEL_API_URL):
        self.base_url = base_url
        self.enabled = SECHEL_ENABLED
        self.client = httpx.AsyncClient(timeout=30.0)

    async def ingest_turn(
        self,
        session_id: str,
        turn_id: int,
        speaker: str,
        text: str,
        metadata: dict = None
    ) -> Optional[int]:
        """Envia turno para Sechel consolidar."""
        if not self.enabled:
            return None

        try:
            response = await self.client.post(
                f"{self.base_url}/ingest",
                json={
                    "session_id": session_id,
                    "turn_id": turn_id,
                    "speaker": speaker,
                    "raw_text": text,
                    "metadata": metadata or {}
                }
            )
            response.raise_for_status()
            data = response.json()
            return data.get("wal_id")
        except Exception as e:
            print(f"⚠️  Falha ao enviar para Sechel: {e}")
            return None

    async def retrieve_context(
        self,
        query: str,
        subject: str = None,
        filters: dict = None
    ) -> Dict:
        """Busca contexto estruturado de Sechel."""
        if not self.enabled:
            return self._empty_context_pack()

        try:
            response = await self.client.post(
                f"{self.base_url}/retrieve",
                json={
                    "query": query,
                    "filters": {
                        **({"subject": subject} if subject else {}),
                        **(filters or {})
                    }
                }
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"⚠️  Falha ao buscar contexto: {e}")
            return self._empty_context_pack()

    def _empty_context_pack(self) -> Dict:
        """Context pack vazio para fallback."""
        return {
            "canonical_state": "",
            "relevant_context": "",
            "open_conflicts": [],
            "trace": []
        }

    async def close(self):
        """Fecha conexão HTTP."""
        await self.client.aclose()
