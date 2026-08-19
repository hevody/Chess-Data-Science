import os






def game_stripper(pgn):
    with open(pgn, 'r') as f:
        contents = f.readlines()



    #emag = 1
    gamesList = []
    firstSlicer = 0
    secondSlicer = 23
    addend = 25
    while True:
        game = contents[firstSlicer:secondSlicer]
        if game == []:
            break
        #print(f'This is game number: {emag}')
        gamesList = gamesList + [game]
        firstSlicer = firstSlicer + addend
        secondSlicer = secondSlicer + addend
        #emag = emag + 1

    #print(gamesList)
    gamesList.reverse()
    os.chdir('../PGNs_indiv')
    #os.system('del *')
    #input()

    game_number = 0
    for indivGame in gamesList:
        game_number = game_number + 1
        game_number_stringify = str(game_number)
        game_number_stringify = game_number_stringify.rjust(3, '0')
        filename = f'{pgn[:-4]}-GAME-{game_number_stringify}.txt'
        print(f'[*] Building {filename}...')
        for line in indivGame:
            with open(filename, 'a') as f:
                f.write(line.strip())    
                f.write('\n')
    
    os.chdir('../PGNs')

os.chdir('./PGNs')
pgns = os.listdir()

for monthlyPGN in pgns:
    game_stripper(monthlyPGN)

