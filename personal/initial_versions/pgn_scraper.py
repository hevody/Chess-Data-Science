import requests
import os

os.chdir('./PGNs')

months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
years = ['2023', '2024']
accounts = ['Percival120', 'hevory']

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"}




for account in accounts:
    for year in years:
        for month in months:
            print(f'[*] Getting history for: {account} on {month}-{year}')
            
            pgnRequester = requests.get(f'https://api.chess.com/pub/player/{account}/games/{year}/{month}/pgn', headers=headers)
            pgnRequester.raise_for_status()
            pgnFile = open(f'{account}-{year}-{month}.txt', 'wb')  
            for chunk in pgnRequester.iter_content(100000):    
                pgnFile.write(chunk)
            pgnFile.close()
input()

'''
pgnRequester = requests.get('http://api.chess.com/pub/player/percival120/games/2024/12/pgn', headers=headers)

pgnRequester.raise_for_status()  

pgnFile = open('pgnTest.txt', 'wb')  
for chunk in pgnRequester.iter_content(100000):  
    pgnFile.write(chunk)
pgnFile.close()
'''