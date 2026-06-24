"""
run_analyzer.py — วิเคราะห์ท่าวิ่งจากวิดีโอด้านข้าง
ต้องการ: pip install mediapipe opencv-python numpy pandas

วิธีใช้:
  python run_analyzer.py --video myvideo.mp4
  python run_analyzer.py --folder ./videos/          # วิเคราะห์ทุกวิดีโอในโฟลเดอร์
  python run_analyzer.py --video myvideo.mp4 --show  # แสดงผลแบบ realtime
"""

import cv2
import mediapipe as mp
import numpy as np
import pandas as pd
import argparse
import os
import json
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Optional

# ─── MediaPipe setup ────────────────────────────────────────────────────────
mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils
mp_style = mp.solutions.drawing_styles


# ─── Data classes ────────────────────────────────────────────────────────────
@dataclass
class FrameData:
    frame_idx: int
    timestamp_sec: float
    # มุมข้อต่อ (องศา)
    knee_angle: Optional[float] = None        # มุมเข่าขณะ foot strike
    hip_angle: Optional[float] = None         # มุม hip flexion
    ankle_angle: Optional[float] = None       # มุม ankle dorsiflexion
    trunk_lean: Optional[float] = None        # องศาเอียงลำตัว (forward lean)
    # ตำแหน่ง foot strike
    foot_x_rel_hip: Optional[float] = None   # ตำแหน่งเท้าเทียบกับสะโพก (+= ข้างหน้า)
    # keypoints ดิบ (สำหรับ train AI)
    keypoints: dict = field(default_factory=dict)


@dataclass
class VideoReport:
    filename: str
    total_frames: int
    fps: float
    duration_sec: float
    avg_knee_angle: Optional[float] = None
    avg_hip_angle: Optional[float] = None
    avg_trunk_lean: Optional[float] = None
    avg_foot_x_rel_hip: Optional[float] = None
    feedback: list = field(default_factory=list)
    score: int = 0   # 0-100


# ─── Geometry helpers ────────────────────────────────────────────────────────
def angle_between(a, b, c) -> float:
    """คำนวณมุมที่จุด b (องศา) จาก 3 จุด a-b-c"""
    a, b, c = np.array(a), np.array(b), np.array(c)
    ba = a - b
    bc = c - b
    cosine = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc) + 1e-8)
    return float(np.degrees(np.arccos(np.clip(cosine, -1.0, 1.0))))


def trunk_lean_angle(shoulder, hip) -> float:
    """
    คำนวณมุมเอียงลำตัวจากแนวดิ่ง
    ค่าบวก = เอนไปข้างหน้า (ดี), ค่าลบ = เอนไปข้างหลัง
    """
    dx = shoulder[0] - hip[0]
    dy = hip[1] - shoulder[1]   # y กลับด้านใน image coords
    angle = np.degrees(np.arctan2(dx, dy))
    return float(angle)


# ─── Landmark extraction ─────────────────────────────────────────────────────
LANDMARK = mp_pose.PoseLandmark

# landmark indices สำหรับมุมข้าง (ใช้ฝั่งที่มองเห็น)
SIDE_LANDMARKS = {
    "left_shoulder":  LANDMARK.LEFT_SHOULDER,
    "left_hip":       LANDMARK.LEFT_HIP,
    "left_knee":      LANDMARK.LEFT_KNEE,
    "left_ankle":     LANDMARK.LEFT_ANKLE,
    "left_heel":      LANDMARK.LEFT_HEEL,
    "left_foot_index":LANDMARK.LEFT_FOOT_INDEX,
    "right_shoulder": LANDMARK.RIGHT_SHOULDER,
    "right_hip":      LANDMARK.RIGHT_HIP,
    "right_knee":     LANDMARK.RIGHT_KNEE,
    "right_ankle":    LANDMARK.RIGHT_ANKLE,
    "right_heel":     LANDMARK.RIGHT_HEEL,
    "right_foot_index":LANDMARK.RIGHT_FOOT_INDEX,
}


def get_xy(landmarks, name: str, w: int, h: int) -> tuple:
    lm = landmarks[SIDE_LANDMARKS[name].value]
    return (lm.x * w, lm.y * h)


def extract_frame_metrics(landmarks, w: int, h: int, frame_idx: int, ts: float) -> FrameData:
    """แยก metrics จาก landmarks 1 frame"""
    try:
        # ดึง keypoints ฝั่งซ้าย
        l_shoulder = get_xy(landmarks, "left_shoulder", w, h)
        l_hip      = get_xy(landmarks, "left_hip", w, h)
        l_knee     = get_xy(landmarks, "left_knee", w, h)
        l_ankle    = get_xy(landmarks, "left_ankle", w, h)
        l_heel     = get_xy(landmarks, "left_heel", w, h)

        r_shoulder = get_xy(landmarks, "right_shoulder", w, h)
        r_hip      = get_xy(landmarks, "right_hip", w, h)
        r_knee     = get_xy(landmarks, "right_knee", w, h)
        r_ankle    = get_xy(landmarks, "right_ankle", w, h)

        # เลือกฝั่งที่มีค่า visibility สูงกว่า
        lm = landmarks
        l_vis = (lm[LANDMARK.LEFT_HIP.value].visibility +
                 lm[LANDMARK.LEFT_KNEE.value].visibility) / 2
        r_vis = (lm[LANDMARK.RIGHT_HIP.value].visibility +
                 lm[LANDMARK.RIGHT_KNEE.value].visibility) / 2

        if l_vis >= r_vis:
            shoulder, hip, knee, ankle, heel = l_shoulder, l_hip, l_knee, l_ankle, l_heel
        else:
            shoulder, hip, knee, ankle, heel = r_shoulder, r_hip, r_knee, r_ankle, get_xy(landmarks, "right_heel", w, h)

        # คำนวณมุม
        knee_ang  = angle_between(hip, knee, ankle)
        hip_ang   = angle_between(shoulder, hip, knee)
        ankle_ang = angle_between(knee, ankle, heel)
        trunk     = trunk_lean_angle(shoulder, hip)

        # foot position relative to hip (normalized by image width)
        foot_rel = (heel[0] - hip[0]) / w

        # เก็บ keypoints ดิบ (normalized 0-1)
        kp = {}
        for name, idx in SIDE_LANDMARKS.items():
            lm_pt = landmarks[idx.value]
            kp[name] = {"x": round(lm_pt.x, 4),
                        "y": round(lm_pt.y, 4),
                        "z": round(lm_pt.z, 4),
                        "vis": round(lm_pt.visibility, 3)}

        return FrameData(
            frame_idx=frame_idx,
            timestamp_sec=round(ts, 3),
            knee_angle=round(knee_ang, 1),
            hip_angle=round(hip_ang, 1),
            ankle_angle=round(ankle_ang, 1),
            trunk_lean=round(trunk, 1),
            foot_x_rel_hip=round(foot_rel, 4),
            keypoints=kp,
        )

    except Exception:
        return FrameData(frame_idx=frame_idx, timestamp_sec=round(ts, 3))


# ─── Feedback engine ──────────────────────────────────────────────────────────
"""
Reference ranges (งานวิจัย biomechanics นักวิ่งระดับดี):
  - Knee angle at foot strike: 20–30° (flexion) → จาก full extension = 150–165°
    ในที่นี้วัดมุมภายใน hip-knee-ankle ดังนั้น "ดี" ≈ 155–175°
  - Hip angle: 150–170° (ไม่ overstriding)
  - Trunk lean forward: 5–15°
  - Foot strike: เท้าไม่ควรตกหน้า hip มาก (foot_x_rel_hip < 0.08)
"""

RULES = [
    {
        "key": "knee_angle",
        "label": "มุมเข่าตอน foot strike",
        "good_min": 148, "good_max": 178,
        "low_msg":  "⚠️ เข่างอมากเกินไป (overstriding/หน้าแข้งตั้งชัน) — ลองลดก้าวให้สั้นลง",
        "high_msg": "⚠️ เข่าเหยียดตึงเกินไปตอนเท้าแตะพื้น — เสี่ยงต่อ heel strike แรง",
        "ok_msg":   "✅ มุมเข่าอยู่ในเกณฑ์ดี",
    },
    {
        "key": "hip_angle",
        "label": "มุม Hip flexion",
        "good_min": 145, "good_max": 175,
        "low_msg":  "⚠️ Hip flexion มากเกิน — อาจก้าวยาวเกินไปหรือก้มตัวมาก",
        "high_msg": "⚠️ Hip extension น้อย — ลำตัวตั้งตรงเกิน หรือก้าวสั้นเกิน",
        "ok_msg":   "✅ มุม Hip อยู่ในเกณฑ์ดี",
    },
    {
        "key": "trunk_lean",
        "label": "การเอนลำตัวไปข้างหน้า",
        "good_min": 4, "good_max": 15,
        "low_msg":  "⚠️ ลำตัวตั้งตรงหรือเอนหลังเกิน — ลองเอนตัวไปข้างหน้านิดนึง (~5–10°)",
        "high_msg": "⚠️ เอนลำตัวไปข้างหน้ามากเกิน — อาจทำให้ก้มหลังและเมื่อยต้นคอ",
        "ok_msg":   "✅ การเอนลำตัวอยู่ในเกณฑ์ดี",
    },
    {
        "key": "foot_x_rel_hip",
        "label": "ตำแหน่ง foot strike เทียบ hip",
        "good_min": -0.15, "good_max": 0.06,
        "low_msg":  "ℹ️ เท้าตกหลัง hip มาก (ไม่ปกติในมุมข้าง)",
        "high_msg": "⚠️ เท้าตกหน้า hip มาก (overstriding) — เพิ่ม cadence หรือลดก้าว",
        "ok_msg":   "✅ ตำแหน่ง foot strike ดี (ใต้ hip)",
    },
]


def generate_feedback(report_data: dict) -> tuple[list, int]:
    feedback = []
    score = 100
    for rule in RULES:
        val = report_data.get(rule["key"])
        if val is None:
            continue
        if val < rule["good_min"]:
            feedback.append(rule["low_msg"])
            score -= 15
        elif val > rule["good_max"]:
            feedback.append(rule["high_msg"])
            score -= 15
        else:
            feedback.append(rule["ok_msg"])
    return feedback, max(0, score)


# ─── Main analyzer ────────────────────────────────────────────────────────────
def analyze_video(video_path: str, show: bool = False, output_dir: str = ".") -> VideoReport:
    path = Path(video_path)
    print(f"\n{'='*60}")
    print(f"📹 กำลังวิเคราะห์: {path.name}")

    cap = cv2.VideoCapture(str(path))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    all_frames: list[FrameData] = []

    with mp_pose.Pose(
        static_image_mode=False,
        model_complexity=1,
        smooth_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    ) as pose:

        frame_idx = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            ts = frame_idx / fps
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(rgb)

            if results.pose_landmarks:
                fd = extract_frame_metrics(
                    results.pose_landmarks.landmark, w, h, frame_idx, ts
                )
                all_frames.append(fd)

                if show:
                    # วาด skeleton
                    mp_draw.draw_landmarks(
                        frame,
                        results.pose_landmarks,
                        mp_pose.POSE_CONNECTIONS,
                        landmark_drawing_spec=mp_style.get_default_pose_landmarks_style(),
                    )
                    # แสดงมุม live
                    texts = [
                        f"Knee: {fd.knee_angle:.0f}°",
                        f"Hip:  {fd.hip_angle:.0f}°",
                        f"Trunk: {fd.trunk_lean:.0f}°",
                    ]
                    for i, t in enumerate(texts):
                        cv2.putText(frame, t, (10, 30 + i*28),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,100), 2)

            if show:
                cv2.imshow(f"Running Analyzer — {path.name}", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            frame_idx += 1
            if frame_idx % 100 == 0:
                print(f"  ประมวลผลแล้ว {frame_idx}/{total} frames")

    cap.release()
    if show:
        cv2.destroyAllWindows()

    # ─── สรุปค่าเฉลี่ย ────────────────────────────────────────────
    def safe_mean(key):
        vals = [getattr(f, key) for f in all_frames if getattr(f, key) is not None]
        return round(float(np.mean(vals)), 1) if vals else None

    report = VideoReport(
        filename=path.name,
        total_frames=total,
        fps=round(fps, 1),
        duration_sec=round(total / fps, 1),
        avg_knee_angle=safe_mean("knee_angle"),
        avg_hip_angle=safe_mean("hip_angle"),
        avg_trunk_lean=safe_mean("trunk_lean"),
        avg_foot_x_rel_hip=safe_mean("foot_x_rel_hip"),
    )

    report.feedback, report.score = generate_feedback({
        "knee_angle":      report.avg_knee_angle,
        "hip_angle":       report.avg_hip_angle,
        "trunk_lean":      report.avg_trunk_lean,
        "foot_x_rel_hip":  report.avg_foot_x_rel_hip,
    })

    # ─── บันทึก CSV keypoints (สำหรับ train AI) ──────────────────
    out_dir = Path(output_dir)
    out_dir.mkdir(exist_ok=True)
    stem = path.stem

    rows = []
    for fd in all_frames:
        row = {
            "video": path.name,
            "frame": fd.frame_idx,
            "time_sec": fd.timestamp_sec,
            "knee_angle": fd.knee_angle,
            "hip_angle": fd.hip_angle,
            "ankle_angle": fd.ankle_angle,
            "trunk_lean": fd.trunk_lean,
            "foot_x_rel_hip": fd.foot_x_rel_hip,
        }
        # flatten keypoints
        for kp_name, kp_val in fd.keypoints.items():
            row[f"{kp_name}_x"] = kp_val["x"]
            row[f"{kp_name}_y"] = kp_val["y"]
            row[f"{kp_name}_z"] = kp_val["z"]
            row[f"{kp_name}_vis"] = kp_val["vis"]
        rows.append(row)

    csv_path = out_dir / f"{stem}_keypoints.csv"
    pd.DataFrame(rows).to_csv(csv_path, index=False)

    # บันทึก JSON report
    json_path = out_dir / f"{stem}_report.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(asdict(report), f, ensure_ascii=False, indent=2)

    # ─── พิมพ์ผล ──────────────────────────────────────────────────
    print(f"\n📊 ผลวิเคราะห์: {path.name}")
    print(f"   ความยาว: {report.duration_sec:.1f} วินาที | {report.total_frames} frames @ {report.fps} fps")
    print(f"   ─────────────────────────────────────────")
    print(f"   มุมเข่าเฉลี่ย:       {report.avg_knee_angle}°  (ดี: 148–178°)")
    print(f"   มุม Hip เฉลี่ย:      {report.avg_hip_angle}°  (ดี: 145–175°)")
    print(f"   เอนลำตัวเฉลี่ย:      {report.avg_trunk_lean}°  (ดี: 4–15°)")
    print(f"   Foot strike (rel):  {report.avg_foot_x_rel_hip}  (ดี: < 0.06)")
    print(f"   ─────────────────────────────────────────")
    print(f"   🏆 คะแนนท่าวิ่ง: {report.score}/100")
    print(f"\n   📝 Feedback:")
    for fb in report.feedback:
        print(f"      {fb}")
    print(f"\n   💾 บันทึกแล้ว:")
    print(f"      keypoints CSV → {csv_path}")
    print(f"      report JSON   → {json_path}")

    return report


# ─── Batch mode ──────────────────────────────────────────────────────────────
def analyze_folder(folder: str, show: bool, output_dir: str):
    folder_path = Path(folder)
    videos = list(folder_path.glob("*.mp4")) + \
             list(folder_path.glob("*.mov")) + \
             list(folder_path.glob("*.avi"))

    if not videos:
        print(f"❌ ไม่พบไฟล์วิดีโอใน {folder}")
        return

    print(f"📂 พบ {len(videos)} วิดีโอใน {folder}")
    all_reports = []
    for v in videos:
        r = analyze_video(str(v), show=show, output_dir=output_dir)
        all_reports.append(asdict(r))

    # สรุป summary ทุกวิดีโอ
    summary_path = Path(output_dir) / "summary.csv"
    summary_cols = ["filename", "duration_sec", "avg_knee_angle",
                    "avg_hip_angle", "avg_trunk_lean", "avg_foot_x_rel_hip", "score"]
    pd.DataFrame(all_reports)[summary_cols].to_csv(summary_path, index=False)
    print(f"\n{'='*60}")
    print(f"✅ เสร็จทั้งหมด! Summary → {summary_path}")


# ─── CLI ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="วิเคราะห์ท่าวิ่งด้านข้างด้วย MediaPipe")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--video",  help="path ของวิดีโอเดียว")
    group.add_argument("--folder", help="โฟลเดอร์ที่มีหลายวิดีโอ")
    parser.add_argument("--show",  action="store_true",
                        help="แสดง skeleton realtime ขณะวิเคราะห์")
    parser.add_argument("--output", default="./output",
                        help="โฟลเดอร์สำหรับบันทึกผล (default: ./output)")
    args = parser.parse_args()

    if args.video:
        analyze_video(args.video, show=args.show, output_dir=args.output)
    else:
        analyze_folder(args.folder, show=args.show, output_dir=args.output)
