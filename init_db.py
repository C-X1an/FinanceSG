"""Create an empty local SQLite database; never overwrite an existing file."""
import argparse
import os
import sqlite3
from contextlib import closing
from pathlib import Path


def initialize_database(path):
    path = Path(path)
    descriptor = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    os.close(descriptor)
    try:
        with closing(sqlite3.connect(path)) as connection:
            with connection:
                connection.executescript(Path(__file__).with_name("schema.sql").read_text())
    except Exception:
        path.unlink()  # Only the newly created file can reach this branch.
        raise
    return path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", default="financesg.db")
    args = parser.parse_args()
    print("Created empty database:", initialize_database(args.database))
