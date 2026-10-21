# 纯摄像头测试脚本 - 无任何AI，无任何依赖
import cv2

# 打开摄像头 (0 是默认摄像头)
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# 设置基础分辨率
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

print("正在测试摄像头...按 Q 退出")

while True:
    ret, frame = cap.read()

    if not ret:
        print("❌ 摄像头读取失败！")
        break

    # 显示画面
    cv2.imshow("Camera Test", frame)

    # 按 Q 退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放资源
cap.release()
cv2.destroyAllWindows()