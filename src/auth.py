from src.database import get_connection

def register_user(username, password, age, height, weight):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        INSERT INTO users (username, password, age, height, weight)
        VALUES (?, ?, ?, ?, ?)
        """, (username, password, age, height, weight))

        conn.commit()
        return True

    except:
        return False

    finally:
        conn.close()


def login_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM users WHERE username = ? AND password = ?
    """, (username, password))

    user = cursor.fetchone()
    conn.close()

    return user