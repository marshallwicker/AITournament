from isolation import *
import random

X = True


def congruent_mod(x, y, n):
    return (x - y) % n == 0


class PlayerAgent(Player):
    mid_tiles = {16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31}

    def __init__(self, name, token):
        """
        Initialize a new instance
        :param name: this player's name
        :param token: This player's token
        """

        super().__init__(name, token)
        self.turn_count = 0
        if self.token() == Board.BLUE_TOKEN:
            self.opp = Board.RED_TOKEN
        else:
            self.opp = Board.BLUE_TOKEN

    def take_turn(self, board):
        """
        Make a move on the isolation board
        :param board: an Board object
        :return: Return a Move object
        """
        #start=sw()
        # if X:
        #     print("\n{} taking turn: ".format(self._name), end='')
        #     print(self.turn_count)
        if self.turn_count < 6:
            to_space_id, push_out_space_id = early_move(self, board)
            move = Move(to_space_id, push_out_space_id)
            self.turn_count += 1
        elif self.turn_count < 15:
            to_space_id, push_out_space_id = late_strategy_with_punch(self, board, 5)
            move = Move(to_space_id, push_out_space_id)
            self.turn_count += 1
        else:
            to_space_id, push_out_space_id = late_strategy_with_punch(self, board, 10)
            move = Move(to_space_id, push_out_space_id)
            self.turn_count += 1
        #if X: print('   ', move)
        #print(sw()-start)
        return move


def random_move(player, board):
    space_id = board.token_location(player.token())
    neighbors = board.neighbor_tiles(space_id)
    print('possible moves:', neighbors)
    return random.choice(list(neighbors))


def random_punch(player, board, move_to,adj=False):
    cur_loc = board.token_location(player.token())
    opp_loc = board.token_location(player.opp)
    tiled_spaces = board.push_outable_square_ids()
    tiled_spaces.discard(move_to)
    tiled_spaces.add(cur_loc)
    if adj:
        possible_punch=board.neighbor_tiles(opp_loc)
        tmp2=board.tile_square_ids()
        punch = possible_punch.intersection(tmp2)
    else:
        tmp = board.neighbor_tiles(opp_loc)
        punch = list(tmp)
        for tile in tmp:
            for outer in board.neighbor_tiles(tile):
                if not(outer in punch):
                    punch.append(outer)
        if move_to in punch:
            punch.remove(move_to)
        if cur_loc in board.neighbors(opp_loc) or cur_loc in board.squares_at_radius(opp_loc, 2):
            punch.append(cur_loc)
    if move_to in punch:
        punch.remove(move_to)
    if punch:
        return random.choice(list(punch))
    else:
        return random.choice(list(tiled_spaces))


def early_move(player, board):
    if player.token() == Board.BLUE_TOKEN:
        move = early_move_blue(player, board)
        punch = early_punch_blue(player, board, move)
    else:
        move = early_move_red(player, board)
        punch = early_punch_red(player, board, move)
    return move, punch


def early_move_blue(player, board):
    cur_loc = board.token_location(player.token())
    if cur_loc in player.mid_tiles:
        if cur_loc + 1 in board.push_outable_square_ids() and not (congruent_mod(cur_loc, board.N - 1, board.N)):
            to_space_id = cur_loc + 1
        elif cur_loc >= (board.N * board.M / 2):
            if cur_loc - board.N + 1 in board.push_outable_square_ids() and not (
                    congruent_mod(cur_loc, board.N - 1, board.N)):
                to_space_id = cur_loc - board.N + 1
            elif cur_loc - board.N in board.push_outable_square_ids():
                to_space_id = cur_loc - board.N
            else:
                to_space_id = random_move(player, board)
        elif cur_loc < (board.N * board.M / 2):
            if cur_loc + board.N + 1 in board.push_outable_square_ids() and not (
            congruent_mod(cur_loc, board.N - 1, board.N)):
                to_space_id = cur_loc + board.N + 1
            elif cur_loc + board.N in board.push_outable_square_ids():
                to_space_id = cur_loc + board.N
            else:
                to_space_id = random_move(player, board)
        else:
            to_space_id = random_move(player, board)
    else:
        possible_loc = board.neighbor_tiles(cur_loc).intersection(player.mid_tiles)
        if bool(possible_loc):
            distances = []
            for element in possible_loc:
                tmp = (element, board.distance_between(element, board.token_location(Board.RED_TOKEN)))
                distances.append(tmp)
            cur_min = distances[0]
            for i in range(1, len(distances)):
                if distances[i][1] < cur_min[1]:
                    cur_min = distances[i]
            to_space_id = cur_min[0]
        else:
            to_space_id = random_move(player, board)
    return to_space_id


def early_move_red(player, board):
    cur_loc = board.token_location(player.token())
    if cur_loc in player.mid_tiles:
        if cur_loc - 1 in board.push_outable_square_ids() and not (congruent_mod(cur_loc, 0, board.N)):
            to_space_id = cur_loc - 1
        elif cur_loc >= (board.N * board.M / 2):
            if cur_loc - board.N - 1 in board.push_outable_square_ids() and not (congruent_mod(cur_loc, 0, board.N)):
                to_space_id = cur_loc - board.N - 1
            elif cur_loc - board.N in board.push_outable_square_ids():
                to_space_id = cur_loc - board.N
            else:
                to_space_id = random_move(player, board)
        elif cur_loc < (board.N * board.M / 2):
            if cur_loc + board.N - 1 in board.push_outable_square_ids() and not (congruent_mod(cur_loc, 0, board.N)):
                to_space_id = cur_loc + board.N - 1
            elif cur_loc + board.N in board.push_outable_square_ids():
                to_space_id = cur_loc + board.N
            else:
                to_space_id = random_move(player, board)
        else:
            to_space_id = random_move(player, board)
    else:
        possible_loc = board.neighbor_tiles(cur_loc).intersection(player.mid_tiles)
        if bool(possible_loc):
            distances = []
            for element in possible_loc:
                tmp = (element, board.distance_between(element, board.token_location(player.opp)))
                distances.append(tmp)
            cur_min = distances[0]
            for i in range(1, len(distances)):
                if distances[i][1] < cur_min[1]:
                    cur_min = distances[i]
            to_space_id = cur_min[0]
        else:
            to_space_id = random_move(player, board)
    return to_space_id


def early_punch_blue(player, board, move):
    push_out_space_id = move
    opp_loc = board.token_location(player.opp)
    if opp_loc - 1 in board.push_outable_square_ids() and not (congruent_mod(opp_loc, 0, board.N)):
        push_out_space_id = opp_loc - 1
        if move != push_out_space_id: return push_out_space_id
    alt_push = {opp_loc + 1, opp_loc - 1, opp_loc + Board.N, opp_loc - Board.N}.intersection(
        board.neighbor_tiles(opp_loc))
    possible_push = board.neighbor_tiles(opp_loc) - alt_push
    if bool(possible_push):
        distances = []
        for element in possible_push:
            tmp = (element, board.distance_between(element, move))
            distances.append(tmp)
        cur_max = distances[0]
        for i in range(1, len(distances)):
            if distances[i][1] > cur_max[1]:
                cur_max = distances[i]
        push_out_space_id = cur_max[0]
    elif opp_loc + 1 in board.push_outable_square_ids() and not (congruent_mod(opp_loc, board.N - 1, board.N)):
        push_out_space_id = opp_loc + 1
    if move != push_out_space_id:
        return push_out_space_id
    else:
        return random_punch(player, board, move)


def early_punch_red(player, board, move):
    push_out_space_id = move
    opp_loc = board.token_location(player.opp)
    if opp_loc + 1 in board.push_outable_square_ids() and not (congruent_mod(opp_loc, board.N - 1, board.N)):
        push_out_space_id = opp_loc + 1
        if move != push_out_space_id: return push_out_space_id
    alt_push = {opp_loc + 1, opp_loc - 1, opp_loc + Board.N, opp_loc - Board.N}.intersection(
        board.neighbor_tiles(opp_loc))
    possible_push = board.neighbor_tiles(opp_loc) - alt_push
    if bool(possible_push):
        distances = []
        for element in possible_push:
            tmp = (element, board.distance_between(element, move))
            distances.append(tmp)
        cur_max = distances[0]
        for i in range(1, len(distances)):
            if distances[i][1] > cur_max[1]:
                cur_max = distances[i]
        push_out_space_id = cur_max[0]
    elif opp_loc - 1 in board.push_outable_square_ids() and not (congruent_mod(opp_loc, 0, board.N)):
        push_out_space_id = opp_loc - 1
    if move != push_out_space_id:
        return push_out_space_id
    else:
        return random_punch(player, board, move)


def late_strategy(player, board, look_ahead):
    cur_loc = board.token_location(player.token())
    opp_loc = board.token_location(player.opp)
    knowledge = []
    new_board = Board()
    for tile in board.neighbor_tiles(cur_loc):
        if player.token() == Board.BLUE_TOKEN:
            new_board.set_state(tile, opp_loc, board.pushed_out_square_ids())
        else:
            new_board.set_state(opp_loc, tile, board.pushed_out_square_ids())
        tmp = (tile, h(tile, opp_loc, board))
        knowledge.append(tmp)
    for i in range(1, look_ahead):
        for tile in knowledge:
            for next_tile in new_board.neighbor_tiles(tile[0]):
                if player.token() == Board.BLUE_TOKEN:
                    new_board.set_state(next_tile, opp_loc, board.pushed_out_square_ids())
                else:
                    new_board.set_state(opp_loc, next_tile, board.pushed_out_square_ids())
                tmp = (tile[0], next_tile, h(tile, player, new_board))
                knowledge.append(tmp)
            knowledge.remove(tile)
    move_to = max(knowledge, key=lambda x: x[len(x) - 1])[0]
    return move_to, random_punch(player, board, move_to,True)


def look_ahead(token,knowledge,other_knowledge,current_board):
    board = Board()
    knowledge_copy=knowledge[:]
    for anti_fact in other_knowledge:
        fut_opp_loc=anti_fact.get_cur_loc()
        for fact in knowledge_copy:
            for next_tile in current_board.neighbor_tiles(fact.get_cur_loc()):
                possible_opp_moves=current_board.neighbors(fut_opp_loc)
                missing_tiles = anti_fact.get_punches().union(fact.get_punches(), current_board.pushed_out_square_ids())
                if next_tile in possible_opp_moves:
                    possible_opp_moves-={next_tile}
                possible_opp_moves-=missing_tiles
                for push in possible_opp_moves:
                    missing_tiles.add(push)
                    if token == Board.BLUE_TOKEN:
                        board.set_state(next_tile, fut_opp_loc, missing_tiles)
                    else:
                        board.set_state(fut_opp_loc, next_tile, missing_tiles)
                    tmp1 = (next_tile,push)
                    new_moves=fact.get_moves()
                    new_moves.append(tmp1)
                    new_punches=fact.get_punches()
                    new_punches.add(push)
                    tmp2 = Fact(h(next_tile,fut_opp_loc,board),new_moves,new_punches)
                    knowledge.append(tmp2)
                    missing_tiles.discard(push)
            if fact in knowledge: knowledge.remove(fact)
    return knowledge


def late_strategy_with_punch(player, board, steps):
    cur_loc = board.token_location(player.token())
    opp_loc = board.token_location(player.opp)
    self_knowledge = [Fact(h(cur_loc,opp_loc,board),[(cur_loc,None)])]
    opp_knowledge=[Fact(h(opp_loc,cur_loc,board),[(opp_loc,None)])]
    self_knowledge = look_ahead(player.token(), self_knowledge, opp_knowledge, board)
    self_knowledge.sort(key=lambda x: x.get_h(),reverse=True)
    if len(self_knowledge)>15:
        self_knowledge=self_knowledge[:15]
    for i in range(1,steps):
        opp_knowledge=look_ahead(player.opp,opp_knowledge,self_knowledge,board)
        opp_knowledge.sort(key=lambda x: x.get_h(),reverse=True)
        if len(opp_knowledge) > 15:
            opp_knowledge = opp_knowledge[:15]
        self_knowledge=look_ahead(player.token(),self_knowledge,opp_knowledge,board)
        self_knowledge.sort(key=lambda x:x.get_h(),reverse=True)
        if len(self_knowledge) > 15:
            self_knowledge = self_knowledge[:15]
    if self_knowledge:
        for i in range(0,15):
            ret = self_knowledge[i].next_move()
            if ret[0]!=ret[1]:
                break
        if ret[0] == ret[1]:
            move_to = random_move(player, board)
            ret = (move_to, random_punch(player, board,move_to, True))
    else:
        move_to=random_move(player,board)
        ret = (move_to,random_punch(player,board,move_to,True))
    return ret[0],ret[1]


def h(tile, opp_loc, board):
    return len(board.neighbor_tiles(tile)) - len(board.neighbor_tiles(opp_loc))


class Fact:

    def __init__(self,value,sequence=[],pushes=set()):
        self._moves=sequence
        self._punch=pushes
        self._h=value

    def get_moves(self):
        return self._moves[:]

    def get_punches(self):
        return self._punch.copy()

    def get_h(self):
        return self._h

    def get_cur_loc(self):
        return self._moves[len(self._moves)-1][0]

    def next_move(self):
        return self._moves[1]

    def __eq__(self, other):
        return self._h==other._h and self._moves==other._moves and self._punch==other._punch

    def __ne__(self, other):
        return self._h != other._h and self._moves != other._moves and self._punch != other._punch

    def __lt__(self, other):
        return self._h < other.h

    def __gt__(self, other):
        return self._h > other.h

    def __le__(self, other):
        return self._h <= other.h

    def __ge__(self, other):
        return self._h >= other.h


# Board.set_dimensions(6, 8)
# # match = Match(AgentPlayer('Blue', Board.BLUE_TOKEN),
# #               AgentPlayer('Red', Board.RED_TOKEN))
# # print(match.start_play())
# d={'Blue':0,'Red':0}
# for i in range(100):
#     match = Match(AgentPlayer('Blue', Board.BLUE_TOKEN),
#               AgentPlayer('Red', Board.RED_TOKEN))
#     tmp =match.start_play()
#     d[tmp]+=1
# print('Blue:',d['Blue'])
# print('Red:',d['Red'])
#
# # match = Match(hp.HumanPlayer('Blue', Board.BLUE_TOKEN),
# #               AgentPlayer('Red', Board.RED_TOKEN))
# # print(match.start_play())
