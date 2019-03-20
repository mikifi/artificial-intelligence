from sample_players import DataPlayer
import random


class CustomPlayer(DataPlayer):
    """ Implement an agent using any combination of techniques discussed
        in lecture (or that you find online on your own) that can beat
        sample_players.GreedyPlayer in >80% of "fair" matches (see tournament.py
        or readme for definition of fair matches).

        Implementing get_action() is the only required method, but you can add any
        other methods you want to perform minimax/alpha-beta/monte-carlo tree search,
        etc.

        **********************************************************************
        NOTE: The test cases will NOT be run on a machine with GPU access, or
              be suitable for using any other machine learning techniques.
        **********************************************************************
        """

    def get_action(self, state, max_depth = 4):
        """ Choose an action available in the current state

        See RandomPlayer and GreedyPlayer for examples.

        This method must call self.queue.put(ACTION) at least once, and may
        call it as many times as you want; the caller is responsible for
        cutting off the function after the search time limit has expired.

        **********************************************************************
        NOTE: since the caller is responsible for cutting off search, calling
              get_action() from your own code will create an infinite loop!
              See (and use!) the Isolation.play() function to run games.
        **********************************************************************
        """
        # Select a move from opening book as player 1 or 2 for the first plies, otherwise
        # return the optimal minimax move using iterative deepening
        if state.ply_count < 2:
            if state in self.data.keys():
                self.queue.put(self.data[state])
            else:
                self.queue.put(random.choice(state.actions()))
        else:
            for depth in range(1, max_depth + 1):
                self.queue.put(self.minimax(state, depth=depth))

    def minimax(self, state, depth):

        def min_value(state, depth):
            if state.terminal_test(): return state.utility(self.player_id)
            if depth <= 0: return self.score(state)
            value = float("inf")
            for action in state.actions():
                value = min(value, max_value(state.result(action), depth - 1))
            return value

        def max_value(state, depth):
            if state.terminal_test(): return state.utility(self.player_id)
            if depth <= 0: return self.score(state)
            value = float("-inf")
            for action in state.actions():
                value = max(value, min_value(state.result(action), depth - 1))
            return value

        return max(state.actions(), key=lambda x: min_value(state.result(x), depth - 1))

    def score(self, state):
        own_loc = state.locs[self.player_id]
        opp_loc = state.locs[1 - self.player_id]
        own_liberties = state.liberties(own_loc)
        opp_liberties = state.liberties(opp_loc)
        liberties_heuristic = len(own_liberties) - len(opp_liberties)
        return liberties_heuristic
