from src.preferences import get_preferences

def calculate_score(option, preferences):
    score = 0
    reasons = []

    if not preferences:
        return 0, ["Kullanıcı tercihleri bulunamadı."]

    favorite_colors = preferences[2].split(",") if preferences[2] else []
    disliked_colors = preferences[3].split(",") if preferences[3] else []
    favorite_styles = preferences[4].split(",") if preferences[4] else []
    budget_min = preferences[5] if preferences[5] is not None else 0
    budget_max = preferences[6] if preferences[6] is not None else 999999

    # Renk puanı
    if option["color"] in favorite_colors:
        score += 20
        reasons.append(f"{option['color']} sevdiğin renklerden biri (+20)")

    if option["color"] in disliked_colors:
        score -= 15
        reasons.append(f"{option['color']} sevmediğin renklerden biri (-15)")

    # Stil puanı
    if option["style"] in favorite_styles:
        score += 20
        reasons.append(f"{option['style']} tarzına uygun (+20)")

    # Bütçe puanı
    if budget_min <= option["price"] <= budget_max:
        score += 25
        reasons.append("Bütçene uygun (+25)")
    else:
        score -= 10
        reasons.append("Bütçe aralığının dışında (-10)")

    return score, reasons


def choose_best_option(options, preferences):
    results = []

    for option in options:
        score, reasons = calculate_score(option, preferences)
        option["score"] = score
        option["reasons"] = reasons
        results.append(option)

    best_option = max(results, key=lambda x: x["score"])
    return best_option, results