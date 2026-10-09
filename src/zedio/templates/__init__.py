from importlib.resources import files
from pathlib import Path

PROJECT_TEMPLATES_PATH = files("zedio") / "templates" / "project"
COMPILATIONDB_TOOLCHAIN_SCRIPT = Path("scripts") / "compilationdb_toolchain.py"
TEMPLATE_SUFFIX = ".template"