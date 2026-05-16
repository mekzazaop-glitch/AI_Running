import streamlit as st

def show():
    st.markdown("""
    <div style='padding: 1.5rem 0 1rem;'>
        <div style='font-family: Orbitron, monospace; font-size: 1.8rem; font-weight: 900;
             background: linear-gradient(90deg, #8BA7C7, #00F5FF);
             -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
            📚 คู่มือการใช้งาน
        </div>
        <div style='color: #8BA7C7; font-size: 1rem; margin-top: 0.3rem;'>
            วิธีใช้งาน RunAI Coach อย่างละเอียด
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["🚀 เริ่มต้นใช้งาน", "📹 ถ่ายวิดีโอ", "🔬 ผลวิเคราะห์", "⚙️ ติดตั้ง"])

    with tab1:
        _quick_start()
    with tab2:
        _video_guide()
    with tab3:
        _results_guide()
    with tab4:
        _install_guide()


def _quick_start():
    st.markdown("""
    <div style='font-family:Orbitron; color:#00F5FF; font-size:1rem;
         text-transform:uppercase; margin:0.8rem 0; letter-spacing:0.1em;'>
        ⚡ เริ่มใช้งาน 4 ขั้นตอน
    </div>
    """, unsafe_allow_html=True)

    steps = [
        ("1", "#00F5FF", "📤 อัปโหลดวิดีโอ",
         "กดเมนู 'อัปโหลดวิดีโอ' ทางซ้าย → ลากไฟล์วางหรือคลิกเลือกไฟล์ → รองรับ MP4, MOV, AVI",
         ["ขนาดไฟล์สูงสุด 500MB", "ความยาวแนะนำ 10-30 วินาที", "ความละเอียดขั้นต่ำ 720p"]),
        ("2", "#39FF14", "🤖 เริ่มวิเคราะห์",
         "กดเมนู 'วิเคราะห์ท่าวิ่ง' → เลือก 'วิเคราะห์ด้วย YOLOv8' หรือ 'ทดลองด้วย Demo'",
         ["YOLOv8 ต้องติดตั้ง ultralytics", "Demo Mode ใช้ได้ทันทีไม่ต้องติดตั้ง", "ระยะเวลา 30 วิ - 3 นาที"]),
        ("3", "#FFD700", "📊 ดูผลวิเคราะห์",
         "ดูคะแนนรวม → ตรวจสอบมุมข้อต่อ → อ่านคำแนะนำจาก AI Coach",
         ["คะแนน 80+ = ดีมาก", "คะแนน 60-79 = พอใช้", "คะแนต่ำกว่า 60 = ต้องพัฒนา"]),
        ("4", "#FF3CAC", "💪 วางแผนฝึก",
         "กดเมนู 'แผนฝึก AI' → กรอกข้อมูลส่วนตัว → รับแผนฝึกซ้อมเฉพาะบุคคล",
         ["ระบุระดับและเป้าหมาย", "ดูแบบฝึกแก้จุดอ่อน", "ทำตามแผน 4-8 สัปดาห์"]),
    ]

    for num, color, title, desc, tips in steps:
        with st.expander(f"ขั้นตอนที่ {num}: {title}", expanded=(num == "1")):
            st.markdown(f"""
            <div style='color:#E8F4FD; font-size:0.95rem; line-height:1.7;
                 margin-bottom:0.8rem;'>{desc}</div>
            """, unsafe_allow_html=True)
            for tip in tips:
                st.markdown(f"""
                <div style='background:{color}11; border-left:3px solid {color};
                     padding:0.4rem 0.8rem; border-radius:0 6px 6px 0;
                     color:{color}; font-size:0.85rem; margin-bottom:0.3rem;'>
                    ▸ {tip}
                </div>
                """, unsafe_allow_html=True)


def _video_guide():
    st.markdown("""
    <div style='font-family:Orbitron; color:#FF3CAC; font-size:1rem;
         text-transform:uppercase; margin:0.8rem 0; letter-spacing:0.1em;'>
        📹 วิธีถ่ายวิดีโอให้ได้ผลดีที่สุด
    </div>
    """, unsafe_allow_html=True)

    tips = [
        ("📐 ตำแหน่งกล้อง", "#00F5FF", [
            "ตั้งกล้องในแนวนอน (Landscape) เสมอ",
            "วางกล้องสูงระดับสะโพก (ประมาณ 80-100 cm)",
            "ถ่ายจากด้านข้างตรงๆ 90° กับทิศทางการวิ่ง",
            "ระยะห่างจากนักวิ่ง 5-8 เมตร",
            "ไม่ขยับกล้องขณะวิดีโอ (ใช้ขาตั้งกล้อง)",
        ]),
        ("☀️ แสงและพื้นหลัง", "#FFD700", [
            "วิ่งกลางแจ้งในเวลาที่มีแสงสว่างพอ (7-17 น.)",
            "หลีกเลี่ยงแสงย้อนหลัง (sun behind runner)",
            "พื้นหลังควรตัดกับสีเสื้อผ้า",
            "ไม่วิ่งผ่านเงาหรือแสงสลับมืดสว่าง",
        ]),
        ("👗 เครื่องแต่งกาย", "#39FF14", [
            "สวมเสื้อผ้าพอดีตัว ไม่หลวมเกินไป",
            "สีตัดกับพื้นหลัง (เช่น เสื้อสว่างบนพื้นหลังมืด)",
            "ไม่สวมเสื้อกันหนาวหลวมๆ ที่บดบังลำตัว",
            "สวมรองเท้าวิ่งที่ใช้จริง",
        ]),
        ("🏃 การวิ่ง", "#FF3CAC", [
            "วิ่งด้วยความเร็วปกติตามธรรมชาติ ไม่เกร็งกล้าม",
            "วิ่งผ่านหน้ากล้องอย่างน้อย 5-8 ครั้ง",
            "วิ่งตรงๆ ไม่เบี้ยวหรือเลี้ยว",
            "ถ้าวิ่งบนลู่ ปิดป้ายและพื้นหลังให้สะอาด",
            "ถ่าย 10-30 วินาทีก็เพียงพอ",
        ]),
    ]

    cols = st.columns(2)
    for i, (title, color, items) in enumerate(tips):
        with cols[i % 2]:
            st.markdown(f"""
            <div style='background:var(--bg-card); border:1px solid {color}33;
                 border-radius:12px; padding:1.2rem; margin-bottom:1rem;
                 border-top: 3px solid {color};'>
                <div style='font-family:Orbitron; color:{color}; font-size:0.85rem;
                     margin-bottom:0.8rem; text-transform:uppercase;'>{title}</div>
            """, unsafe_allow_html=True)
            for item in items:
                st.markdown(f"""
                <div style='color:#8BA7C7; font-size:0.85rem; padding:0.3rem 0;
                     border-bottom:1px solid rgba(255,255,255,0.04); line-height:1.5;'>
                    ✓ {item}
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    # Common mistakes
    st.markdown("""
    <div style='font-family:Orbitron; color:#FF6B35; font-size:0.9rem;
         text-transform:uppercase; margin:1.2rem 0 0.8rem; letter-spacing:0.1em;'>
        ❌ ข้อผิดพลาดที่พบบ่อย
    </div>
    """, unsafe_allow_html=True)

    mistakes = [
        "ถ่ายจากด้านหน้าหรือด้านหลัง (AI จะวิเคราะห์ได้น้อยลง)",
        "กล้องสั่นหรือขยับตามนักวิ่ง",
        "วิดีโอมืดหรือสว่างเกินไป",
        "นักวิ่งออกจากเฟรมบางส่วน",
        "วิ่งด้วยท่าที่ไม่เป็นธรรมชาติ (รู้ว่าถูกถ่าย)",
    ]
    for m in mistakes:
        st.markdown(f"""
        <div style='background:rgba(255,107,53,0.08); border:1px solid rgba(255,107,53,0.25);
             border-radius:8px; padding:0.6rem 1rem; margin-bottom:0.3rem;
             color:#FF6B35; font-size:0.9rem;'>
            ❌ {m}
        </div>
        """, unsafe_allow_html=True)


def _results_guide():
    st.markdown("""
    <div style='font-family:Orbitron; color:#39FF14; font-size:1rem;
         text-transform:uppercase; margin:0.8rem 0; letter-spacing:0.1em;'>
        🔬 ทำความเข้าใจผลวิเคราะห์
    </div>
    """, unsafe_allow_html=True)

    metrics_explain = [
        ("Head Lean", "มุมเอียงศีรษะ", "°", "< 8°", "#00F5FF",
         "วัดมุมที่ศีรษะเอียงไปข้างหน้าเทียบกับแนวตั้ง ถ้าเอียงมากเกินไปจะเพิ่มแรงกดที่คอและทำให้ท่าวิ่งแย่ลง"),
        ("Shoulder Roll", "การหมุนไหล่", "°", "< 5°", "#FF3CAC",
         "วัดความเอียงของแนวไหล่ซ้าย-ขวา ไหล่แกว่งมากจะเพิ่มแรงต้านและเสียพลังงาน"),
        ("Pelvic Drop", "การตกสะโพก", "°", "< 4°", "#FFD700",
         "วัดความตกของสะโพกด้านที่ไม่ลงน้ำหนัก บ่งบอกความแข็งแรงของ Glute Med"),
        ("Torso Lean", "มุมเอียงลำตัว", "°", "8-12°", "#39FF14",
         "วัดมุมที่ลำตัวเอียงไปข้างหน้า มุมที่เหมาะสมช่วยใช้แรงโน้มถ่วงช่วยขับเคลื่อน"),
        ("Knee Angle", "มุมเข่า", "°", "85-95°", "#FF6B35",
         "วัดมุมงอเข่าขณะก้าว มุมน้อยเกินไป = ก้าวสั้น มุมมากเกินไป = แรกกระแทกมาก"),
    ]

    for metric, label, unit, ideal, color, desc in metrics_explain:
        with st.expander(f"📐 {label} ({metric})"):
            col_a, col_b = st.columns([2, 1])
            with col_a:
                st.markdown(f"""
                <div style='color:#8BA7C7; font-size:0.9rem; line-height:1.7;'>{desc}</div>
                """, unsafe_allow_html=True)
            with col_b:
                st.markdown(f"""
                <div style='text-align:center; background:{color}11; border:1px solid {color}44;
                     border-radius:8px; padding:1rem;'>
                    <div style='font-family:Orbitron; color:{color}; font-size:1.2rem;'>{ideal}</div>
                    <div style='color:#8BA7C7; font-size:0.75rem;'>ค่าอุดมคติ</div>
                </div>
                """, unsafe_allow_html=True)

    # Score legend
    st.markdown("""
    <div style='font-family:Orbitron; color:#FFD700; font-size:0.9rem;
         text-transform:uppercase; margin:1.2rem 0 0.8rem;'>
        🏅 เกณฑ์คะแนน
    </div>
    """, unsafe_allow_html=True)

    grades = [
        ("90-100", "A+", "#00F5FF", "ระดับนักวิ่งมืออาชีพ ท่าวิ่งยอดเยี่ยม"),
        ("80-89", "A", "#39FF14", "ท่าวิ่งดีมาก มีจุดปรับปรุงเล็กน้อย"),
        ("65-79", "B", "#FFD700", "ท่าวิ่งพอใช้ ควรพัฒนา 2-3 จุด"),
        ("50-64", "C", "#FF6B35", "ต้องปรับปรุงหลายจุด เสี่ยงบาดเจ็บ"),
        ("< 50", "D", "#FF3CAC", "ควรพบผู้เชี่ยวชาญหรือโค้ช"),
    ]

    for score, grade, color, desc in grades:
        st.markdown(f"""
        <div style='display:flex; align-items:center; gap:1rem; padding:0.7rem 1rem;
             background:var(--bg-card); border:1px solid {color}33; border-radius:8px;
             margin-bottom:0.3rem;'>
            <div style='font-family:Orbitron; font-size:1.2rem; color:{color}; min-width:40px;'>
                {grade}
            </div>
            <div style='font-family:Space Mono; color:#8BA7C7; font-size:0.85rem; min-width:70px;'>
                {score}
            </div>
            <div style='color:#E8F4FD; font-size:0.9rem;'>{desc}</div>
        </div>
        """, unsafe_allow_html=True)


def _install_guide():
    st.markdown("""
    <div style='font-family:Orbitron; color:#FFD700; font-size:1rem;
         text-transform:uppercase; margin:0.8rem 0; letter-spacing:0.1em;'>
        ⚙️ วิธีติดตั้งและรันเว็บ
    </div>
    """, unsafe_allow_html=True)

    steps_install = [
        ("1️⃣ ติดตั้ง Python", "python.org", "ดาวน์โหลด Python 3.9+ จาก python.org"),
        ("2️⃣ สร้าง Virtual Environment", None,
         "python -m venv runai_env\nsource runai_env/bin/activate  # Mac/Linux\nrunai_env\\Scripts\\activate  # Windows"),
        ("3️⃣ ติดตั้ง Dependencies", None,
         "pip install streamlit ultralytics opencv-python numpy plotly"),
        ("4️⃣ วางไฟล์โปรเจ็กต์", None,
         "วางโฟลเดอร์ running_coach/ ไว้ในที่ที่ต้องการ"),
        ("5️⃣ รันเว็บแอป", None,
         "cd running_coach\nstreamlit run app.py"),
        ("6️⃣ เปิดเบราว์เซอร์", None,
         "เปิด http://localhost:8501\nหรือเบราว์เซอร์จะเปิดอัตโนมัติ"),
    ]

    for step, link, cmd in steps_install:
        st.markdown(f"""
        <div style='background:var(--bg-card); border:1px solid rgba(255,215,0,0.2);
             border-radius:10px; padding:1rem; margin-bottom:0.5rem;'>
            <div style='color:#FFD700; font-weight:700; margin-bottom:0.4rem;'>{step}</div>
            <pre style='background:#050A14; border:1px solid rgba(0,245,255,0.15);
                 border-radius:6px; padding:0.7rem; color:#00F5FF; font-size:0.85rem;
                 overflow-x:auto; white-space:pre-wrap;'>{cmd}</pre>
        </div>
        """, unsafe_allow_html=True)

    # requirements.txt
    st.markdown("""
    <div style='font-family:Orbitron; color:#00F5FF; font-size:0.9rem;
         text-transform:uppercase; margin:1.2rem 0 0.5rem;'>
        📦 requirements.txt
    </div>
    """, unsafe_allow_html=True)

    req_content = """streamlit>=1.28.0
ultralytics>=8.0.0
opencv-python>=4.8.0
numpy>=1.24.0
plotly>=5.17.0"""

    st.code(req_content, language="text")

    st.markdown("""
    <div style='background:rgba(57,255,20,0.06); border:1px solid rgba(57,255,20,0.25);
         border-radius:10px; padding:1rem; margin-top:1rem;'>
        <div style='color:#39FF14; font-family:Orbitron; font-size:0.85rem; margin-bottom:0.5rem;'>
            💡 เคล็ดลับ
        </div>
        <div style='color:#8BA7C7; font-size:0.85rem; line-height:1.7;'>
            • ถ้าไม่มี GPU ใช้ YOLOv8n (nano) จะเร็วที่สุด<br>
            • ใช้ Demo Mode ทดสอบฟีเจอร์ก่อนโดยไม่ต้องวิดีโอจริง<br>
            • Streamlit Cloud: push โค้ดขึ้น GitHub แล้ว deploy ฟรีที่ share.streamlit.io
        </div>
    </div>
    """, unsafe_allow_html=True)
