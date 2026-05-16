import numpy as np
import time

# Optional heavy imports - loaded lazily
try:
    import cv2
except ImportError:
    cv2 = None

# ============================================================
# Biomechanical calculation functions
# ============================================================

def calculate_angle(a, b, c):
    a, b, c = np.array(a), np.array(b), np.array(c)
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    return float(360 - angle if angle > 180.0 else angle)

def calculate_lean_angle(top_point, bottom_point):
    dx = bottom_point[0] - top_point[0]
    dy = bottom_point[1] - top_point[1]
    angle = np.degrees(np.arctan2(dx, dy))
    return float(abs(angle))

def calculate_roll_angle(left_point, right_point):
    dx = right_point[0] - left_point[0]
    dy = right_point[1] - left_point[1]
    angle = np.degrees(np.arctan2(dy, dx))
    return float(angle)

# ============================================================
# Pro athlete reference benchmarks
# ============================================================

PRO_BENCHMARKS = {
    "Head_Lean":     {"ideal": 5.0,  "good": 8.0,  "warning": 12.0, "unit": "°", "label": "มุมเอียงศีรษะ"},
    "Shoulder_Roll": {"ideal": 2.0,  "good": 5.0,  "warning": 8.0,  "unit": "°", "label": "การหมุนไหล่"},
    "Pelvic_Drop":   {"ideal": 2.0,  "good": 4.0,  "warning": 7.0,  "unit": "°", "label": "การตกสะโพก"},
    "Torso_Lean":    {"ideal": 8.0,  "good": 12.0, "warning": 18.0, "unit": "°", "label": "มุมเอียงลำตัว"},
    "L_Hip_Ang":     {"ideal": 90.0, "good": 80.0, "warning": 65.0, "unit": "°", "label": "มุมสะโพกซ้าย"},
    "R_Hip_Ang":     {"ideal": 90.0, "good": 80.0, "warning": 65.0, "unit": "°", "label": "มุมสะโพกขวา"},
    "L_Knee_Ang":    {"ideal": 90.0, "good": 80.0, "warning": 65.0, "unit": "°", "label": "มุมเข่าซ้าย"},
    "R_Knee_Ang":    {"ideal": 90.0, "good": 80.0, "warning": 65.0, "unit": "°", "label": "มุมเข่าขวา"},
    "L_Arm_Ang":     {"ideal": 90.0, "good": 80.0, "warning": 65.0, "unit": "°", "label": "มุมแขนซ้าย"},
    "R_Arm_Ang":     {"ideal": 90.0, "good": 80.0, "warning": 65.0, "unit": "°", "label": "มุมแขนขวา"},
}

def score_metric(value, benchmark):
    ideal = benchmark["ideal"]
    good  = benchmark["good"]
    warning = benchmark["warning"]
    diff = abs(value - ideal)
    if diff <= 2: return 100
    elif diff <= abs(good - ideal): return 75
    elif diff <= abs(warning - ideal): return 50
    else: return max(0, 25)

def get_metric_status(value, benchmark):
    ideal   = benchmark["ideal"]
    good    = benchmark["good"]
    warning = benchmark["warning"]
    diff = abs(value - ideal)
    if diff <= abs(good - ideal):
        return "good", "#39FF14", "ดีเยี่ยม"
    elif diff <= abs(warning - ideal):
        return "warning", "#FFD700", "พอใช้"
    else:
        return "poor", "#FF6B35", "ต้องแก้ไข"

# ============================================================
# Main analysis function
# ============================================================

def analyze_video(video_path, progress_callback=None, use_demo=False):
    if use_demo or cv2 is None:
        return generate_demo_results()
    try:
        from ultralytics import YOLO
        model = YOLO('yolov8n-pose.pt')
        cap = cv2.VideoCapture(video_path)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)

        all_metrics = {k: [] for k in [
            "Head_Lean","Shoulder_Roll","Pelvic_Drop","Torso_Lean",
            "L_Hip_Ang","R_Hip_Ang","L_Knee_Ang","R_Knee_Ang",
            "L_Arm_Ang","R_Arm_Ang","Step_Length_px","Vert_Osc","Strike"
        ]}

        frame_idx = 0
        for r in model(source=video_path, stream=True, verbose=False):
            frame_idx += 1
            if progress_callback and frame_idx % 10 == 0:
                progress_callback(min(frame_idx / max(total_frames, 1), 1.0), frame_idx)
            if r.keypoints is None or r.keypoints.data is None:
                continue
            for person in r.keypoints.data.cpu().numpy():
                if len(person) <= 16:
                    continue
                try:
                    nose = person[0][:2]
                    l_sh, r_sh = person[5][:2], person[6][:2]
                    l_el, r_el = person[7][:2], person[8][:2]
                    l_wr, r_wr = person[9][:2], person[10][:2]
                    l_hip, r_hip = person[11][:2], person[12][:2]
                    l_knee, r_knee = person[13][:2], person[14][:2]
                    l_ankle, r_ankle = person[15][:2], person[16][:2]
                    if any(v[0] == 0 for v in [l_hip, l_knee, l_ankle, l_sh]):
                        continue
                    mid_sh  = [(l_sh[0]+r_sh[0])/2,   (l_sh[1]+r_sh[1])/2]
                    mid_hip = [(l_hip[0]+r_hip[0])/2,  (l_hip[1]+r_hip[1])/2]
                    all_metrics["Head_Lean"].append(calculate_lean_angle(nose, mid_sh) if nose[0] != 0 else 0)
                    all_metrics["Shoulder_Roll"].append(calculate_roll_angle(l_sh, r_sh))
                    all_metrics["Pelvic_Drop"].append(calculate_roll_angle(l_hip, r_hip))
                    all_metrics["Torso_Lean"].append(calculate_lean_angle(mid_sh, mid_hip))
                    all_metrics["L_Hip_Ang"].append(calculate_angle(l_sh, l_hip, l_knee))
                    all_metrics["R_Hip_Ang"].append(calculate_angle(r_sh, r_hip, r_knee))
                    all_metrics["L_Knee_Ang"].append(calculate_angle(l_hip, l_knee, l_ankle))
                    all_metrics["R_Knee_Ang"].append(calculate_angle(r_hip, r_knee, r_ankle))
                    all_metrics["L_Arm_Ang"].append(calculate_angle(l_sh, l_el, l_wr))
                    all_metrics["R_Arm_Ang"].append(calculate_angle(r_sh, r_el, r_wr))
                    all_metrics["Step_Length_px"].append(abs(l_ankle[0] - r_ankle[0]))
                    all_metrics["Vert_Osc"].append(float(mid_hip[1]))
                    all_metrics["Strike"].append("Left" if l_ankle[1] > r_ankle[1] else "Right")
                except Exception:
                    continue
        cap.release()
        if not all_metrics["Head_Lean"]:
            return generate_demo_results()
        return compute_summary(all_metrics, fps)
    except Exception:
        return generate_demo_results()

def compute_summary(all_metrics, fps=30):
    summary = {}
    for key in ["Head_Lean","Shoulder_Roll","Pelvic_Drop","Torso_Lean",
                "L_Hip_Ang","R_Hip_Ang","L_Knee_Ang","R_Knee_Ang","L_Arm_Ang","R_Arm_Ang"]:
        vals = [v for v in all_metrics[key] if v is not None and not np.isnan(v)]
        if vals:
            summary[key] = {
                "mean": float(np.mean(vals)), "std": float(np.std(vals)),
                "min": float(np.min(vals)),   "max": float(np.max(vals)),
                "values": vals
            }
    step_vals = [v for v in all_metrics["Step_Length_px"] if v > 0]
    vert_vals  = all_metrics["Vert_Osc"]
    strikes    = all_metrics["Strike"]
    summary["Step_Length_px"] = {"mean": float(np.mean(step_vals)) if step_vals else 150}
    summary["Vert_Osc"] = {
        "range": float(np.max(vert_vals) - np.min(vert_vals)) if vert_vals else 30,
        "values": vert_vals
    }
    summary["Strike"] = {
        "left_pct":  strikes.count("Left")  / max(len(strikes), 1) * 100,
        "right_pct": strikes.count("Right") / max(len(strikes), 1) * 100,
    }
    summary["total_frames"] = len(all_metrics["Head_Lean"])
    summary["fps"] = fps
    scores = [score_metric(summary[k]["mean"], PRO_BENCHMARKS[k])
              for k in PRO_BENCHMARKS if k in summary]
    summary["overall_score"] = int(np.mean(scores)) if scores else 72
    return summary

# ============================================================
# Demo data
# ============================================================

def generate_demo_results():
    np.random.seed(42)
    n = 150
    return {
        "Head_Lean":     {"mean": 7.2,  "std": 1.8,  "min": 3.1,  "max": 14.5, "values": list(np.random.normal(7.2,  1.8,  n))},
        "Shoulder_Roll": {"mean": 4.5,  "std": 2.1,  "min": 0.5,  "max": 9.8,  "values": list(np.random.normal(4.5,  2.1,  n))},
        "Pelvic_Drop":   {"mean": 6.8,  "std": 2.4,  "min": 1.2,  "max": 13.0, "values": list(np.random.normal(6.8,  2.4,  n))},
        "Torso_Lean":    {"mean": 9.3,  "std": 3.2,  "min": 2.5,  "max": 18.7, "values": list(np.random.normal(9.3,  3.2,  n))},
        "L_Hip_Ang":     {"mean": 87.5, "std": 12.3, "min": 55.0, "max": 125.0,"values": list(np.random.normal(87.5, 12.3, n))},
        "R_Hip_Ang":     {"mean": 85.2, "std": 11.8, "min": 52.0, "max": 122.0,"values": list(np.random.normal(85.2, 11.8, n))},
        "L_Knee_Ang":    {"mean": 92.3, "std": 18.5, "min": 45.0, "max": 155.0,"values": list(np.random.normal(92.3, 18.5, n))},
        "R_Knee_Ang":    {"mean": 88.7, "std": 17.2, "min": 42.0, "max": 150.0,"values": list(np.random.normal(88.7, 17.2, n))},
        "L_Arm_Ang":     {"mean": 88.4, "std": 15.6, "min": 50.0, "max": 140.0,"values": list(np.random.normal(88.4, 15.6, n))},
        "R_Arm_Ang":     {"mean": 91.2, "std": 16.1, "min": 48.0, "max": 145.0,"values": list(np.random.normal(91.2, 16.1, n))},
        "Step_Length_px": {"mean": 148.5},
        "Vert_Osc":      {"range": 38.2, "values": list(np.random.normal(350, 19, n))},
        "Strike":        {"left_pct": 51.3, "right_pct": 48.7},
        "total_frames": n, "fps": 30,
        "overall_score": 68, "is_demo": True,
    }

# ============================================================
# Coaching feedback
# ============================================================

def generate_coaching_feedback(results):
    issues, strengths = [], []
    checks = {
        "Head_Lean":     (8.0,  12.0, "ศีรษะเอียงมากเกินไป ลองมองไปข้างหน้า 10-15 เมตร",   "ตำแหน่งศีรษะดี มองตรงข้างหน้า"),
        "Pelvic_Drop":   (4.0,  7.0,  "สะโพกตกมาก ต้องเสริมความแข็งแรง Glute Med",          "สมดุลสะโพกดีเยี่ยม"),
        "Torso_Lean":    (12.0, 18.0, "ลำตัวเอียงมากเกินไป ปรับให้ตรงขึ้นเล็กน้อย",         "มุมลำตัวอยู่ในเกณฑ์ดี"),
        "Shoulder_Roll": (5.0,  8.0,  "ไหล่แกว่งมาก ลดการหมุนของลำตัวส่วนบน",              "การแกว่งไหล่สมดุลดี"),
    }
    for metric, (good_t, warn_t, issue_msg, strength_msg) in checks.items():
        val = results.get(metric, {}).get("mean", 0) if isinstance(results.get(metric), dict) else 0
        if val > warn_t:
            issues.append({"metric": metric, "message": issue_msg, "severity": "high",   "value": val})
        elif val > good_t:
            issues.append({"metric": metric, "message": issue_msg, "severity": "medium", "value": val})
        else:
            strengths.append({"metric": metric, "message": strength_msg, "value": val})
    return {
        "issues":       sorted(issues, key=lambda x: {"high": 0, "medium": 1}[x["severity"]]),
        "strengths":    strengths,
        "priority_fix": issues[0] if issues else None,
    }
