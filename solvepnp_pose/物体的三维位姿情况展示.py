import cv2
import numpy as np
import os  # 新增了 os 模块，用于检查文件是否存在

# =========================
# 1. 真实矩形尺寸，单位：mm
# =========================
RECT_W = 100.0  # 矩形真实宽度，单位 mm
RECT_H = 70.0   # 矩形真实高度，单位 mm

# =========================
# 2. 是否保存视频
# =========================
SAVE_VIDEO = True
OUTPUT_PATH = "solvepnp_result.mp4"
CALIBRATION_FILE = "camera_params.npz" # 标定文件路径


def order_points(pts):
    pts = np.array(pts, dtype=np.float32)
    s = pts.sum(axis=1)
    diff = np.diff(pts, axis=1).reshape(-1)

    left_up = pts[np.argmin(s)]
    right_down = pts[np.argmax(s)]
    right_up = pts[np.argmin(diff)]
    left_down = pts[np.argmax(diff)]

    return np.array([left_up, right_up, right_down, left_down], dtype=np.float32)


def find_rectangle_corners(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    gray_enhanced = clahe.apply(gray)
    blur = cv2.GaussianBlur(gray_enhanced, (5, 5), 0)

    binary = cv2.adaptiveThreshold(
        blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 31, 9
    )

    kernel3 = np.ones((3, 3), np.uint8)
    kernel5 = np.ones((5, 5), np.uint8)
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel5, iterations=1)
    binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel3, iterations=1)

    contours, _ = cv2.findContours(
        binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    best_quad = None
    best_score = -1

    frame_area = frame.shape[0] * frame.shape[1]
    min_area = max(100, frame_area * 0.0005)
    expected_ratio = max(RECT_W, RECT_H) / min(RECT_W, RECT_H)

    for contour in contours:
        area = cv2.contourArea(contour)
        if area < min_area:
            continue

        perimeter = cv2.arcLength(contour, True)
        if perimeter == 0:
            continue

        quad = None
        for eps_multiplier in [0.015, 0.02, 0.035]:
            approx = cv2.approxPolyDP(contour, eps_multiplier * perimeter, True)
            if len(approx) == 4 and cv2.isContourConvex(approx):
                quad = approx.reshape(4, 2).astype(np.float32)
                break

        if quad is not None:
            ordered = order_points(quad)
            side_w = (np.linalg.norm(ordered[1] - ordered[0]) + np.linalg.norm(ordered[2] - ordered[3])) / 2
            side_h = (np.linalg.norm(ordered[3] - ordered[0]) + np.linalg.norm(ordered[2] - ordered[1])) / 2

            if min(side_w, side_h) < 5:
                continue

            current_ratio = max(side_w, side_h) / min(side_w, side_h)
            ratio_error = abs(current_ratio - expected_ratio) / expected_ratio

            if ratio_error < 0.45:
                score = area * (1.0 - ratio_error)
                if score > best_score:
                    best_score = score
                    best_quad = ordered

    if best_quad is None:
        return None, binary

    h, w = gray.shape
    best_quad[:, 0] = np.clip(best_quad[:, 0], 0, w - 1)
    best_quad[:, 1] = np.clip(best_quad[:, 1], 0, h - 1)

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    best_quad = cv2.cornerSubPix(
        gray, best_quad.reshape(-1, 1, 2), (5, 5), (-1, -1), criteria
    )

    return best_quad.reshape(4, 2), binary


def draw_axes(frame, camera_matrix, dist_coeffs, rvec, tvec):
    axis_len = 50.0

    axis_points = np.float32([
        [0, 0, 0],
        [axis_len, 0, 0],
        [0, axis_len, 0],
        [0, 0, -axis_len],
    ])

    projected_points, _ = cv2.projectPoints(
        axis_points, rvec, tvec, camera_matrix, dist_coeffs
    )

    projected_points = projected_points.reshape(-1, 2).astype(int)

    origin = tuple(projected_points[0])
    x_point = tuple(projected_points[1])
    y_point = tuple(projected_points[2])
    z_point = tuple(projected_points[3])

    cv2.line(frame, origin, x_point, (0, 0, 255), 3)
    cv2.line(frame, origin, y_point, (0, 255, 0), 3)
    cv2.line(frame, origin, z_point, (255, 0, 0), 3)

    cv2.putText(frame, "X", x_point, cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
    cv2.putText(frame, "Y", y_point, cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    cv2.putText(frame, "Z", z_point, cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)


def main():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("摄像头打开失败，请检查摄像头编号。")
        return

    # ⚠️ 极度关键：强制设置分辨率为 1280x720，与标定时完全保持一致！
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    ret, frame = cap.read()
    if not ret:
        print("无法读取摄像头画面。")
        cap.release()
        return

    height, width = frame.shape[:2]
    print(f"当前摄像头实际分辨率: {width}x{height}")

    # =========================
    # 3. 智能加载相机内参 (你心心念念的关键步骤！)
    # =========================
    if os.path.exists(CALIBRATION_FILE):
        calibration = np.load(CALIBRATION_FILE)
        camera_matrix = calibration["camera_matrix"].astype(np.float32)
        dist_coeffs = calibration["dist_coeffs"].astype(np.float32)
        print(f"✅ 已成功加载神级标定参数：{CALIBRATION_FILE}")
    else:
        print("❌ 未找到 camera_params.npz，使用不准确的盲猜内参！测距将严重失真！")
        fx = width
        fy = width
        cx = width / 2
        cy = height / 2

        camera_matrix = np.array([
            [fx, 0, cx],
            [0, fy, cy],
            [0, 0, 1],
        ], dtype=np.float32)
        dist_coeffs = np.zeros((5, 1), dtype=np.float32)

    # =========================
    # 4. 定义真实世界中的四个 3D 点
    # =========================
    object_points = np.array([
        [-RECT_W / 2, -RECT_H / 2, 0],
        [RECT_W / 2, -RECT_H / 2, 0],
        [RECT_W / 2, RECT_H / 2, 0],
        [-RECT_W / 2, RECT_H / 2, 0],
    ], dtype=np.float32)

    writer = None

    if SAVE_VIDEO:
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        writer = cv2.VideoWriter(OUTPUT_PATH, fourcc, 20.0, (width, height))
        if not writer.isOpened():
            print("视频写入器打开失败，请检查输出路径、编码器或文件后缀。")
            writer = None

    print("程序已启动。按 q 退出。")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        corners, binary = find_rectangle_corners(frame)

        if corners is not None:
            image_points = corners.astype(np.float32)

            flags = cv2.SOLVEPNP_IPPE if hasattr(cv2, "SOLVEPNP_IPPE") else cv2.SOLVEPNP_ITERATIVE

            success, rvec, tvec = cv2.solvePnP(
                object_points,
                image_points,
                camera_matrix,
                dist_coeffs,
                flags=flags,
            )

            if success:
                pts = image_points.astype(int)
                cv2.polylines(frame, [pts], True, (0, 255, 255), 2)

                for i, p in enumerate(pts):
                    cv2.circle(frame, tuple(p), 5, (255, 0, 255), -1)
                    cv2.putText(
                        frame,
                        str(i),
                        tuple(p),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (255, 0, 255),
                        2,
                    )

                draw_axes(frame, camera_matrix, dist_coeffs, rvec, tvec)

                x, y, z = tvec.flatten()
                cv2.putText(
                    frame,
                    f"tvec: x={x:.1f}mm y={y:.1f}mm z={z:.1f}mm",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 255),
                    2,
                )

        cv2.imshow("solvePnP Pose Estimation", frame)
        cv2.imshow("Binary", binary)

        if writer is not None:
            writer.write(frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    cap.release()

    if writer is not None:
        writer.release()
        print(f"视频已保存到：{OUTPUT_PATH}")

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()