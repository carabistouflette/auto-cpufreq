import sqlite3
import datetime
from pathlib import Path

def get_db_path():
    """Returns the path to the database file."""
    # Using ~/.config/auto-cpufreq/ as a base for user-specific data
    config_dir = Path.home() / ".config" / "auto-cpufreq"
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir / "profiler.db"

def initialize_database():
    """Initializes the database and creates the applications table if it doesn't exist."""
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            process_name TEXT PRIMARY KEY,
            total_runtime_ms INTEGER,
            high_load_runtime_ms INTEGER,
            last_accessed TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()

def update_app_stats(process_name: str, total_runtime_ms: int, high_load_runtime_ms: int):
    """
    Updates the statistics for a given application.
    If the application is not in the database, it will be inserted.
    """
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check if the process already exists
    cursor.execute("SELECT total_runtime_ms, high_load_runtime_ms FROM applications WHERE process_name = ?", (process_name,))
    result = cursor.fetchone()

    now = datetime.datetime.now()

    if result:
        # Update existing record
        new_total_runtime = result[0] + total_runtime_ms
        new_high_load_runtime = result[1] + high_load_runtime_ms
        cursor.execute("""
            UPDATE applications
            SET total_runtime_ms = ?, high_load_runtime_ms = ?, last_accessed = ?
            WHERE process_name = ?
        """, (new_total_runtime, new_high_load_runtime, now, process_name))
    else:
        # Insert new record
        cursor.execute("""
            INSERT INTO applications (process_name, total_runtime_ms, high_load_runtime_ms, last_accessed)
            VALUES (?, ?, ?, ?)
        """, (process_name, total_runtime_ms, high_load_runtime_ms, now))

    conn.commit()
    conn.close()


if __name__ == "__main__":
    initialize_database()
    print(f"Database initialized at {get_db_path()}")
