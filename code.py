import streamlit as st
import cv2
from ultralytics import YOLO
import numpy as np

st.title("YOLOv8n-Pose กับ Streamlit 🤸‍♂️")

# 1. โหลดโมเดลด้วย Cache เพื่อไม่ให้แอปช้าและป้องกันการแครช
@st.cache_resource
def load_model():
    # ระบบจะดาวน์โหลดไฟล์ yolov8n-pose.pt มาให้อัตโนมัติในครั้งแรก
    return YOLO("yolov8n-pose.pt")

try:
    model = load_model()
    st.success("โหลดโมเดล YOLOv8n-Pose สำเร็จ!")
except Exception as e:
    st.error(f"เกิดข้อผิดพลาดในการโหลดโมเดล: {e}")

# 2. ส่วนอัปโหลดรูปภาพ
uploaded_file = st.file_uploader("เลือกรูปภาพที่ต้องการตรวจจับท่าทาง...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # แปลงไฟล์ที่อัปโหลดให้เป็น OpenCV Image
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, 1)
    
    # สั่งให้โมเดลทำ Pose Estimation
    # conf=0.25 คือค่าความมั่นใจขั้นต่ำ
    results = model(image, conf=0.25)
    
    # วาดจุดและเส้นเชื่อมลงบนภาพ (Plot results)
    annotated_frame = results[0].plot()
    
    # แปลงสีจาก BGR (OpenCV) เป็น RGB (Streamlit)
    annotated_frame_rgb = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
    original_image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # แสดงผลเปรียบเทียบใน Streamlit
    col1, col2 = st.columns(2)
    with col1:
        st.image(original_image_rgb, caption="รูปต้นฉบับ", use_column_width=True)
    with col2:
        st.image(annotated_frame_rgb, caption="ผลลัพธ์ YOLOv8n-Pose", use_column_width=True)