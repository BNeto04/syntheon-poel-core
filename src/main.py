from poel.persistence import load_state, save_state
from poel.attention import build_input
from poel.brain import think

def main():
    state = load_state()
    print("Poel ativado. Digite 'sair' para encerrar.\n")

    while True:
        user_input = input("Você: ").strip()
        if not user_input:
            continue
        if user_input.lower() in {"sair", "exit", "quit"}:
            save_state(state)
            print("Poel desativado. Estado salvo.")
            break

        input_items = build_input(state, user_input)
        response = think(input_items)

        state.add_user(user_input)
        state.add_assistant(response)
        save_state(state)

        print(f"\nPoel: {response}\n")

if __name__ == "__main__":
    main()
