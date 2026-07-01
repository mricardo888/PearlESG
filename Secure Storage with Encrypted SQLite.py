import sqlcipher3

def init_encrypted_db(db_path="secure_data.db", key: bytes):
    conn = sqlcipher3.connect(db_path)
    conn.execute(f"PRAGMA key='{key.decode()}';")  # Use derived key
    # Create tables for inputs and results
    conn.execute('''CREATE TABLE IF NOT EXISTS inputs 
                    (id INTEGER PRIMARY KEY, encrypted_data BLOB)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS results 
                    (id INTEGER PRIMARY KEY, encrypted_report BLOB)''')
    conn.commit()
    return conn