import asyncio
from bleak import BleakScanner
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.prompt import Prompt

console = Console()
DEFAULT_TIMEOUT = 10


async def _scan_classic(timeout: int) -> list[dict]:
    """Classic Bluetooth (BR/EDR) inquiry via hcitool scan --flush."""
    try:
        proc = await asyncio.create_subprocess_exec(
            'hcitool', 'scan', '--flush',
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.DEVNULL,
        )
        try:
            stdout, _ = await asyncio.wait_for(proc.communicate(), timeout=timeout + 5)
        except asyncio.TimeoutError:
            proc.kill()
            await proc.communicate()
            return []

        devices = []
        for line in stdout.decode().splitlines():
            line = line.strip()
            if not line or line.startswith('Scanning'):
                continue
            parts = line.split('\t')
            if len(parts) >= 1 and ':' in parts[0]:
                devices.append({
                    'address': parts[0],
                    'name': parts[1] if len(parts) > 1 else 'Unknown',
                    'rssi': None,
                    'type': 'Classic',
                })
        return devices
    except FileNotFoundError:
        console.print("[yellow]:warning:  hcitool not found — Classic scan skipped[/yellow]")
        return []


def _build_table(devices: dict, remaining: int) -> Table:
    if remaining > 0:
        title = f"[bold]Scanning... {remaining}s remaining[/bold]  ({len(devices)} found)"
    else:
        title = f"[bold green]Scan complete[/bold green]  —  {len(devices)} device(s) found"

    table = Table(title=title, border_style="bright_blue", show_lines=True)
    table.add_column("#",           justify="right",  style="cyan",    width=3)
    table.add_column("Type",        justify="center",                   width=9)
    table.add_column("Name",        style="magenta",  min_width=20)
    table.add_column("MAC Address", style="green",                      width=19)
    table.add_column("RSSI",        justify="right",  style="yellow",  width=9)

    for i, dev in enumerate(devices.values(), 1):
        type_fmt = "[bright_cyan]BLE[/bright_cyan]" if dev['type'] == 'BLE' else "[bright_red]Classic[/bright_red]"
        rssi_fmt = f"{dev['rssi']} dBm" if dev['rssi'] is not None else "—"
        table.add_row(str(i), type_fmt, dev['name'], dev['address'], rssi_fmt)

    return table


async def main(timeout: int = DEFAULT_TIMEOUT) -> str | None:
    all_devices: dict = {}
    remaining = timeout

    with Live(_build_table(all_devices, remaining), console=console, refresh_per_second=4) as live:

        async def countdown():
            nonlocal remaining
            for _ in range(timeout):
                await asyncio.sleep(1)
                remaining -= 1
                live.update(_build_table(all_devices, remaining))

        async def ble_scan():
            def on_device(device, adv):
                all_devices[device.address] = {
                    'address': device.address,
                    'name': device.name or adv.local_name or 'Unknown',
                    'rssi': adv.rssi,
                    'type': 'BLE',
                }
                live.update(_build_table(all_devices, remaining))

            async with BleakScanner(detection_callback=on_device):
                await asyncio.sleep(timeout)

        async def classic_scan():
            devs = await _scan_classic(timeout)
            for d in devs:
                # BLE entry takes priority if the same MAC was already found via BLE
                all_devices.setdefault(d['address'], d)
            live.update(_build_table(all_devices, remaining))

        await asyncio.gather(countdown(), ble_scan(), classic_scan())

    if not all_devices:
        console.print("[red]:warning:  No Bluetooth devices found.[/red]")
        return None

    return _select_device(list(all_devices.values()))


def _select_device(devices: list) -> str:
    while True:
        sel = Prompt.ask("[cyan]Select device number")
        try:
            idx = int(sel) - 1
            if 0 <= idx < len(devices):
                return devices[idx]['address']
        except ValueError:
            pass
        console.print("[red]Invalid selection, try again.[/red]")


if __name__ == "__main__":
    asyncio.run(main())
