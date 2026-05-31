import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parents[1]


def load_dotenv(path: Path) -> None:
    if not path.exists():
        return

    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def load_default_env_files() -> None:
    load_dotenv(ROOT_DIR / ".env")
    load_dotenv(BASE_DIR / ".env")


def build_conninfo() -> str:
    load_default_env_files()

    database_url = os.environ.get("HERMES_MEMORY_DATABASE_URL")
    if database_url:
        return database_url

    required = ["PGHOST", "PGPORT", "PGDATABASE", "PGUSER", "PGPASSWORD"]
    missing = [key for key in required if not os.environ.get(key)]
    if missing:
        raise SystemExit(
            "Missing database configuration: "
            + ", ".join(missing)
            + ". Set HERMES_MEMORY_DATABASE_URL or PG* variables."
        )

    return (
        f"host={os.environ['PGHOST']} "
        f"port={os.environ['PGPORT']} "
        f"dbname={os.environ['PGDATABASE']} "
        f"user={os.environ['PGUSER']} "
        f"password={os.environ['PGPASSWORD']}"
    )
