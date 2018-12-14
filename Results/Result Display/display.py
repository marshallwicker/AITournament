match_tallies = {
        'aqua': 0,
        'silver': 0,
        'blue': 0,
        'fuchsia': 0,
        'lime': 0,
        'maroon': 0,
        'olive': 0,
        'teal': 0
}
win_tallies = {
        'aqua': 0,
        'silver': 0,
        'blue': 0,
        'fuchsia': 0,
        'lime': 0,
        'maroon': 0,
        'olive': 0,
        'teal': 0
}

games_run = 0
with open('results.txt', 'r') as results_file:
    for line in results_file:
        win = eval(line)
        games_run += 1
        match_tallies[win['blue']] += 1
        match_tallies[win['red']] += 1
        win_tallies[win['winner']] += 1

        #print('Player 1:', win['blue'], 'Player 2', win['red'], 'Winner: ', win['winner'])

for player, tallies in win_tallies.items():
    print(player + ':', tallies, '/', match_tallies[player], '=', "{:.0%}".format(tallies / match_tallies[player]))
    