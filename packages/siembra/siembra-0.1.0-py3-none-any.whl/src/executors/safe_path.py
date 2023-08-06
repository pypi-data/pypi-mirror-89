from pathlib import Path


def safe_path(base, path):
    base = Path(base).resolve()
    absolute = Path(base).joinpath(path).resolve()
    absolute.relative_to(Path(base).resolve())
    return absolute
