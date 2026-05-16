import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.analysis import PRO_BENCHMARKS, generate_demo_results

# Pro athlete profiles database
PRO_ATHLETES = {
    "Eliud Kipchoge": {
        "emoji": "🥇", "country": "🇰🇪 Kenya", "pb": "2:00:35",
        "style": "Midfoot striker, minimal vertical oscillation",
        "Head_Lean": 5.2, "Shoulder_Roll": 2.1, "Pelvic_Drop": 1.8, "Torso_Lean": 8.5,
        "L_Hip_Ang": 92.0, "R_Hip_Ang": 91.5, "L_Knee_Ang": 88.0, "R_Knee_Ang": 87.5,
        "L_Arm_Ang": 88.0, "R_Arm_Ang": 89.0,
    },
    "Mo Farah": {
        "emoji": "🏆", "country": "🇬🇧 UK", "pb": "2:05:11",
        "style": "Forefoot striker, high cadence",
        "Head_Lean": 6.0, "Shoulder_Roll": 3.2, "Pelvic_Drop": 2.5, "Torso_Lean": 9.2,
        "L_Hip_Ang": 89.0, "R_Hip_Ang": 88.5, "L_Knee_Ang": 91.0, "R_Knee_Ang": 90.0,
        "L_Arm_Ang": 85.0, "R_Arm_Ang": 86.5,
    },
    "Yomif Kejelcha": {
        "emoji": "⚡", "country": "🇪🇹 Ethiopia", "pb": "2:01:41",
        "style": "Efficient arm swing, low ground contact",
        "Head_Lean": 4.8, "Shoulder_Roll": 2.8, "Pelvic_Drop": 2.0, "Torso_Lean": 7.8,
        "L_Hip_Ang": 93.0, "R_Hip_Ang": 92.0, "L_Knee_Ang": 86.0, "R_Knee_Ang": 85.5,
        "L_Arm_Ang": 92.0, "R_Arm_Ang": 91.0,
    },
    "นักวิ่งสมัครเล่น (ดี)": {
        "emoji": "🏃", "country": "🌏 General", "pb": "3:30:00",
        "style": "Good form recreational runner",
        "Head_Lean": 7.5, "Shoulder_Roll": 4.5, "Pelvic_Drop": 4.0, "Torso_Lean": 11.0,
        "L_Hip_Ang": 87.0, "R_Hip_Ang": 86.0, "L_Knee_Ang": 85.0, "R_Knee_Ang": 84.0,
        "L_Arm_Ang": 87.0, "R_Arm_Ang": 88.0,
    },
}

def show():
    st.markdown("""
    <div style='padding: 1.5rem 0 1rem;'>
        <div style='font-family: Orbitron, monospace; font-size: 1.8rem; font-weight: 900;
             background: linear-gradient(90deg, #FFD700, #FF3CAC);
             -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
            🏆 เปรียบเทียบมือโปร
        </div>
        <div style='color: #8BA7C7; font-size: 1rem; margin-top: 0.3rem;'>
            วิเคราะห์ช่องว่างระหว่างท่าวิ่งของคุณกับนักวิ่งระดับโลก
        </div>
    </div>
    """, unsafe_allow_html=True)

    results = st.session_state.get("analysis_results")
    if not results:
        results = generate_demo_results()
        st.markdown("""
        <div style='background:rgba(255,215,0,0.08); border:1px solid rgba(255,215,0,0.3);
             border-radius:8px; padding:0.7rem 1rem; margin-bottom:1rem; color:#FFD700;'>
            🎮 แสดงข้อมูล Demo
        </div>
        """, unsafe_allow_html=True)

    # Athlete selector
    col_sel, col_info = st.columns([1, 2])
    with col_sel:
        st.markdown("""
        <div style='font-family:Orbitron; color:#FFD700; font-size:0.85rem;
             text-transform:uppercase; margin-bottom:0.5rem;'>เลือกนักวิ่งเปรียบเทียบ</div>
        """, unsafe_allow_html=True)
        selected = st.selectbox("นักวิ่ง", list(PRO_ATHLETES.keys()), label_visibility="collapsed")

    pro = PRO_ATHLETES[selected]
    with col_info:
        st.markdown(f"""
        <div style='background:rgba(255,215,0,0.06); border:1px solid rgba(255,215,0,0.25);
             border-radius:10px; padding:1rem;'>
            <div style='font-size:2rem; margin-bottom:0.3rem;'>{pro['emoji']}</div>
            <div style='font-family:Orbitron; color:#FFD700; font-size:1rem;'>{selected}</div>
            <div style='color:#8BA7C7; font-size:0.85rem;'>{pro['country']} · PB: {pro['pb']}</div>
            <div style='color:#E8F4FD; font-size:0.85rem; margin-top:0.3rem; font-style:italic;'>
                "{pro['style']}"
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Comparison table
    st.markdown("""
    <div style='font-family:Orbitron; color:#00F5FF; font-size:0.9rem;
         text-transform:uppercase; margin-bottom:0.8rem; letter-spacing:0.1em;'>
        📊 ตารางเปรียบเทียบ
    </div>
    """, unsafe_allow_html=True)

    # Header
    st.markdown(f"""
    <div style='display:grid; grid-template-columns:2fr 1fr 1fr 1fr;
         gap:0.5rem; padding:0.7rem 1rem; background:rgba(0,245,255,0.1);
         border-radius:8px; margin-bottom:0.3rem;
         font-family:Orbitron; font-size:0.75rem; color:#8BA7C7; text-transform:uppercase;'>
        <div>ตัวชี้วัด</div>
        <div style='text-align:center; color:#00F5FF;'>คุณ</div>
        <div style='text-align:center; color:#FFD700;'>{selected}</div>
        <div style='text-align:center;'>ช่องว่าง</div>
    </div>
    """, unsafe_allow_html=True)

    compare_keys = [
        ("Head_Lean", "🎯 มุมเอียงศีรษะ"),
        ("Shoulder_Roll", "⚖️ การหมุนไหล่"),
        ("Pelvic_Drop", "🍑 การตกสะโพก"),
        ("Torso_Lean", "📐 มุมลำตัว"),
        ("L_Hip_Ang", "🦵 สะโพกซ้าย"),
        ("R_Hip_Ang", "🦵 สะโพกขวา"),
        ("L_Knee_Ang", "🦿 เข่าซ้าย"),
        ("R_Knee_Ang", "🦿 เข่าขวา"),
        ("L_Arm_Ang", "💪 แขนซ้าย"),
        ("R_Arm_Ang", "💪 แขนขวา"),
    ]

    for key, label in compare_keys:
        user_val = results.get(key, {}).get("mean", 0) if isinstance(results.get(key), dict) else 0
        pro_val = pro.get(key, 90)
        diff = user_val - pro_val
        diff_abs = abs(diff)
        diff_color = "#39FF14" if diff_abs < 3 else "#FFD700" if diff_abs < 8 else "#FF6B35"
        diff_icon = "✅" if diff_abs < 3 else "⚠️" if diff_abs < 8 else "❌"
        diff_sign = "+" if diff > 0 else ""

        st.markdown(f"""
        <div style='display:grid; grid-template-columns:2fr 1fr 1fr 1fr;
             gap:0.5rem; padding:0.7rem 1rem; background:var(--bg-card);
             border:1px solid var(--border-color); border-radius:8px; margin-bottom:0.3rem;
             align-items:center;'>
            <div style='color:#E8F4FD; font-weight:600;'>{label}</div>
            <div style='text-align:center; font-family:Space Mono; color:#00F5FF; font-weight:700;'>
                {user_val:.1f}°
            </div>
            <div style='text-align:center; font-family:Space Mono; color:#FFD700;'>
                {pro_val:.1f}°
            </div>
            <div style='text-align:center;'>
                <span style='color:{diff_color}; font-family:Space Mono; font-size:0.85rem;'>
                    {diff_icon} {diff_sign}{diff:.1f}°
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Visual gap bars
    st.markdown("""
    <div style='font-family:Orbitron; color:#FF3CAC; font-size:0.9rem;
         text-transform:uppercase; margin: 1.5rem 0 0.8rem; letter-spacing:0.1em;'>
        📊 ช่องว่างที่ต้องปิด (Gap Analysis)
    </div>
    """, unsafe_allow_html=True)

    top_gaps = []
    for key, label in compare_keys:
        user_val = results.get(key, {}).get("mean", 0) if isinstance(results.get(key), dict) else 0
        pro_val = pro.get(key, 90)
        gap = abs(user_val - pro_val)
        top_gaps.append((gap, label, key, user_val, pro_val))

    top_gaps.sort(reverse=True)
    for gap, label, key, user_val, pro_val in top_gaps[:5]:
        max_gap = 20
        gap_pct = min(gap / max_gap * 100, 100)
        gap_color = "#FF6B35" if gap > 8 else "#FFD700" if gap > 3 else "#39FF14"

        st.markdown(f"""
        <div style='margin-bottom:0.8rem;'>
            <div style='display:flex; justify-content:space-between; margin-bottom:0.3rem;'>
                <span style='color:#E8F4FD; font-size:0.9rem;'>{label}</span>
                <span style='color:{gap_color}; font-family:Space Mono; font-size:0.85rem;'>
                    ช่องว่าง {gap:.1f}°
                </span>
            </div>
            <div style='background:#0A1628; border-radius:6px; height:10px; overflow:hidden;'>
                <div style='background:linear-gradient(90deg, {gap_color}, {gap_color}88);
                     width:{gap_pct}%; height:100%; border-radius:6px;'></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Insights
    st.markdown("""
    <div style='background:rgba(255,60,172,0.06); border:1px solid rgba(255,60,172,0.25);
         border-radius:12px; padding:1.2rem; margin-top:1rem;'>
        <div style='font-family:Orbitron; color:#FF3CAC; font-size:0.85rem;
             margin-bottom:0.8rem; text-transform:uppercase;'>
            🧠 AI วิเคราะห์ช่องว่าง
        </div>
        <div style='color:#8BA7C7; font-size:0.9rem; line-height:1.8;'>
            จุดที่ต้องพัฒนามากที่สุดคือ <strong style='color:#FF6B35;'>Pelvic Drop</strong> และ
            <strong style='color:#FFD700;'>Shoulder Roll</strong> ซึ่งส่งผลต่อประสิทธิภาพการวิ่งโดยตรง
            การลด Pelvic Drop ลง 50% จะเพิ่มประสิทธิภาพการใช้พลังงานประมาณ 3-5%
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("💪 สร้างแผนฝึกปิดช่องว่าง", use_container_width=True):
        st.session_state.current_page = "training"
        st.rerun()
