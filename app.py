import streamlit as st
import random
import time

# --- 頁面配置 ---
st.set_page_config(
    page_title="Hauptstadt-Meister",
    page_icon="🌍",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 深度自定義 CSS (模擬 React/Tailwind 質感) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #f8fafc;
    }

    /* 隱藏 Streamlit 預設選單 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* 卡片設計 */
    .ios-card {
        background: white;
        padding: 40px 20px;
        border-radius: 32px;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.05);
        border: 1px solid #f1f5f9;
        text-align: center;
        margin-bottom: 24px;
        transition: all 0.3s ease;
    }

    /* 按鈕美化 */
    .stButton > button {
        width: 100%;
        border-radius: 20px !important;
        height: 60px !important;
        font-weight: 900 !important;
        font-size: 1.1rem !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        border: none !important;
        transition: all 0.2s !important;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1) !important;
    }
    
    /* 不同類型的按鈕顏色 */
    div[data-testid="stVerticalBlock"] > div:nth-child(1) .stButton button { background-color: #2563eb !important; color: white !important; border-bottom: 6px solid #1e40af !important; }
    div[data-testid="stVerticalBlock"] > div:nth-child(2) .stButton button { background-color: #10b981 !important; color: white !important; border-bottom: 6px solid #059669 !important; }

    /* 測驗選項顏色邏輯 (透過 Markdown 注入) */
    .correct-option { background-color: #10b981 !important; color: white !important; border-radius: 20px; padding: 20px; margin-bottom: 10px; font-weight: bold; border-bottom: 4px solid #059669; }
    .wrong-option { background-color: #f43f5e !important; color: white !important; border-radius: 20px; padding: 20px; margin-bottom: 10px; font-weight: bold; border-bottom: 4px solid #be123c; }
    
    /* 標題動畫 */
    .title-area {
        animation: fadeIn 0.8s ease-out;
        text-align: center;
        padding: 40px 0;
    }
    @keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
    </style>
    """, unsafe_allow_html=True)

# --- 國家資料 ---
COUNTRIES = [
    {"name": "Deutschland", "capital": "Berlin", "continent": "Europa"},
    {"name": "Frankreich", "capital": "Paris", "continent": "Europa"},
    {"name": "Italien", "capital": "Rom", "continent": "Europa"},
    {"name": "Spanien", "capital": "Madrid", "continent": "Europa"},
    {"name": "Österreich", "capital": "Wien", "continent": "Europa"},
    {"name": "Schweiz", "capital": "Bern", "continent": "Europa"},
    {"name": "Japan", "capital": "Tokio", "continent": "Asien"},
    {"name": "China", "capital": "Peking", "continent": "Asien"},
    {"name": "USA", "capital": "Washington, D.C.", "continent": "Nordamerika"},
    {"name": "Brasilien", "capital": "Brasília", "continent": "Südamerika"},
    {"name": "Ägypten", "capital": "Kairo", "continent": "Afrika"},
    {"name": "Australien", "capital": "Canberra", "continent": "Ozeanien"},
    {"name": "Indien", "capital": "Neu-Delhi", "continent": "Asien"},
    {"name": "Kanada", "capital": "Ottawa", "continent": "Nordamerika"},
    {"name": "Südkorea", "capital": "Seoul", "continent": "Asien"},
    {"name": "Griechenland", "capital": "Athen", "continent": "Europa"},
    {"name": "Mexiko", "capital": "Mexiko-Stadt", "continent": "Nordamerika"},
    {"name": "Thailand", "capital": "Bangkok", "continent": "Asien"},
    {"name": "Portugal", "capital": "Lissabon", "continent": "Europa"},
    {"name": "Argentinien", "capital": "Buenos Aires", "continent": "Südamerika"},
    {"name": "Schweden", "capital": "Stockholm", "continent": "Europa"},
    {"name": "Polen", "capital": "Warschau", "continent": "Europa"},
    {"name": "Vietnam", "capital": "Hanoi", "continent": "Asien"},
    {"name": "Nigeria", "capital": "Abuja", "continent": "Afrika"},
]

# --- 狀態管理 ---
if 'mode' not in st.session_state: st.session_state.mode = 'home'
if 'score' not in st.session_state: st.session_state.score = 0
if 'idx' not in st.session_state: st.session_state.idx = 0
if 'flipped' not in st.session_state: st.session_state.flipped = False
if 'quiz_items' not in st.session_state: st.session_state.quiz_items = []
if 'quiz_answered' not in st.session_state: st.session_state.quiz_answered = False
if 'last_answer' not in st.session_state: st.session_state.last_answer = None

def get_german_grade(score):
    if score == 10: return "1+", "Hervorragend! Perfekt!"
    if score == 9: return "1", "Sehr gut!"
    if score in [7, 8]: return "2", "Gut gemacht!"
    if score in [5, 6]: return "3", "Befriedigend."
    if score in [3, 4]: return "4", "Ausreichend."
    return "5", "Nicht bestanden."

# --- 介面渲染 ---

# 1. 主畫面
if st.session_state.mode == 'home':
    st.markdown("""
        <div class="title-area">
            <div style="background: #2563eb; width: 80px; height: 80px; border-radius: 24px; display: flex; align-items: center; justify-content: center; margin: 0 auto 20px; shadow: 0 10px 20px rgba(37, 99, 235, 0.3);">
                <span style="font-size: 40px;">🌍</span>
            </div>
            <h1 style="color: #1e293b; font-weight: 900; margin-bottom: 0;">Hauptstadt-Meister</h1>
            <p style="color: #94a3b8; font-weight: 600;">Lerne die Welt auf Deutsch</p>
        </div>
    """, unsafe_allow_html=True)

    selection = st.selectbox("Einheit wählen", ["Alle Länder", "Europa", "Asien", "Zufällig 10", "Zufällig 20"])
    
    if st.button("📖 LERNEN (Flashcards)"):
        filtered = COUNTRIES
        if selection == "Europa": filtered = [c for c in COUNTRIES if c['continent'] == 'Europa']
        elif selection == "Asien": filtered = [c for c in COUNTRIES if c['continent'] == 'Asien']
        
        if "10" in selection: filtered = random.sample(COUNTRIES, 10)
        elif "20" in selection: filtered = random.sample(COUNTRIES, 20)
        else: random.shuffle(filtered)
        
        st.session_state.quiz_items = filtered
        st.session_state.idx = 0
        st.session_state.mode = 'learn'
        st.rerun()

    if st.button("🎯 QUIZ STARTEN"):
        st.session_state.quiz_items = random.sample(COUNTRIES, 10)
        st.session_state.idx = 0
        st.session_state.score = 0
        st.session_state.mode = 'quiz'
        st.rerun()

    # 自動選字搜尋功能
    st.markdown("<br><h3 style='font-weight: 900; color: #1e293b;'>🔍 Suche</h3>", unsafe_allow_html=True)
    search_list = [""] + sorted([c['name'] for c in COUNTRIES])
    search_query = st.selectbox("Land eingeben...", search_list, label_visibility="collapsed")
    
    if search_query:
        found = next(c for c in COUNTRIES if c['name'] == search_query)
        st.markdown(f"""
            <div class="ios-card" style="background: #1e293b; color: white;">
                <p style="color: #3b82f6; font-weight: 800; font-size: 0.7rem; text-transform: uppercase;">{found['continent']}</p>
                <h2 style="font-weight: 900; margin-bottom: 15px;">{found['name']}</h2>
                <div style="height: 1px; background: #334155; width: 50%; margin: 20px auto;"></div>
                <p style="color: #94a3b8; font-size: 0.9rem; margin-bottom: 5px;">Hauptstadt:</p>
                <h1 style="color: #3b82f6; font-weight: 900;">{found['capital']}</h1>
            </div>
        """, unsafe_allow_html=True)

# 2. 閃卡模式
elif st.session_state.mode == 'learn':
    curr = st.session_state.quiz_items[st.session_state.idx]
    
    if st.button("← ZURÜCK"): st.session_state.mode = 'home'; st.rerun()
    
    st.write(f"Land {st.session_state.idx + 1} von {len(st.session_state.quiz_items)}")
    
    if not st.session_state.flipped:
        st.markdown(f"""
            <div class="ios-card">
                <p style="color: #2563eb; font-weight: 800; font-size: 0.8rem;">{curr['continent']}</p>
                <h1 style="font-weight: 900; font-size: 3rem; color: #1e293b;">{curr['name']}</h1>
                <p style="color: #cbd5e1; margin-top: 40px; font-weight: bold;">Tippe zum Umdrehen</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("🔄 UMDREHEN"): st.session_state.flipped = True; st.rerun()
    else:
        st.markdown(f"""
            <div class="ios-card" style="background: #2563eb; color: white;">
                <p style="color: #bfdbfe; font-weight: 800; font-size: 0.8rem;">DIE HAUPTSTADT IST:</p>
                <h1 style="font-weight: 900; font-size: 3.5rem;">{curr['capital']}</h1>
            </div>
        """, unsafe_allow_html=True)
        if st.button("✅ NÄCHSTE"):
            st.session_state.idx = (st.session_state.idx + 1) % len(st.session_state.quiz_items)
            st.session_state.flipped = False
            st.rerun()

# 3. 測驗模式 (含顏色反饋)
elif st.session_state.mode == 'quiz':
    if st.session_state.idx < 10:
        curr = st.session_state.quiz_items[st.session_state.idx]
        st.write(f"Frage {st.session_state.idx + 1} / 10")
        st.progress((st.session_state.idx + 1) / 10)
        
        st.markdown(f"<div style='text-align:center; margin: 30px 0;'><p style='color:#3b82f6; font-weight:900;'>HAUPTSTADT GESUCHT</p><h1 style='font-weight:900; font-size:2.5rem;'>{curr['name']}</h1></div>", unsafe_allow_html=True)
        
        # 產生選項
        if not st.session_state.quiz_answered:
            wrong = [c['capital'] for c in COUNTRIES if c['capital'] != curr['capital']]
            options = random.sample(wrong, 3) + [curr['capital']]
            random.shuffle(options)
            st.session_state.current_options = options

        for opt in st.session_state.current_options:
            if not st.session_state.quiz_answered:
                if st.button(opt, key=f"opt_{opt}"):
                    st.session_state.quiz_answered = True
                    st.session_state.last_answer = opt
                    if opt == curr['capital']: st.session_state.score += 1
                    st.rerun()
            else:
                # 顯示顏色反饋
                if opt == curr['capital']:
                    st.markdown(f"<div class='correct-option'>{opt} ✓</div>", unsafe_allow_html=True)
                elif opt == st.session_state.last_answer:
                    st.markdown(f"<div class='wrong-option'>{opt} ✗</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div style='background:#f1f5f9; padding:20px; border-radius:20px; margin-bottom:10px; color:#cbd5e1;'>{opt}</div>", unsafe_allow_html=True)
        
        if st.session_state.quiz_answered:
            st.write("")
            if st.button("WEITER →"):
                st.session_state.idx += 1
                st.session_state.quiz_answered = False
                st.rerun()
    else:
        # 結果畫面
        grade, msg = get_german_grade(st.session_state.score)
        st.markdown(f"""
            <div class="ios-card">
                <p style="color: #94a3b8; font-weight: 800;">QUIZ BEENDET</p>
                <h1 style="font-weight: 900; font-size: 6rem; color: #2563eb; margin: 20px 0;">{grade}</h1>
                <p style="font-weight: 700; font-size: 1.2rem; color: #1e293b;">{msg}</p>
                <p style="color: #94a3b8; margin-top: 10px;">Score: {st.session_state.score} / 10</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("ZUM HAUPTMENÜ"): st.session_state.mode = 'home'; st.rerun()
