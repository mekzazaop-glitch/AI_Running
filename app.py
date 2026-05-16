import streamlit as st
import os

st.set_page_config(
    page_title="RunAI Coach",
    page_icon="🏃",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "RunAI Coach - AI-Powered Running Form Analyzer"
    }
)

# Load custom CSS
def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;500;600;700&family=Space+Mono:ital,wght@0,400;0,700;1,400&display=swap');

    :root {
        --bg-primary: #050A14;
        --bg-secondary: #0A1628;
        --bg-card: #0D1F3C;
        --bg-card-hover: #112444;
        --accent-primary: #00F5FF;
        --accent-secondary: #FF3CAC;
        --accent-green: #39FF14;
        --accent-orange: #FF6B35;
        --accent-yellow: #FFD700;
        --text-primary: #E8F4FD;
        --text-secondary: #8BA7C7;
        --text-muted: #4A6080;
        --border-color: #1A3050;
        --border-glow: rgba(0, 245, 255, 0.3);
        --gradient-hero: linear-gradient(135deg, #050A14 0%, #0A1628 50%, #0D1F3C 100%);
    }

    * { box-sizing: border-box; }

    .stApp {
        background: var(--bg-primary) !important;
        color: var(--text-primary) !important;
        font-family: 'Rajdhani', sans-serif !important;
    }

    #MainMenu, footer, header { visibility: hidden !important; }

    /* Hide default Streamlit page navigation */
    [data-testid="stSidebarNav"] { display: none !important; }
    [data-testid="stSidebarNavItems"] { display: none !important; }
    [data-testid="stSidebarNavSeparator"] { display: none !important; }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: var(--bg-secondary) !important;
        border-right: 1px solid var(--border-color) !important;
    }
    [data-testid="stSidebar"] * { color: var(--text-primary) !important; }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--accent-primary), #0099CC) !important;
        color: #000 !important;
        border: none !important;
        border-radius: 8px !important;
        font-family: 'Orbitron', monospace !important;
        font-weight: 700 !important;
        font-size: 0.85rem !important;
        padding: 0.6rem 1.5rem !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase !important;
        letter-spacing: 0.1em !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(0,245,255,0.4) !important;
    }

    /* Cards */
    .metric-card {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 1.2rem;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, var(--accent-primary), var(--accent-secondary));
    }
    .metric-card:hover {
        border-color: var(--accent-primary);
        box-shadow: 0 0 20px rgba(0,245,255,0.15);
        transform: translateY(-2px);
    }

    /* Score ring */
    .score-ring {
        width: 120px; height: 120px;
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        margin: 0 auto;
        font-family: 'Orbitron', monospace;
        font-size: 1.8rem;
        font-weight: 900;
        position: relative;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: var(--bg-secondary) !important;
        border-radius: 10px !important;
        gap: 4px !important;
        padding: 4px !important;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        color: var(--text-secondary) !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        font-size: 1rem !important;
    }
    .stTabs [aria-selected="true"] {
        background: var(--accent-primary) !important;
        color: #000 !important;
    }

    /* Progress bars */
    .stProgress > div > div {
        background: linear-gradient(90deg, var(--accent-primary), var(--accent-secondary)) !important;
    }

    /* Alerts */
    .good-alert {
        background: rgba(57, 255, 20, 0.1);
        border: 1px solid var(--accent-green);
        border-radius: 8px;
        padding: 0.8rem 1rem;
        color: var(--accent-green);
        margin: 0.4rem 0;
        font-size: 0.95rem;
    }
    .warn-alert {
        background: rgba(255, 107, 53, 0.1);
        border: 1px solid var(--accent-orange);
        border-radius: 8px;
        padding: 0.8rem 1rem;
        color: var(--accent-orange);
        margin: 0.4rem 0;
        font-size: 0.95rem;
    }
    .info-alert {
        background: rgba(0, 245, 255, 0.08);
        border: 1px solid var(--accent-primary);
        border-radius: 8px;
        padding: 0.8rem 1rem;
        color: var(--accent-primary);
        margin: 0.4rem 0;
        font-size: 0.95rem;
    }

    /* Inputs */
    .stFileUploader {
        background: var(--bg-card) !important;
        border: 2px dashed var(--border-color) !important;
        border-radius: 12px !important;
    }
    .stSelectbox select, .stTextInput input {
        background: var(--bg-card) !important;
        color: var(--text-primary) !important;
        border-color: var(--border-color) !important;
    }

    /* Hide streamlit branding */
    .viewerBadge_container__1QSob { display: none !important; }
    </style>
    """, unsafe_allow_html=True)

load_css()

# Sidebar navigation
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 1rem 0 1.5rem;'>
        <div style='font-family: Orbitron, monospace; font-size: 1.6rem; font-weight: 900;
             background: linear-gradient(135deg, #00F5FF, #FF3CAC);
             -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
            🏃 RunAI
        </div>
        <div style='font-family: Rajdhani, sans-serif; color: #8BA7C7; font-size: 0.85rem;
             letter-spacing: 0.2em; text-transform: uppercase; margin-top: 4px;'>
            Elite Coach
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    pages = {
        "🏠 หน้าหลัก": "home",
        "📤 อัปโหลดวิดีโอ": "upload",
        "🤖 วิเคราะห์ท่าวิ่ง": "analyze",
        "📊 รายงานละเอียด": "report",
        "🏆 เปรียบเทียบมือโปร": "compare",
        "💪 แผนฝึก AI": "training",
        "📚 คู่มือการใช้งาน": "guide",
    }

    if "current_page" not in st.session_state:
        st.session_state.current_page = "home"
    if "uploaded_video" not in st.session_state:
        st.session_state.uploaded_video = None
    if "analysis_results" not in st.session_state:
        st.session_state.analysis_results = None
    if "video_path" not in st.session_state:
        st.session_state.video_path = None

    for label, page_id in pages.items():
        is_active = st.session_state.current_page == page_id
        style = "background: rgba(0,245,255,0.15); border: 1px solid rgba(0,245,255,0.4);" if is_active else ""
        if st.button(label, key=f"nav_{page_id}", use_container_width=True):
            st.session_state.current_page = page_id
            st.rerun()

    st.divider()

    # Status indicator
    if st.session_state.uploaded_video:
        st.markdown("""
        <div style='background: rgba(57,255,20,0.1); border: 1px solid #39FF14;
             border-radius: 8px; padding: 0.6rem; text-align: center; font-size: 0.85rem; color: #39FF14;'>
            ✅ วิดีโอพร้อมวิเคราะห์
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style='background: rgba(255,107,53,0.1); border: 1px solid #FF6B35;
             border-radius: 8px; padding: 0.6rem; text-align: center; font-size: 0.85rem; color: #FF6B35;'>
            ⚠️ ยังไม่มีวิดีโอ
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='color: #4A6080; font-size: 0.75rem; text-align: center;'>
        RunAI Coach v2.0<br>Powered by YOLOv8
    </div>
    """, unsafe_allow_html=True)

# Route to pages
page = st.session_state.current_page

if page == "home":
    from pages import home
    home.show()
elif page == "upload":
    from pages import upload
    upload.show()
elif page == "analyze":
    from pages import analyze
    analyze.show()
elif page == "report":
    from pages import report
    report.show()
elif page == "compare":
    from pages import compare
    compare.show()
elif page == "training":
    from pages import training
    training.show()
elif page == "guide":
    from pages import guide
    guide.show()
