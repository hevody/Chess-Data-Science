import requests
import json
import chess
import chess.pgn
from io import StringIO
from tabulate import tabulate
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")
#logging.disable(logging.CRITICAL)

### config ###
with open('config.json') as f:
  config = json.load(fp=f)
with open('lc_token.env') as f:
  lc_token = f.read()


general_headers = config["HEADERS"]
username = config["USERNAME"]
game_archive_url = config["GAME_ARCHIVE_URL"].format(cc_username=username)
length_of_game_moves = config["LENGTH_OF_GAME_MOVES"] - 1
config["LICHESS_HEADERS"]["Authorization"]= config["LICHESS_HEADERS"]["Authorization"].format(token=lc_token)
lichess_headers = config["LICHESS_HEADERS"]
master_database_api_call = config["MASTER_DATABASE_API_CALL"]
color_of_the_side = config["COLOR_SIDE"]
games_outcome = config["OUTCOME"]

def perform_get_request(url: str, specific_headers: str) -> dict | str:
  logging.info('Performing a GET request')
  response = requests.get(url, headers=specific_headers)

  if response.headers.get("Content-Type", "") == 'application/json; charset=utf-8':
    return response.json()
  else:
    return response.text

def important_game_metadata(pgn1: str) -> tuple[bool, str, str]: # bool for win or lost, str for username's side, str for the list of moves in the game
  logging.info('Capturing the Important Game Metadata')
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


game_archives = perform_get_request(url=game_archive_url, specific_headers=general_headers)["archives"]
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
  games_for_that_month = perform_get_request(url=month_url, specific_headers=general_headers)["games"]  # list
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
  logging.info('Ranking the moves based on frequency')
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

def convert_move_list_to_human_readable_pgn(moves_list: str) -> str:
  logging.info('Converting the list of moves into human readable PGN')
  board = chess.Board()
  #move_objects = [board.parse_san(move) for move in moves_list]

  move_objects = []
  for move in moves_list:
    parsed_move = board.parse_san(move)
    move_objects.append(parsed_move)
    board.push(parsed_move)

  board.reset()

  formatted_string = board.variation_san(move_objects)
  return formatted_string

def convert_to_uci(PREVIOUS_moves_list: list) -> str:
  logging.info("Converting the previous moves into UCI to be used for the Lichess Masters Database")
  board = chess.Board()

  uci_moves = []
  for move in PREVIOUS_moves_list:
    parsed_move = board.parse_san(move)
    uci_moves.append(parsed_move.uci())
    board.push(parsed_move)

  uciANDJoined = ','.join(uci_moves)

  return uciANDJoined

if config["ANALYZE"]:
  FrequencyLineAppears = rank(color_side=color_of_the_side, outcome=games_outcome)

  multiple_line_data = []
  for SINGULARLine in FrequencyLineAppears.keys():
    single_line_data = []
    mov_li = json.loads(SINGULARLine)
    human_readable_line = convert_move_list_to_human_readable_pgn(moves_list=mov_li)
    thisLineFrequency = FrequencyLineAppears[SINGULARLine] 

    previous_move_only_line = mov_li[:-1]

    uciGET = convert_to_uci(PREVIOUS_moves_list=previous_move_only_line)
    responseMainLineMove = perform_get_request(master_database_api_call.format(uci=uciGET), specific_headers=lichess_headers)
    try:
      mainLineMove = json.loads(responseMainLineMove)["moves"][0]["san"]
    except: 
      mainLineMove = 'NULL'

    single_line_data.append(human_readable_line)
    single_line_data.append(thisLineFrequency)
    single_line_data.append(mainLineMove)

    multiple_line_data += [single_line_data]

  headers = ["Line", "Frequency", "Mainline Move"]
  print(tabulate(multiple_line_data, headers=headers, tablefmt="grid"))
