"""
A random player selects moves randomly.

Last update: 25 NOV 2018
"""
import isolation
import randomplayer
import random

# old code dictionary
h_dict = {
    0: 3,
    1: 5,
    2: 5,
    3: 5,
    4: 5,
    5: 5,
    6: 5,
    7: 3,
    8: 5,
    9: 8,
    10: 8,
    11: 8,
    12: 8,
    13: 8,
    14: 8,
    15: 5,
    16: 5,
    17: 8,
    18: 8,
    19: 8,
    20: 8,
    21: 8,
    22: 8,
    23: 5,
    24: 5,
    25: 8,
    26: 8,
    27: 8,
    28: 8,
    29: 8,
    30: 8,
    31: 5,
    32: 5,
    33: 8,
    34: 8,
    35: 8,
    36: 8,
    37: 8,
    38: 8,
    39: 5,
    40: 3,
    41: 5,
    42: 5,
    43: 5,
    44: 5,
    45: 5,
    46: 5,
    47: 3
}


class PlayerAgent(isolation.Player):
    """
    A random player selects moves at random
    """

    def __init__(self, name, token):
        """
        Initialize this player
        :param name: This player's name
        :param token: This player's token
        """
        super().__init__(name, token)
        if token is isolation.Board.RED_TOKEN:
            self._opponent = isolation.Board.BLUE_TOKEN
        else:
            self._opponent = isolation.Board.RED_TOKEN

    def h(self, board):
        """

        Determines the heuristic of all neighbors
        :param board:
        :return:
        """

    def move(self, board):
        """

        :param board:
        :return: space_move

        """
        space_id = board.token_location(self._token)
        curr_neighbors = list(board.neighbor_tiles(space_id))  # neighbors
        copy_neighbors = curr_neighbors.copy()

        to_space_id = curr_neighbors[0]  # place holder for space id
        curr_best = 0  # place holder for length of set

        if len(curr_neighbors) == 1:
            to_space_id = curr_neighbors[0]
        else:

            for i in curr_neighbors:
                x = copy_neighbors.pop()
                neighbors_pass2 = board.neighbor_tiles(x)  # neighbors for each neighbor
                copy_neighbors_pass2 = neighbors_pass2.copy()
                for i in neighbors_pass2:
                    y = copy_neighbors_pass2.pop()
                    neighbors_pass3 = board.neighbor_tiles(y)  # neighbors' for neighbors of each neighbor
                    copy_neighbors_pass3 = neighbors_pass3.copy()
                    for i in neighbors_pass3:
                        z = copy_neighbors_pass3.pop()
                        neighbors_pass4 = board.neighbor_tiles(z)  # neighbors for the last pass

                        length = len(neighbors_pass4)  # len of neighbors for this pass

                        if length >= curr_best:
                            curr_best = length
                            to_space_id = x

        # old code using dictionary ------------------------------------
        # # moving section
        # space_id = board.token_location(self._token)
        # # gets  neighbors of our location
        # curr_neighbors = board.neighbor_tiles(space_id)
        # # list of current neighbors
        # list_neighbors = list(curr_neighbors)
        #
        # curr_best = 0
        # to_space_id = 0
        #
        # # goes in the the dictionary and finds the best key who has the biggest value number
        # for i in range(len(list_neighbors)):
        #     x = h_dict[i]
        #     if x > curr_best:
        #         curr_best = x
        #         to_space_id = list_neighbors[i]
        # # old code^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        # this part checks to see which color token is us and which color token is the enemy.
        # space_id_enemy = board.token_location(board.RED_TOKEN)  <---------- old code

        if self._token == board.RED_TOKEN:
            space_id_enemy = board.token_location(board.BLUE_TOKEN)
        else:
            space_id_enemy = board.token_location(board.RED_TOKEN)

        # pushout section
        curr_neighbors_enemy = board.neighbor_tiles(space_id_enemy)

        # gets rid of problem about choosing the spot that you were going to move to to pop out
        curr_neighbors_enemy.add(space_id)
        curr_neighbors_enemy.discard(to_space_id)
        copy_enemy = curr_neighbors_enemy.copy()

        list_copy = list(copy_enemy)
        to_pushout = list_copy[0]
        curr_best_pushout = 0

        for i in curr_neighbors_enemy:
            x = copy_enemy.pop()
            enemy_pass2 = board.neighbor_tiles(x)  # neighbors for each neighbor
            copy_enemy_pass2 = enemy_pass2.copy()
            for i in enemy_pass2:
                y = copy_enemy_pass2.pop()
                enemy_pass3 = board.neighbor_tiles(y)  # neighbors' for neighbors of each neighbor
                length = len(enemy_pass3)  # len of neighbors for this pass
                if length >= curr_best_pushout:
                    curr_best_pushout = length
                    to_pushout = x

        # old code using dictionary ----------------------------------------
        #
        # if self._token == board.RED_TOKEN:
        #     space_id_enemy = board.token_location(board.BLUE_TOKEN)
        # else:
        #     space_id_enemy = board.token_location(board.RED_TOKEN)
        #
        # # pushout section
        # curr_neighbors_enemy = board.neighbor_tiles(space_id_enemy)
        #
        # # gets rid of problem about choosing the spot that you were going to move to to pop out
        # curr_neighbors_enemy.add(space_id)
        # curr_neighbors_enemy.discard(to_space_id)
        #
        # list_neighbors_pushout = list(curr_neighbors_enemy)
        #
        # to_pushout = 0
        # curr_best_pushout = 0
        # for i in range(len(list_neighbors_pushout)):
        #     y = h_dict[i]
        #     if y > curr_best_pushout:
        #         curr_best_pushout = y
        #         to_pushout = list_neighbors_pushout[i]
        #     h_dict[to_pushout] -= 1

        return to_space_id, to_pushout

    def take_turn(self, board):
        """
        Make a move on the isolation board
        :param board: an Board object
        :return: Return a Move object
        """

        print("\n{} taking turn: ".format(self._name), end='')

        # Collect board state info to generate a move from
        space_id = board.token_location(self._token)
        neighbors = board.neighbor_tiles(space_id)
        print('possible moves:', neighbors)

        # Select a square to move to and a tile to push out.
        # Once a neighbor square is chosen to move to,
        # that square can no longer be pushed out, but
        # the square vacated might be able to be pushed out

        to_space_id, push_out_space_id = PlayerAgent.move(self, board)

        move = isolation.Move(to_space_id, push_out_space_id)
        print('   ', move)

        return move


if __name__ == '__main__':
    # Create a match
    isolation.Board.set_dimensions(6, 8)
    match = isolation.Match(PlayerAgent('Blue', isolation.Board.BLUE_TOKEN),
                            randomplayer.RandomPlayer('Red', isolation.Board.RED_TOKEN),
                            isolation.Board())
    match.start_play()

    # Play 100 more matches
    # for i in range(100):
    #     match = isolation.Match(PlayerAgent('Blue', isolation.Board.BLUE_TOKEN),
    #                             randomplayer.RandomPlayer('Red', isolation.Board.RED_TOKEN))
    #     print(match.start_play())
    #     print('*' * 40)
