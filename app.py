import streamlit as st
from src.database import create_tables
from src.auth import register_user, login_user
from src.preferences import save_preferences, get_preferences
from src.decision_engine import choose_best_option
from src.history import save_decision, get_user_history

st.set_page_config(page_title="Selectra", layout="wide")

COLORS = [
    "Siyah", "Beyaz", "Kırmızı", "Mavi", "Yeşil", "Bej",
    "Lacivert", "Bordo", "Gri", "Kahverengi", "Turuncu",
    "Mor", "Pembe", "Sarı", "Krem", "Mint", "Lila"
]

STYLES = ["Oversize", "Basic", "Spor", "Klasik"]

create_tables()

if "user" not in st.session_state:
    st.session_state.user = None

st.title("✨ Selectra")

if st.session_state.user:
    st.success(f"Hoş geldin {st.session_state.user[1]}!")

    st.markdown("---")
    st.subheader("🎯 Ana Panel")
    st.write("Artık karar vermeye başlayabilirsin 😄")

    if st.button("Çıkış Yap"):
        st.session_state.user = None
        st.rerun()

    st.markdown("---")
    st.subheader("🎨 Tercihlerini Belirle")

    fav_colors = st.multiselect("Sevdiğin renkler", COLORS)
    disliked_colors = st.multiselect("Sevmediğin renkler", COLORS)
    styles = st.multiselect("Tarzın", STYLES)

    budget_min = st.number_input("Minimum bütçe", min_value=0, step=10)
    budget_max = st.number_input("Maximum bütçe", min_value=0, step=10)

    if st.button("💾 Tercihleri Kaydet"):
        save_preferences(
            st.session_state.user[0],
            fav_colors,
            disliked_colors,
            styles,
            budget_min,
            budget_max
        )
        st.success("Tercihler kaydedildi!")

    st.markdown("---")
    st.subheader("🧠 Karar Ver")

    category = st.selectbox(
        "Kategori seç",
        ["Clothing"]
    )

    st.write("### 1. Seçenek")
    option1_name = st.text_input("1. seçenek adı")
    option1_color = st.selectbox("1. seçenek rengi", COLORS, key="opt1_color")
    option1_style = st.selectbox("1. seçenek tarzı", STYLES, key="opt1_style")
    option1_price = st.number_input("1. seçenek fiyatı", min_value=0, step=10, key="opt1_price")

    st.write("### 2. Seçenek")
    option2_name = st.text_input("2. seçenek adı")
    option2_color = st.selectbox("2. seçenek rengi", COLORS, key="opt2_color")
    option2_style = st.selectbox("2. seçenek tarzı", STYLES, key="opt2_style")
    option2_price = st.number_input("2. seçenek fiyatı", min_value=0, step=10, key="opt2_price")

    st.write("### 3. Seçenek")
    option3_name = st.text_input("3. seçenek adı")
    option3_color = st.selectbox("3. seçenek rengi", COLORS, key="opt3_color")
    option3_style = st.selectbox("3. seçenek tarzı", STYLES, key="opt3_style")
    option3_price = st.number_input("3. seçenek fiyatı", min_value=0, step=10, key="opt3_price")

    if st.button("✨ En iyi seçeneği öner"):
        preferences = get_preferences(st.session_state.user[0])

        options = [
            {
             "name": option1_name,
             "color": option1_color,
             "style": option1_style,
             "price": option1_price
            },
            {
             "name": option2_name,
             "color": option2_color,
             "style": option2_style,
             "price": option2_price
            },
            {
             "name": option3_name,
             "color": option3_color,
             "style": option3_style,
             "price": option3_price
          }
        ]
        best_option, results = choose_best_option(options, preferences)

        st.success(f"Önerilen seçenek: {best_option['name']}")
        st.write(f"Toplam puan: {best_option['score']}")

        st.write("### Neden bu seçenek?")
        for reason in best_option["reasons"]:
            st.write(f"- {reason}")

        st.write("### Tüm seçeneklerin puanları")

        for item in results:
            stars = "⭐" * max(1, item["score"] // 20)
            st.write(f"**{item['name']}** → {stars} ({item['score']} puan)")

        save_decision(
            st.session_state.user[0],
            category,
            option1_name,
            option2_name,
            best_option["name"],
            best_option["score"]
        )

    st.markdown("---")
    st.subheader("📜 Geçmiş Kararlarım")

    history = get_user_history(st.session_state.user[0])

    if history:
        for item in history:
            st.write(f"📌 {item[0]} | {item[1]} vs {item[2]}")
            st.write(f"✅ Seçilen: {item[3]} ({item[4]} puan)")
            st.write(f"🕒 {item[5]}")
            st.markdown("---")
    else:
        st.info("Henüz kayıtlı karar yok.")

else:
    menu = st.sidebar.selectbox("Menü", ["Giriş Yap", "Kayıt Ol"])

    if menu == "Kayıt Ol":
        st.subheader("Yeni Hesap Oluştur")

        username = st.text_input("Kullanıcı adı")
        password = st.text_input("Şifre", type="password")
        age = st.number_input("Yaş", min_value=10, max_value=100, step=1)
        height = st.number_input("Boy (cm)", min_value=100, max_value=250, value=170, step=1)
        weight = st.number_input("Kilo (kg)", min_value=30, max_value=200, value=60, step=1)

        if st.button("Kayıt Ol"):
            success = register_user(username, password, age, height, weight)

            if success:
                st.success("Kayıt başarılı!")
            else:
                st.error("Bu kullanıcı adı zaten var!")

    elif menu == "Giriş Yap":
        st.subheader("Giriş Yap")

        username = st.text_input("Kullanıcı adı")
        password = st.text_input("Şifre", type="password")

        if st.button("Giriş Yap"):
            user = login_user(username, password)

            if user:
                st.session_state.user = user
                st.rerun()
            else:
                st.error("Hatalı giriş!")