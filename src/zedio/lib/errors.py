from pathlib import Path


class PioError(Exception):
    pass

class PioProjectNotFoundError(PioError):
    def __init__(self, cwd: Path):
        super().__init__(f"'platformio.ini' not found on current working directory ({cwd})")
