''' third test is to see how to convert string into list; answer: .split() method
with open('hevory-2023-08-GAME-1.txt') as f:
    contents = f.readlines()

main_pgn = contents[22]
main_pgn_listified = main_pgn.split()
print(main_pgn_listified)
'''

''' second test -- if append option creates a file = TRUE
with open('somerandomFile.txt', 'a') as f:
    f.write('random') 
'''

''' first test -- as to where they the slice starts and ends, start index is included whereas end index is not included, previous only
import os


os.chdir('./PGNs')

with open('hevory-2023-08.txt', 'r') as f:
    PGN = f.readlines()

print(PGN[0:25])
'''