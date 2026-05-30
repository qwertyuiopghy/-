import cv2
import numpy as np
import glob

# ==========================================
# ⚠️ 必须修改的参数 ⚠️
# ==========================================
# 1. 棋盘格的【内角点】数量。
# 比如你的棋盘格有 10 个方块宽，7 个方块高，那么内角点就是 (9, 6)
CHECKERBOARD = (9, 6)

# 2. 你刚才拿尺子量出来的一个黑色小方块的边长，单位：毫米 (mm)
SQUARE_SIZE = 25.0  # <--- 改成你的实际测量值！
# ==========================================

# 寻找亚像素角点的迭代终止条件
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# 准备 3D 真实世界坐标点，如 (0,0,0), (25,0,0), (50,0,0) ...
objp = np.zeros((CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)
objp = objp * SQUARE_SIZE

# 用来存储所有图片的 3D 坐标和 2D 坐标
objpoints = []  # 真实世界中的 3D 点
imgpoints = []  # 图像平面中的 2D 像素点

# 读取刚刚拍的所有照片
images = glob.glob('calibration_images/*.jpg')

if not images:
    print("❌ 没有找到照片，请先运行 capture_images.py 拍照！")
    exit()

print(f"正在分析 {len(images)} 张照片，请稍候...")

for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 寻找棋盘格角点
    ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, None)

    # 如果找到了，就添加到数组里
    if ret:
        objpoints.append(objp)
        # 亚像素级优化，让坐标更精准
        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners2)

        # 可视化展示找点过程（可以注释掉）
        cv2.drawChessboardCorners(img, CHECKERBOARD, corners2, ret)
        cv2.imshow('Finding Corners...', img)
        cv2.waitKey(100)

cv2.destroyAllWindows()

if len(objpoints) < 5:
    print("❌ 有效照片太少，请确保照片里的棋盘格清晰完整，且内角点数量设置正确！")
    exit()

# ==========================================
# 核心计算：求解相机内参和畸变系数
# ==========================================
print("照片分析完毕，正在进行复杂的矩阵计算...")
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
    objpoints, imgpoints, gray.shape[::-1], None, None
)

print("\n🎉 标定成功！")
print("相机内参矩阵 (Camera Matrix):\n", mtx)
print("畸变系数 (Distortion Coeffs):\n", dist)

# 计算重投影误差（评估标定质量，越接近 0 越好）
mean_error = 0
for i in range(len(objpoints)):
    imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
    error = cv2.norm(imgpoints[i], imgpoints2, cv2.NORM_L2) / len(imgpoints2)
    mean_error += error
print(f"总平均重投影误差: {mean_error / len(objpoints):.4f} px (小于 0.5 说明极其精准)")

# 保存参数到文件，给你的主程序用！
np.savez("camera_params.npz", camera_matrix=mtx, dist_coeffs=dist)
print("✅ 参数已保存为 'camera_params.npz' 文件！")