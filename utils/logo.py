import fade
from rich.console import Console

_LOGO_ = r"""

 ______             ______
|  _ \ \            \  ___)
| |_) ) \  _   _ ___ \ \ ___  ___  _  _  _____
|  _ ( > \| | | / __) > >   )/ _ \| || |/ / __)
| |_) ) ^ \ |_| > _) / /_| || |_) ) ||   <> _)
|____/_/ \_\___/\___)_____)_)  __/ \_)_|\_\___)
                            | |
                            |_|   - By StealthIQ
"""


def print_logo():
    Console().clear()
    print(fade.water(_LOGO_))


if __name__ == "__main__":
    print_logo()
