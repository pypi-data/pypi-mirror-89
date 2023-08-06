#!/usr/bin/env python3

import json
import math
import os
from typing import Dict, Any, Union

import chess
import chess.engine
import chess.pgn
import chess.svg
import chess.polyglot

from chessAnalyzer.chess_graph import graph


# TODO
#  Maybe add chess.engine.Wdl() to see what your winning chances are


def classify_fen(fen, eco_db):
    """
    Searches a JSON file with Encyclopedia of Chess Openings (ECO) data to
    check if the given FEN matches an existing opening record
    Returns a classification
    A classification is a dictionary containing the following elements:
        "code":         The ECO code of the matched opening
        "desc":         The long description of the matched opening
        "path":         The main variation of the opening
    """
    classification = {"code": "", "desc": "", "path": ""}

    for opening_eco in eco_db:
        if opening_eco['f'] == fen:
            classification["code"] = opening_eco['c']
            classification["desc"] = opening_eco['n']
            classification["path"] = opening_eco['m']

    return classification


def eco_fen(board):
    """
    Takes a board position and returns a FEN string formatted for matching with
    eco.json
    """
    board_fen = board.board_fen()
    castling_fen = board.castling_xfen()

    to_move = 'w' if board.turn else 'b'

    return "{} {} {}".format(board_fen, to_move, castling_fen)


def opening(game_in_question):
    ply_count = 0
    root_node = game_in_question.parent
    node = game_in_question.end()
    with open('eco_codes/eco.json', 'r') as eco_file:
        eco_data = json.load(eco_file)
        while not node == game_in_question.parent:
            prev_node = node.parent

            fen = eco_fen(node.board())
            classification = classify_fen(fen, eco_data)

            if classification["code"] != "":
                # Add some comments classifying the opening
                node.comment = "{} {}".format(classification["code"],
                                              classification["desc"])
                # Remember this position so we don't analyze the moves
                # preceding it later
                root_node = node
                # Break (don't classify previous positions)
                break

            ply_count += 1
            node = prev_node

        return node.parent, root_node, ply_count


def winning_chances(centipawns):
    """
    You don't need this anymore.
    You can use 'chess.engine.Wdl()' for winning,
    drawing and losing chances.
    """
    return 50 + 50 * (2 / (1 + math.exp(-0.004 * centipawns)) - 1)


def needs_annotation(best, played):
    b = winning_chances(int(best * 100))
    p = winning_chances(int(played * 100))
    d = b - p
    return d > 7.5


class bColors:
    HEADER = '\033[95m'
    OK_BLUE = '\033[94m'
    OK_CYAN = '\033[96m'
    OK_GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END_C = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class AnnotatePosition:

    def __init__(self, eval_time: float, cwd: str, eng_file: str = 'Engine/Stockfish_12.exe'):
        """
        Please use full path for 'cwd'.
        """
        self.eval_time = eval_time
        self.eng_file = eng_file
        self.engine = chess.engine.SimpleEngine.popen_uci(self.eng_file)
        self.white_mvs, self.black_mvs, self.black_lpos, self.white_lpos = 0, 0, list(), list()
        self.current_working_directory = cwd
        os.mkdir(self.current_working_directory + '/Game Report')

    def get_eval(self, fen: str) -> float:
        """
        Gets the current evaluation of the position
        Chances to win --> 50 + 50 * (2 / (1 + math.exp(-0.004 * centipawns)) - 1)

        score:
        info = engine.analyse(board, chess.engine.Limit(eval_time))
        info["score"].white().score(mate_score=10000)
        """
        board = chess.Board(fen)
        info = self.engine.analyse(board, chess.engine.Limit(self.eval_time))
        return int(str(info["score"].white().score(mate_score=10000))) / 100

    def get_best_move(self, fen: str, uci=False) -> chess.Move or str:
        """
        Gets best move from uci in position
        """
        board = chess.Board(fen)
        result = self.engine.analyse(board, chess.engine.Limit(time=self.eval_time))
        if uci:
            return result['pv'][0]
        else:
            return board.san(result['pv'][0])

    def get_best_var(self, fen: str, uci=False) -> list or str:
        """
        Gets the best variation from uci in position
        """
        board = chess.Board(fen)
        result = self.engine.analyse(board, chess.engine.Limit(time=self.eval_time))
        if uci:
            return result['pv']
        else:
            return board.variation_san(result['pv'])

    def graph(self, pgn_loc: str, loc: str):
        graph(pgn_loc, self.eng_file, location=loc)

    def annotate_game(self, pgn_loc: str) -> chess.pgn.Game:
        """
        Goes through the game_in_question and analyses and annotates it
        """
        # Read game_in_question and create starting position
        pgn = chess.pgn.read_game(open(pgn_loc))

        # Find out what opening the game_in_question has
        opening(pgn)

        # Mark the end of the game_in_question
        pgn.end().comment = "End of game_in_question. " \
                            "The moves after this one are just telling you how the game_in_question could have gone on."
        # Set variables for the loop
        # prev_eva = 0.00  # not needed anymore
        is_opening = True

        # Iterate through the game_in_question
        for node in pgn.mainline():
            move = node.move
            board = node.board()
            eva = self.get_eval(board.fen())  # Get evaluation of the current position
            if is_opening:  # Checking if the variation is still in the book
                if node.comment:
                    is_opening = False
                    continue
                else:
                    is_opening = True
                    continue
            board.pop()
            actual_best_move = self.get_best_move(board.fen(), uci=True)
            board.push(actual_best_move)
            actual_best_eval = self.get_eval(board.fen())
            board.pop()
            board.push(move)
            delta = eva - actual_best_eval
            parent_node = node.parent
            parent_board = parent_node.board()  # The move is not yet pushed.
            if delta > -0.1:
                pass
            elif delta > -0.3:  # Good move
                parent_node.add_line(self.get_best_var(parent_board.fen(), uci=True),
                                     starting_comment='Good move, but better was: ',
                                     comment=str(self.get_eval(parent_board.fen()))
                                     )
            elif delta > -0.4:  # Interesting move
                parent_node.add_line(self.get_best_var(parent_board.fen(), uci=True),
                                     starting_comment='Interesting move, but better was: ',
                                     comment=str(self.get_eval(parent_board.fen()))
                                     )
            elif delta > -0.5:  # Inaccuracy
                parent_node.add_line(self.get_best_var(parent_board.fen(), uci=True),
                                     starting_comment='This was an Inaccuracy. More accurate would have been: ',
                                     comment=str(self.get_eval(parent_board.fen()))
                                     )
            elif delta > -1.5:  # Mistake
                parent_node.add_line(self.get_best_var(parent_board.fen(), uci=True),
                                     starting_comment='Mistake. You should have played: ',
                                     comment=str(self.get_eval(parent_board.fen()))
                                     )
            elif delta > -3.0:  # Blunder
                parent_node.add_line(self.get_best_var(parent_board.fen(), uci=True),
                                     starting_comment='That was a Blunder, you should have played: ',
                                     comment=str(self.get_eval(parent_board.fen()))
                                     )

            # prev_eva = eva  # making the previous evaluation
        print(f'\n\n\n{bColors.WARNING}{bColors.BOLD}Use <print(pgn, file=open(pgn_loc, "w"), end="\\n\\n")> '
              f'to add the '
              f'annotations to '
              f'the game_in_question.\n\n{bColors.END_C}')
        return pgn

    @staticmethod
    def train_coordinates():
        os.chdir('Chess-Coordinate-Trainer-master')
        os.system('python chess_coordinate_trainer.py')
        os.chdir('..')

    def game_report(self, pgn_loc: str, annotate=False) -> tuple:

        # Read game_in_question and create starting position
        pgn = chess.pgn.read_game(open(pgn_loc))

        board = chess.Board()

        opening(pgn)

        # Mark the end of the game_in_question
        pgn.end().comment = "End of game_in_question. " \
                            "The moves after this one are just telling you how the game_in_question could have gone on."
        # Set variables for the loop
        is_opening = True
        self.white_mvs: Dict[str, Union[int, Any]] = {'Forced move': 0, 'Best move': 0, 'Excellent move': 0,
                                                      'Good move': 0, 'Interesting move': 0, 'Book move': 0,
                                                      'Inaccuracy': 0, 'Mistake': 0, 'Blunder': 0}
        self.black_mvs: Dict[str, Union[int, Any]] = {'Forced move': 0, 'Best move': 0, 'Excellent move': 0,
                                                      'Good move': 0, 'Interesting move': 0, 'Book move': 0,
                                                      'Inaccuracy': 0, 'Mistake': 0, 'Blunder': 0}

        # Iterate through the game_in_question
        for node in pgn.mainline():
            move = node.move
            lgl_mvs = len([i for i in board.legal_moves])
            board = node.board()
            if is_opening:  # Checking if the variation is still in the book
                if node.comment:
                    is_opening = False
                    if board.turn:
                        self.black_mvs['Book move'] += 1
                    else:
                        self.white_mvs['Book move'] += 1
                    continue
                else:
                    is_opening = True
                    if board.turn:
                        self.black_mvs['Book move'] += 1
                    else:
                        self.white_mvs['Book move'] += 1
                    continue

            eva = self.get_eval(board.fen())
            board.pop()
            actual_best_move = self.get_best_move(board.fen(), uci=True)
            board.push(actual_best_move)
            actual_best_eval = self.get_eval(board.fen())
            board.pop()
            board.push(move)
            delta = eva - actual_best_eval
            parent_node = node.parent
            parent_board = parent_node.board()  # The move is not yet pushed.
            if delta == 0:  # Best move
                if parent_board.turn:
                    if lgl_mvs == 1:
                        self.white_mvs['Forced move'] = self.white_mvs['Forced move'] + 1
                    else:
                        self.white_mvs['Best move'] = self.white_mvs['Best move'] + 1
                else:
                    if lgl_mvs == 1:
                        self.black_mvs['Forced move'] = self.black_mvs['Forced move'] + 1
                    else:
                        self.black_mvs['Best move'] = self.black_mvs['Best move'] + 1
            elif delta > -0.1:  # Excellent move
                if parent_board.turn:
                    self.white_mvs['Excellent move'] = self.white_mvs['Excellent move'] + 1
                else:
                    self.black_mvs['Excellent move'] = self.black_mvs['Excellent move'] + 1
            elif delta > -0.3:  # Good move
                if parent_board.turn:
                    self.white_mvs['Good move'] = self.white_mvs['Good move'] + 1
                else:
                    self.black_mvs['Good move'] = self.black_mvs['Good move'] + 1
            elif delta > -0.4:  # Interesting move
                if parent_board.turn:
                    self.white_mvs['Interesting move'] = self.white_mvs['Interesting move'] + 1  # maybe add 'lpos' here
                else:
                    self.black_mvs['Interesting move'] = self.black_mvs['Interesting move'] + 1  # maybe add 'lpos' here
            elif delta > -0.5:  # Inaccuracy
                if parent_board.turn:
                    self.white_mvs['Inaccuracy'] = self.white_mvs['Inaccuracy'] + 1
                    self.white_lpos.append(parent_board.fen())
                else:
                    self.black_mvs['Inaccuracy'] = self.black_mvs['Inaccuracy'] + 1
                    self.black_lpos.append(parent_board.fen())
            elif delta > -1.5:  # Mistake
                if parent_board.turn:
                    self.white_mvs['Mistake'] = self.white_mvs['Mistake'] + 1
                    self.white_lpos.append(parent_board.fen())
                else:
                    self.black_mvs['Mistake'] = self.black_mvs['Mistake'] + 1
                    self.black_lpos.append(parent_board.fen())
            elif delta > -3.0:  # Blunder
                if parent_board.turn:
                    self.white_mvs['Blunder'] = self.white_mvs['Blunder'] + 1
                    self.white_lpos.append(parent_board.fen())
                else:
                    self.black_mvs['Blunder'] = self.black_mvs['Blunder'] + 1
                    self.black_lpos.append(parent_board.fen())

        headers = chess.pgn.read_headers(open(pgn_loc))

        exists = False

        os.chdir('Game Report')
        try:
            os.mkdir(headers["White"] + " vs " + headers["Black"])
        except FileExistsError:
            pass
        os.chdir(headers["White"] + " vs " + headers["Black"])
        try:
            os.mkdir('White')
            os.mkdir('Black')
            os.mkdir('Graph')
        except FileExistsError:
            exists = True
            pass

        os.chdir('../' + headers["White"] + " vs " + headers["Black"])
        os.chdir("..")
        os.chdir("..")

        if not exists:
            for index, svg in enumerate(self.white_lpos):
                board = chess.Board(svg)
                board_svg = chess.svg.board(board=board)
                f = open(f'{self.current_working_directory}/Game Report/{headers["White"] + " vs " + headers["Black"]}/'
                         f'White/Position '
                         f'{index + 1}.SVG', 'w')
                f.write(board_svg)
                f.close()
            for index, svg in enumerate(self.black_lpos):
                board = chess.Board(svg)
                board_svg = chess.svg.board(board=board)
                f = open(f'{self.current_working_directory}/Game Report/{headers["White"] + " vs " + headers["Black"]}/'
                         f'Black/Position '
                         f'{index + 1}.SVG', 'w')
                f.write(board_svg)
                f.close()

            loc = 'Game Report/%s/Graph/Graph of {}.html' % (headers["White"] + " vs " + headers["Black"])
            self.graph(pgn_loc, loc)
        else:
            pass

        if annotate:
            annotated_pgn = self.annotate_game(pgn_loc)
            return [self.white_mvs, self.white_lpos], [self.black_mvs, self.black_lpos], [annotated_pgn.game()]
        else:
            return [self.white_mvs, self.white_lpos], [self.black_mvs, self.black_lpos]
