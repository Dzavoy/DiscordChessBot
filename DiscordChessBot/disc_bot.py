from typing import Optional, List
import discord
from discord.ext import commands
from discord import Message
import asyncio
import chess
from chess import Board
import chess_logic
from chess_format import BoardFormat
import os
import sys
from dotenv import load_dotenv

load_dotenv()

board: Board = chess.Board()
formatter: BoardFormat = BoardFormat()
last_board_messages: List[discord.Message] = []

intents: discord.Intents = discord.Intents.default()
intents.message_content = True

bot: commands.Bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready() -> None:
    print(f"Logged in as {bot.user}")

@bot.command()
async def new_game(ctx: commands.Context) -> None:
    global board, last_board_messages
    board.reset()
    lines: list[str] = formatter.format_chess(board).split("\n")

    for msg in last_board_messages:
        try:
            await msg.delete()  
        except Exception:
            pass

    last_board_messages = []
    for line in lines:
        msg = await ctx.send(line)
        last_board_messages.append(msg)
        await asyncio.sleep(0.4)

@bot.command()
async def move(ctx: commands.Context, move: str) -> None:
    global last_board_messages

    error: Optional[str] = chess_logic.make_move(board, move)
    if error:
        await ctx.send(error)
        return

    new_lines: list[str] = formatter.format_chess(board).split("\n")

    for i, new_line in enumerate(new_lines):
        if i >= len(last_board_messages):
            msg: Message = await ctx.send(new_line)
            last_board_messages.append(msg)
        else:
            old_msg: Message = last_board_messages[i]
            if old_msg.content != new_line:
                await old_msg.edit(content=new_line)

    error = chess_logic.fish_move(board)
    if error:
        await ctx.send(error)
        return

    new_lines = formatter.format_chess(board).split("\n")
    for i, new_line in enumerate(new_lines):
        if i >= len(last_board_messages):
            msg = await ctx.send(new_line)
            last_board_messages.append(msg)
        else:
            old_msg = last_board_messages[i]
            if old_msg.content != new_line:
                await old_msg.edit(content=new_line)

def main() -> None:
    token: Optional[str] = os.getenv("DISCORD_TOKEN")
    if token is None:
        print("Error: DISCORD_TOKEN is not set in environment variables.")
        sys.exit(1)
    bot.run(token)

if __name__ == "__main__":
    main()