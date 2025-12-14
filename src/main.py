import json
import click
from poel.persistence import load_state, save_state, create_new_session, get_last_session
from poel.attention import build_context
from poel.brain import think

@click.command()
@click.argument("message")
@click.option("--session", default=None, help="The session ID to use.")
@click.option("--new", is_flag=True, help="Create a new session.")
@click.option("--continue", "continue_session", is_flag=True, help="Continue the last session.")
@click.option("--format", "output_format", type=click.Choice(["json", "text"]), default="text", help="The output format.")
@click.option("--verbose", is_flag=True, help="Enable verbose output.")
def chat(message: str, session: str | None, new: bool, continue_session: bool, output_format: str, verbose: bool):
    session_id = None
    if new:
        session_id = create_new_session()
    elif session:
        session_id = session
    elif continue_session:
        session_id = get_last_session()
    else:
        session_id = get_last_session()
        if not session_id:
            session_id = create_new_session()

    state = load_state(session_id)

    context = build_context(state, message)
    poel_output = think(context)

    state.add_user(message)
    state.add_assistant(poel_output.response)
    save_state(session_id, state)

    if output_format == "json":
        click.echo(poel_output.json())
    elif verbose:
        click.echo(f"Thought: {poel_output.thought}")
        click.echo(f"Response: {poel_output.response}")
        click.echo(f"Confidence: {poel_output.confidence}")
    else:
        click.echo(f"Poel: {poel_output.response}")

def main():
    chat()

if __name__ == "__main__":
    main()
