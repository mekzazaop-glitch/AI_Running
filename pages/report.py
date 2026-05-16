import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.analysis import PRO_BENCHMARKS, get_metric_status, generate_demo_results

def show():
    st.markdown("""
    <div style='padding: 1.5rem 0 1rem;'>
        <div style='font-family: Orbitron, monospace; font-size: 1.8rem; font-weight: 900;
             background: linear-gradient(90deg, #FF3CAC, #FFD700);
             -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
            📊 รายงานละเอียด
        </div>
        <div style='color: #8BA7C7; font-size: 1rem; margin-top: 0.3rem;'>
            Full Biomechanics Report · Frame-by-Frame Analysis
        </div>
    </div>
    """, unsafe_allow_html=True)

    results = st.session_state.get("analysis_results")
    if not results:
        results = generate_demo_results()
        st.markdown("""
        <div style='background:rgba(255,215,0,0.08); border:1px solid rgba(255,215,0,0.3);
             border-radius:8px; padding:0.7rem 1rem; margin-bottom:1rem; color:#FFD700;'>
            🎮 แสดงข้อมูล Demo — กลับไปอัปโหลดวิดีโอและวิเคราะห์ก่อน
        </div>
        """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📐 ข้อมูลมุมข้อต่อ", "📈 กราฟรายเฟรม", "📋 สรุปผล"])

    with tab1:
        _show_angles_table(results)

    with tab2:
        _show_charts(results)

    with tab3:
        _show_summary(results)


def _show_angles_table(results):
    st.markdown("""
    <div style='font-family:Orbitron; color:#00F5FF; font-size:0.9rem;
         text-transform:uppercase; margin:0.8rem 0; letter-spacing:0.1em;'>
        มุมข้อต่อเฉลี่ย เทียบมาตรฐาน
    </div>
    """, unsafe_allow_html=True)

    rows = [
        ("Head_Lean",    "🎯", "มุมเอียงศีรษะ",   "ควร < 8°"),
        ("Shoulder_Roll","⚖️", "การหมุนไหล่",    "ควร < 5°"),
        ("Pelvic_Drop",  "🍑", "การตกสะโพก",     "ควร < 4°"),
        ("Torso_Lean",   "📐", "มุมเอียงลำตัว",  "8–12° อุดมคติ"),
        ("L_Hip_Ang",    "🦵", "มุมสะโพกซ้าย",   "90° อุดมคติ"),
        ("R_Hip_Ang",    "🦵", "มุมสะโพกขวา",   "90° อุดมคติ"),
        ("L_Knee_Ang",   "🦿", "มุมเข่าซ้าย",    "90° อุดมคติ"),
        ("R_Knee_Ang",   "🦿", "มุมเข่าขวา",    "90° อุดมคติ"),
        ("L_Arm_Ang",    "💪", "มุมแขนซ้าย",    "90° อุดมคติ"),
        ("R_Arm_Ang",    "💪", "มุมแขนขวา",    "90° อุดมคติ"),
    ]

    # Header
    st.markdown("""
    <div style='display:grid; grid-template-columns:2fr 1fr 1fr 1fr 1fr 1fr;
         gap:0.5rem; padding:0.6rem 1rem; background:rgba(0,245,255,0.1);
         border-radius:8px; margin-bottom:0.3rem;
         font-family:Orbitron; font-size:0.75rem; color:#8BA7C7; text-transform:uppercase;'>
        <div>ตัวชี้วัด</div>
        <div style='text-align:center;'>เฉลี่ย</div>
        <div style='text-align:center;'>Min</div>
        <div style='text-align:center;'>Max</div>
        <div style='text-align:center;'>SD</div>
        <div style='text-align:center;'>สถานะ</div>
    </div>
    """, unsafe_allow_html=True)

    for key, icon, label, note in rows:
        if key not in results:
            continue
        d = results[key]
        val = d.get("mean", 0)
        bench = PRO_BENCHMARKS.get(key, {"ideal":90,"good":80,"warning":65})
        _, color, status_label = get_metric_status(val, bench)

        st.markdown(f"""
        <div style='display:grid; grid-template-columns:2fr 1fr 1fr 1fr 1fr 1fr;
             gap:0.5rem; padding:0.7rem 1rem; background:var(--bg-card);
             border:1px solid var(--border-color); border-radius:8px; margin-bottom:0.3rem;
             border-left: 3px solid {color}; align-items:center;'>
            <div>
                <span style='font-size:1.1rem;'>{icon}</span>
                <span style='color:#E8F4FD; font-weight:600; margin-left:0.4rem;'>{label}</span>
                <div style='color:#4A6080; font-size:0.75rem;'>{note}</div>
            </div>
            <div style='text-align:center; font-family:Space Mono; color:{color}; font-weight:700;'>
                {val:.1f}°
            </div>
            <div style='text-align:center; font-family:Space Mono; color:#8BA7C7; font-size:0.85rem;'>
                {d.get("min",0):.1f}°
            </div>
            <div style='text-align:center; font-family:Space Mono; color:#8BA7C7; font-size:0.85rem;'>
                {d.get("max",0):.1f}°
            </div>
            <div style='text-align:center; font-family:Space Mono; color:#8BA7C7; font-size:0.85rem;'>
                ±{d.get("std",0):.1f}
            </div>
            <div style='text-align:center;'>
                <span style='background:{color}22; color:{color}; padding:0.2rem 0.6rem;
                      border-radius:20px; font-size:0.75rem;'>{status_label}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)


def _show_charts(results):
    try:
        import plotly.graph_objects as go
        import plotly.express as px
        import numpy as np

        # Radar chart
        categories = ["ศีรษะ", "ไหล่", "สะโพก", "ลำตัว", "เข่าซ้าย", "เข่าขวา", "แขนซ้าย", "แขนขวา"]
        keys = ["Head_Lean", "Shoulder_Roll", "Pelvic_Drop", "Torso_Lean",
                "L_Knee_Ang", "R_Knee_Ang", "L_Arm_Ang", "R_Arm_Ang"]

        user_scores = []
        pro_scores = []
        for key in keys:
            bench = PRO_BENCHMARKS.get(key, {"ideal":90,"good":80,"warning":65})
            val = results.get(key, {}).get("mean", bench["ideal"])
            ideal = bench["ideal"]
            good = bench["good"]
            diff = abs(val - ideal)
            score = max(0, 100 - diff * 5)
            user_scores.append(score)
            pro_scores.append(95)

        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=user_scores + [user_scores[0]],
            theta=categories + [categories[0]],
            fill='toself',
            name='คุณ',
            line_color='#00F5FF',
            fillcolor='rgba(0,245,255,0.15)'
        ))
        fig_radar.add_trace(go.Scatterpolar(
            r=pro_scores + [pro_scores[0]],
            theta=categories + [categories[0]],
            fill='toself',
            name='มืออาชีพ',
            line_color='#FF3CAC',
            fillcolor='rgba(255,60,172,0.1)'
        ))
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100], gridcolor='rgba(255,255,255,0.1)'),
                angularaxis=dict(gridcolor='rgba(255,255,255,0.1)')
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#8BA7C7', family='Rajdhani'),
            legend=dict(font=dict(color='#E8F4FD')),
            title=dict(text='เรดาร์ท่าวิ่ง vs มืออาชีพ', font=dict(color='#00F5FF', size=14)),
            margin=dict(t=60, b=20)
        )
        st.plotly_chart(fig_radar, use_container_width=True)

        # Line chart frame data
        if "L_Knee_Ang" in results and "values" in results["L_Knee_Ang"]:
            vals_l = results["L_Knee_Ang"]["values"][:100]
            vals_r = results.get("R_Knee_Ang", {}).get("values", vals_l)[:100]
            frames = list(range(len(vals_l)))

            fig_line = go.Figure()
            fig_line.add_trace(go.Scatter(x=frames, y=vals_l, name='เข่าซ้าย',
                line=dict(color='#00F5FF', width=2)))
            fig_line.add_trace(go.Scatter(x=frames, y=vals_r, name='เข่าขวา',
                line=dict(color='#FF3CAC', width=2)))
            fig_line.add_hline(y=90, line_dash="dash", line_color="#FFD700",
                annotation_text="อุดมคติ 90°", annotation_font_color="#FFD700")
            fig_line.update_layout(
                title=dict(text='มุมเข่ารายเฟรม (100 เฟรมแรก)', font=dict(color='#FF3CAC', size=14)),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(13,31,60,0.5)',
                font=dict(color='#8BA7C7'),
                xaxis=dict(gridcolor='rgba(255,255,255,0.05)', title='เฟรม'),
                yaxis=dict(gridcolor='rgba(255,255,255,0.05)', title='มุม (°)'),
                legend=dict(font=dict(color='#E8F4FD'))
            )
            st.plotly_chart(fig_line, use_container_width=True)

    except ImportError:
        st.markdown("""
        <div class='info-alert'>
            📦 ติดตั้ง plotly เพื่อดูกราฟ: <code>pip install plotly</code>
        </div>
        """, unsafe_allow_html=True)
        # Fallback with streamlit native
        import pandas as pd
        if "L_Knee_Ang" in results and "values" in results["L_Knee_Ang"]:
            vals = results["L_Knee_Ang"]["values"][:100]
            st.line_chart({"เข่าซ้าย": vals})


def _show_summary(results):
    score = results.get("overall_score", 72)
    total_frames = results.get("total_frames", 0)
    fps = results.get("fps", 30)
    duration = total_frames / fps if fps > 0 else 0

    st.markdown(f"""
    <div style='background:var(--bg-card); border:1px solid rgba(0,245,255,0.2);
         border-radius:12px; padding:1.5rem; margin-bottom:1rem;'>
        <div style='font-family:Orbitron; color:#00F5FF; font-size:0.9rem;
             margin-bottom:1rem; text-transform:uppercase;'>📋 สรุปการวิเคราะห์</div>
        <div style='display:grid; grid-template-columns:1fr 1fr 1fr; gap:1rem;'>
            <div style='text-align:center;'>
                <div style='font-family:Orbitron; font-size:2rem; color:#FFD700;'>{total_frames}</div>
                <div style='color:#8BA7C7; font-size:0.85rem;'>เฟรมที่วิเคราะห์</div>
            </div>
            <div style='text-align:center;'>
                <div style='font-family:Orbitron; font-size:2rem; color:#FF3CAC;'>{duration:.1f}s</div>
                <div style='color:#8BA7C7; font-size:0.85rem;'>ความยาววิดีโอ</div>
            </div>
            <div style='font-family:Orbitron; font-size:2rem; color:#39FF14; text-align:center;'>
                <div>{score}/100</div>
                <div style='color:#8BA7C7; font-size:0.85rem;'>คะแนนรวม</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Recommendations
    st.markdown("""
    <div style='font-family:Orbitron; color:#FFD700; font-size:0.9rem;
         text-transform:uppercase; margin:1rem 0 0.5rem;'>
        🎯 แผนพัฒนาลำดับความสำคัญ
    </div>
    """, unsafe_allow_html=True)

    recommendations = [
        ("1", "#FF6B35", "ลด Pelvic Drop", "ฝึก Single-leg Deadlift และ Clamshell เพื่อเสริม Glute Med"),
        ("2", "#FFD700", "ลด Head Lean", "ฝึกมองไปข้างหน้า 10-15 เมตร และเสริมกล้ามเนื้อคอ"),
        ("3", "#39FF14", "เพิ่ม Arm Drive", "แกว่งแขน 90° ขนานกับลำตัว ไม่ข้ามเส้นกลาง"),
        ("4", "#00F5FF", "ปรับ Cadence", "เป้าหมาย 170-180 ก้าวต่อนาที ลด Vertical Oscillation"),
    ]

    for num, color, title, desc in recommendations:
        st.markdown(f"""
        <div style='display:flex; gap:1rem; padding:1rem; background:var(--bg-card);
             border:1px solid {color}33; border-radius:10px; margin-bottom:0.5rem;
             border-left:4px solid {color};'>
            <div style='font-family:Orbitron; font-size:1.5rem; color:{color}; min-width:30px;'>
                {num}
            </div>
            <div>
                <div style='color:#E8F4FD; font-weight:600; margin-bottom:0.3rem;'>{title}</div>
                <div style='color:#8BA7C7; font-size:0.9rem;'>{desc}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    if st.button("💪 สร้างแผนฝึกซ้อม AI", use_container_width=True):
        st.session_state.current_page = "training"
        st.rerun()
