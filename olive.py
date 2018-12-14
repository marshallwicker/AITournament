import isolation
# import randomplayer
# from display import Displayable
import random


def bfs_shortest_path(board, start, goal):
    explored = []
    queue = [[start]]
    while queue:
        path = queue.pop(0)
        # print('PATH:', path, 'GOAL:', goal)
        last_node = path[-1]
        if last_node == goal:
            return path
        else:
            if goal in board.neighbors(last_node):
                # Found a path!
                path.append(goal)
                # print('FOUND', path)
                return path
            # print('    CHECKING TILED NEIGHBORS:', board.neighbor_tiles(last_node))
            for neighbor in board.neighbor_tiles(last_node):
                if neighbor not in explored:
                    queue.append(path + [neighbor])
                    explored.append(neighbor)
                    # print('        ADDING PATH:', queue[-1])

    return []

# def mini_max_alpha_beta_pruning(node, alpha, beta, depth=0):
#     best = None
#     if node.is_leaf():
#         return node.evaluate(),None
#     elif node.is_max:
#         for C in node.children():
#             score, path = mini_max_alpha_beta_pruning(C, alpha, beta, depth+1)
#             if score >= beta:
#                 return score, None
#             if score > alpha:
#                 alpha = score
#                 best = C.name, path
#         return alpha, best
#     else:
#         for C in node.children():
#             score, path = mini_max_alpha_beta_pruning(C, alpha, beta, depth+1)
#             if score <= alpha:
#                 return score, None
#             if score < beta:
#                 beta = score
#                 best = C.name, path
#             return beta, best


# class Node(Displayable):
#
#     def __init__(self, name, is_max, value, children):
#         self.name = name
#         self.is_max = is_max
#         self.value = value
#         self.all_children = children
#
#     def is_leaf(self):
#         """returns true if this is a leaf node"""
#         return self.all_children is None
#
#     def children(self):
#         """return the list of all children"""
#         return self.all_children
#
#     def evaluate(self):
#         """returns the evaluation for this node if it is a leaf or if it is at a certain depth"""
#         return self.value


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

        if len(board.pushed_out_square_ids()) <= 9:
            print("EARLY GAME")

            # give locations for start and goal tiles
            start = board.token_location(self._token)
            goal = board.token_location(self._opponent)

            new_path = bfs_shortest_path(board, start, goal)
            if len(new_path) > 1:
                if new_path[1] == goal:
                    space_id = board.token_location(self._token)
                    neighbors = board.neighbor_tiles(space_id)
                    to_space_id = random.choice(list(neighbors))
                    for x in neighbors:
                        if len(board.neighbor_tiles(x)) > len(board.neighbor_tiles(to_space_id)):
                            to_space_id = x
                else:
                    to_space_id = new_path[1]
                tiled_spaces = board.push_outable_square_ids()
                tiled_spaces.discard(to_space_id)
                tiled_spaces.add(start)
                opponent_edge_pieces = list(set(tiled_spaces).intersection(board.neighbors(board.token_location(self._opponent))))
                if len(opponent_edge_pieces) > 0:
                    pop_space_id = random.choice(opponent_edge_pieces)
                else:
                    pop_space_id = random.choice(list(tiled_spaces))
                move = isolation.Move(to_space_id, pop_space_id)
                print("Move to ", to_space_id, "Push out ", pop_space_id)

            else:
                print("NO PATH FOUND")
                # since no path is found, it switches to the late game strategy
                # Move to neighbor tile with the most neighbors
                space_id = board.token_location(self._token)
                possible_moves = board.neighbor_tiles(space_id)
                to_space_id = random.choice(list(possible_moves))
                for move in possible_moves:
                    if len(board.neighbor_tiles(move)) > len(board.neighbor_tiles(to_space_id)):
                        to_space_id = move

                # Remove best_move from tiles you can push out
                # Add space_id to tiles you can push out
                tiled_spaces = board.push_outable_square_ids()
                tiled_spaces.discard(to_space_id)
                tiled_spaces.add(space_id)

                # Find token to pop
                other_token = board.token_location(self._opponent)
                possible_pops = board.neighbor_tiles(other_token)

                if to_space_id in possible_pops:
                    possible_pops.discard(to_space_id)
                if len(possible_pops) > 0:
                    best_pop = random.choice(list(possible_pops))
                    for pop in possible_pops:
                        if len(board.neighbor_tiles(pop)) > len(board.neighbor_tiles(best_pop)):
                            best_pop = pop
                else:
                    best_pop = random.choice(list(tiled_spaces))

                push_out_space_id = best_pop

                print('    Moving to', to_space_id, 'and pushing out', push_out_space_id)
                if to_space_id == push_out_space_id:
                    print('same tile')
                move = isolation.Move(to_space_id, push_out_space_id)
                print("Move to ", to_space_id, "Push out ", push_out_space_id)
            return move

        if len(board.pushed_out_square_ids()) > 9:

            print("LATE GAME")
            # Move to neighbor tile with the most neighbors
            space_id = board.token_location(self._token)
            possible_moves = board.neighbor_tiles(space_id)
            to_space_id = random.choice(list(possible_moves))
            for move in possible_moves:
                if len(board.neighbor_tiles(move)) > len(board.neighbor_tiles(to_space_id)):
                    to_space_id = move

            # Move to the neighbor tile with the neighbor that has the most neighbors
            # space_id = board.token_location(self._token)
            # tiles_two_away = set(board.squares_at_radius(space_id, 2))
            # pushed_out = set(board.pushed_out_square_ids())
            # moveable_tiles_two = set()
            # for tile in tiles_two_away:
            #     if tile not in pushed_out:
            #         moveable_tiles_two.add(tile)
            # if len(moveable_tiles_two) == 0:
            #     moveable_tiles_two = set(board.neighbor_tiles(space_id))
            # best_tile = random.choice(list(moveable_tiles_two))
            # for tile in moveable_tiles_two:
            #     if len(board.neighbor_tiles(tile)) > len(board.neighbor_tiles(best_tile)):
            #         best_tile = tile
            #
            # path = bfs_shortest_path(board, space_id, best_tile)
            # to_space_id = path[1]

            # Remove best_move from tiles you can push out
            # Add space_id to tiles you can push out
            tiled_spaces = board.push_outable_square_ids()
            tiled_spaces.discard(to_space_id)
            tiled_spaces.add(space_id)

            # Find token to pop
            other_token = board.token_location(self._opponent)
            possible_pops = board.neighbor_tiles(other_token)

            if to_space_id in possible_pops:
                possible_pops.discard(to_space_id)
            if len(possible_pops) > 0:
                best_pop = random.choice(list(possible_pops))
                for pop in possible_pops:
                    if len(board.neighbor_tiles(pop)) > len(board.neighbor_tiles(best_pop)):
                        best_pop = pop
            else:
                best_pop = random.choice(list(tiled_spaces))

            push_out_space_id = best_pop

            print('    Moving to', to_space_id, 'and pushing out', push_out_space_id)
            if to_space_id == push_out_space_id:
                print('same tile')
            move = isolation.Move(to_space_id, push_out_space_id)
            return move


# if __name__ == '__main__':
#     # Create a match
#     isolation.Board.set_dimensions(6, 8)
#     match = isolation.Match(randomplayer.RandomPlayer('Blue', isolation.Board.BLUE_TOKEN),
#                             PlayerAgent('Red', isolation.Board.RED_TOKEN),
#                             isolation.Board())
#     match.start_play()
            


