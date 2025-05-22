import chess
from chess import Board, Square, Piece
from typing import Optional

class BoardFormat:
    def __init__(self) -> None:
        self.squares: dict[str, str] = {
            "bbg": "<:bbg:1374821919987339426>",
            "wbg": "<:wbg:1374822188699353192>",
        }

        self.border: dict[str, str] = {
            "wA": "<:wA:1374822621299998893>",
            "wB": "<:wB:1374822648135024792>",
            "wC": "<:wC:1374822667466571928>",
            "wD": "<:wD:1374822679445639268>",
            "wE": "<:wE:1374822695358824518>",
            "wF": "<:wF:1374822710844199035>",
            "wG": "<:wG:1374822727495581809>",
            "wH": "<:wH:1374822746067964107>",
            "w1": "<:w1:1374822398158831797>",
            "w2": "<:w2:1374822410817241369>",
            "w3": "<:w3:1374822421500264640>",
            "w4": "<:w4:1374822432917032980>",
            "w5": "<:w5:1374822463149441177>",
            "w6": "<:w6:1374822474180595823>",
            "w7": "<:w7:1374822537468579890>",
            "w8": "<:w8:1374822606628454410>",
            "wsb": "<:wsb:1374822763843293224>"
        }

        self.pieces: dict[str, dict[str, str]] = {
            "black": {
                "bpawnbbg": "<:bpawnbbg:1374822044612431993>",
                "bpawnwbg": "<:bpawnwbg:1374822056604205116>",

                "brookbbg": "<:brookbbg:1374822105874694174>",
                "brookwbg": "<:brookwbg:1374822116842668063>",

                "bknightbbg": "<:bknightbbg:1374822017756303512>",
                "bknightwbg": "<:bknightwbg:1374822031438118993>",

                "bbishopbbg": "<:bbishopbbg:1374821947548110958>",
                "bbishopwbg": "<:bbishopwbg:1374821962031042622>",

                "bqueenbbg": "<:bqueenbbg:1374822070478704640>",
                "bqueenwbg": "<:bqueenwbg:1374822081555988634>",

                "bkingbbg": "<:bkingbbg:1374821981672837180>",
                "bkingwbg": "<:bkingwbg:1374821995153199307>"
            },

            "white": {
                "wpawnbbg": "<:wpawnbbg:1374822300523823347>",
                "wpawnwbg": "<:wpawnwbg:1374822315342434465>",

                "wrookbbg": "<:wrookbbg:1374822371046719605>",
                "wrookwbg": "<:wrookwbg:1374822384200192060>",

                "wknightbbg": "<:wknightbbg:1374822268433334383>",
                "wknightwbg": "<:wknightwbg:1374822281305653509>",

                "wbishopbbg": "<:wbishopbbg:1374822206005182534>",
                "wbishopwbg": "<:wbishopwbg:1374822218646683779>",

                "wqueenbbg": "<:wqueenbbg:1374822331545030807>",
                "wqueenwbg": "<:wqueenwbg:1374822343423164618>",

                "wkingbbg": "<:wkingbbg:1374822236636184646>",
                "wkingwbg": "<:wkingwbg:1374822253472256100>"
            }
        }

    def format_chess(self, board: Board) -> str:
        lines: list[str] = []

        symbol_to_name: dict[str, str] = {
            'p': 'pawn',
            'r': 'rook',
            'n': 'knight',
            'b': 'bishop',
            'q': 'queen',
            'k': 'king'
        }

        for rank in range(7, -1, -1):
            row: list[str] = [self.border[f"w{rank + 1}"]]
            for file in range(8):
                square: Square = chess.square(file, rank)
                piece: Optional[Piece] = board.piece_at(square)
                is_light_square: bool = (rank + file) % 2 == 1
                square_color: str = "wbg" if is_light_square else "bbg"

                if piece:
                    color: str = "white" if piece.color == chess.WHITE else "black"
                    symbol: str = piece.symbol().lower()
                    piece_name: str = symbol_to_name[symbol]
                    piece_key: str = f"{color[0]}{piece_name}{square_color}"
                    emoji: str = self.pieces[color].get(piece_key, self.squares[square_color])
                else:
                    emoji = self.squares[square_color]

                row.append(emoji)
            lines.append(" ".join(row))

        bottom: list[str] = [self.border["wsb"]]
        for file in range(8):
            col_letter: str = chr(ord('A') + file)
            bottom.append(self.border[f"w{col_letter}"])
        lines.append(" ".join(bottom))

        return "\n".join(lines)