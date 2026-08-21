import sqlite3
from pathlib import Path
from typing import Any


# ============================================================
# DATABASE CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATABASE_PATH = DATA_DIR / "sentinels.db"


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection() -> sqlite3.Connection:
    """
    Create and return a connection to the SQLite database.

    The database directory is created automatically.
    The database schema is also ensured before the connection
    is returned.
    """

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(
        str(DATABASE_PATH),
        check_same_thread=False,
    )

    connection.row_factory = sqlite3.Row

    # Make sure required tables exist.
    _create_tables(connection)

    return connection


# ============================================================
# CREATE DATABASE TABLES
# ============================================================

def _create_tables(connection: sqlite3.Connection) -> None:
    """
    Create all required database tables if they do not exist.
    """

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS claims (
            id TEXT PRIMARY KEY,
            claim TEXT NOT NULL,
            verification_status TEXT NOT NULL,
            confidence REAL NOT NULL,
            source TEXT,
            reasoning TEXT,
            created_at TEXT NOT NULL
        )
        """
    )

    connection.commit()


# ============================================================
# DATABASE INITIALIZATION
# ============================================================

def initialize_database() -> None:
    """
    Initialize the SQLite database and create all required tables.
    """

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(
        str(DATABASE_PATH),
        check_same_thread=False,
    )

    try:
        connection.row_factory = sqlite3.Row

        _create_tables(connection)

        # Verify that the claims table actually exists.
        table = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
              AND name = 'claims'
            """
        ).fetchone()

        if table is None:
            raise RuntimeError(
                "Database initialization failed: "
                "'claims' table was not created."
            )

    finally:
        connection.close()


# ============================================================
# INSERT CLAIM
# ============================================================

def insert_claim(
    claim_id: str,
    claim: str,
    verification_status: str,
    confidence: float,
    source: str | None,
    reasoning: str | None,
    created_at: str,
) -> None:
    """
    Insert a claim into the knowledge base.
    """

    connection = get_connection()

    try:
        connection.execute(
            """
            INSERT INTO claims (
                id,
                claim,
                verification_status,
                confidence,
                source,
                reasoning,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                claim_id,
                claim,
                verification_status,
                confidence,
                source,
                reasoning,
                created_at,
            ),
        )

        connection.commit()

    finally:
        connection.close()


# ============================================================
# GET CLAIM BY ID
# ============================================================

def get_claim(claim_id: str) -> dict[str, Any] | None:
    """
    Retrieve a claim by its ID.
    """

    connection = get_connection()

    try:
        row = connection.execute(
            """
            SELECT
                id,
                claim,
                verification_status,
                confidence,
                source,
                reasoning,
                created_at
            FROM claims
            WHERE id = ?
            """,
            (claim_id,),
        ).fetchone()

        if row is None:
            return None

        return dict(row)

    finally:
        connection.close()


# ============================================================
# GET ALL CLAIMS
# ============================================================

def get_all_claims() -> list[dict[str, Any]]:
    """
    Retrieve all claims from the knowledge base.
    """

    connection = get_connection()

    try:
        rows = connection.execute(
            """
            SELECT
                id,
                claim,
                verification_status,
                confidence,
                source,
                reasoning,
                created_at
            FROM claims
            ORDER BY created_at DESC
            """
        ).fetchall()

        return [dict(row) for row in rows]

    finally:
        connection.close()


# ============================================================
# DATABASE HEALTH CHECK
# ============================================================

def database_health_check() -> dict[str, Any]:
    """
    Verify that the database is accessible and the claims table exists.
    """

    connection = get_connection()

    try:
        table = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
              AND name = 'claims'
            """
        ).fetchone()

        claims_count = connection.execute(
            "SELECT COUNT(*) AS count FROM claims"
        ).fetchone()["count"]

        return {
            "database": "connected",
            "database_path": str(DATABASE_PATH),
            "claims_table": table is not None,
            "claims_count": claims_count,
        }

    finally:
        connection.close()


# ============================================================
# INITIALIZE DATABASE WHEN RUN DIRECTLY
# ============================================================

if __name__ == "__main__":
    initialize_database()

    print("SQLite database initialized successfully.")
    print(f"Database location: {DATABASE_PATH}")

    health = database_health_check()

    print(f"Database health: {health}")