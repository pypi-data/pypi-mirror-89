#!/usr/bin/env python3

def graph(pgn, engine, location):
    import chess.pgn
    print('Loading everything...')

    # for i in range(1, 3):
    act_game = chess.pgn.read_game(open(pgn))

    headers = chess.pgn.read_headers(open(pgn))

    print('Analyzing this game_in_question: ' + headers["Event"] + " | " + headers["White"] +
          " - " + headers["Black"] + "  " + headers["Result"] +
          " | " + headers["Date"])

    # import chess.engine
    #
    # engine = chess.engine.SimpleEngine.popen_uci("C:/Users/iitda/Chess_analysis/stockfish_9_x64.exe")

    import chess.engine

    engine = chess.engine.SimpleEngine.popen_uci(engine)

    board = act_game.board()
    board.fen()

    import numpy as np

    print('Making functions...')

    def fentotensor(inputstr):
        pieces_str = "PNBRQK"
        pieces_str += pieces_str.lower()
        pieces = set(pieces_str)
        valid_spaces = set(range(1, 9))
        pieces_dict = {pieces_str[0]: 1, pieces_str[1]: 2, pieces_str[2]: 3, pieces_str[3]: 4,
                       pieces_str[4]: 5, pieces_str[5]: 6,
                       pieces_str[6]: -1, pieces_str[7]: -2, pieces_str[8]: -3, pieces_str[9]: -4,
                       pieces_str[10]: -5, pieces_str[11]: -6}

        boardtensor = np.zeros((8, 8, 6))

        inputliste = inputstr.split()
        rownr = 0
        colnr = 0
        for i, c in enumerate(inputliste[0]):
            if c in pieces:
                boardtensor[rownr, colnr, np.abs(pieces_dict[c]) - 1] = np.sign(pieces_dict[c])
                colnr = colnr + 1
            elif c == '/':  # new row
                rownr = rownr + 1
                colnr = 0
            elif int(c) in valid_spaces:
                colnr = colnr + int(c)
            else:
                raise ValueError("invalid fenstr at index: {} char: {}".format(i, c))

        return boardtensor

    def countpieces(fen):
        boardtensor = fentotensor(fen)
        count = np.sum(np.abs(boardtensor))
        return count

    # print(countpieces(board.fen()))
    countpieces(board.fen())

    # print(fentotensor(board.fen()))

    def pawnending(fen):
        boardtensor = fentotensor(fen)
        counts_1 = np.sum(np.abs(boardtensor), axis=(0, 1))
        if counts_1[1] == 0 and counts_1[2] == 0 and counts_1[3] == 0 and counts_1[4] == 0:
            return True
        else:
            return False

    def rookending(fen):
        boardtensor = fentotensor(fen)
        counts_2 = np.sum(np.abs(boardtensor), axis=(0, 1))
        if counts_2[1] == 0 and counts_2[2] == 0 and counts_2[4] == 0 and counts_2[3] > 0:
            return True
        else:
            return False

    # Register a standard info handler.
    # info_handler = chess.uci.InfoHandler()
    # engine.info_handlers.append(info_handler)

    counts = {"movecount": [], "scores": [], "check": [], "bestdiff": [], "pawnending": [], "rookending": []}

    # Iterate through all moves and play them on a board.
    board = act_game.board()

    print('Analyzing game_in_question...')

    for move in act_game.mainline_moves():
        board.push(move)
        cnt = len([i for i in board.legal_moves])
        counts["movecount"].append(cnt)
        counts["check"].append(board.is_check())
        counts["pawnending"].append(pawnending(board.fen()))
        counts["rookending"].append(rookending(board.fen()))

        # Start a search.
        info = engine.analyse(board, chess.engine.Limit(time=0.1))
        if board.turn == chess.WHITE:
            counts["scores"].append(int(str(info["score"].white().score(mate_score=10000))) / 100)
        else:
            counts["scores"].append(int(str(info["score"].white().score(mate_score=10000))) / 100)
        nextmovescores = []

        for mov in board.legal_moves:
            board.push(mov)
            info = engine.analyse(board, chess.engine.Limit(time=0.02))
            if board.turn == chess.WHITE:
                if str(info["score"].white().score(mate_score=10000)) is not None:
                    try:
                        nextmovescores.append(int(str(info["score"].white().score(mate_score=10000))))
                    except:
                        nextmovescores.append(+99)
            elif board.turn == chess.BLACK:
                if str(info["score"].white().score(mate_score=10000)) is not None:
                    try:
                        nextmovescores.append(int(str(info["score"].white().score(mate_score=10000))))
                    except:
                        nextmovescores.append(-99)
            board.pop()

        if len(nextmovescores) > 1:
            nextmovescores.sort(reverse=True)
            counts["bestdiff"].append(nextmovescores[0] - nextmovescores[1])
        else:
            counts["bestdiff"].append(0)

    engine.quit()

    import plotly
    import plotly.graph_objs as go

    print('Creating graph...')

    # username = 'iitdanand' # Replace with YOUR USERNAME
    # api_key = 'SxRczLKT7c4RV4QStrMu' # Replace with YOUR API KEY

    # auth = HTTPBasicAuth(username, api_key)

    # py.sign_in('iitdanand', 'SxRczLKT7c4RV4QStrMu')

    # py.sign_in('PythonAPI', 'SxRczLKT7c4RV4QStrMu')

    checkcolor = ['red' if i else 'white' for i in counts["check"]]
    checknr = [i for (i, s) in enumerate(counts["check"]) if s]
    bubble = [s / 2 for s in counts["movecount"]]
    best = [np.log(s + 1) for s in counts["bestdiff"]]

    rookcolor = ['blue' if i else 'white' for i in counts["rookending"]]
    pawncolor = ['green' if i else 'white' for i in counts["pawnending"]]

    shapes = []
    lists = [checkcolor, rookcolor, pawncolor]
    for (i, list_num) in enumerate(lists):
        shapes = shapes + [
            dict(
                type='rect',
                # x-reference is assigned to the x-values
                xref='x',
                # y-reference is assigned to the plot paper [0,1]
                yref='paper',
                x0=i,
                y0=0,
                x1=i + 1,
                y1=1,
                fillcolor=s,
                opacity=0.2,
                line=dict(
                    width=0,
                )
            )
            for (i, s) in enumerate(list_num)]

    annotations = [dict(
        xref='x',
        yref='paper',
        x=s,
        y=(0.05 + i * 0.2) % 1,
        text='Check!',
        opacity=0.8,
        xanchor='left',
        showarrow=False,
        ax=20,
        ay=-30,
        font=dict(
            family='Courier New, monospace',
            size=16,
            color='red'
        ),
    )
        for (i, s) in enumerate(checknr)]

    # print(counts_1["scores"])

    trace1 = go.Scatter(
        mode='markers+lines',
        y=counts["scores"],
        name='Scores',

        line=dict(
            color='black',
            width=4,
        ),
        marker=dict(
            size=bubble,
            line=dict(color='rgb(231, 99, 250)', width=1),
            cmax=max(best),
            cmin=min(best),
            color=best,
            colorbar=dict(title='Criticality'),
            colorscale='Jet'
        )
    )

    data = [trace1]

    ht = headers["Event"] + " || " + headers["White"] + " - " + headers["Black"] + "  " + \
         headers["Result"] + " || " + headers["Date"]

    layout = dict(title=ht,
                  xaxis=dict(title='Half Move'),
                  yaxis=dict(title='Score'),
                  shapes=shapes,
                  annotations=annotations
                  )

    fig = {
        'data': data,
        'layout': layout,
    }

    # plotly.plot(fig, filename='chessviz{}'.format('New2'), kind=)
    plotly.offline.plot(fig, filename=location.format(headers["White"] + ' vs ' + headers["Black"]))
