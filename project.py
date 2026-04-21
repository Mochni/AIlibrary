import streamlit as st
import requests

API_KEY = st.secrets["MY_API_KEY"]

def get_ai_recommendation(item_type, genre, author, character, length, mood, extra):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://streamlit.io",
        "X-Title": "Book Advisor"
    }
    
    # Оставил только одну модель
    models_to_try = [
        "openai/gpt-oss-120b:free"
    ]
    
    # Скорректировал инструкцию, чтобы меньше галлюцинировала
    system_instruction = f"Ты — эксперт по {item_type}ам. Советуй только реально существующие произведения. Не выдумывай персонажей и сюжеты. Если не уверен — не пиши херни. Посоветуй 3 годноты на русском."
    user_query = f"Жанр: {genre}. Тема: {character}. Автор: {author}. Настроение: {mood}. {extra}"
    
    for model_id in models_to_try:
        data = {
            "model": model_id, 
            "messages": [
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": user_query}
            ],
            "temperature": 0.3  # Снижаем креативность для точности
        }
        try:
            response = requests.post(url, headers=headers, json=data, timeout=30)
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
        except:
            continue
    return "Слушай, сервера перегружены. Попробуй еще раз, или проверь MY_API_KEY в Secrets."

st.set_page_config(page_title="Book Advisor", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #1e1e1e; color: #d1d1d1; }
    .main-title {
        color: #ffffff; font-size: 26px; font-weight: 600;
        border-left: 4px solid #4a90e2; padding-left: 15px; margin-bottom: 25px;
    }
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stTextArea>div>div>textarea {
        background-color: #2d2d2d !important; color: #ffffff !important; border: 1px solid #3d3d3d !important;
    }
    label, p { color: #bbbbbb !important; }
    .stButton>button {
        background-color: #4a90e2; color: white; border: none; border-radius: 4px;
        height: 45px; transition: 0.3s; font-weight: 500; width: 100%;
    }
    .stButton>button:hover { background-color: #357abd; }
    .result-area {
        background-color: #252525; padding: 20px; border-radius: 8px;
        border: 1px solid #333; margin-top: 20px; color: white;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<div class='main-title'>Система подбора литературы</div>", unsafe_allow_html=True)

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        f_type = st.radio("Материал", ["Книга", "Комикс"], horizontal=True)
        f_genre = st.selectbox("Жанр", [
            "Киберпанк", "Научная фантастика", "Постапокалипсис", "Антиутопия", "Космоопера", 
            "Темное фэнтези", "Героическое фэнтези", "Городское фэнтези", "Славянское фэнтези",
            "Нуар", "Психологический триллер", "Классический детектив", "Боевик",
            "Хоррор", "Мистика", "Лавкрафтовские ужасы",
            "Магический реализм", "Исторический роман", "Сатира", "Биография", "Супергероика", "Исторический детектив", "Любовный роман"
        ])
        f_author = st.text_input("Автор (необязательно)")
    with col2:
        f_char = st.text_input("Персонаж / Тема (необязательно)")
        f_len = st.select_slider("Объем", options=["Короткий", "Средний", "Большой"])
        f_mood = st.select_slider("Настроение", options=["Мрачное", "Нейтральное", "Бодрое"])
    
    f_extra = st.text_area("Особые пожелания (необязательно)")
    
    st.write("") 
    if st.button("Сформировать рекомендации"):
        with st.spinner("Связь с ИИ..."):
            res = get_ai_recommendation(f_type, f_genre, f_author, f_char, f_len, f_mood, f_extra)
            st.divider()
            st.markdown(f"<div class='result-area'>{res}</div>", unsafe_allow_html=True)
