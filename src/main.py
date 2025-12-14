import asyncio
from poel.persistence import load_state, save_state
from poel.attention import build_input
from poel.brain import think
from poel.sechel_client import SechelClient
from poel.config import SECHEL_ENABLED

async def chat_loop(session_id: str = None):
    """Loop principal de conversação."""

    # Inicializar
    state = load_state(session_id)
    sechel = SechelClient() if SECHEL_ENABLED else None

    print(f"🧠 Poel ativado (sessão: {state.session_id[:8]})")
    if SECHEL_ENABLED:
        print("✅ Integração com Sechel ativa")
    print("Digite 'sair' para encerrar.\n")

    try:
        while True:
            user_input = input("Você: ").strip()

            if user_input.lower() in {"sair", "exit", "quit"}:
                save_state(state)
                print("\n👋 Poel desativado. Estado salvo.")
                break

            if not user_input:
                continue

            # 1. Construir input com contexto de Sechel
            input_items = await build_input(state, user_input, sechel)

            # 2. Pensar
            response = await think(input_items)

            # 3. Atualizar state
            state.add_user(user_input)
            state.add_assistant(response)
            save_state(state)

            # 4. Enviar para Sechel (se disponível)
            if sechel:
                await sechel.ingest_turn(
                    state.session_id,
                    state.turn_id,
                    "MANO",
                    user_input
                )
                await sechel.ingest_turn(
                    state.session_id,
                    state.turn_id,
                    "POEL",
                    response
                )

            # 5. Exibir resposta
            print(f"\n🤖 Poel: {response}\n")

    finally:
        if sechel:
            await sechel.close()

def main():
    """Entrypoint síncrono para pyproject.toml."""
    asyncio.run(chat_loop())

if __name__ == "__main__":
    main()
