from isolation import *
from math import *
from itertools import *
import copy
import time


class PlayerAgent(Player):
    def __init__(self, name, token):
        super(PlayerAgent, self).__init__(name, token)
        # self._token, self._name in superclass
        self._enemyToken = Board.BLUE_TOKEN if self._token == Board.RED_TOKEN else Board.RED_TOKEN
        self._strategy = EarlyStrat(self._token, self._enemyToken)

    def take_turn(self, board):
        """
        Make a move on the Isolation board and push out space
        :param board: a Board object
        :return: a Move object
        """
        start = time.clock()
        #print("Aqua taking turn!")
        if len(self._strategy.moves(board, self._token)) == 0:
            self._strategy = LateStrat(self._token, self._enemyToken)
        move = self._strategy.minimax(board, 3, -math.inf, math.inf, True)[1]
        #print("Aqua's neighbors: ", board.neighbor_tiles(board.token_location(self._token)))
        #print("Aqua's move: ", move)
        end = time.clock()
        print("Aqua turn time: ", end - start, " sec")
        return move

class Strategy:
    def __init__(self, token, enemyToken):
        # self.board = board
        self._token = token
        self._enemyToken = enemyToken

    def moves(self, board, token):
        """
        Returns the ids of the potential spaces to move to
        :param board: a Board object
        :param token: a token string
        :return: to_space_id
        """
        raise NotImplementedError

    def pushouts(self, board, token):
        """
        Returns the ids of the potential spaces to push
        :param board: a Board object
        :param token: a token string
        :return: push_space_id
        """
        raise NotImplementedError

    def safety(self, board, tile):
        """
        Deterimine the safety of a given tile where safety is defined on a scale of 0,
        meaning the tile has no neighboring tiles, to 8, meaning all neighboring tiles
        are present and not pushed out
        :param board: a Board object
        :param tile: a tile on the board
        :return: the number of neighboring tiles a tile has
        """
        return len(board.neighbor_tiles(tile))

    def extended_safety(self, board, start, depth):
        """
        Returns the total safety for a square equaling the total safety of depth squares away from it
        :param board: a Board object
        :param start: a starting tile id
        :param depth: the distance away that the safety is to be calculated using
        :return: the total calculated safety
        """
        if depth == 0:
            return self.safety(board, start)
        else:
            return self.safety(board, start) + sum([self.extended_safety(board, tile, depth-1)
                                                    for tile in board.neighbor_tiles(start)])

    def squares_in_radius(self, board, tokenLocation, radius):
        squares = set([])
        for i in range(radius):
            squares |= board.squares_at_radius(tokenLocation, i)
        return squares

    def pushable_in_radius(self, board, enemyLocation, radius):
        return self.squares_in_radius(board, enemyLocation, radius) & board.push_outable_square_ids()

    # position is board state, children are all possible moves, static eval of position is
    # number of neighbor_tiles
    # alpha should be -infinity, beta should be +infinity
    def minimax(self, board, depth, alpha, beta, maximizingPlayer):
        RADII = 2
        tokenLocation = board.token_location(self._token)
        enemyLocation = board.token_location(self._enemyToken)
        # if at end of a path on the tree OR their are no possible moves to make

        if depth == 0 or (not board.neighbor_tiles(tokenLocation) and maximizingPlayer) \
                or (not board.neighbor_tiles(enemyLocation) and not maximizingPlayer):
            if not board.neighbor_tiles(tokenLocation) and maximizingPlayer:
                return -math.inf, None
            elif not board.neighbor_tiles(enemyLocation) and not maximizingPlayer:
                return math.inf, None
            else:
                return self.extended_safety(board, tokenLocation, RADII) - self.extended_safety(board, enemyLocation, RADII), None
                #return len(board.neighbor_tiles(tokenLocation)) - len(board.neighbor_tiles(enemyLocation)), None

        if maximizingPlayer:
            maxEval = -math.inf
            bestMove = None
            # max 8 children - one for each neighbor tile that a pawn can move to
            moveList = self.moves(board, self._token)
            pushList = self.pushouts(board, self._enemyToken) + [tokenLocation]
            for child in [(move, push) for move in moveList for push in pushList]:
                ourMove = Move(child[0], child[1])
                if ourMove.to_square_id == ourMove.pushout_square_id:
                    continue
                elif not bestMove:
                    bestMove = ourMove
                boardCopy = copy.deepcopy(board)
                boardCopy.make_move(self._token, ourMove)
                eval = self.minimax(boardCopy, depth - 1, alpha, beta, False)[0]
                if eval > maxEval:
                    bestMove = ourMove
                    maxEval = eval
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return maxEval, bestMove

        else:
            minEval = math.inf
            moveList = list(board.neighbor_tiles(board.token_location(self._enemyToken)))
            pushList = list(self.pushable_in_radius(board, tokenLocation, RADII)) # Assume opponent will only push near us
            if not pushList:
                pushList = list(board.push_outable_square_ids()) + [enemyLocation]
            for child in [(move, push) for move in moveList for push in pushList]:
                theirMove = Move(child[0], child[1])
                if theirMove.to_square_id == theirMove.pushout_square_id:
                    continue
                boardCopy = copy.deepcopy(board)
                boardCopy.make_move(self._enemyToken, theirMove)
                eval = self.minimax(boardCopy, depth - 1, alpha, beta, True)[0]
                minEval = min(minEval, eval)
                beta = min(beta, eval)
                if alpha <= beta:
                    break
            return minEval, None


class LateStrat(Strategy):
    """
    Follow the Late Strategy of moving to space with
    most available moves on next turn
    """
    def __init__(self, token, enemyToken):
        super(LateStrat, self).__init__(token, enemyToken)

    def moves(self, board, token):
        """
        Returns the ids of the potential spaces to move to
        :param board: a Board object
        :param token: a token string
        :return: to_space_id
        """
        #return list(board.neighbor_tiles(board.token_location(token)))
        return [move[0] for move in self.potentialLateMoves(board, board.token_location(token))]

    def pushouts(self, board, token):
        """
        Returns the ids of the potential spaces to push
        :param board: a Board object
        :param token: a token string
        :return: push_space_id
        """
        considering_for_push = self.pushable_in_radius(board, board.token_location(token), 3)
        if considering_for_push:
            return list(considering_for_push)
        else:
            return list(board.push_outable_square_ids())

    def potentialLateMoves(self, board, tokenLocation):
        tileSafenessList = [(tile, self.extended_safety(board, tile, 4)) for tile in board.neighbor_tiles(tokenLocation)]
        tileSafenessListSorted = sorted(tileSafenessList, key=lambda x: x[1], reverse=True)

        return tileSafenessListSorted



class EarlyStrat(Strategy):
    """
    Follow the Early Strategy of moving toward enemy pawn
    """
    def __init__(self, token, enemyToken):
        super(EarlyStrat, self).__init__(token, enemyToken)

    def moves(self, board, token):
        """
        Returns list of first values in list of tuples created in potentialEarlyMoves
        :param board: A Board object
        :param token: a token string
        :return: a list of tile ids that are possible move locations
        """
        return [move[0] for move in self.potentialEarlyMoves(board, board.token_location(token))]

    def pushouts(self, board, token):
        """
        Returns the ids of the potential spaces to push
        :param board: a Board object
        :param token: a token string
        :return: push_space_id
        """
        return [push[0] for push in self.potentialPushes(board, board.token_location(token))]

    def potentialEarlyMoves(self, board, tokenLocation):
        """
        Determines which of the spaces possible is the safest to move to where safeness is defined
        as the number of neighbroing tiles a tile has such that the max safety is 8
        :param board: A Board object
        :param tokenLocation: a tile id for the token
        :return: A sorted list of tuples containg the possible tiles with their safety rating
        """
        tileSafenessList = [(tile, self.safety(board, tile)) for tile in board.neighbor_tiles(tokenLocation)
                            if self.path_exists(board, tile)]
        tileSafenessListSorted = sorted(tileSafenessList, key=lambda x: x[1], reverse=True)

        return tileSafenessListSorted

    def path_exists(self, board, start):
        """
        Determines if a path exists to the enemy pawn in which the player pawn can continuously move
        towards the enemy
        :param board: A Board object
        :param start: The starting tile
        :return: True if a path exists, False if not
        """
        found = False
        visited = set([])
        q = [start]
        while q and not found:
            curr = q.pop(0)
            visited.add(curr)
            for tile in board.neighbor_tiles(curr):
                if board.token_location(self._enemyToken) in board.neighbors(tile):
                    found = True
                    break
                if tile not in visited and self.moving_closer(board, curr, tile):
                    q.append(tile)
        return found

    def moving_closer(self, board, start, tile):
        """
        Return true if a tile is closer to the enemy pawn than a start tile
        :param board: A Board object
        :param start: The starting tile
        :param tile: The tile under consideration for moving to
        :return: True if tile is closer to the enemy pawn than start, False if not
        """
        if board.distance_between(tile, board.token_location(self._enemyToken)) \
                <= board.distance_between(start, board.token_location(self._enemyToken)) - 1:
            return True
        else:
            return False

    def potentialPushes(self, board, enemy):
        """
        Determine which of the enemy's neighboring tiles is the best tile to push using void edge
        heuristic where the tile with the most void edges in the neighbor tiles is the ideal push
        :param board: A Board object
        :param enemy: the enemy tile location
        :return: a sorted list of the neighboring tiles in descending order of void edges
        """
        voidEdgeList = [(tile, self.getVoidEdges(board, tile)) for tile in board.neighbor_tiles(enemy)]
        voidEdgeListSorted = sorted(voidEdgeList, key=lambda x: x[1], reverse=True)

        return voidEdgeListSorted

    def getVoidEdges(self, board, tile):
        """
        Determine the number of void edges of a given tile
        :param board: A Board object
        :param tile: a tile on the Board
        :return: an integer representing the number of pushed out spaces within the
        neighbors of tile
        """
        return 8 - len(board.neighbor_tiles(tile))
