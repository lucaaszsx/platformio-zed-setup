from importlib.resources import files
from pathlib import Path
from typing import NamedTuple


class Template(NamedTuple):
    src: str
    dest: str


TEMPLATE_MAP: dict[str, Template] = {
    "compiledbtc": Template("compiledbtc.py.template", "scripts/compiledbtc.py"),
    "readme": Template("readme.md.template", "README.md"),
    "gitignore": Template(".gitignore.template", ".gitignore"),
    "clangd": Template(".clangd.template", ".clangd"),
}


def template_src_path(key: str) -> Path:
    return Path(str(files("zedio") / "templates" / TEMPLATE_MAP[key].src))


def template_dest_path(key: str, project: Path) -> Path:
    return project / TEMPLATE_MAP[key].dest
