import streamlit as st
import random

# 1. 頁面基礎設定 (強制使用淺色背景與手機寬度)
st.set_page_config(
    page_title="Hauptstadt-Meister",
    page_icon="🌍",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. 強制注入 CSS (還原 img1.png 的視覺外觀)
st.markdown("""
    <style>
    /* 強制全局背景為淺灰色 */
    .stApp {
        background-color: #f8fafc !important;
    }
    
    /* 隱藏 Streamlit 預設標籤與頁首 */
    #MainMenu, footer, header { visibility: hidden; }
    
    /* 自定義字體 */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    /* 頂部標題區塊 */
    .header-container { text-align: center; padding: 30px 0; }
    .logo-box {
        background: #2563eb; width: 70px; height: 70px; border-radius: 20px;
        display: flex; align-items: center; justify-content: center;
        margin: 0 auto 15px; box-shadow: 0 10px 20px rgba(37, 99, 235, 0.2);
    }

    /* 網格篩選按鈕樣式 */
    .filter-btn-grid {
        display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 30px;
    }

    /* 選項與按鈕的共通設計 */
    .stButton > button {
        border-radius: 18px !important;
        border: none !important;
        font-weight: 700 !important;
        transition: all 0.2s !important;
        height: 55px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05) !important;
    }
    
    /* 底部大型動作按鈕 */
    div.stButton > button[kind="primary"] {
        background-color: #2563eb !important; color: white !important;
        border-bottom: 6px solid #1e40af !important;
    }
    
    /* 綠色按鈕 (Quiz Start) */
    .quiz-start-btn button {
        background-color: #10b981 !important; color: white !important;
        border-bottom: 6px solid #059669 !important;
    }

    /* 測驗回饋樣式 */
    .res-box { padding: 20px; border-radius: 20px; margin-bottom: 10px; font-weight: 800; font-size: 1.1rem; display: flex; justify-content: space-between; }
    .correct { background: #10b981; color: white; border-bottom: 4px solid #059669; }
    .wrong { background: #f43f5e; color: white; border-bottom: 4px solid #be123c; }
    .neutral { background: white; color: #cbd5e1; border: 1px solid #f1f5f9; }
    
    /* 卡片設計 */
    .card { background: white; padding: 40px 20px; border-radius: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.05); text-align: center; margin: 20px 0; border: 1px solid #f1f5f9; }
    </style>
""", unsafe_allow_html=True)

# 3. 資料庫
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
    {"name": "Australien", "capital": "Canberra", "continent": "Ozeanien"},
    {"name": "Ägypten", "capital": "Kairo", "continent": "Afrika"},
    {"name": "Südkorea", "capital": "Seoul", "continent": "Asien"},
    {"name": "Indien", "capital": "Neu-Delhi", "continent": "Asien"},
    {"name": "Griechenland", "capital": "Athen", "continent": "Europa"},
    {"name": "Mexiko", "capital": "Mexiko-Stadt", "continent": "Nordamerika"},
    {"name": "Thailand", "capital": "Bangkok", "continent": "Asien"},
    {"name": "Argentinien", "capital": "Buenos Aires", "continent": "Südamerika"},
]

# 4. 初始化 Session State (確保隨機性被固定)
if 'mode' not in st.session_state: st.session_state.mode = 'home'
if 'filter' not in st.session_state: st.session_state.filter = 'Alle Länder'
if 'quiz_pool' not in st.session_state: st.session_state.quiz_pool = []
if 'idx' not in st.session_state: st.session_state.idx = 0
if 'score' not in st.session_state: st.session_state.score = 0
if 'answered' not in st.session_state: st.session_state.answered = False
if 'user_choice' not in st.session_state: st.session_state.user_choice = None

def setup_quiz():
    # 抽 10 題並預先固定選項，防止重新整理時選項跑掉
    pool = random.sample(COUNTRIES, 10)
    final_pool = []
    for q in pool:
        wrong = [c['capital'] for c in COUNTRIES if c['capital'] != q['capital']]
        opts = random.sample(wrong, 3) + [q['capital']]
        random.shuffle(opts)
        final_pool.append({"q": q, "opts": opts})
    st.session_state.quiz_pool = final_pool
    st.session_state.idx = 0
    st.session_state.score = 0
    st.session_state.mode = 'quiz'

# 5. 主介面邏輯
if st.session_state.mode == 'home':
    # 標題與 Logo (還原 img1.png)
    st.markdown("""
        <div class="header-container">
            <div class="logo-box">
                <span style="font-size: 35px;">🌍</span>
            </div>
            <h1 style="color: #1e293b; font-weight: 900; margin-bottom: 5px; font-size: 1.8rem;">Hauptstadt-Meister</h1>
            <p style="color: #94a3b8; font-weight: 600; font-size: 0.9rem;">Entdecke die Welt auf Deutsch</p>
        </div>
    """, unsafe_allow_html=True)

    # 篩選單元網格
    st.markdown("<p style='font-weight: 900; color: #1e293b; font-size: 1.1rem;'>Einheit</p>", unsafe_allow_html=True)
    
    filters = ["Alle Länder", "Europa", "Asien", "Afrika", "Nordamerika", "Südamerika", "Ozeanien", "A-Z", "Mix 10", "Mix 20"]
    cols = st.columns(2)
    for i, f in enumerate(filters):
        with cols[i % 2]:
            if st.button(f, key=f"filter_{f}"):
                st.session_state.filter = f
    
    st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)

    # 底部大型動作按鈕 (與 img1.png 一致)
    if st.button("📖 LERNEN", type="primary", use_container_width=True):
        st.session_state.mode = 'learn'
        st.session_state.idx = 0
        st.rerun()
    
    st.markdown('<div class="quiz-start-btn">', unsafe_allow_width=True)
    if st.button("🎯 QUIZ STARTEN", use_container_width=True):
        setup_quiz()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.mode == 'quiz':
    if st.session_state.idx < len(st.session_state.quiz_pool):
        data = st.session_state.quiz_pool[st.session_state.idx]
        q = data['q']
        opts = data['opts']

        st.progress((st.session_state.idx + 1) / 10)
        st.markdown(f"<div class='card'><p style='color:#2563eb; font-weight:900;'>HAUPTSTADT VON</p><h1 style='font-weight:900; font-size:2.5rem;'>{q['name']}</h1></div>", unsafe_allow_html=True)

        if not st.session_state.answered:
            # 尚未回答：顯示按鈕
            for o in opts:
                if st.button(o, key=f"opt_{o}", use_container_width=True):
                    st.session_state.user_choice = o
                    st.session_state.answered = True
                    if o == q['capital']: st.session_state.score += 1
                    st.rerun()
        else:
            # 已回答：鎖定畫面並顯示顏色
            for o in opts:
                if o == q['capital']:
                    st.markdown(f"<div class='res-box correct'><span>{o}</span><span>✓</span></div>", unsafe_allow_html=True)
                elif o == st.session_state.user_choice:
                    st.markdown(f"<div class='res-box wrong'><span>{o}</span><span>✗</span></div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='res-box neutral'>{o}</div>", unsafe_allow_html=True)
            
            st.write("")
            if st.button("WEITER →", type="primary", use_container_width=True):
                st.session_state.idx += 1
                st.session_state.answered = False
                st.rerun()
    else:
        # 顯示成績單
        s = st.session_state.score
        st.markdown(f"<div class='card'><h1>Ergebnis</h1><h1 style='font-size:5rem; color:#2563eb;'>{s}/10</h1><p>Gut gemacht!</p></div>", unsafe_allow_html=True)
        if st.button("ZUM MENÜ", use_container_width=True):
            st.session_state.mode = 'home'
            st.rerun()

elif st.session_state.mode == 'learn':
    # (閃卡模式略，邏輯與先前相同但套用新的 CSS 卡片類別)
    curr = COUNTRIES[st.session_state.idx]
    if st.button("← ZURÜCK"): st.session_state.mode = 'home'; st.rerun()
    st.markdown(f"<div class='card'><h3>{curr['name']}</h3><br><h1 style='color:#2563eb;'>{curr['capital']}</h1></div>", unsafe_allow_html=True)
    if st.button("NÄCHSTE", type="primary", use_container_width=True):
        st.session_state.idx = (st.session_state.idx + 1) % len(COUNTRIES)
        st.rerun()
