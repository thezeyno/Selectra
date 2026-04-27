from src.database import get_connection

def save_decision(user_id, category, option1, option2, chosen, score):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO decisions (user_id, category, option1, option2, chosen, score)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, category, option1, option2, chosen, score))

    conn.commit()
    conn.close()

def get_user_history(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT category, option1, option2, chosen, score, created_at
    FROM decisions
    WHERE user_id = ?
    ORDER BY created_at DESC
    """, (user_id,))

    data = cursor.fetchall()
    conn.close()
    return data