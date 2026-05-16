import streamlit as st
import time
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.analysis import analyze_video, generate_demo_results, PRO_BENCHMARKS, get_metric_status, generate_coaching_feedback

def show():
    st.markdown("""
    <div style='padding: 1.5rem 0 1rem;'>
        <div style='font-family: Orbitron, monospace; font-size: 1.8rem; font-weight: 900;
             background: linear-gradient(90deg, #00F5FF, #39FF14);
             -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
            🤖 วิเคราะห์ท่าวิ่ง
        </div>
        <div style='color: #8BA7C7; font-size: 1rem; margin-top: 0.3rem;'>
            AI YOLOv8 Pose Estimation · Biomechanics Analysis
        </div>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.get("uploaded_video"):
        st.markdown("""
        <div style='background: rgba(255,107,53,0.1); border: 1px solid #FF6B35;
             border-radius: 12px; padding: 2rem; text-align: center; margin: 2rem 0;'>
            <div style='font-size: 3rem; margin-bottom: 1rem;'>⚠️</div>
            <div style='font-family: Orbitron; color: #FF6B35; font-size: 1.1rem; margin-bottom: 0.5rem;'>
                ยังไม่มีวิดีโอ
            </div>
            <div style='color: #8BA7C7;'>กรุณาอัปโหลดวิดีโอก่อนเริ่มวิเคราะห์</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("📤 ไปอัปโหลดวิดีโอ", use_container_width=False):
            st.session_state.current_page = "upload"
            st.rerun()
        return

    # Already analyzed?
    if st.session_state.get("analysis_results"):
        _show_results(st.session_state.analysis_results)
        return

    # Show video info + start button
    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown(f"""
        <div style='background: rgba(0,245,255,0.06); border: 1px solid rgba(0,245,255,0.2);
             border-radius: 12px; padding: 1.2rem; margin-bottom: 1rem;'>
            <div style='color: #00F5FF; font-family: Orbitron; font-size: 0.85rem; margin-bottom: 0.5rem;'>
                📁 วิดีโอที่อัปโหลด
            </div>
            <div style='color: #E8F4FD; font-size: 1rem;'>🎬 {st.session_state.uploaded_video}</div>
            <div style='color: #8BA7C7; font-size: 0.85rem; margin-top: 0.3rem;'>พร้อมวิเคราะห์</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style='background: rgba(57,255,20,0.05); border: 1px solid rgba(57,255,20,0.2);
             border-radius: 12px; padding: 1rem; margin-bottom: 1rem;'>
            <div style='color: #39FF14; font-family: Orbitron; font-size: 0.85rem; margin-bottom: 0.8rem;'>
                🔬 จะวิเคราะห์อะไรบ้าง?
            </div>
            <div style='color: #8BA7C7; font-size: 0.9rem; line-height: 2;'>
                🎯 ตรวจจับ 17 จุดร่างกายด้วย YOLOv8 Pose<br>
                📐 คำนวณมุมข้อต่อ 10 ค่า ทุกเฟรม<br>
                ⚖️ วัดสมดุลซ้าย-ขวา และความสม่ำเสมอ<br>
                👣 วิเคราะห์รูปแบบการก้าวและลงเท้า<br>
                🏆 เปรียบเทียบกับมาตรฐานนักวิ่งมืออาชีพ
            </div>
        </div>
        """, unsafe_allow_html=True)

        col_a, col_b = st.columns(2)
        with col_a:
            start_real = st.button("🤖 วิเคราะห์ด้วย YOLOv8", use_container_width=True)
        with col_b:
            start_demo = st.button("🎮 ทดลองด้วย Demo Data", use_container_width=True)

    with col2:
        st.markdown("""
        <div class='metric-card'>
            <div style='font-family: Orbitron; color: #FFD700; font-size: 0.85rem; margin-bottom: 1rem;'>
                ⏱️ เวลาโดยประมาณ
            </div>
        """, unsafe_allow_html=True)
        times = [
            ("วิดีโอ 10 วินาที", "~30 วิ"),
            ("วิดีโอ 30 วินาที", "~1.5 นาที"),
            ("วิดีโอ 60 วินาที", "~3 นาที"),
        ]
        for label, t in times:
            st.markdown(f"""
            <div style='display:flex; justify-content:space-between; padding:0.4rem 0;
                 border-bottom:1px solid rgba(255,255,255,0.05);'>
                <span style='color:#8BA7C7; font-size:0.85rem;'>{label}</span>
                <span style='color:#FFD700; font-family:Space Mono; font-size:0.85rem;'>{t}</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("""
            <div style='margin-top:0.8rem; color:#4A6080; font-size:0.8rem;'>
                ขึ้นอยู่กับความละเอียดและ CPU/GPU
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Run analysis
    if start_real or start_demo:
        _run_analysis(use_demo=start_demo)


def _run_analysis(use_demo=False):
    progress_placeholder = st.empty()
    status_placeholder = st.empty()

    with progress_placeholder.container():
        st.markdown("""
        <div style='background: var(--bg-card); border: 1px solid rgba(0,245,255,0.3);
             border-radius: 12px; padding: 2rem; text-align: center;'>
            <div style='font-size: 3rem; margin-bottom: 1rem;'>🤖</div>
            <div style='font-family: Orbitron; color: #00F5FF; font-size: 1.1rem; margin-bottom: 1rem;'>
                AI กำลังวิเคราะห์...
            </div>
        </div>
        """, unsafe_allow_html=True)

    steps = [
        (0.1, "⚙️ โหลด YOLOv8 Pose Model..."),
        (0.25, "🎬 อ่านเฟรมวิดีโอ..."),
        (0.45, "🦴 ตรวจจับจุดบนร่างกาย (Keypoints)..."),
        (0.65, "📐 คำนวณมุมข้อต่อและ Biomechanics..."),
        (0.80, "🏆 เปรียบเทียบกับมาตรฐานมืออาชีพ..."),
        (0.95, "📊 สร้างรายงานและคำแนะนำ..."),
    ]

    prog_bar = st.progress(0)
    status_text = st.empty()

    for prog, msg in steps:
        prog_bar.progress(prog)
        status_text.markdown(f"""
        <div style='text-align:center; color:#8BA7C7; font-size:0.9rem; padding:0.5rem;'>{msg}</div>
        """, unsafe_allow_html=True)
        time.sleep(0.6 if use_demo else 0.8)

    # Actually run
    try:
        video_path = st.session_state.get("video_path", "")
        results = analyze_video(video_path, use_demo=use_demo or not video_path)
        st.session_state.analysis_results = results
    except Exception as e:
        results = generate_demo_results()
        st.session_state.analysis_results = results

    prog_bar.progress(1.0)
    status_text.markdown("""
    <div style='text-align:center; color:#39FF14; font-size:1rem; padding:0.5rem;'>
        ✅ วิเคราะห์เสร็จสมบูรณ์!
    </div>
    """, unsafe_allow_html=True)
    time.sleep(0.8)
    progress_placeholder.empty()
    status_text.empty()
    prog_bar.empty()
    st.rerun()


def _show_results(results):
    is_demo = results.get("is_demo", False)
    if is_demo:
        st.markdown("""
        <div style='background:rgba(255,215,0,0.08); border:1px solid rgba(255,215,0,0.3);
             border-radius:8px; padding:0.6rem 1rem; margin-bottom:1rem; color:#FFD700; font-size:0.9rem;'>
            🎮 กำลังแสดงข้อมูล Demo — อัปโหลดวิดีโอจริงเพื่อผลลัพธ์ที่แม่นยำ
        </div>
        """, unsafe_allow_html=True)

    # Overall score
    score = results.get("overall_score", 72)
    score_color = "#39FF14" if score >= 80 else "#FFD700" if score >= 60 else "#FF6B35"
    score_label = "ยอดเยี่ยม" if score >= 80 else "ดี" if score >= 65 else "ต้องพัฒนา"

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
        <div style='text-align:center; padding: 1.5rem; background: var(--bg-card);
             border: 2px solid {score_color}; border-radius: 16px; margin-bottom: 1.5rem;
             box-shadow: 0 0 30px {score_color}33;'>
            <div style='font-family:Orbitron; font-size:0.9rem; color:#8BA7C7;
                 text-transform:uppercase; letter-spacing:0.15em; margin-bottom:0.5rem;'>
                คะแนนรวม
            </div>
            <div style='font-family:Orbitron; font-size:4rem; font-weight:900; color:{score_color};
                 line-height:1; margin-bottom:0.3rem;'>{score}</div>
            <div style='font-size:2rem;'>/ 100</div>
            <div style='font-family:Orbitron; color:{score_color}; font-size:1rem;
                 margin-top:0.5rem; text-transform:uppercase;'>{score_label}</div>
        </div>
        """, unsafe_allow_html=True)

    # Key metrics grid
    st.markdown("""
    <div style='font-family:Orbitron; font-size:1rem; color:#00F5FF;
         margin: 1rem 0 0.8rem; text-transform:uppercase; letter-spacing:0.1em;'>
        📐 ผลวิเคราะห์รายตัวชี้วัด
    </div>
    """, unsafe_allow_html=True)

    metric_keys = [
        ("Head_Lean", "มุมเอียงศีรษะ", "°"),
        ("Shoulder_Roll", "การหมุนไหล่", "°"),
        ("Pelvic_Drop", "การตกสะโพก", "°"),
        ("Torso_Lean", "มุมเอียงลำตัว", "°"),
        ("L_Knee_Ang", "มุมเข่าซ้าย", "°"),
        ("R_Knee_Ang", "มุมเข่าขวา", "°"),
        ("L_Hip_Ang", "มุมสะโพกซ้าย", "°"),
        ("R_Hip_Ang", "มุมสะโพกขวา", "°"),
        ("L_Arm_Ang", "มุมแขนซ้าย", "°"),
        ("R_Arm_Ang", "มุมแขนขวา", "°"),
    ]

    cols = st.columns(2)
    for i, (key, label, unit) in enumerate(metric_keys):
        if key not in results:
            continue
        val = results[key]["mean"]
        bench = PRO_BENCHMARKS.get(key, {"ideal": 90, "good": 80, "warning": 65})
        status, color, status_label = get_metric_status(val, bench)

        with cols[i % 2]:
            ideal = bench["ideal"]
            pct = min(max(int((1 - abs(val - ideal) / max(ideal, 1)) * 100), 0), 100)
            st.markdown(f"""
            <div style='background: var(--bg-card); border: 1px solid {color}33;
                 border-radius: 10px; padding: 0.9rem; margin-bottom: 0.7rem;
                 border-left: 3px solid {color};'>
                <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:0.4rem;'>
                    <span style='color:#E8F4FD; font-weight:600; font-size:0.9rem;'>{label}</span>
                    <span style='background:{color}22; color:{color}; padding:0.15rem 0.5rem;
                          border-radius:20px; font-size:0.75rem; font-family:Space Mono;'>{status_label}</span>
                </div>
                <div style='display:flex; align-items:baseline; gap:0.3rem; margin-bottom:0.4rem;'>
                    <span style='font-family:Orbitron; font-size:1.5rem; font-weight:700;
                          color:{color};'>{val:.1f}</span>
                    <span style='color:#8BA7C7; font-size:0.85rem;'>{unit}</span>
                    <span style='color:#4A6080; font-size:0.75rem; margin-left:0.3rem;'>
                        (อุดมคติ: {ideal}{unit})
                    </span>
                </div>
                <div style='background:#0A1628; border-radius:4px; height:6px; overflow:hidden;'>
                    <div style='background:{color}; width:{pct}%; height:100%;
                         border-radius:4px; transition:width 1s ease;'></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Foot strike & step
    st.markdown("""
    <div style='font-family:Orbitron; font-size:1rem; color:#FF3CAC;
         margin: 1.2rem 0 0.8rem; text-transform:uppercase; letter-spacing:0.1em;'>
        👣 รูปแบบการก้าวและลงเท้า
    </div>
    """, unsafe_allow_html=True)

    col_a, col_b, col_c = st.columns(3)
    strike = results.get("Strike", {})
    step = results.get("Step_Length_px", {}).get("mean", 148)
    vert = results.get("Vert_Osc", {}).get("range", 38)

    with col_a:
        st.markdown(f"""
        <div class='metric-card' style='text-align:center;'>
            <div style='font-size:2rem; margin-bottom:0.5rem;'>👣</div>
            <div style='font-family:Orbitron; color:#00F5FF; font-size:0.8rem; margin-bottom:0.5rem;'>
                FOOT STRIKE
            </div>
            <div style='color:#E8F4FD; font-size:0.9rem;'>
                ซ้าย: <strong style='color:#39FF14;'>{strike.get('left_pct',50):.0f}%</strong><br>
                ขวา: <strong style='color:#FF3CAC;'>{strike.get('right_pct',50):.0f}%</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_b:
        step_color = "#39FF14" if 120 <= step <= 180 else "#FFD700"
        st.markdown(f"""
        <div class='metric-card' style='text-align:center;'>
            <div style='font-size:2rem; margin-bottom:0.5rem;'>📏</div>
            <div style='font-family:Orbitron; color:#FF3CAC; font-size:0.8rem; margin-bottom:0.5rem;'>
                STEP LENGTH
            </div>
            <div style='font-family:Orbitron; font-size:1.5rem; color:{step_color};'>{step:.0f}</div>
            <div style='color:#8BA7C7; font-size:0.75rem;'>pixels (เฉลี่ย)</div>
        </div>
        """, unsafe_allow_html=True)

    with col_c:
        vert_color = "#39FF14" if vert < 40 else "#FFD700" if vert < 60 else "#FF6B35"
        st.markdown(f"""
        <div class='metric-card' style='text-align:center;'>
            <div style='font-size:2rem; margin-bottom:0.5rem;'>📊</div>
            <div style='font-family:Orbitron; color:#FFD700; font-size:0.8rem; margin-bottom:0.5rem;'>
                VERT. OSC.
            </div>
            <div style='font-family:Orbitron; font-size:1.5rem; color:{vert_color};'>{vert:.1f}</div>
            <div style='color:#8BA7C7; font-size:0.75rem;'>pixels (range)</div>
        </div>
        """, unsafe_allow_html=True)

    # AI Coaching feedback
    st.markdown("""
    <div style='font-family:Orbitron; font-size:1rem; color:#FFD700;
         margin: 1.5rem 0 0.8rem; text-transform:uppercase; letter-spacing:0.1em;'>
        💬 คำแนะนำจาก AI Coach
    </div>
    """, unsafe_allow_html=True)

    feedback = generate_coaching_feedback(results)
    for issue in feedback["issues"]:
        sev_color = "#FF6B35" if issue["severity"] == "high" else "#FFD700"
        icon = "🔴" if issue["severity"] == "high" else "🟡"
        st.markdown(f"""
        <div style='background:rgba(255,107,53,0.08); border:1px solid {sev_color}55;
             border-radius:8px; padding:0.8rem 1rem; margin-bottom:0.5rem;
             border-left:3px solid {sev_color};'>
            <span style='color:{sev_color};'>{icon} <strong>แก้ไขด่วน:</strong></span>
            <span style='color:#E8F4FD; margin-left:0.5rem;'>{issue["message"]}</span>
        </div>
        """, unsafe_allow_html=True)

    for strength in feedback["strengths"]:
        st.markdown(f"""
        <div style='background:rgba(57,255,20,0.06); border:1px solid rgba(57,255,20,0.3);
             border-radius:8px; padding:0.8rem 1rem; margin-bottom:0.5rem;
             border-left:3px solid #39FF14;'>
            <span style='color:#39FF14;'>✅ <strong>จุดแข็ง:</strong></span>
            <span style='color:#E8F4FD; margin-left:0.5rem;'>{strength["message"]}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_r1, col_r2, col_r3 = st.columns(3)
    with col_r1:
        if st.button("📊 ดูรายงานละเอียด", use_container_width=True):
            st.session_state.current_page = "report"
            st.rerun()
    with col_r2:
        if st.button("🏆 เปรียบกับมือโปร", use_container_width=True):
            st.session_state.current_page = "compare"
            st.rerun()
    with col_r3:
        if st.button("🔄 วิเคราะห์ใหม่", use_container_width=True):
            st.session_state.analysis_results = None
            st.rerun()
