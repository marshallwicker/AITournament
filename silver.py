import isolation
import random
import randomplayer
import humanplayer
import csv


class PlayerAgent(isolation.Player):
    """
    Our Player Known as 'Silver'
    """

    def __init__(self, name, token):
        """
        Initialize this player
        :param name: This player's name
        :param token: This player's token
        """
        super().__init__(name, token)

    def self_heuristic(self, board):
        """
        :param board: A Board object
        :return: A neighbor that is the best move for player
        """

        turn = len(board.pushed_out_square_ids())
        # turn = 0  # dummy

        best_move = 0  # place holder for space id
        current_move = 0  # place holder for length of set

        space_id = board.token_location(self._token)

        neighbors = board.neighbor_tiles(space_id)  # neighbors
        list_neighbors = list(neighbors)

        copy_nbors = neighbors.copy()

        if len(list_neighbors) == 1:
            best_move = list_neighbors[0]
        if len(list_neighbors) == 2:
            spot_one = list(board.neighbor_tiles(list_neighbors[0]))
            spot_two = list(board.neighbor_tiles(list_neighbors[1]))
            if spot_one >= spot_two:
                best_move = list_neighbors[0]
            else:
                 best_move = list_neighbors[1]
        elif turn >= 4:  # mid game checker
            for i in neighbors:
                x = copy_nbors.pop()
                neighbors_2 = board.neighbor_tiles(x)
                nbors2_copy = neighbors_2.copy()
                for j in neighbors_2:
                    y = nbors2_copy.pop()  # neighbor
                    neighbors_3 = board.neighbor_tiles(y)  # neighbors' neighbors neighbors
                    length = len(neighbors_3)  # len of neighbors_3
                    if length >= current_move:
                        current_move = length
                        best_move = x
        else:
            for i in neighbors:
                x = copy_nbors.pop()
                y = board.neighbor_tiles(x)  # negihbors
                length = len(y)
                if length >= current_move:
                    current_move = length
                    best_move = x
        return best_move

    def push_out_heuristic(self, board, recent_move):
        """
        :param board: A board object
        :param recent_move: players most recent move
        :return: The best place for our player to punch out
        """


        turn = len(board.pushed_out_square_ids())
        # turn = 0  # dummy
        if self._token == board.RED_TOKEN:
            space_id = board.token_location(board.BLUE_TOKEN) #location of the other player
        else:
            space_id = board.token_location(board.RED_TOKEN)  # need location of other player
        neighbors = board.neighbor_tiles(space_id) #opponent neighbors
        copy_nbors = list(neighbors)
        current_push = 0
        best_push = 0
        player_id = recent_move
        if len(copy_nbors) == 1 and player_id in copy_nbors:
            push = list((board.push_outable_square_ids()))
            best_push = random.choice(push)
            return best_push
        #my_neighbors = list(board.neighbor_tiles(player_id))
        if turn >= 4 and len(copy_nbors) == 2 and player_id in copy_nbors:  # late game check
            copy_nbors.remove(player_id)
            best_push = copy_nbors[0]
            return best_push

        elif turn >= 4 and len(copy_nbors) > 2:
            for i in copy_nbors:
                y = board.neighbor_tiles(i)
                a = len(y)  # neighbor's neighbors
                if a >= current_push and i != player_id:
                    current_push = a
                    best_push = i
            return best_push

        else:
            for i in neighbors:
                x = copy_nbors.pop()
                y = board.neighbor_tiles(x)  # neighbor's neighbors
                length = len(y)
                if length >= current_push and x != player_id:
                    current_push = length
                    best_push = x
            return best_push

    def take_turn(self, board):
        """
        Make a move on the isolation board
        :param board: an Board object
        :return: Return a Move object
        """
        print("\n{} taking turn: ".format(self._name), end='')
        tiled_spaces = board.push_outable_square_ids()
        my_space_id = board.token_location(self._token)
        to_space_id = PlayerAgent.self_heuristic(self, board)
        tiled_spaces.discard(to_space_id)
        tiled_spaces.add(my_space_id)

        neighbors = board.neighbor_tiles(my_space_id)

        print('possible moves:', neighbors)

        push_out_space_id = PlayerAgent.push_out_heuristic(self, board, to_space_id)


        move = isolation.Move(to_space_id, push_out_space_id)
        print('   ', move)
        return move

if __name__ == '__main__':
    # Create a match
    isolation.Board.set_dimensions(6, 8)
    match = isolation.Match(PlayerAgent('Blue', isolation.Board.BLUE_TOKEN),
                            PlayerAgent('Red', isolation.Board.RED_TOKEN),
                            isolation.Board())
    match.start_play()
