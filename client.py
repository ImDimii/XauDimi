import asyncio
import websockets
import hashlib
import json
import platform
import os
import sys
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from rich.text import Text
from rich import box
from rich.align import Align
from rich.theme import Theme
import pyfiglet

SERVER_URI = "ws://dimitricotilli.it:8765"
console = Console(theme=Theme({
    "menu": "bold bright_green",
    "header": "bold bright_green",
    "signal_buy": "bold bright_green",
    "signal_sell": "bold bright_red",
    "signal_hold": "bold bright_yellow",
    "signal_warm": "bold bright_cyan",
    "data": "bright_white",
    "footer": "dim bright_green"
}))

# Pre-generate Figlet ASCII art for performance
FIGLET_TITLE = pyfiglet.figlet_format("XAUDIMI", font="slant")
# Figlet title will be generated dynamically
SUBTITLE = Text("by dimi v1", style="menu", justify="center")

BORDER_STYLE = "bright_green"


def md5_hash(text: str) -> str:
    return hashlib.md5(text.encode()).hexdigest()

def get_pc_id():
    info = platform.uname()
    unique_string = info.system + info.node + info.release + info.version + info.machine
    return md5_hash(unique_string)

def print_header():
    console.clear()
    # Titolo Figlet in verde stile hacker
    console.print(Align.center(Text(FIGLET_TITLE, style="header")))
    console.print(Align.center(SUBTITLE, vertical="middle"))
    console.print(Align.center(Text(f"PC ID: {get_pc_id()}", style="footer")), justify="center")
    console.rule(style=BORDER_STYLE)

def print_data(data):
    table = Table(title="[bold bright_white]XAU/USD Live Data[/]", box=box.SIMPLE_HEAVY, style="data", width=60, border_style=BORDER_STYLE)
    table.add_column("Campo", style="bold cyan", justify="right")
    table.add_column("Valore", style="bold white", justify="left")
    table.add_row("Timestamp", str(data.get('timestamp', 'N/A')))
    table.add_row("Prezzo XAU/USD", str(data.get('price', 'N/A')))
    table.add_row("EMA(20)", str(data.get('ema20', 'N/A')))
    table.add_row("RSI(14)", str(data.get('rsi', 'N/A')))
    macd = data.get('macd')
    if macd:
        table.add_row("MACD", f"{macd[0]}")
        table.add_row("Signal Line", f"{macd[1]}")
    else:
        table.add_row("MACD", "N/A")
        table.add_row("Signal Line", "N/A")
    boll = data.get('bollinger')
    if boll:
        table.add_row("Bollinger Upper", str(boll[0]))
        table.add_row("Bollinger Lower", str(boll[1]))
    else:
        table.add_row("Bollinger Upper", "N/A")
        table.add_row("Bollinger Lower", "N/A")
    signal = data.get('signal', 'N/A')
    if signal == "Buy":
        signal_style = "signal_buy"
    elif signal == "Sell":
        signal_style = "signal_sell"
    elif signal == "Hold":
        signal_style = "signal_hold"
    else:
        signal_style = "signal_warm"
    table.add_row("Segnale", Text(signal, style=signal_style))
    console.print(table)
    console.rule(style=BORDER_STYLE)

def print_menu():
    menu_panel = Panel(
        Align.center(
            "[menu]1)[/] [bold white]Inserisci KEY e connetti\n"
            "[menu]2)[/] [bold white]Esci\n",
            vertical="middle"
        ),
        title="[menu]MENU PRINCIPALE",
        border_style="menu",
        box=box.SQUARE,
        width=40
    )
    console.print(menu_panel)

def print_message(msg, style="footer"):
    console.print(Panel(msg, style=style, width=50, border_style=BORDER_STYLE, box=box.ROUNDED))

async def receive_data(websocket):
    try:
        async for message in websocket:
            try:
                data = json.loads(message)
                print_header()
                print_data(data)
            except json.JSONDecodeError:
                print_header()
                print_message(f"Messaggio dal server: {message}", style="signal_warm")
    except websockets.ConnectionClosed:
        print_header()
        print_message("Connessione chiusa dal server.", style="signal_sell")

async def connect_and_listen(key):
    try:
        async with websockets.connect(SERVER_URI) as websocket:
            print_header()
            print_message(f"Connesso a {SERVER_URI}", style="signal_warm")
            await websocket.send(key)
            response = await websocket.recv()
            if "KEY ACCEPTED" not in response:
                print_message(f"Server: {response}", style="signal_sell")
                print_message("Chiudo connessione per key non valida.", style="signal_sell")
                await asyncio.sleep(2)
                return
            print_message(f"Server: {response}", style="signal_buy")
            await receive_data(websocket)
    except ConnectionRefusedError:
        print_message("Impossibile connettersi al server, server non attivo o non raggiungibile.", style="signal_sell")
        await asyncio.sleep(2)
    except Exception as e:
        print_message(f"Errore durante la connessione: {e}", style="signal_sell")
        await asyncio.sleep(2)

async def menu():
    while True:
        print_header()
        print_menu()
        choice = Prompt.ask("[menu]Scegli un'opzione[/]", choices=["1", "2"], default="1")
        if choice == "1":
            key = Prompt.ask("[menu]Inserisci la tua KEY[/]")
            if not key:
                print_message("KEY non valida.", style="signal_sell")
                await asyncio.sleep(1.5)
                continue
            await connect_and_listen(key)
            print_message("Premi invio per tornare al menu.", style="footer")
            input()
        elif choice == "2":
            print_message("Chiusura client. Bye!", style="footer")
            await asyncio.sleep(1)
            break

if __name__ == "__main__":
    try:
        asyncio.run(menu())
    except KeyboardInterrupt:
        console.clear()
        print_message("Client terminato manualmente.", style="signal_sell")
