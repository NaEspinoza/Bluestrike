import random
import os

OUI_MAP = {
    "Apple":     "00:1F:7F",
    "Dell":      "00:14:5F",
    "HP":        "00:4C:6F",
    "Lenovo":    "00:50:C2",
    "Microsoft": "00:50:F2",  # was VMware's OUI by mistake
    "Samsung":   "00:1C:42",
    "Sony":      "00:0A:95",
    "Acer":      "00:26:A9",
    "Asus":      "00:19:D8",
    "Google":    "3C:5A:B4",  # was Oracle VirtualBox's OUI by mistake
    "HTC":       "00:1F:B5",
    "Intel":     "00:19:5D",
    "LG":        "00:1C:61",
    "Motorola":  "00:1F:42",
    "Toshiba":   "00:1E:67",
    "Xiaomi":    "00:26:A8",
}


def get_oui(brand):
    return OUI_MAP.get(brand)


def generate_mac_address(brand):
    oui = get_oui(brand)
    if oui is None:
        raise ValueError(f"Unknown brand: {brand}")
    last_bytes = [random.randint(0x00, 0xFF) for _ in range(3)]
    return oui + ":" + ":".join(f"{b:02x}" for b in last_bytes)


if __name__ == "__main__":
    try:
        os.system("clear||cls")
        print("-- Available Devices --")
        for i, key in enumerate(OUI_MAP, start=1):
            print(f"  {i} - {key}")
        brand = input("\nEnter the brand name of your device: ")
        print(generate_mac_address(brand))
    except (KeyboardInterrupt, ValueError) as e:
        print(f'\nAborted: {e}')
        exit()
