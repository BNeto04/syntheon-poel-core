import asyncio
import click
from poel.persistence import load_state, save_state
from poel.attention import build_input
from poel.brain import think
from poel.sechel_client import SechelClient
from poel.config import settings
from poel.exceptions import SechelError


async def chat_loop(state, sechel_client):
    """Loop principal de conversação."""
    print(f"🧠 Poel ativado (sessão: {state.session_id[:8]})")
    if sechel_client.enabled:
        print("✅ Integração com Sechel ativa")
    print("Digite 'sair' para encerrar.\n")

    while True:
        user_input = click.prompt("Você", type=str)
        if user_input.lower() in {"sair", "exit", "quit"}:
            save_state(state)
            click.echo("\n👋 Poel desativado. Estado salvo.")
            break

        if not user_input:
            continue

        try:
            input_items = await build_input(state, user_input, sechel_client)
            response = await think(input_items)

            state.add_user(user_input)
            state.add_assistant(response)
            save_state(state)

            if sechel_client.enabled:
                await sechel_client.ingest_turn(
                    state.session_id, state.turn_id, "MANO", user_input
                )
                await sechel_client.ingest_turn(
                    state.session_id, state.turn_id, "POEL", response
                )

            click.echo(f"\n🤖 Poel: {response}\n")

        except SechelError as e:
            click.echo(f"\n⚠️ Erro de comunicação com Sechel: {e}\n", err=True)
        except Exception as e:
            click.echo(f"\n🚨 Ocorreu um erro inesperado: {e}\n", err=True)


@click.command()
@click.option("--session-id", default=None, help="ID da sessão para carregar.")
def cli(session_id: str | None):
    """Entrypoint síncrono para a CLI Poel."""

    async def run():
        state = load_state(session_id)

        try:
            async with SechelClient() as sechel_client:
                await chat_loop(state, sechel_client)
        except SechelError as e:
            click.echo(f"⚠️ Não foi possível conectar ao Sechel: {e}", err=True)
        except Exception as e:
            click.echo(f"🚨 Falha ao iniciar Poel: {e}", err=True)

    asyncio.run(run())


def main():
    # Carrega as configurações (e valida) antes de tudo
    try:
        _ = settings.OPENAI_API_KEY
    except Exception as e:
        click.echo(f"🚨 Erro de configuração: {e}", err=True)
        return

    cli()


if __name__ == "__main__":
    main()
