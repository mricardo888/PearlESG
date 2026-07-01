import sqlcipher3
from security_keys import get_or_create_master_key
from security_crypto import encrypt_data, decrypt_data

DB_PATH = "secure_scope3_data.db"

def init_encrypted_db() -> sqlcipher3.Connection:
    """Initialize encrypted SQLite database."""
    key = get_or_create_master_key()
    conn = sqlcipher3.connect(DB_PATH)
    conn.execute(f"PRAGMA key='{key.decode()}';")
    
    # Create tables
    conn.execute('''
        CREATE TABLE IF NOT EXISTS inputs (
            id INTEGER PRIMARY KEY,
            category TEXT,
            encrypted_data BLOB,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY,
            report_type TEXT,
            encrypted_report BLOB,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    return conn

def save_input(conn, category: str, data: str, key: bytes):
    """Save encrypted input data."""
    encrypted = encrypt_data(data, key)
    conn.execute("INSERT INTO inputs (category, encrypted_data) VALUES (?, ?)",
                 (category, encrypted))
    conn.commit()

def save_result(conn, report_type: str, report: str, key: bytes):
    """Save encrypted calculation result."""
    encrypted = encrypt_data(report, key)
    conn.execute("INSERT INTO results (report_type, encrypted_report) VALUES (?, ?)",
                 (report_type, encrypted))
    conn.commit()

def get_all_inputs(conn, key: bytes) -> list:
    """Retrieve and decrypt all inputs (for calculation use)."""
    cursor = conn.execute("SELECT category, encrypted_data FROM inputs")
    return [(row[0], decrypt_data(row[1], key)) for row in cursor.fetchall()]