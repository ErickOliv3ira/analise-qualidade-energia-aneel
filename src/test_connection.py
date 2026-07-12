"""Valida a conexao com o PostgreSQL e a existencia dos schemas do projeto."""
from __future__ import annotations

import logging
import os
import sys

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

EXPECTED_SCHEMAS = {"raw", "staging", "dw"}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger("test_connection")


def build_url() -> str:
    load_dotenv()
    user = os.environ["POSTGRES_USER"]
    password = os.environ["POSTGRES_PASSWORD"]
    host = os.environ["POSTGRES_HOST"]
    port = os.environ["POSTGRES_PORT"]
    db = os.environ["POSTGRES_DB"]
    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"


def main() -> int:
    engine = create_engine(build_url())
    with engine.connect() as conn:
        version = conn.execute(text("SELECT version()")).scalar_one()
        log.info("Conectado: %s", version)

        rows = conn.execute(
            text(
                "SELECT schema_name FROM information_schema.schemata "
                "WHERE schema_name = ANY(:names)"
            ),
            {"names": list(EXPECTED_SCHEMAS)},
        ).all()
        found = {r[0] for r in rows}

    missing = EXPECTED_SCHEMAS - found
    if missing:
        log.error("Schemas ausentes: %s", sorted(missing))
        return 1
    log.info("Schemas OK: %s", sorted(found))
    return 0


if __name__ == "__main__":
    sys.exit(main())
