import streamlit as st
import os
import tempfile
import time

def show():
    st.markdown("""
    <div style='padding: 1.5rem 0 1rem;'>
        <div style='font-family: Orbitron, monospace; font-size: 1.8rem; font-weight: 900;
             background: linear-gradient(90deg, #00F5FF, #FF3CAC);
             -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
            📤 อัปโหลดวิดีโอ
        </div>
        <div style='color: #8BA7C7; font-size: 1rem; margin-top: 0.3rem;'>
            อัปโหลดคลิปวิ่งของคุณเพื่อเริ่มการวิเคราะห์
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    with col1:
        # Tips before upload
        st.markdown("""
        <div style='background: rgba(0,245,255,0.06); border: 1px solid rgba(0,245,255,0.25);
             border-radius: 12px; padding: 1.2rem; margin-bottom: 1.5rem;'>
            <div style='font-family: Orbitron; font-size: 0.9rem; color: #00F5FF;
                 margin-bottom: 0.8rem; text-transform: uppercase;'>
                💡 เคล็ดลับเพื่อผลลัพธ์ที่ดีที่สุด
            </div>
            <div style='color: #8BA7C7; font-size: 0.9rem; line-height: 1.8;'>
                📹 <strong style='color:#E8F4FD;'>ตำแหน่งกล้อง:</strong> ถ่ายจากด้านข้าง ระดับสะโพก ไม่ขยับกล้อง<br>
                ☀️ <strong style='color:#E8F4FD;'>แสง:</strong> แสงสว่างเพียงพอ ไม่มีเงาบดบัง<br>
                👗 <strong style='color:#E8F4FD;'>เครื่องแต่งกาย:</strong> เสื้อผ้าพอดีตัว สีตัดกับพื้นหลัง<br>
                ⏱️ <strong style='color:#E8F4FD;'>ความยาว:</strong> 5-60 วินาที ความละเอียด 720p ขึ้นไป<br>
                🏃 <strong style='color:#E8F4FD;'>วิธีวิ่ง:</strong> วิ่งด้วยความเร็วปกติ ผ่านกล้องอย่างน้อย 5 รอบ
            </div>
        </div>
        """, unsafe_allow_html=True)

        # File uploader - styled
        st.markdown("""
        <div style='font-family: Orbitron; font-size: 0.85rem; color: #00F5FF;
             text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.5rem;'>
            เลือกไฟล์วิดีโอ
        </div>
        """, unsafe_allow_html=True)

        uploaded_file = st.file_uploader(
            label="วิดีโอ",
            type=["mp4", "mov", "avi", "mkv"],
            help="รองรับ: MP4, MOV, AVI, MKV (สูงสุด 500MB)",
            label_visibility="collapsed"
        )

        if uploaded_file is not None:
            # Show file info
            file_size_mb = uploaded_file.size / (1024 * 1024)
            st.markdown(f"""
            <div style='background: rgba(57,255,20,0.08); border: 1px solid rgba(57,255,20,0.3);
                 border-radius: 10px; padding: 1rem; margin: 1rem 0;'>
                <div style='font-family: Orbitron; color: #39FF14; font-size: 0.85rem; margin-bottom: 0.5rem;'>
                    ✅ ไฟล์พร้อมแล้ว
                </div>
                <div style='color: #E8F4FD;'>📁 {uploaded_file.name}</div>
                <div style='color: #8BA7C7; font-size: 0.85rem;'>
                    ขนาด: {file_size_mb:.1f} MB &nbsp;|&nbsp; ประเภท: {uploaded_file.type}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Preview video
            st.markdown("""
            <div style='font-family: Orbitron; font-size: 0.85rem; color: #8BA7C7;
                 text-transform: uppercase; margin: 1rem 0 0.5rem;'>
                🎬 ดูตัวอย่าง
            </div>
            """, unsafe_allow_html=True)
            st.video(uploaded_file)

            # Save to temp file
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
                tmp.write(uploaded_file.read())
                tmp_path = tmp.name

            st.session_state.uploaded_video = uploaded_file.name
            st.session_state.video_path = tmp_path
            st.session_state.analysis_results = None  # Reset previous analysis

            st.markdown("<br>", unsafe_allow_html=True)

            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.button("🤖 เริ่มวิเคราะห์ทันที!", use_container_width=True):
                    st.session_state.current_page = "analyze"
                    st.rerun()
            with col_btn2:
                if st.button("🔄 เปลี่ยนไฟล์", use_container_width=True):
                    st.session_state.uploaded_video = None
                    st.session_state.video_path = None
                    st.rerun()

    with col2:
        # Format requirements
        st.markdown("""
        <div class='metric-card' style='margin-bottom: 1rem;'>
            <div style='font-family: Orbitron; font-size: 0.85rem; color: #FF3CAC;
                 margin-bottom: 1rem; text-transform: uppercase;'>📋 รองรับ</div>
        """, unsafe_allow_html=True)

        formats = [
            ("🎬 MP4", "แนะนำ"),
            ("🎥 MOV", "iPhone/Mac"),
            ("📹 AVI", "Windows"),
            ("🎞️ MKV", "HD Video"),
        ]
        for fmt, note in formats:
            st.markdown(f"""
                <div style='display: flex; justify-content: space-between;
                     padding: 0.4rem 0; border-bottom: 1px solid rgba(255,255,255,0.05);'>
                    <span style='color: #E8F4FD; font-size: 0.9rem;'>{fmt}</span>
                    <span style='color: #8BA7C7; font-size: 0.8rem;'>{note}</span>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        # Resolution guide
        st.markdown("""
        <div class='metric-card' style='margin-bottom: 1rem;'>
            <div style='font-family: Orbitron; font-size: 0.85rem; color: #FFD700;
                 margin-bottom: 1rem; text-transform: uppercase;'>📐 ความละเอียด</div>
        """, unsafe_allow_html=True)

        resolutions = [
            ("480p", "ขั้นต่ำ", "#FF6B35"),
            ("720p", "แนะนำ", "#39FF14"),
            ("1080p", "ดีมาก", "#00F5FF"),
            ("4K", "ยอดเยี่ยม", "#FF3CAC"),
        ]
        for res, label, color in resolutions:
            st.markdown(f"""
                <div style='display: flex; justify-content: space-between; align-items: center;
                     padding: 0.4rem 0; border-bottom: 1px solid rgba(255,255,255,0.05);'>
                    <span style='font-family: Space Mono; color: {color}; font-size: 0.85rem;'>{res}</span>
                    <span style='color: #8BA7C7; font-size: 0.8rem;'>{label}</span>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        # Max file size
        st.markdown("""
        <div style='background: rgba(255,215,0,0.08); border: 1px solid rgba(255,215,0,0.3);
             border-radius: 10px; padding: 1rem; text-align: center;'>
            <div style='font-size: 2rem; margin-bottom: 0.3rem;'>💾</div>
            <div style='font-family: Orbitron; color: #FFD700; font-size: 1.2rem;'>500 MB</div>
            <div style='color: #8BA7C7; font-size: 0.8rem;'>ขนาดไฟล์สูงสุด</div>
        </div>
        """, unsafe_allow_html=True)
