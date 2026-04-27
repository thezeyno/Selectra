from src.database import get_connection

def save_preferences(user_id, fav_colors, disliked_colors, styles, budget_min, budget_max):
    conn = get_connection()
    cursor = conn.cursor()

    # Önce varsa eski kaydı sil (tek kayıt tutacağız)
    cursor.execute("DELETE FROM preferences WHERE user_id = ?", (user_id,))

    cursor.execute("""
    INSERT INTO preferences (user_id, favorite_colors, disliked_colors, favorite_styles, budget_min, budget_max)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        ",".join(fav_colors),
        ",".join(disliked_colors),
        ",".join(styles),
        budget_min,
        budget_max
    ))

    conn.commit()
    conn.close()


def get_preferences(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM preferences WHERE user_id = ?", (user_id,))
    data = cursor.fetchone()

    conn.close()

    return data