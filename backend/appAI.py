from flask import Flask, render_template, Response, jsonify, request
import cv2
import mediapipe as mp
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# 确保工作目录正确，模型文件在 backend 目录下
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# ==============================
# 深蹲（你最初完美版 完全不动）
# ==============================
squat_count = 0
is_squat_down = False
base_shoulder_y = 0.5

# ==============================
# 臂展（超级稳简单逻辑）
# ==============================
arm_count = 0
arm_last_down = True

# 当前动作
current_action = "squat"

# 模型加载
BaseOptions = mp.tasks.BaseOptions
PoseLandmarker = mp.tasks.vision.PoseLandmarker
PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = PoseLandmarkerOptions(
    base_options=BaseOptions(model_asset_path="pose_landmarker_lite.task"),
    running_mode=VisionRunningMode.IMAGE
)
landmarker = PoseLandmarker.create_from_options(options)

# ==============================
# 视频流 + 识别
# ==============================
def generate_frames():
    global squat_count, is_squat_down, base_shoulder_y, arm_count, arm_last_down, current_action

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    while True:
        success, frame = cap.read()
        if not success:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        result = landmarker.detect(mp_image)

        if result.pose_landmarks:
            lm = result.pose_landmarks[0]
            h, w = frame.shape[:2]

            # 画点
            for p in lm:
                cx = int(p.x * w)
                cy = int(p.y * h)
                cv2.circle(frame, (cx, cy), 4, (0, 255, 0), -1)

            # =====================
            # 深蹲逻辑（原版）
            # =====================
            if current_action == "squat":
                l_sh = lm[11].y
                r_sh = lm[12].y
                avg_sh = (l_sh + r_sh) / 2

                if base_shoulder_y == 0.5:
                    base_shoulder_y = avg_sh

                down = base_shoulder_y + 0.06
                up = base_shoulder_y + 0.02

                if avg_sh > down:
                    is_squat_down = True
                    cv2.putText(frame, "Squat Down", (20, 40), 0, 1, (0, 0, 255), 2)
                elif avg_sh < up:
                    if is_squat_down:
                        squat_count += 1
                        is_squat_down = False
                    cv2.putText(frame, "Stand Up", (20, 40), 0, 1, (0, 255, 0), 2)

                cv2.putText(frame, f"Count: {squat_count}", (20, 100), 0, 1, (255, 0, 0), 2)

            # =====================
            # 臂展逻辑（修复版）
            # =====================
            elif current_action == "arm":
                l_sh = lm[11].y
                r_sh = lm[12].y
                l_el = lm[13].y
                r_el = lm[14].y   # 修复：之前错误用了 lm[15]（左腕）
                l_wr = lm[15].y
                r_wr = lm[16].y

                # 双手手腕和手肘都明显高于肩膀 = 双臂完全打开
                is_up = (l_el < l_sh - 0.08) and (r_el < r_sh - 0.08) and (l_wr < l_sh - 0.05) and (r_wr < r_sh - 0.05)

                if is_up and arm_last_down:
                    arm_count += 1
                    arm_last_down = False
                    cv2.putText(frame, "Arm OPEN +1", (20, 40), 0, 1, (0, 0, 255), 2)
                elif not is_up:
                    arm_last_down = True
                    cv2.putText(frame, "Arm READY", (20, 40), 0, 1, (0, 255, 0), 2)

                cv2.putText(frame, f"Count: {arm_count}", (20, 100), 0, 1, (255, 0, 0), 2)

        # 输出帧
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    cap.release()

# ==============================
# 路由
# ==============================
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/api/get-count')
def get_count():
    global current_action
    t = request.args.get("type", "squat")
    current_action = t
    return jsonify(score=squat_count if t == "squat" else arm_count)

@app.route('/api/reset', methods=['POST'])
def reset():
    global squat_count, is_squat_down, base_shoulder_y, arm_count, arm_last_down
    squat_count = 0
    is_squat_down = False
    base_shoulder_y = 0.5
    arm_count = 0
    arm_last_down = True
    return jsonify(status="ok")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)