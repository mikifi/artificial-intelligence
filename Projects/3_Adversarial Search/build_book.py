import random
import pickle
import sys
from isolation import Isolation

NUM_ROUNDS = 100000
DEPTH = 10

def build_table(num_rounds=NUM_ROUNDS, depth=DEPTH):
    # Builds a table that maps from game state -> action
    # by choosing the action that accumulates the most
    # wins for the active player. (Note that this uses
    # raw win counts, which are a poor statistic to
    # estimate the value of an action; better statistics
    # exist.)
    from collections import defaultdict, Counter
    book = defaultdict(Counter)
    for i in range(num_rounds):
        if i % 100000 == 0:
            sys.stdout.write("\n=={}==\n".format(i))
            sys.stdout.flush()
        if i % 1000 == 0:
            sys.stdout.write(".")
            sys.stdout.flush()
        state = Isolation()
        build_tree(state, book, depth)
    return {k: max(v, key=v.get) for k, v in book.items()}


def build_tree(state, book, depth=2):
    if depth <= 0 or state.terminal_test():
        return -simulate(state)
    action = random.choice(state.actions())
    reward = build_tree(state.result(action), book, depth - 1)
    book[state][action] += reward
    return -reward


def simulate(state):
    player_id = state.player()
    while not state.terminal_test():
        state = state.result(random.choice(state.actions()))
    return -1 if state.utility(player_id) < 0 else 1


if __name__ == "__main__":
    print("Building book...")
    with open("data.pickle", 'wb') as f:
        pickle.dump(build_table(), f)
    print("Done")