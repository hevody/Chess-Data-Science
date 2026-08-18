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
length_of_game_moves = config["LENGTH_OF_GAME_MOVES"] - 1



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
  individual_game_moves_order = []
  for move in game_func1.mainline_moves():
    san_move = board.san(move)
    board.push(move=move)
    individual_game_moves_order += [san_move]
  
  return win, side, individual_game_moves_order


game_archives = perform_get_request(url=game_archive_url)["archives"]
if config["DEPTH_OF_MONTH"] == 0: # means entire game archive
  depth_of_month = 0
else:
  depth_of_month = len(game_archives) - config["DEPTH_OF_MONTH"]

win_rate_dict = {"White": {"Win": 0, "Lost": 0},
                 "Black": {"Win": 0, "Lost": 0}}

games_move_order = {"White": {"Win": [],
                              "Lost": []},
                    "Black": {"Win": [],
                              "Lost": []}}

for index in range(depth_of_month, len(game_archives)):
  month_url = game_archives[index]
  games_for_that_month = perform_get_request(url=month_url)["games"]  # list
  for index_of_game in range(len(games_for_that_month)):             
    pgn_from_game = games_for_that_month[index_of_game]["pgn"]        # just use if statement onward so the cache will not be wasted and keeps the program blazing fast
    winner, color, ig_move_order = important_game_metadata(pgn1=pgn_from_game)
    if config["CALCULATE_WIN_RATE"]:
      if color == "White" and winner == True:
        win_rate_dict["White"]["Win"] += 1
      elif color == "White" and winner == False:
        win_rate_dict["White"]["Lost"] += 1
      elif color == "Black" and winner == True:
        win_rate_dict["Black"]["Win"] += 1
      elif color == "Black" and winner == False:
        win_rate_dict["Black"]["Lost"] += 1
    if config["OPENING_ANALYZER"]:
      if color == 'White' and winner == True:
        games_move_order["White"]["Win"] += [ig_move_order]
      if color == 'White' and winner == False:
        games_move_order["White"]["Lost"] += [ig_move_order]
      if color == 'Black' and winner == True:
        games_move_order["Black"]["Win"] += [ig_move_order]
      if color == 'Black' and winner == False:
        games_move_order["Black"]["Lost"] += [ig_move_order]

def rank(color_side: str, outcome: str) -> dict:
  ColorComplyLength = []
  DictTallyColorUniqueLine = {}
  ColorOutcome = games_move_order[color_side][outcome]
  for GAMEColor in ColorOutcome:
    if color_side == 'White':
      oe_number_generator = [x for x in range(1, len(GAMEColor), 2)]
    if color_side == 'Black':
      oe_number_generator = [x for x in range(2, len(GAMEColor), 2)]
    try:
      ColorComplyLength += [GAMEColor[:oe_number_generator[length_of_game_moves]]]
    except:
      ColorComplyLength += [GAMEColor]

  KeysColorUniqueLine = [list(x) for x in dict.fromkeys(tuple(item) for item in ColorComplyLength)]
  StringKeysColorUniqueLine = [json.dumps(sublist) for sublist in KeysColorUniqueLine]
  DictTallyColorUniqueLine = dict.fromkeys(StringKeysColorUniqueLine, 0)

  for key in list(DictTallyColorUniqueLine.keys()):
    for SINGULARColorLength in ColorComplyLength:
      if SINGULARColorLength == json.loads(key):
        DictTallyColorUniqueLine[key] += 1

  RANKEDDictTallyColorUniqueLine =  dict(sorted(DictTallyColorUniqueLine.items(), key=lambda item: item[1], reverse=True))

  return RANKEDDictTallyColorUniqueLine

if config["ANALYZE"]:
  print(rank('Black', 'Lost'))
  

