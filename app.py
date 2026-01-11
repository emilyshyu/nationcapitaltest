import streamlit as st
import random

# --- 頁面配置 (行動裝置優化) ---
st.set_page_config(
    page_title="Hauptstadt-Meister",
    page_icon="🌍",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 國家資料庫 ---
COUNTRIES = [
    {"name": "Deutschland", "capital": "Berlin", "continent": "Europa"},
    {"name": "Frankreich", "capital": "Paris", "continent": "Europa"},
    {"name": "Italien", "capital": "Rom", "continent": "Europa"},
    {"name": "Spanien", "capital": "Madrid", "continent": "Europa"},
    {"name": "Österreich", "capital": "Wien", "continent": "Europa"},
    {"name": "Schweiz", "capital": "Bern", "continent": "Europa"},
    {"name": "Vereinigtes Königreich", "capital": "London", "continent": "Europa"},
    {"name": "Niederlande", "capital": "Amsterdam", "continent": "Europa"},
    {"name": "Japan", "capital": "Tokio", "continent": "Asien"},
    {"name": "China", "capital": "Peking", "continent": "Asien"},
    {"name": "USA", "capital": "Washington, D.C.", "continent": "Nordamerika"},
    {"name": "Brasilien", "capital": "Brasília", "continent": "Südamerika"},
    {"name": "Ägypten", "capital": "Kairo", "continent": "Afrika"},
    {"name": "Australien", "capital": "Canberra", "continent": "Ozeanien"},
    {"name": "Südkorea", "capital": "Seoul", "continent": "Asien"},
    {"name": "Indien", "capital": "Neu-Delhi", "continent": "Asien"},
    {"name": "Kanada", "capital": "Ottawa", "continent": "Nordamerika"},
    {"name": "Mexiko", "capital": "Mexiko-Stadt", "continent": "Nordamerika"},
    {"name": "Griechenland", "capital": "Athen", "continent": "Europa"},
    {"name": "Schweden", "capital": "Stockholm", "continent": "Europa"}
]

# --- 深度自定義 CSS (iOS 質感與按鈕回饋) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #f8fafc;
    }

    /* 隱藏不必要的組件 */
    #MainMenu, footer, header { visibility: hidden; }

    /* iOS 風格卡片 */
    .ios-card {
        background: white;
        padding: 40px 25px;
        border-radius: 35px;
        box-shadow: 0 15px 35px -5px rgba(0, 0, 0, 0.05);
        border: 1px solid #f1f5f9;
        text-align: center;
        margin-bottom: 20px;
    }

    /* 閃卡背面設計 */
    .flashcard-back {
        background: #2563eb;
        color: white;
        padding: 40px 25px;
        border-radius: 35px;
        text-align: center;
        box-shadow: 0 20px 30px -10px rgba(37, 99, 235, 0.5);
    }

    /* 測驗選項設計 */
    .option-base {
        padding: 22px;
        border-radius: 24px;
        margin-bottom: 12px;
        font-weight: 800;
        font-size: 1.2rem;
        text-align: left;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 5px solid rgba(0,0,0,0.1);
        transition: all 0.2s;
    }
    .option-correct { background-color: #10b981; color: white; border-bottom-color: #059669; }
    .option-wrong { background-color: #f43f5e; color: white; border-bottom-color: #be123c; }
    .option-neutral { background-color: white; color: #cbd5e1; border-bottom-color: #f1f5f9; }

    /* 主按鈕設計 */
    .stButton > button {
        width: 100% !important;
        border-radius: 24px !important;
        height: 65px !important;
        font-weight: 900 !important;
        font-size: 1.1rem !important;
        text-transform: uppercase;
        border: none !important;
        box-shadow: 0 10px 20px -5px rgba(0, 0, 0, 0.1) !important;
        border-bottom: 6px solid rgba(0,0,0,0.2) !important;
    }
    
    /* 點擊回饋 */
    .stButton > button:active { transform: translateY(2px); border-bottom-width: 2px !important; }

    /* 藍色按鈕區塊 */
    div[data-testid="stVerticalBlock"] > div:nth-child(1) .stButton button { background-color: #2563eb !important; color: white !important; }
    /* 綠色按鈕區塊 */
    div[data-testid="stVerticalBlock"] > div:nth-child(2) .stButton button { background-color: #10b981 !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- Session 狀態初始化 ---
if 'mode' not in st.session_state: st.session_state.mode = 'home'
if 'idx' not in st.session_state: st.session_state.idx = 0
if 'score' not in st.session_state: st.session_state.score = 0
if 'quiz_pool' not in st.session_state: st.session_state.quiz_pool = []
if 'answered' not in st.session_state: st.session_state.answered = False
if 'user_choice' not in st.session_state: st.session_state.user_choice = None
if 'flipped' not in st.session_state: st.session_state.flipped = False

def start_quiz():
    pool = []
    # 抽 10 個題目並預先決定好選項
    questions = random.sample(COUNTRIES, 10)
    for q in questions:
        wrong = [c['capital'] for c in COUNTRIES if c['capital'] != q['capital']]
        opts = random.sample(wrong, 3) + [q['capital']]
        random.shuffle(opts)
        pool.append({
            "name": q['name'],
            "correct": q['capital'],
            "continent": q['continent'],
            "options": opts
        })
    st.session_state.quiz_pool = pool
    st.session_state.idx = 0
    st.session_state.score = 0
    st.session_state.answered = False
    st.session_state.mode = 'quiz'

# --- 介面渲染 ---

# 1. 主畫面
if st.session_state.mode == 'home':
    st.markdown("""
        <div style="text-align: center; padding: 40px 0;">
            <div style="background: #2563eb; width: 85px; height: 85px; border-radius: 28px; display: flex; align-items: center; justify-content: center; margin: 0 auto 20px; box-shadow: 0 15px 30px rgba(37, 99, 235, 0.3); transform: rotate(-3deg);">
                <span style="font-size: 45px;">🌍</span>
            </div>
            <h1 style="color: #1e293b; font-weight: 900; margin-bottom: 0; font-size: 2.2rem; letter-spacing: -1px;">Hauptstadt-Meister</h1>
            <p style="color: #94a3b8; font-weight: 700; font-size: 1rem;">Lerne die Welt auf Deutsch</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("📖 LERNEN"):
            st.session_state.quiz_pool = random.sample(COUNTRIES, len(COUNTRIES))
            st.session_state.idx = 0
            st.session_state.flipped = False
            st.session_state.mode = 'learn'
            st.rerun()
    with col2:
        if st.button("🎯 QUIZ"):
            start_quiz()
            st.rerun()

    st.markdown("<br><p style='font-weight: 900; color: #1e293b; margin-bottom: 10px;'>🔍 SCHNELLE SUCHE</p>", unsafe_allow_html=True)
    search_list = [""] + sorted([c['name'] for c in COUNTRIES])
    query = st.selectbox("Suche...", search_list, label_visibility="collapsed")
    
    if query:
        item = next(c for c in COUNTRIES if c['name'] == query)
        st.markdown(f"""
            <div class="ios-card" style="background: #1e293b; color: white; padding: 30px;">
                <p style="color: #3b82f6; font-weight: 900; font-size: 0.7rem; text-transform: uppercase;">{item['continent']}</p>
                <h2 style="font-weight: 900;">{item['name']}</h2>
                <div style="height: 1px; background: #334155; width: 40%; margin: 15px auto;"></div>
                <h1 style="color: #3b82f6; font-weight: 900; font-size: 2.5rem;">{item['capital']}</h1>
            </div>
        """, unsafe_allow_html=True)

# 2. 測驗模式 (重點：鎖定選項，紅綠反饋)
elif st.session_state.mode == 'quiz':
    if st.session_state.idx < 10:
        q = st.session_state.quiz_pool[st.session_state.idx]
        
        # 進度與標題
        st.write(f"Frage {st.session_state.idx + 1} / 10")
        st.progress((st.session_state.idx + 1) / 10)
        st.markdown(f"<div style='text-align:center; margin: 30px 0;'><p style='color:#3b82f6; font-weight:900; letter-spacing: 2px;'>HAUPTSTADT VON</p><h1 style='font-weight:900; font-size:2.8rem; color:#1e293b;'>{q['name']}</h1></div>", unsafe_allow_html=True)

        # 選項邏輯
        if not st.session_state.answered:
            # 尚未回答時顯示按鈕
            for opt in q['options']:
                if st.button(opt, key=f"q_{st.session_state.idx}_{opt}"):
                    st.session_state.answered = True
                    st.session_state.user_choice = opt
                    if opt == q['correct']:
                        st.session_state.score += 1
                    st.rerun()
        else:
            # 已回答時，顯示彩色靜態卡片，不顯示按鈕
            for opt in q['options']:
                if opt == q['correct']:
                    # 正確答案：永遠綠色
                    st.markdown(f"<div class='option-base option-correct'><span>{opt}</span><span>✓</span></div>", unsafe_allow_html=True)
                elif opt == st.session_state.user_choice:
                    # 使用者選錯的那個：紅色
                    st.markdown(f"<div class='option-base option-wrong'><span>{opt}</span><span>✗</span></div>", unsafe_allow_html=True)
                else:
                    # 其他無關選項：淡出
                    st.markdown(f"<div class='option-base option-neutral'><span>{opt}</span></div>", unsafe_allow_html=True)
            
            st.write("")
            if st.button("WEITER →"):
                st.session_state.idx += 1
                st.session_state.answered = False
                st.session_state.user_choice = None
                st.rerun()
    else:
        # 結果畫面
        s = st.session_state.score
        grade = "1+" if s==10 else "1" if s==9 else "2" if s>=7 else "3" if s>=5 else "4" if s>=3 else "5"
        st.markdown(f"""
            <div class="ios-card">
                <p style="color: #94a3b8; font-weight: 900;">ERGEBNIS</p>
                <h1 style="font-weight: 900; font-size: 6.5rem; color: #2563eb; margin: 10px 0;">{grade}</h1>
                <p style="font-weight: 800; font-size: 1.3rem; color: #1e293b;">{s} von 10 richtig!</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("ZUM HAUPTMENÜ"): st.session_state.mode = 'home'; st.rerun()

# 3. 閃卡模式
elif st.session_state.mode == 'learn':
    curr = st.session_state.quiz_pool[st.session_state.idx]
    if st.button("← ZURÜCK"): st.session_state.mode = 'home'; st.rerun()
    
    st.write(f"Land {st.session_state.idx + 1} / {len(st.session_state.quiz_pool)}")
    
    if not st.session_state.flipped:
        st.markdown(f"""
            <div class="ios-card">
                <p style="color: #2563eb; font-weight: 900; font-size: 0.8rem;">{curr['continent'].upper()}</p>
                <h1 style="font-weight: 900; font-size: 3.2rem; color: #1e293b; margin-top: 10px;">{curr['name']}</h1>
                <p style="color: #cbd5e1; margin-top: 50px; font-weight: 800; font-size: 0.9rem;">TIPPE ZUM UMDREHEN</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("🔄 UMDREHEN"): st.session_state.flipped = True; st.rerun()
    else:
        st.markdown(f"""
            <div class="flashcard-back">
                <p style="color: #bfdbfe; font-weight: 900; font-size: 0.8rem;">HAUPTSTADT:</p>
                <h1 style="font-weight: 900; font-size: 3.5rem;">{curr['capital']}</h1>
            </div>
        """, unsafe_allow_html=True)
        if st.button("NÄCHSTE ✅"):
            st.session_state.idx = (st.session_state.idx + 1) % len(st.session_state.quiz_pool)
            st.session_state.flipped = False
            st.rerun()
