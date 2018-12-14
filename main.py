"""
This module runs a sequence of round-robin matches.
It flips a coin to determine who moves first
"""
import itertools
import urllib.request
import urllib.parse
import json
import pickle
import time
import random
import os
import datetime
import sys
from copy import deepcopy

import isolation

import aqua  # ['Will', 'David S']
import silver  # ['Sergio', 'David W']
import blue  # ['Seth', 'Alex']
import fuchsia  # ['Aaron', 'Logan']
import lime  # ['Orlando', 'Brendon']
import maroon  # ['Sunny', 'Zach']
import olive  # ['Michael', 'Alec']
import teal  # ['Eduardo', 'Marshall']

CGI_ROOT = 'http://wocoders.com/~sykesda/cgi-bin/'


def server_request(script, args):
    """
    Send a GET request to a server
    :param script: server CGI script to run
    :param args: a dictionary of argument, value pairings
    :return: A data structure created from a JSON response
    """
    url = CGI_ROOT + script + '?' + urllib.parse.urlencode(args)
    print(url)
    response = urllib.request.urlopen(url)

    return json.loads(response.read())


TEAMS = {
    'silver': ['Sergio', 'David W'],
    'blue': ['Seth', 'Alex'],
    'fuchsia': ['Aaron', 'Logan'],
    'lime': ['Orlando', 'Brendon'],
    'maroon': ['Sunny', 'Zach'],
    'olive': ['Michael', 'Alec'],
    'teal': ['Eduardo', 'Marshall']
}


def generate_matches(agent_classes):
    """
    Generate matches on the server and store the data in a pickle
    file matchinfo.txt
    :param agent_classes: a dictionary of player classes {color: class, ...}
    :return: None
    """
    colors = agent_classes.keys()
    pairings = [pair for pair in itertools.product(colors, colors) if pair[0] != pair[1]]

    matches = []
    for pairing in pairings:
        players = list(pairing)
        random.shuffle(players)
        blue, red = players
        match_info = server_request('newmatch.py', {'bluetoken': blue, 'redtoken': red})
        matches.append(match_info)
        time.sleep(1.0)

    print('\n'.join(str(match) for match in matches))

    pickle_file = open('matchinfo.txt', 'wb')
    pickle.dump(matches, pickle_file)
    pickle_file.close()


def print_results(filename='results.txt'):
    player_tallies = {
        'aqua': 0,
        'silver': 0,
        'blue': 0,
        'fuchsia': 0,
        'lime': 0,
        'maroon': 0,
        'olive': 0,
        'teal': 0
    }

    match_tallies = {
        'aqua': [0, deepcopy(player_tallies)],
        'silver': [0, deepcopy(player_tallies)],
        'blue': [0, deepcopy(player_tallies)],
        'fuchsia': [0, deepcopy(player_tallies)],
        'lime': [0, deepcopy(player_tallies)],
        'maroon': [0, deepcopy(player_tallies)],
        'olive': [0, deepcopy(player_tallies)],
        'teal': [0, deepcopy(player_tallies)]
    }

    win_tallies = deepcopy(match_tallies)

    with open('results.txt', 'r') as results_file:
        for line in results_file:
            match_result = eval(line)
            blue = match_result['blue']
            red = match_result['red']
            winner = match_result['winner']
            loser = blue if winner == red else red

            match_tallies[blue][0] += 1
            match_tallies[red][0] += 1
            match_tallies[blue][1][red] += 1
            match_tallies[red][1][blue] += 1
            win_tallies[winner][0] += 1
            win_tallies[winner][1][loser] += 1

            # print('Player 1:', win['blue'], 'Player 2', win['red'], 'Winner: ', win['winner'])
    line_length = 29
    print('-' * line_length)
    print('OVERALL TOURNAMENT DATA'.center(line_length))
    print('-' * line_length)
    format_string = '{:>7}: {:>4} / {:>4} = {:.2%}'
    for player, tallies in win_tallies.items():
        overall_wins = tallies[0]
        overall_matches_played = match_tallies[player][0]
        overall_win_percentage = overall_wins / overall_matches_played
        print(format_string.format(player.upper(), overall_wins, overall_matches_played, overall_win_percentage))

    print('-' * line_length)
    print()
    print('-' * line_length)
    print('INDIVIDUAL MATCH-UP DATA'.center(line_length))
    print('-' * line_length)
    for player, tallies in win_tallies.items():
        print()
        print('{:^29}'.format(player.upper()))
        print('-' * line_length)
        for vs_player, wins_against_player in win_tallies[player][1].items():
            if vs_player != player:
                matches_against_player = match_tallies[player][1][vs_player]
                win_percentage_against_player = wins_against_player / matches_against_player
                print(format_string.format(vs_player.upper(), wins_against_player,
                                           matches_against_player, win_percentage_against_player))


def run_tournament(agent_classes, start_match_index=0, tournament_run_count=1, debug=False):
    """
    Play a bunch of matches between the teams listed in teams
    :param debug: if set to true, it requires user input before going to the next match
    :param tournament_run_count: specifies how many tournaments to run
    :param start_match_index: if the code breaks, you can choose where to start
    :param agent_classes: a dictionary of player classes
    :return:
    """

    # Create new red players
    # red_agents = {team: agent_classes[team](team, isolation.Board.RED_TOKEN) for team in agent_classes}
    #
    # blue_agents = {team: agent_classes[team](team, isolation.Board.BLUE_TOKEN) for team in agent_classes}

    pairings = [pair for pair in itertools.product(agent_classes.keys(), agent_classes.keys()) if pair[0] != pair[1]]

    print(pairings)

    wins = {team: 0 for team in agent_classes}

    results = []
    for i in range(tournament_run_count):
        for team1, team2 in pairings[start_match_index:]:
            # Flip a coin to see who goes first
            if random.choice(('H', 'T')) == 'H':
                blue_player = agent_classes[team1](team1, isolation.Board.BLUE_TOKEN)
                red_player = agent_classes[team2](team2, isolation.Board.RED_TOKEN)
            else:
                blue_player = agent_classes[team2](team2, isolation.Board.BLUE_TOKEN)
                red_player = agent_classes[team1](team1, isolation.Board.RED_TOKEN)

            board = isolation.Board()
            match = isolation.Match(blue_player, red_player, board)

            match.start_play()

            wins[match.winner().name()] += 1

            results.append({'blue': blue_player.name(),
                            'red': red_player.name(), 'winner': match.winner().name()})

            moves = board.moves()
            filename = f'{blue_player.name()}_{red_player.name()}.txt'

            if not os.path.isdir('Matches'):
                os.mkdir('Matches')
            with open('Matches/' + filename, 'w') as log_file:
                print('\n'.join(str(move) for move in moves), file=log_file)

            with open('results.txt', 'w') as results_file:
                print('\n'.join(str(result) for result in results), file=results_file)

            if debug:
                input('Hit RETURN to continue')


if __name__ == '__main__':
    if os.path.isfile('results.txt'):
        os.rename('results.txt', 'results_' + str(datetime.datetime.now()).replace(':', '_').replace('/', '-') + '.txt')
    isolation.Board.set_dimensions(6, 8)

    agent_classes = {
        'aqua': aqua.PlayerAgent,
        'silver': silver.PlayerAgent,
        'blue': blue.PlayerAgent,
        'fuchsia': fuchsia.PlayerAgent,
        'lime': lime.PlayerAgent,
        'maroon': maroon.PlayerAgent,
        'olive': olive.PlayerAgent,
        'teal': teal.PlayerAgent,
    }
    tournament_run_count = 1
    if len(sys.argv) > 1:
        tournament_run_count = int(sys.argv[1])
    generate_matches(agent_classes)
    run_tournament(agent_classes, tournament_run_count=tournament_run_count)

    print_results()
