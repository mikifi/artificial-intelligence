import pickle
from isolation import Isolation
from isolation import DebugState


def inspect_book(book):
    clean_state = Isolation()

    first_move_state = clean_state.result(book[clean_state])
    print("Best first move:\n{}".format(book[clean_state]))
    print("State after first move:\n{}".format(first_move_state))
    print(DebugState.from_state(first_move_state))

    next_move_state = first_move_state.result(book[first_move_state])
    print("Best follow up move:\n{}".format(book[next_move_state]))
    print("State after follow up move:\n{}".format(next_move_state))
    print(DebugState.from_state(next_move_state))


if __name__ == "__main__":
    print("Inspecting book...")
    with open("data.pickle", 'rb') as f:
        inspect_book(pickle.load(f))
    print("Done")
