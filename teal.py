import isolation
from humanplayer import HumanPlayer
from randomplayer import RandomPlayer
from random import random, choice, randint
from heapq import *


class PlayerAgent(isolation.Player):
    __definedInitialValues = False
    __totalTiles = None
    __earlyStrategy = True
    SWITCH_TILE_COUNT = 100
    DISTANCE_FOR_EARLY_STRATEGY = 2

    OTHER_PLAYER_TOKEN = None

    TARGET_LOCATION = 19

    def take_turn(self, board):

        if not self.OTHER_PLAYER_TOKEN:
            self.OTHER_PLAYER_TOKEN = board.RED_TOKEN if self.token() == board.BLUE_TOKEN else board.BLUE_TOKEN

        move_to = self.getNextLocation(board)
        knockout_id = self.find_knockout_square(board, move_to)
        move = isolation.Move(to_square_id=move_to, pushout_square_id=knockout_id)
        return move

    def calculate_move(self, board):

        my_possible_moves = board.neighbor_tiles(board.token_location(self.token())) - board.tile_square_ids()
        other_agent_possible_moves = board.neighbor_tiles(board.token_location(self.OTHER_PLAYER_TOKEN))
        if self.__earlyStrategy:
            current_tile_location = board.token_location(self.token())
            current_quadrant = self.BOARD_QUADRANTS[current_tile_location]
            if self.BOARD_CENTER_SQUARES[current_quadrant] in board.pushed_out_square_ids():
                return choice(list(my_possible_moves))
        else:
            return choice(list(my_possible_moves))

    def find_knockout_square(self, board, move_to_square):

        myLocation = board.token_location(self.token())
        opponent = board.RED_TOKEN if self.token() == board.BLUE_TOKEN else board.BLUE_TOKEN

        radiusOne = board.neighbor_tiles(board.token_location(opponent))
        radiusTwo = board.squares_at_radius(board.token_location(opponent), 1)
        radiusThree = board.squares_at_radius(board.token_location(opponent), 2)
        goTo = (board.push_outable_square_ids() - {move_to_square})

        hey = [radiusOne, radiusTwo, radiusThree, goTo]
        hey = [goTo & element if element else set() for element in hey]

        doThisThing = []

        for index, optionSet in enumerate(hey):
            [heappush(doThisThing, (100 * index + randint(0, 50) - 10*(board.distance_between(element, myLocation)), element)) for element in optionSet]

        return heappop(doThisThing)[1]

    def getNextTargetLocation(self, board):

        pushOutable = set(board.push_outable_square_ids())

        quadrants = {key: set() for key in range(4)}

        for tile in pushOutable:
            xCoord = tile % board.N
            yCoord = (tile - xCoord)//board.M

            quadrant = 0
            distance = 0

            if 0 <= xCoord < board.N // 2:
                if 0 <= yCoord <= board.M // 2:
                    distance = board.distance_between(0, tile)
                    quadrant = 0
                else:
                    distance = board.distance_between(board.N*(board.M-1), tile)
                    quadrant = 2
            if xCoord >= board.N // 2:
                if 0 <= yCoord <= board.M // 2:
                    distance = board.distance_between(board.N - 1, tile)
                    quadrant = 1
                else:
                    distance = board.distance_between((board.M * board.N) - 1, tile)
                    quadrant = 3

            quadrants[quadrant].add((distance, tile))

        prepareSelection = []
        for key, someTuples in quadrants.items():
            for someTuple in someTuples:
                heappush(prepareSelection, (someTuple[0] + (200 - len(someTuples)), someTuple[1]))

        self.TARGET_LOCATION = heappop(prepareSelection)[0]

    def getNextLocation(self, board):

        path = []

        pushedOut = board.pushed_out_square_ids()
        otherPlayerLocation = {board.token_location(self.OTHER_PLAYER_TOKEN)}
        pushedOutTiles =  pushedOut

        self.getNextTargetLocation(board)

        path = self.AStarAlgorithm(self.TARGET_LOCATION, board)
        path = path if path else list(board.neighbor_tiles(board.token_location(self.token())))

        return path[0]

    def hCalc(self, currentLocation, targetLocation, historyLen, board):
        numN = len(board.neighbor_tiles(currentLocation))
        multiplier = 1000 if numN == 1 else 1
        return multiplier*(10*(historyLen + board.distance_between(currentLocation, targetLocation)) + randint(1, 50) - 100*numN)
        
    def AStarAlgorithm(self, targetLocation, board):

        possibleMoves = board.neighbor_tiles(board.token_location(self.token()))

        iterations = 0
        frequencies = {}
        mostFrequent = 0

        myHeap = []
        for move in possibleMoves:
            heappush(myHeap, (self.hCalc(move, targetLocation, 1, board), move, [move]))

        while myHeap:

            iterations += 1
            hVal, possibleMove, history = heappop(myHeap)

            if history[0] not in frequencies:
                frequencies[history[0]] = 0

            frequencies[history[0]] += 1
            mostFrequent = history[0] if not mostFrequent or history[0] > frequencies[mostFrequent] else mostFrequent

            if iterations >= 500:
                return [mostFrequent] if mostFrequent else choice(possibleMove)

            if possibleMove == targetLocation:
                return history

            getAdjacentTiles = board.neighbor_tiles(possibleMove)
            setHistory = set(history)

            for tile in getAdjacentTiles:

                if tile in setHistory:
                    continue

                nHistory = history + [tile]
                nHeuristic = self.hCalc(tile, targetLocation, len(nHistory), board)
                nElement = (nHeuristic, tile, nHistory)
                heappush(myHeap, (nHeuristic, tile, nHistory))


if __name__ == '__main__':
    # Create a match
    isolation.Board.set_dimensions(6, 8)
    red_wins = 0
    wins = {}
    for i in range(500):
        ref = isolation.Match(RandomPlayer('Blue', isolation.Board.BLUE_TOKEN),
                              PlayerAgent('Red', isolation.Board.RED_TOKEN),
                              isolation.Board())
        ref.start_play(debug=False)

        if ref.winner() is None:
            continue

        if ref.winner().name() not in wins:
            wins[ref.winner().name()] = 0

        wins[ref.winner().name()] += 1

    print(wins)

    # print(red_wins)
