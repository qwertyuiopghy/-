import cv2
import os

# 创建存放照片的文件夹
os.makedirs("calibration_images", exist_ok=True)

cap = cv2.VideoCapture(0)

# 强制设置与你主程序完全一样的分辨率！这一步极其关键！
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

count = 0
print("摄像头已打开！")
print("请拿着棋盘格在镜头前变换各种角度（倾斜、远近、平移）。")
print("按 's' 键保存图片，按 'q' 键退出。至少需要拍 15-20 张！")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow("Capture Calibration Images", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('s'):
        filename = f"calibration_images/img_{count}.jpg"
        cv2.imwrite(filename, frame)
        print(f"✅ 已保存第 {count + 1} 张照片: {filename}")
        count += 1
    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print(f"拍照完成，共保存了 {count} 张照片！")