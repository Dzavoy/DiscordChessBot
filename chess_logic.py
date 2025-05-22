from typing import Optional
import chess
import chess.engine
from chess import Board
import os
from dotenv import load_dotenv

load_dotenv()

STOCKFISH_PATH: Optional[str] = os.getenv("STOCKFISH_PATH")

def make_move(board: Board, move: str) -> Optional[str]:
    try:
        move_obj = chess.Move.from_uci(move)
        if move_obj in board.legal_moves:
            board.push(move_obj)
        else:
            return "Invalid move: Not a legal move in this position."
    except ValueError:
        return "Invalid move format: Use UCI format like 'e2e4'."

    return None

def fish_move(board: Board) -> Optional[str]:
    if STOCKFISH_PATH is None:
        return "Error: STOCKFISH_PATH is not set in environment variables."
        
    with chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH) as engine:
        result = engine.play(board, chess.engine.Limit(time=1))
        if result.move is not None:
            board.push(result.move)
            return None
        else:
            return "Stockfish did not return a move."