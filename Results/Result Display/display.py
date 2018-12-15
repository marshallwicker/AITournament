from copy import deepcopy
import datetime
import csv


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
    format_string = '{:>7}: {:>5} / {:>5} = {:.2%}'
    now = str(datetime.datetime.now()).replace(':', '_').replace('/', '-') + '.csv'
    csv_file = open('overall_results' + now, 'w')
    csv_writer = csv.writer(csv_file)
    for player, tallies in win_tallies.items():
        overall_wins = tallies[0]
        overall_matches_played = match_tallies[player][0]
        overall_win_percentage = overall_wins / overall_matches_played
        csv_writer.writerow([player, overall_wins, overall_matches_played, overall_win_percentage])
        print(format_string.format(player.upper(), overall_wins, overall_matches_played, overall_win_percentage))
    csv_file.close()
    print('-' * line_length)
    print()
    print('-' * line_length)
    print('INDIVIDUAL MATCH-UP DATA'.center(line_length))
    print('-' * line_length)
    csv_file = open('individual_results' + now, 'w')
    csv_writer = csv.writer(csv_file)
    for player, tallies in win_tallies.items():
        csv_list = []
        print()
        print('{:^29}'.format(player.upper()))
        csv_list.append(player.upper())
        print('-' * line_length)
        for vs_player, wins_against_player in win_tallies[player][1].items():
            if vs_player != player:
                matches_against_player = match_tallies[player][1][vs_player]
                win_percentage_against_player = wins_against_player / matches_against_player
                csv_list.append(wins_against_player)
                csv_list.append(matches_against_player)
                print(format_string.format(vs_player.upper(), wins_against_player,
                                           matches_against_player, win_percentage_against_player))
        csv_writer.writerow(csv_list)
    csv_file.close()


if __name__ == '__main__':
    print_results()
