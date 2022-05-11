import os
from datetime import datetime


def add_entry_text(text, file, name):
    now = datetime.now()
    if os.path.exists(file):
        with open(file, 'a') as fl:
            fl.write(f"{now} -- {text} -- {name}\n\n")
    else:
        with open(file, 'x') as fl:
            fl.write(f"{now} -- {text} -- {name}\n\n")
    