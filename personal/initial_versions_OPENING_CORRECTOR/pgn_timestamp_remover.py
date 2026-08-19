import os





def timestamp_remover(game):
    with open(game) as f:
        contents = f.readlines()
 
    keeps = contents[:22]

    try:
        timestamped_pgn = contents[22]
    except:
        return



    main_pgn_listified = timestamped_pgn.split()

    without_timestamp_list = [] 

    starting_number_index = 0
    white_move_index = 1
    black_move_index = 5

    while True:
        try:
            starting_number = main_pgn_listified[starting_number_index]
            white_move = main_pgn_listified[white_move_index]
            black_move = main_pgn_listified[black_move_index]
            
            
            without_timestamp_list = without_timestamp_list + [starting_number]
            without_timestamp_list = without_timestamp_list + [white_move]
            without_timestamp_list = without_timestamp_list + [black_move]

            starting_number_index = starting_number_index + 8
            white_move_index = white_move_index+ 8
            black_move_index = black_move_index + 8
        
        except IndexError:
            break

    #print(without_timestamp_list)

    os.chdir('../PGNs_clean')

    filename = f'{game[:-4]}-CL.txt'
    print(f'[*] Building {filename}...')

    with open(filename, 'a') as f:
        for line_num in range(22):
            line = keeps[line_num].strip()
            f.write(line)
            f.write('\n')
        
        for move in without_timestamp_list:
            f.write(move)
            f.write(' ')
    
    os.chdir('../PGNs_indiv')

os.chdir('./PGNs_indiv')
game_pgns = os.listdir()

for game_pgn in game_pgns:
    timestamp_remover(game_pgn)