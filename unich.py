import aiohttp
import asyncio
import time
import sys
from datetime import datetime, timedelta, timezone
from rich.console import Console
from rich.progress import track
from rich import print as rprint
from rich.live import Live
from rich.text import Text

console = Console()

# Animated Banner Function
async def animated_banner():
    banner_lines = [
        "╔════════════════════════════════════════════════════╗",
        "║                 OYACHAT AUTO BOT                   ║",
        "║         Automate your Oyachat registration!        ║",
        "║    Developed by: https://t.me/Offical_Im_kazuha    ║",
        "║    GitHub: https://github.com/Kazuha787            ║",
        "╠════════════════════════════════════════════════════╣",
        "║                                                    ║",
        "║  ██╗  ██╗ █████╗ ███████╗██╗   ██╗██╗  ██╗ █████╗  ║",
        "║  ██║ ██╔╝██╔══██╗╚══███╔╝██║   ██║██║  ██║██╔══██╗ ║",
        "║  █████╔╝ ███████║  ███╔╝ ██║   ██║███████║███████║ ║",
        "║  ██╔═██╗ ██╔══██║ ███╔╝  ██║   ██║██╔══██║██╔══██║ ║",
        "║  ██║  ██╗██║  ██║███████╗╚██████╔╝██║  ██║██║  ██║ ║",
        "║  ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝ ║",
        "║                                                    ║",
        "╚════════════════════════════════════════════════════╝",
    ]
    
    console.clear()  # Clear screen before printing banner
    for line in banner_lines:
        rprint(f"[bold cyan]{line}[/bold cyan]")
        await asyncio.sleep(0.1)  # Animation delay

# API endpoint
API_URL = "https://api.unich.com/airdrop/user/v1/mining/start"

# Read auth tokens from file
def load_auth_tokens(filename="auth.txt"):
    try:
        with open(filename, "r") as file:
            tokens = [line.strip() for line in file if line.strip()]
        return tokens
    except FileNotFoundError:
        rprint("[bold red]❌ Error: auth.txt not found.[/bold red]")
        return []

# Function to simulate loading animation
def loading_animation(text):
    for _ in track(range(10), description=text):
        time.sleep(0.1)

async def start_mining(session, token):
    headers = {
        "accept": "application/json, text/plain, */*",
        "authorization": f"Bearer {token}",
        "origin": "https://unich.com",
        "referer": "https://unich.com/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0"
    }
    try:
        async with session.post(API_URL, headers=headers) as response:
            result = await response.text()
            rprint(f"🔹 [bold green]Token: {token[:10]}... Response: {result}[/bold green] ✅")
    except Exception as e:
        rprint(f"❌ [bold red]Error with token {token[:10]}: {e}[/bold red]")

async def run_bot():
    await animated_banner()
    loading_animation("🚀 Starting Unich Mining Bot...")

    tokens = load_auth_tokens()
    if not tokens:
        rprint("[bold red]⚠️ No auth tokens found. Exiting...[/bold red]")
        return

    rprint(f"📌 [bold cyan]Total auth tokens loaded: {len(tokens)}[/bold cyan]")

    async with aiohttp.ClientSession() as session:
        tasks = [start_mining(session, token) for token in tokens]
        await asyncio.gather(*tasks)

async def countdown_timer(time_remaining):
    with Live(auto_refresh=False) as live:
        while time_remaining > 0:
            hours, remainder = divmod(time_remaining, 3600)
            minutes, seconds = divmod(remainder, 60)
            countdown_text = Text(f"⏳ Next run in: {int(hours):02d}:{int(minutes):02d}:{int(seconds):02d} ⏰", style="bold yellow")
            live.update(countdown_text, refresh=True)
            await asyncio.sleep(1)
            time_remaining -= 1

async def wait_until_next_run():
    now = datetime.now(timezone.utc)
    next_run_time = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)

    if now >= next_run_time:
        next_run_time += timedelta(days=1)

    time_remaining = int((next_run_time - now).total_seconds())

    rprint(f"\n⏳ [bold yellow]Next run scheduled at: {next_run_time.strftime('%Y-%m-%d %H:%M:%S UTC')}[/bold yellow] ⏰\n")

    await countdown_timer(time_remaining)

async def main():
    while True:
        await run_bot()
        await wait_until_next_run()

if __name__ == "__main__":
    asyncio.run(main())
