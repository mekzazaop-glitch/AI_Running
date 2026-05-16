import streamlit as st

def show():
    # Hero Section
    st.markdown("""
    <div style='text-align: center; padding: 3rem 0 2rem;'>
        <div style='font-family: Orbitron, monospace; font-size: 3.5rem; font-weight: 900; line-height: 1.1;
             background: linear-gradient(135deg, #00F5FF 0%, #FF3CAC 50%, #FFD700 100%);
             -webkit-background-clip: text; -webkit-text-fill-color: transparent;
             text-shadow: none; margin-bottom: 1rem;'>
            RunAI Coach
        </div>
        <div style='font-family: Rajdhani, sans-serif; font-size: 1.3rem; color: #8BA7C7;
             letter-spacing: 0.15em; text-transform: uppercase; margin-bottom: 0.5rem;'>
            AI-Powered Elite Running Form Analyzer
        </div>
        <div style='font-family: Space Mono, monospace; font-size: 0.85rem; color: #4A6080;'>
            Powered by YOLOv8 Pose Estimation · Real-time Biomechanics Analysis
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Animated stats bar
    st.markdown("""
    <div style='background: linear-gradient(90deg, rgba(0,245,255,0.05), rgba(255,60,172,0.05));
         border: 1px solid rgba(0,245,255,0.15); border-radius: 12px;
         padding: 1.2rem 2rem; margin: 1rem 0 2rem; display: flex;
         justify-content: space-around; flex-wrap: wrap; gap: 1rem;'>
        <div style='text-align: center;'>
            <div style='font-family: Orbitron; font-size: 1.8rem; color: #00F5FF; font-weight: 900;'>14</div>
            <div style='color: #8BA7C7; font-size: 0.8rem;'>Biomechanical<br>Metrics</div>
        </div>
        <div style='text-align: center;'>
            <div style='font-family: Orbitron; font-size: 1.8rem; color: #FF3CAC; font-weight: 900;'>60fps</div>
            <div style='color: #8BA7C7; font-size: 0.8rem;'>Frame<br>Analysis</div>
        </div>
        <div style='text-align: center;'>
            <div style='font-family: Orbitron; font-size: 1.8rem; color: #39FF14; font-weight: 900;'>AI</div>
            <div style='color: #8BA7C7; font-size: 0.8rem;'>Personal<br>Coach</div>
        </div>
        <div style='text-align: center;'>
            <div style='font-family: Orbitron; font-size: 1.8rem; color: #FFD700; font-weight: 900;'>Pro</div>
            <div style='color: #8BA7C7; font-size: 0.8rem;'>Athlete<br>Database</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Feature cards
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class='metric-card' style='height: 200px;'>
            <div style='font-size: 2.5rem; margin-bottom: 0.8rem;'>🎯</div>
            <div style='font-family: Orbitron; font-size: 1rem; color: #00F5FF; margin-bottom: 0.5rem;'>
                วิเคราะห์ท่าวิ่ง
            </div>
            <div style='color: #8BA7C7; font-size: 0.9rem; line-height: 1.5;'>
                ตรวจจับ 17 จุดบนร่างกายด้วย YOLOv8
                คำนวณมุมข้อต่อ การก้าว และสมดุลลำตัว
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='metric-card' style='height: 200px;'>
            <div style='font-size: 2.5rem; margin-bottom: 0.8rem;'>🏆</div>
            <div style='font-family: Orbitron; font-size: 1rem; color: #FF3CAC; margin-bottom: 0.5rem;'>
                เปรียบมือโปร
            </div>
            <div style='color: #8BA7C7; font-size: 0.9rem; line-height: 1.5;'>
                เทียบกับฐานข้อมูลนักวิ่งระดับโลก
                ค้นหาจุดที่ต้องพัฒนาและวางแผนซ้อม
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class='metric-card' style='height: 200px;'>
            <div style='font-size: 2.5rem; margin-bottom: 0.8rem;'>💪</div>
            <div style='font-family: Orbitron; font-size: 1rem; color: #39FF14; margin-bottom: 0.5rem;'>
                โปรแกรมซ้อม AI
            </div>
            <div style='color: #8BA7C7; font-size: 0.9rem; line-height: 1.5;'>
                สร้างแผนฝึกซ้อมเฉพาะบุคคล
                ตามจุดอ่อนที่ AI ตรวจพบ
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # How it works
    st.markdown("""
    <div style='font-family: Orbitron; font-size: 1.2rem; color: #00F5FF;
         margin: 1.5rem 0 1rem; text-transform: uppercase; letter-spacing: 0.1em;'>
        ⚡ วิธีการทำงาน
    </div>
    """, unsafe_allow_html=True)

    steps = [
        ("1", "📤", "อัปโหลดวิดีโอ", "รองรับ MP4, MOV, AVI ความยาว 5-60 วินาที ถ่ายจากด้านข้างเพื่อผลลัพธ์ที่ดีที่สุด"),
        ("2", "🤖", "AI วิเคราะห์", "YOLOv8 ตรวจจับ 17 จุดร่างกาย คำนวณมุมข้อต่อ 14 ค่าต่อเฟรม"),
        ("3", "📊", "รับรายงาน", "ดูผลวิเคราะห์ละเอียด เทียบกับมาตรฐานมืออาชีพ และรับคำแนะนำเฉพาะ"),
        ("4", "💪", "พัฒนาต่อ", "แผนฝึกซ้อม AI ปรับแต่งตามจุดอ่อนของคุณ ติดตามพัฒนาการรายสัปดาห์"),
    ]

    cols = st.columns(4)
    for i, (num, icon, title, desc) in enumerate(steps):
        with cols[i]:
            color = ["#00F5FF", "#FF3CAC", "#39FF14", "#FFD700"][i]
            st.markdown(f"""
            <div style='text-align: center; padding: 1rem;'>
                <div style='font-family: Orbitron; font-size: 2rem; color: {color};
                     font-weight: 900; margin-bottom: 0.3rem;'>{icon}</div>
                <div style='font-family: Orbitron; font-size: 0.8rem; color: {color};
                     margin-bottom: 0.5rem; text-transform: uppercase;'>STEP {num}</div>
                <div style='color: #E8F4FD; font-weight: 600; margin-bottom: 0.4rem;'>{title}</div>
                <div style='color: #8BA7C7; font-size: 0.85rem; line-height: 1.5;'>{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # CTA
    col_a, col_b, col_c = st.columns([1, 2, 1])
    with col_b:
        if st.button("🚀 เริ่มวิเคราะห์ท่าวิ่งเลย!", use_container_width=True):
            st.session_state.current_page = "upload"
            st.rerun()

    # Metrics analyzed
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-family: Orbitron; font-size: 1rem; color: #8BA7C7;
         margin: 1rem 0; text-align: center; text-transform: uppercase; letter-spacing: 0.1em;'>
        📐 ตัวชี้วัดที่วิเคราะห์
    </div>
    """, unsafe_allow_html=True)

    metrics_info = [
        ("🎯 Head Lean", "มุมเอียงศีรษะ"),
        ("⚖️ Shoulder Roll", "การหมุนไหล่"),
        ("🍑 Pelvic Drop", "การตกสะโพก"),
        ("📐 Torso Lean", "มุมเอียงลำตัว"),
        ("🦵 Hip Angles", "มุมสะโพก L/R"),
        ("🦿 Knee Angles", "มุมเข่า L/R"),
        ("💪 Arm Angles", "มุมแขน L/R"),
        ("👣 Step Length", "ระยะก้าว"),
        ("📊 Vert. Osc.", "การแกว่งแนวตั้ง"),
        ("🏃 Foot Strike", "การลงเท้า"),
    ]

    cols = st.columns(5)
    for i, (icon_title, desc) in enumerate(metrics_info):
        with cols[i % 5]:
            st.markdown(f"""
            <div style='background: var(--bg-card); border: 1px solid var(--border-color);
                 border-radius: 8px; padding: 0.7rem; text-align: center; margin-bottom: 0.5rem;'>
                <div style='font-size: 0.85rem; color: #E8F4FD; font-weight: 600;'>{icon_title}</div>
                <div style='font-size: 0.75rem; color: #8BA7C7;'>{desc}</div>
            </div>
            """, unsafe_allow_html=True)
