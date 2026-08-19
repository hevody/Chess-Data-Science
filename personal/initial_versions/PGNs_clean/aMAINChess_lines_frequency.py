import os
import copy


os.chdir('./PGNs_clean')
# CONFIGURING FILES THAT ARE NOT SUPPOSED TO BE INCLUDED BECAUSE IT WILL CAUSE INDEX ERROR
games = os.listdir()
removes = []
for game in games:
    if not game.endswith('.txt'):
        removes = removes + [game]
for remove in removes:
    games.remove(remove)



# CONFIGURING THE GAMES IN LIST FORM, IN AN ARRAY
# PLEASE USE THE COPY MODULE TO AVOID BUGS IN ARRAY
lines_listified_more = []
for game in games:
    with open(game) as f:
        contents = f.readlines()
    try:
        line = contents[22]
    except IndexError:
        continue
    line_listified = line.split()
    lines_listified_more = lines_listified_more + [line_listified]

### DECLARATION IN PREPARATION FOR WHILE LOOPS AND FOR LOOPS
white_line_slice_index = 2
black_line_slice_index = 3

line_dictionary = {} # contains vital branches

branch_system = 0
####################################################################

while True:
    # TEMPORARY DECLARATION   
    white_line_g_combination = [] # contains sliced version of the games (or the moves featuring white)
    black_line_g_combination = [] # contains sliced version of the games (or the moves featuring black)
    lines_listified_more_copyyy = copy.deepcopy(lines_listified_more) # copied version for removal purposes
    #####################################
    for game_line in lines_listified_more:

        white_line = game_line[:white_line_slice_index]
        white_line_g_combination = white_line_g_combination + [white_line]
    
        black_line = game_line[:black_line_slice_index]
        black_line_g_combination = black_line_g_combination + [black_line]
    
    ### WHITE SECTION ###
    branch_system = branch_system + 1
    # Searching for unique lines in order to use as a key in the dictionary
    unique_lines = []
    for white_move in white_line_g_combination:
        if white_move in unique_lines:
            continue
        unique_lines = unique_lines + [white_move]
    
    # Dictionary that contains line as a key, and frequency and branch as a value (FOR WHITE)
    # //Frequency counter
    for unique_line in unique_lines:
        frequency  = 0
        for white_move in white_line_g_combination:
            if unique_line == white_move:
                frequency = frequency + 1

        frequency = str(frequency)
        unique_line_joined = ' '.join(unique_line)
        line_dictionary[unique_line_joined] = [frequency] + [f'{branch_system}']
    
    # Search for games who does not match other games
    indexRemoves = []
    for key_from_dict in line_dictionary.keys():
        
        REALfrequency = line_dictionary[key_from_dict][0]
        REALfrequency = int(REALfrequency)
        key_from_dict = key_from_dict.split()
        if REALfrequency == 1:
            for white_move_index in range(len(white_line_g_combination)):
                if key_from_dict == white_line_g_combination[white_move_index]:
                    indexRemoves = indexRemoves + [white_move_index]

    ### BLACK SECTION ###
    branch_system = branch_system + 1
    # Searching for unique lines in order to use as a key in the dictionary
    unique_lines = []
    for black_move in black_line_g_combination:
        if black_move in unique_lines:
            continue
        unique_lines = unique_lines + [black_move]
    
    # Dictionary that contains line as a key, and frequency and branch as a value (FOR WHITE)
    # //Frequency counter
    for unique_line in unique_lines:
        frequency  = 0
        for black_move in black_line_g_combination:
            if unique_line == black_move:
                frequency = frequency + 1

        frequency = str(frequency)
        unique_line_joined = ' '.join(unique_line)
        line_dictionary[unique_line_joined] = [frequency] + [f'{branch_system}']
    
    # Search for games who does not match other games
    for key_from_dict in line_dictionary.keys():
        REALfrequency = line_dictionary[key_from_dict][0]
        REALfrequency = int(REALfrequency)
        key_from_dict = key_from_dict.split()
        if REALfrequency == 1:
            for black_move_index in range(len(black_line_g_combination)):
                if key_from_dict == black_line_g_combination[black_move_index]:
                    indexRemoves = indexRemoves + [black_move_index]
    repeat = []
    for index in indexRemoves:
        if index in repeat:
            continue
        repeat = repeat + [index]
        specific_game = lines_listified_more_copyyy[index]
        lines_listified_more.remove(specific_game)
    
    white_line_slice_index = white_line_slice_index + 3
    black_line_slice_index = black_line_slice_index + 3
    
    if branch_system > 500:
        break

#print(line_dictionary)
#input()

#line_dictionary is the db
##### BEAUTIFY THE PRINT ######
print('[*] Welcome, we will analyze your most used line...')

# Find the longest branch
lines = list(line_dictionary.keys()) # key_list

longBranch = lines[-1]
#print(longBranch)
REAL_longBranch = int(line_dictionary[longBranch][1])
#print(REAL_longBranch)

'''
for branch in range(REAL_longBranch):
    branch = branch + 1
    print(branch)
'''

'''
frequency_description = list(line_dictionary.values())
print(frequency_description)
position = frequency_description.index(['456', '1'])
print(position)
input()
'''



with open('ChessLinesFrequency', 'a') as f:
    for branch in range(REAL_longBranch):
        without_branch_line_dictionary = {}
        branch = branch + 1
        f.write(f'BRANCH {branch}\n\n')
        storage_of_line_key = []
        for line in lines:
            branch_of_line = int(line_dictionary[line][1])
            if branch_of_line == branch:
                storage_of_line_key = storage_of_line_key + [line]
        
        #print(storage_of_line_key)
        

        for key in storage_of_line_key:
            how_frequent = line_dictionary[key][0]
            how_frequent = int(how_frequent)
            without_branch_line_dictionary[key] = how_frequent
        
        #print(without_branch_line_dictionary)
        
        sorted_branched_line_dictionary = dict(sorted(without_branch_line_dictionary.items(), key=lambda x: x[1], reverse=True))
        
        for k, v in sorted_branched_line_dictionary.items():
            v = str(v)
            v = v.ljust(5)
            f.write(f'{v}{k}\n')
        
        f.write('\n')
        
        