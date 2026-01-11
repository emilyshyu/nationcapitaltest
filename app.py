import streamlit as st
import random
import json

# 設定頁面配置 (行動裝置優化)
st.set_page_config(
    page_title="Hauptstadt-Meister",
    page_icon="🌍",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 自定義 CSS 使其更像手機 App
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    .stButton>button {
        width: 100%;
        border-radius: 15px;
        height: 3.5rem;
        font-weight: bold;
        font-size: 1.1rem;
        border: none;
        transition: all 0.2s;
    }
    .stButton>button:active { transform: scale(0.98); }
    div[data-testid="stMetricValue"] { font-size: 2rem; color: #2563eb; }
    .flashcard {
        background-color: white;
        padding: 40px;
        border-radius: 25px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
        text-align: center;
        margin-bottom: 20px;
        border: 1px solid #f1f5f9;
        min-height: 250px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .continent-label {
        color: #3b82f6;
        font-size: 0.8rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 國家資料庫 (JSON 格式)
COUNTRIES_DATA = [
    {"name": "Deutschland", "capital": "Berlin", "continent": "Europa"},
    {"name": "Frankreich", "capital": "Paris", "continent": "Europa"},
    {"name": "Italien", "capital": "Rom", "continent": "Europa"},
    {"name": "Spanien", "capital": "Madrid", "continent": "Europa"},
    {"name": "Österreich", "capital": "Wien", "continent": "Europa"},
    {"name": "Schweiz", "capital": "Bern", "continent": "Europa"},
    {"name": "Vereinigtes Königreich", "capital": "London", "continent": "Europa"},
    {"name": "Niederlande", "capital": "Amsterdam", "continent": "Europa"},
    {"name": "Schweden", "capital": "Stockholm", "continent": "Europa"},
    {"name": "Polen", "capital": "Warschau", "continent": "Europa"},
    {"name": "Griechenland", "capital": "Athen", "continent": "Europa"},
    {"name": "Japan", "capital": "Tokio", "continent": "Asien"},
    {"name": "China", "capital": "Peking", "continent": "Asien"},
    {"name": "Südkorea", "capital": "Seoul", "continent": "Asien"},
    {"name": "Indien", "capital": "Neu-Delhi", "continent": "Asien"},
    {"name": "Thailand", "capital": "Bangkok", "continent": "Asien"},
    {"name": "USA", "capital": "Washington, D.C.", "continent": "Nordamerika"},
    {"name": "Kanada", "capital": "Ottawa", "continent": "Nordamerika"},
    {"name": "Mexiko", "capital": "Mexiko-Stadt", "continent": "Nordamerika"},
    {"name": "Brasilien", "capital": "Brasília", "continent": "Südamerika"},
    {"name": "Argentinien", "capital": "Buenos Aires", "continent": "Südamerika"},
    {"name": "Ägypten", "capital": "Kairo", "continent": "Afrika"},
    {"name": "Südafrika", "capital": "Pretoria", "continent": "Afrika"},
    {"name": "Australien", "capital": "Canberra", "continent": "Ozeanien"},
    {"name": "Neuseeland", "capital": "Wellington", "continent": "Ozeanien"}
]

# 初始化 Session State
if 'mode' not in st.session_state: st.session_state.mode = 'home'
if 'quiz_idx' not in st.session_state: st.session_state.quiz_idx = 0
if 'quiz_score' not in st.session_state: st.session_state.quiz_score = 0
if 'quiz_data' not in st.session_state: st.session_state.quiz_data = []
if 'flash_idx' not in st.session_state: st.session_state.flash_idx = 0
if 'flash_flipped' not in st.session_state: st.session_state.flash_flipped = False
if 'session_list' not in st.session_state: st.session_state.session_list = []

def get_grade(score):
    if score == 10: return "1+", "Hervorragend! Perfekt!"
    if score == 9: return "1", "Sehr gut!"
    if score >= 7: return "2", "Gut gemacht!"
    if score >= 5: return "3", "Befriedigend."
    if score >= 3: return "4", "Ausreichend."
    return "5", "Nicht bestanden."

def reset_to_home():
    st.session_state.mode = 'home'
    st.rerun()

# --- 介面邏輯 ---

# 1. 主畫面
if st.session_state.mode == 'home':
    st.markdown("<h1 style='text-align: center; color: #1e293b;'>🌍 Hauptstadt-Meister</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748b;'>Lerne die Hauptstädte der Welt</p>", unsafe_allow_html=True)
    
    st.subheader("Einheit wählen")
    options = ["Alle Länder", "Europa", "Asien", "Afrika", "Nordamerika", "Südamerika", "Ozeanien", "Zufällig 10", "Zufällig 20"]
    selection = st.selectbox("Bereich auswählen:", options)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📖 Lernen"):
            filtered = COUNTRIES_DATA
            if selection != "Alle Länder" and "Zufällig" not in selection:
                filtered = [c for c in COUNTRIES_DATA if c['continent'] == selection]
            
            if "Zufällig 10" in selection: filtered = random.sample(COUNTRIES_DATA, 10)
            elif "Zufällig 20" in selection: filtered = random.sample(COUNTRIES_DATA, 20)
            else: random.shuffle(filtered)
            
            st.session_state.session_list = filtered
            st.session_state.flash_idx = 0
            st.session_state.flash_flipped = False
            st.session_state.mode = 'flashcards'
            st.rerun()
            
    with col2:
        if st.button("🎯 Quiz"):
            st.session_state.quiz_data = random.sample(COUNTRIES_DATA, 10)
            st.session_state.quiz_idx = 0
            st.session_state.quiz_score = 0
            st.session_state.mode = 'quiz'
            st.rerun()
            
    st.markdown("---")
    st.subheader("🔍 Schnelle Suche")
    search_choice = st.selectbox("Land eingeben:", [""] + [c['name'] for c in sorted(COUNTRIES_DATA, key=lambda x: x['name'])], index=0)
    if search_choice:
        res = next(c for c in COUNTRIES_DATA if c['name'] == search_choice)
        st.markdown(f"""
            <div class='flashcard' style='min-height: 150px; background: #eff6ff; border: 2px solid #3b82f6;'>
                <div class='continent-label'>{res['continent']}</div>
                <div style='font-size: 1.2rem; color: #64748b;'>Die Hauptstadt von {res['name']} ist:</div>
                <div style='font-size: 2.2rem; font-weight: bold; color: #1e40af;'>{res['capital']}</div>
            </div>
        """, unsafe_allow_html=True)

# 2. 閃卡模式
elif st.session_state.mode == 'flashcards':
    data = st.session_state.session_list
    curr = data[st.session_state.flash_idx]
    
    if st.button("⬅️ Menü"): reset_to_home()
    
    st.progress((st.session_state.flash_idx + 1) / len(data))
    st.write(f"Land {st.session_state.flash_idx + 1} von {len(data)}")
    
    # 翻卡顯示
    if not st.session_state.flash_flipped:
        st.markdown(f"""
            <div class='flashcard'>
                <div class='continent-label'>{curr['continent']}</div>
                <div style='font-size: 2.5rem; font-weight: bold; color: #1e293b;'>{curr['name']}</div>
                <div style='color: #94a3b8; margin-top: 20px;'>Tippe auf 'Umdrehen'</div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("🔄 Umdrehen"):
            st.session_state.flash_flipped = True
            st.rerun()
    else:
        st.markdown(f"""
            <div class='flashcard' style='background-color: #2563eb;'>
                <div style='color: #bfdbfe; font-weight: bold;'>HAUPTSTADT:</div>
                <div style='font-size: 2.5rem; font-weight: bold; color: white;'>{curr['capital']}</div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("✅ Nächste"):
            st.session_state.flash_idx = (st.session_state.flash_idx + 1) % len(data)
            st.session_state.flash_flipped = False
            st.rerun()

# 3. 測驗模式
elif st.session_state.mode == 'quiz':
    if st.session_state.quiz_idx < 10:
        q_data = st.session_state.quiz_data[st.session_state.quiz_idx]
        st.write(f"Frage {st.session_state.quiz_idx + 1} / 10")
        st.progress((st.session_state.quiz_idx + 1) / 10)
        
        st.markdown(f"<h2 style='text-align: center;'>Was ist die Hauptstadt von <br><span style='color:#2563eb;'>{q_data['name']}</span>?</h2>", unsafe_allow_html=True)
        
        # 產生選項
        wrong = [c['capital'] for c in COUNTRIES_DATA if c['capital'] != q_data['capital']]
        options = random.sample(wrong, 3) + [q_data['capital']]
        random.shuffle(options)
        
        for opt in options:
            if st.button(opt, key=f"btn_{opt}"):
                if opt == q_data['capital']:
                    st.session_state.quiz_score += 1
                    st.success("Richtig!")
                else:
                    st.error(f"Falsch! Die Antwort war {q_data['capital']}")
                
                st.session_state.quiz_idx += 1
                st.rerun()
    else:
        # 顯示結果
        grade, msg = get_grade(st.session_state.quiz_score)
        st.markdown(f"""
            <div style='text-align: center; padding: 40px; background: white; border-radius: 30px; box-shadow: 0 10px 20px rgba(0,0,0,0.05);'>
                <h1 style='color: #1e293b;'>Ergebnis</h1>
                <div style='font-size: 5rem; font-weight: 900; color: #2563eb;'>{grade}</div>
                <p style='font-size: 1.2rem; color: #64748b;'>{msg}</p>
                <hr>
                <p>Punktzahl: {st.session_state.quiz_score} / 10</p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("Zurück zum Menü"): reset_to_home()
