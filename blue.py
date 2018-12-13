import isolation
import randomplayer
import humanplayer



class PlayerAgent(isolation.Player):
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

    def take_turn(self, board):
        """
        Make a move on the isolation board
        :param board: an Board object
        :return: Return a Move object
        """

        print("\n{} taking turn: ".format(self._name), end='')
        return self.early_move_poke_out(board)



    def h(self, board, token_id):
        neighbors = list(board.neighbor_tiles(token_id))
        opponent = board.token_location(self._opponent)
        opponents_neighbors = list(board.neighbor_tiles(opponent))
        print('NEIGHBORS:', neighbors)
        print('OPPONENTS_NEIGHBORS', opponents_neighbors)
        if len(neighbors) == 1:
            location1 = neighbors[0]
            location2 = neighbors[0]
            return location1, location2
        while len(neighbors) != 2:
            second_neighbor = list(board.neighbor_tiles(neighbors[0]))
            second_neighbor.append(token_id)
            third_neighbor = list(board.neighbor_tiles(neighbors[1]))
            third_neighbor.append(token_id)
            if sum(second_neighbor) <= sum(third_neighbor):
                neighbors.pop(0)
            else:
                neighbors.pop(1)
        location1 = neighbors[0]
        location2 = neighbors[1]
        return location2, location1

        #if is_pushed out is false then counter += 1 use neighbor_tiles
        #loop through for all possible moves
        #For each move repeat to count possible moves for next move

    def push_h2o(self, board, token_id):
        neighbors = list(board.neighbor_tiles(token_id))
        opponent = board.token_location(self._opponent)
        first = []
        location1 = 0
        if len(neighbors) == 1:
            location1 = neighbors[0]
            return location1
        if len(neighbors) == 0:
            push_outable = list(board.push_outable_square_ids())
            location1 = push_outable[0]
            return location1
        if len(neighbors) > 1:
            for i in range(len(neighbors) - 1):
                test = neighbors[i]
                second_neighbor = list(board.neighbor_tiles(neighbors[i]))
                if neighbors[i] != opponent:
                    if len(first) < len(second_neighbor):
                        first = second_neighbor
                        location1 = neighbors[i + 1]
        return location1


    def early_move_poke_out(self, board):
        space_id = board.token_location(self._token)
        poke_out = [42, 2, 34, 26, 18, 10]
        pushed_out = list(board.pushed_out_square_ids())
        pushed_out.append(space_id)
        opponent = board.token_location(self._opponent)
        while poke_out != []:
            move_dest = self.h(board, space_id)
            for i in range(len(poke_out)):  # - 1
                if poke_out[len(poke_out) - 1] in pushed_out or poke_out[len(poke_out) - 1] == opponent or poke_out[len(poke_out) - 1] == space_id:
                    poke_out.pop()
                else:
                    choice = poke_out[len(poke_out) - 1]
                    poke_out.pop()
                    if move_dest[0] == choice:
                        move = isolation.Move(move_dest[1], choice)
                        print(move_dest, choice)
                        return move
                    else:
                        move = isolation.Move(move_dest[0], choice)
                        print(move_dest, choice)
                        return move
        poke_out_late = self.push_h2o(board, opponent)
        move_dest_late = self.push_h2o(board, space_id)
        if poke_out_late == 0:
            opponents_neighbors = list(board.neighbor_tiles(opponent))
            poke_out_late = opponents_neighbors[0]
        if move_dest_late == 0:
            blah = list(board.neighbor_tiles(space_id))
            move_dest_late = blah[0]
        if poke_out_late == move_dest_late or move_dest_late == poke_out_late:
            push_outable = list(board.push_outable_square_ids())
            push_outable.remove(move_dest_late)
            push_outable. append(space_id)
            poke_out_late = push_outable[0]
            move = isolation.Move(move_dest_late, poke_out_late)
            return move
        move = isolation.Move(move_dest_late, poke_out_late)
        print(move)
        return move










if __name__ == '__main__':
    # Create a match

    isolation.Board.set_dimensions(6, 8)
    ref = isolation.Match(PlayerAgent('Blue', isolation.Board.BLUE_TOKEN),
                          randomplayer.RandomPlayer('Red', isolation.Board.RED_TOKEN),
                          isolation.Board())
    ref.start_play()
