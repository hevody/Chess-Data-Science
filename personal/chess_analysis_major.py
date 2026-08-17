import requests
import json
import chess
import chess.pgn
from io import StringIO

### config ###
with open('config.json') as f:
  config = json.load(fp=f)

headers = config["HEADERS"]
username = config["USERNAME"]
game_archive_url = config["GAME_ARCHIVE_URL"].format(cc_username=username)



def perform_get_request(url: str) -> dict | str:
  response = requests.get(url, headers=headers)

  if response.headers.get("Content-Type", "") == 'application/json; charset=utf-8':
    return response.json()
  else:
    return response.text()

def important_game_metadata(pgn1: str) -> tuple[bool, str, str]: # bool for win or lost, str for username's side, str for the list of moves in the game
  game_func1 = chess.pgn.read_game(StringIO(pgn1))
  if game_func1.headers['Termination'].startswith(username):
    win = True
  else: 
    win = False
  if game_func1.headers['White'].startswith(username):
    side = 'White'
  else: 
    side = 'Black'

  board = game_func1.board()
  moves_list_uci = [move for move in game_func1.mainline_moves()]
  moves_list = []
  for move in game_func1.mainline_moves():
    san_move = board.san(move)
    board.push(move=move)
    moves_list += [san_move]

  print(moves_list)
  
  return win, side, moves_list


game_archives = perform_get_request(url=game_archive_url)["archives"]
if config["DEPTH_OF_MONTH"] == 0: # means entire game archive
  depth_of_month = 0
else:
  depth_of_month = len(game_archives) - config["DEPTH_OF_MONTH"]

win_rate_dict = {"White": {"Win": 0, "Lost": 0},
                 "Black": {"Win": 0, "Lost": 0}}

for index in range(depth_of_month, len(game_archives)):
  month_url = game_archives[index]
  games_for_that_month = perform_get_request(url=month_url)["games"]  # list
  for index_of_game in range(len(games_for_that_month)):             
    pgn_from_game = games_for_that_month[index_of_game]["pgn"]        # just use if statement onward so the cache will not be wasted and keeps the program blazing fast
    winner, color, m_list = important_game_metadata(pgn1=pgn_from_game)
    if config["CALCULATE_WIN_RATE"]:
      if color == "White" and winner == True:
        win_rate_dict["White"]["Win"] += 1
      elif color == "White" and winner == False:
        win_rate_dict["White"]["Lost"] += 1
      elif color == "Black" and winner == True:
        win_rate_dict["Black"]["Win"] += 1
      elif color == "Black" and winner == False:
        win_rate_dict["Black"]["Lost"] += 1


print(win_rate_dict)


