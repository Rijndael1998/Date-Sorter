from sys import argv
import re
from pathlib import Path

compiled_regex = re.compile(r"(\d{8}|\d{6}|\d{4}-\d{2}-\d{2})")

def sanity(d: Path):
    return not ("..." in d.name)

def transform_filename(path: Path):
    d = path.name

    if not sanity(path):
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

def exif_transform(path: Path):
    new_d = transform_filename(path)
    if new_d.name != path.name:
        return new_d
    
    # do exif magic here
    return path

def init(d):
    path = Path(d)
    path.resolve()

    if not sanity(path):
        return d
    
    return exif_transform(path)

print(f'{init(argv[1])}')

