from typing import List, Dict, Optional
from .state import PoelState
from .config import WINDOW_TURNS

async def build_input(
    state: PoelState,
    user_text: str,
    sechel_client = None
) -> List[Dict[str, str]]:
    """
    Monta input para Poel com:
    1. Contexto estruturado de Sechel (se disponível)
    2. Histórico recente (janela deslizante)
    3. Mensagem do usuário
    """
    input_items = []

    # 1. Buscar contexto de Sechel (se disponível)
    if sechel_client:
        context_pack = await sechel_client.retrieve_context(
            query=user_text,
            subject=_infer_subject(user_text)
        )

        # Adicionar canonical state como contexto estrutural
        if context_pack.get("canonical_state"):
            input_items.append({
                "role": "system",
                "content": f"""<canonical_state>
{context_pack['canonical_state']}
</canonical_state>

<relevant_context>
{context_pack.get('relevant_context', '')}
</relevant_context>"""
            })

    # 2. Adicionar histórico recente
    recent = state.get_recent(WINDOW_TURNS)
    input_items.extend(recent)

    # 3. Adicionar mensagem do usuário
    input_items.append({"role": "user", "content": user_text})

    return input_items

def _infer_subject(text: str) -> Optional[str]:
    """
    Heurística simples para inferir subject da query.
    TODO: melhorar com LLM se necessário.
    """
    keywords_map = {
        "framework": ["framework", "fastapi", "django", "flask"],
        "database": ["database", "postgres", "mysql", "db"],
        "deploy": ["deploy", "produção", "servidor", "hosting"],
        "stack": ["stack", "tecnologia", "arquitetura"],
    }

    text_lower = text.lower()
    for subject, keywords in keywords_map.items():
        if any(kw in text_lower for kw in keywords):
            return subject

    return None
