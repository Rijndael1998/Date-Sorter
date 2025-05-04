from sys import argv
import re
from pathlib import Path

compiled_regex = re.compile(r"(\d{8}|\d{6}|\d{4}-\d{2}-\d{2})")

def transform_filename(d):
    path = Path(d)
    path.resolve()
    # print(path.absolute())
    d = path.name

    if "..." in d:
        return path.resolve().absolute()

    match = compiled_regex.search(d)
    if match is None:
        return path.resolve().absolute()

    comp = match.group(1)

    date = ""
    length = len(comp)

    if length == 6:
        date = f"20{comp[0:2]}-{comp[2:4]}-{comp[4:6]}"

    elif length == 8:
        date = f"{comp[0:4]}-{comp[4:6]}-{comp[6:8]}"

    elif length == 10:
        date = comp

    else:
        return path.resolve().absolute()
    
    # check for year sanity
    year = int(date[0:4])
    if year > 2030 or year < 2000:
        return path.resolve().absolute()

    return (path.parent.resolve().absolute() / f"{date}...{d}").absolute()

print(f'{transform_filename(argv[1])}')

