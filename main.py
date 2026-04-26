import time
import os
import asyncio

from utils.logo import print_logo
from utils.kick import _kick_, deauth_Method_1
from utils.scanner import main as scan_main

from rich import print
from rich.prompt import Prompt
from rich.console import Console

console = Console()

modules = """[bright_white] [1] :mag: Scan for Bluetooth Devices
 [2] :satellite: Kick Out Bluetooth Devices
[red] [Q] :door: Exit (Ctrl + c)
"""


def Main_Modules():
    while True:
        print_logo()
        print(modules)
        user_choice = Prompt.ask("[cyan] :question: Enter your choice")

        if user_choice == "1":
            raw = Prompt.ask("[cyan] :clock1: Scan duration in seconds", default="10")
            try:
                scan_time = max(5, int(raw))
            except ValueError:
                scan_time = 10

            while True:
                mac_address = asyncio.run(scan_main(timeout=scan_time))
                if mac_address is None:
                    break
                print("Selected MAC address:", mac_address)
                scan_again = Prompt.ask("[green] :question: Scan again? (y/n)").lower() == "y"
                if not scan_again:
                    break

            if mac_address is None:
                continue

            kick_ard = Prompt.ask("[red] :rocket: Do you want to kick the user? (y/n)").lower() == "y"
            if kick_ard:
                start_time = Prompt.ask("[red] :question: In how many seconds do you want to start the attack")
                _kick_(deauth_Method_1, mac_address, 600, 10, int(start_time))
            else:
                print(":door: Exiting...")

        elif user_choice == "2":
            mac_address = Prompt.ask("[red] :signal_strength: Enter the Mac Address")
            start_time = Prompt.ask("[red] :question: In how many seconds do you want to start the attack")
            _kick_(deauth_Method_1, mac_address, 600, 10, int(start_time))

        elif user_choice.lower() == "q":
            console.clear()
            break

        else:
            print("[red] :warning: Invalid Option")
            time.sleep(1)


if __name__ == "__main__":
    try:
        os.system("rfkill unblock bluetooth")
        Main_Modules()
    except KeyboardInterrupt:
        console.clear()
        print("[red] :door: User Quit")
        exit()
    except Exception as e:
        console.clear()
        print(f"[red] :warning: ERROR VALUE [{e}]")
        exit()
