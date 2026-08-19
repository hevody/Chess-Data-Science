import os

def deleteFilesInPGNsindiv():
    os.chdir('./PGNs_indiv')
    os.system('del *')

def deleteFilesInPGNsclean():
    os.chdir('./PGNs_clean')
    os.system('del *')


print('\nWhich tool do you want to use?\n')
print('[1] Delete all files in PGNs_indiv?')
print('[2] Delete all files in PGNs_clean')
print()
choice = input('> ')
choice = int(choice)

tools = ['deleteFilesInPGNsindiv()', 'deleteFilesInPGNsclean()']

exec(tools[choice - 1])
