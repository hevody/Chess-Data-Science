import os

os.chdir('./PGNs')
files = os.listdir()
#print(files)

for file in files:
    with open(file) as f:
        contents = f.read()
    if contents == '':
        os.system(f'del {file}')
        print('successfully deleted')
        


with open(files[0], 'r') as f:
    contents = f.read()

if contents == '':
    print('file is empty')