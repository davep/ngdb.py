from pathlib import Path
from time import perf_counter

from ngdb import NortonGuide


def read_whole_guide(test_guide: Path) -> None:
    guide = NortonGuide(test_guide)
    for entry in guide:
        _ = len(entry)


if __name__ == "__main__":
    start_point = perf_counter()
    read_whole_guide(Path("~/Documents/Norton Guides/rbint.ng").expanduser())
    execution_time = perf_counter() - start_point
    print(f"{execution_time:.4}")
