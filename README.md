# BNGU 北京校区视觉组招新考核项目

## 1. 项目简介

本仓库为 BNGU 北京校区视觉组招新考核项目，主要基于 Python + OpenCV 完成计算机视觉基础任务复现与实践，包括：

1. OpenCV 颜色分割实验
2. OpenCV 最小框选与多边形拟合实验
3. 相机标定与 solvePnP 物体位姿解算实验

项目重点围绕图像预处理、HSV 颜色空间分割、轮廓检测、最小外接矩形、多边形拟合、相机内参使用以及目标物体三维姿态估计展开。通过本项目，我初步熟悉了视觉任务从图像输入、特征提取、目标筛选到结果可视化的完整流程。

---

## 2. 开发环境

### 2.1 系统环境

* 操作系统：Ubuntu 22.04 / Windows
* IDE：PyCharm
* Python 版本：Python 3.x
* 主要依赖库：

  * opencv-python
  * numpy

### 2.2 依赖安装

可以通过以下命令安装项目依赖：

```bash
pip install opencv-python numpy
```

如果使用虚拟环境，建议先创建并激活虚拟环境：

```bash
python -m venv .venv
source .venv/bin/activate
pip install opencv-python numpy
```

Windows 下虚拟环境激活方式：

```bash
.venv\Scripts\activate
pip install opencv-python numpy
```

---

## 3. 仓库结构

```text
.
├── README.md
├── BNGU招新报名表.docx
├── requirements.txt
├── color_segmentation/
│   ├── color_segmentation.py
│   ├── input/
│   └── output/
├── contour_polygon/
│   ├── contour_polygon.py
│   ├── input/
│   └── output/
├── solvepnp_pose/
│   ├── 采集标定照片.py
│   ├── 一键标定计算内参.py
│   ├── 物体的三维位姿情况展示.py
│   ├── camera_params.npz
│   ├── 棋盘格示意图.png
│   ├── solvepnp_result.mp4
│   ├── 一键标定计算内参数.mp4
│   ├── 展现物体的三维位姿情况.mp4
│   └── calibration_images/
│       ├── img_0.jpg
│       ├── img_1.jpg
│       ├── img_2.jpg
│       └── ...
├── assets/
│   ├── images/
│   └── videos/
└── debug_logs/
```

说明：

* `color_segmentation/`：颜色分割实验代码与结果
* `contour_polygon/`：最小框选与多边形拟合实验代码与结果
* `solvepnp_pose/`：相机标定与 solvePnP 位姿解算实验代码与结果
* `camera_params.npz`：相机标定后保存的相机内参矩阵和畸变参数
* `calibration_images/`：用于相机标定的棋盘格照片
* `assets/`：README 中展示用的图片和视频
* `debug_logs/`：调试记录、报错记录、AI 辅助过程记录等
* `BNGU招新报名表.docx`：个人报名表

---

## 4. 实验一：OpenCV 颜色分割

### 4.1 实验目标

本实验主要完成基于 HSV 颜色空间的目标颜色分割。程序将输入图像从 BGR 颜色空间转换到 HSV 颜色空间，并根据目标颜色范围构建掩膜，最终提取出指定颜色区域。

### 4.2 核心思路

主要流程如下：

```text
读取图像
→ BGR 转 HSV
→ 设置 H/S/V 阈值范围
→ cv2.inRange 生成掩膜
→ 形态学处理优化掩膜
→ bitwise_and 提取目标区域
→ 显示并保存结果
```

### 4.3 运行方式

进入对应目录：

```bash
cd color_segmentation
python color_segmentation.py
```

### 4.4 运行结果

原图：

![颜色分割原图](assets/images/color_input.png)

颜色分割结果：

![颜色分割结果](assets/images/color_result.png)

如无法直接显示图片，可在 `color_segmentation/output/` 文件夹中查看输出结果。

---

## 5. 实验二：OpenCV 最小框选与多边形拟合

### 5.1 实验目标

本实验主要完成对目标区域的轮廓检测、最小外接矩形框选和多边形拟合。通过筛选轮廓面积、形状特征和多边形顶点数，尽量只保留目标区域，减少误检。

### 5.2 核心思路

主要流程如下：

```text
读取图像
→ 图像预处理
→ 二值化处理
→ findContours 查找轮廓
→ boundingRect 绘制最小外接矩形
→ approxPolyDP 进行多边形拟合
→ 根据面积、长宽比、顶点数等条件筛选目标
→ 可视化最终框选结果
```

### 5.3 运行方式

进入对应目录：

```bash
cd contour_polygon
python contour_polygon.py
```

### 5.4 运行结果

原图：

![多边形拟合原图](assets/images/contour_input.png)

轮廓检测结果：

![轮廓检测结果](assets/images/contour_result.png)

最终框选结果：

![最终框选结果](assets/images/polygon_result.png)

---

## 6. 实验三：相机标定与 solvePnP 物体三维位姿解算

### 6.1 实验目标

本实验主要完成相机标定与真实矩形目标的三维位姿解算。实验首先使用棋盘格图片对摄像头进行标定，得到相机内参矩阵和畸变系数；随后选取真实世界中的矩形目标，检测矩形四个角点，并结合相机内参使用 `cv2.solvePnP()` 求解目标物体相对于相机的旋转向量和平移向量，最后将三维坐标轴投影到图像中，实现物体三维姿态的可视化。

本实验没有使用手机屏幕显示的矩形，也没有使用他人拍摄的照片，而是使用真实世界中的纸面矩形目标进行检测，从而保证目标具有真实物理尺寸，满足位姿解算要求。

---

### 6.2 实验文件说明

实验三相关文件位于：

```text
solvepnp_pose/
```

文件结构如下：

```text
solvepnp_pose/
├── 采集标定照片.py
├── 一键标定计算内参.py
├── 物体的三维位姿情况展示.py
├── camera_params.npz
├── 棋盘格示意图.png
├── solvepnp_result.mp4
├── 一键标定计算内参数.mp4
├── 展现物体的三维位姿情况.mp4
└── calibration_images/
    ├── img_0.jpg
    ├── img_1.jpg
    ├── img_2.jpg
    └── ...
```

各文件作用如下：

| 文件/文件夹                | 作用                                            |
| --------------------- | --------------------------------------------- |
| `采集标定照片.py`           | 调用摄像头采集棋盘格标定图片，并保存到 `calibration_images/` 文件夹 |
| `calibration_images/` | 存放用于相机标定的多张棋盘格照片                              |
| `一键标定计算内参.py`         | 读取棋盘格图片，计算相机内参矩阵和畸变参数                         |
| `camera_params.npz`   | 保存标定得到的相机内参矩阵和畸变参数                            |
| `物体的三维位姿情况展示.py`      | 检测真实矩形目标，使用 solvePnP 求解三维位姿，并绘制三维坐标轴          |
| `棋盘格示意图.png`          | 相机标定使用的棋盘格示意图                                 |
| `solvepnp_result.mp4` | solvePnP 三维位姿解算结果视频                           |
| `一键标定计算内参数.mp4`       | 相机标定和内参计算过程记录视频                               |
| `展现物体的三维位姿情况.mp4`     | 物体三维位姿展示过程记录视频                                |

---

### 6.3 实验流程

实验三整体流程如下：

```text
采集棋盘格标定图片
→ 计算相机内参和畸变参数
→ 保存 camera_params.npz
→ 准备真实矩形目标
→ 检测矩形四个角点
→ 构建 objectPoints 与 imagePoints
→ 调用 cv2.solvePnP 求解 rvec 和 tvec
→ 调用 cv2.projectPoints 投影三维坐标轴
→ 显示并保存位姿解算结果视频
```

---

### 6.4 第一步：采集棋盘格标定图片

运行：

```bash
cd solvepnp_pose
python 采集标定照片.py
```

程序会打开电脑摄像头，并自动创建 `calibration_images/` 文件夹用于保存标定图片。

本实验中，为了保证标定阶段和后续 solvePnP 阶段使用同一摄像头成像条件，程序中强制设置摄像头分辨率为：

```python
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
```

程序运行后：

* 按 `s` 键保存当前画面；
* 按 `q` 键退出采集程序；
* 保存的图片会自动命名为 `img_0.jpg`、`img_1.jpg`、`img_2.jpg` 等；
* 图片会统一保存到 `calibration_images/` 文件夹中。
<img width="1540" height="454" alt="image" src="https://github.com/user-attachments/assets/46a3c8f9-bab3-4f24-9598-40143d474d24" />

采集时需要让棋盘格在画面中呈现不同位置、不同距离和不同倾斜角度，使标定结果更加稳定。

本次实验中采集了多张棋盘格图片作为相机标定数据。

---

### 6.5 第二步：计算相机内参

运行：

```bash
python 一键标定计算内参.py
```

该程序会读取 `calibration_images/` 文件夹中的棋盘格图片，并完成相机标定。

代码中使用的棋盘格参数如下：

```python
CHECKERBOARD = (9, 6)
SQUARE_SIZE = 25.0
```

其中：

* `CHECKERBOARD = (9, 6)` 表示棋盘格内角点数量为 9 × 6；
* `SQUARE_SIZE = 25.0` 表示一个棋盘格小方块边长为 25.0 mm。

程序主要处理流程如下：

```text
读取 calibration_images 中的棋盘格图片
→ 转换为灰度图
→ cv2.findChessboardCorners 寻找棋盘格内角点
→ cv2.cornerSubPix 进行亚像素角点优化
→ cv2.calibrateCamera 计算相机内参矩阵和畸变参数
→ 计算平均重投影误差
→ 保存 camera_params.npz
```

运行成功后，终端会输出：

* 相机内参矩阵 `Camera Matrix`
* 畸变系数 `Distortion Coeffs`
* 平均重投影误差
* 参数保存成功提示

本次实验中，程序成功生成了：

```text
camera_params.npz
```

该文件中保存了：

* `camera_matrix`：相机内参矩阵
* `dist_coeffs`：相机畸变参数

本次运行得到的平均重投影误差约为：

```text
0.0391 px
```

重投影误差越接近 0，说明标定效果越好。本次误差较小，说明棋盘格角点提取和相机标定结果较为稳定。

---
<img width="692" height="282" alt="image" src="https://github.com/user-attachments/assets/43987792-dc3d-4deb-917a-05b0ff4686c2" />


### 6.6 第三步：solvePnP 三维位姿解算

运行：

```bash
python 物体的三维位姿情况展示.py
```

程序会打开摄像头，读取当前目录下的 `camera_params.npz`，并对真实矩形目标进行检测和三维位姿解算。

本实验中，真实矩形目标尺寸设置为：

```python
RECT_W = 100.0
RECT_H = 70.0
```

单位为 mm。

程序中定义的真实世界 3D 点如下：

```python
object_points = np.array([
    [-RECT_W / 2, -RECT_H / 2, 0],
    [ RECT_W / 2, -RECT_H / 2, 0],
    [ RECT_W / 2,  RECT_H / 2, 0],
    [-RECT_W / 2,  RECT_H / 2, 0],
], dtype=np.float32)
```

这四个点表示真实矩形目标的四个角点，坐标系原点设置在矩形中心，矩形所在平面为 `z = 0` 平面。

---

### 6.7 矩形角点检测方法

在 `物体的三维位姿情况展示.py` 中，程序通过以下方式检测矩形角点：

```text
摄像头读取图像
→ BGR 转灰度图
→ CLAHE 图像增强
→ 高斯滤波降噪
→ 自适应阈值二值化
→ 形态学闭运算、开运算
→ findContours 查找轮廓
→ approxPolyDP 拟合四边形
→ 根据面积和长宽比筛选最合适矩形
→ order_points 对四个点排序
→ cornerSubPix 进行亚像素角点优化
```

其中，`order_points()` 函数用于将检测到的四个角点统一排序为：

```text
左上角 → 右上角 → 右下角 → 左下角
```

这样可以保证 `imagePoints` 与 `objectPoints` 的顺序严格对应，避免出现坐标轴方向错误的问题。

---

### 6.8 solvePnP 核心代码说明

程序加载相机参数：

```python
calibration = np.load(CALIBRATION_FILE)
camera_matrix = calibration["camera_matrix"].astype(np.float32)
dist_coeffs = calibration["dist_coeffs"].astype(np.float32)
```

然后调用 `cv2.solvePnP()` 进行位姿解算：

```python
success, rvec, tvec = cv2.solvePnP(
    object_points,
    image_points,
    camera_matrix,
    dist_coeffs,
    flags=flags,
)
```

其中：

* `object_points`：真实世界中的矩形四个 3D 点；
* `image_points`：图像中检测到的矩形四个 2D 像素点；
* `camera_matrix`：相机内参矩阵；
* `dist_coeffs`：相机畸变系数；
* `rvec`：旋转向量，用于表示目标相对于相机的旋转姿态；
* `tvec`：平移向量，用于表示目标相对于相机的位置。

由于本实验目标为平面矩形，因此程序优先使用：

```python
cv2.SOLVEPNP_IPPE
```

如果当前 OpenCV 版本不支持该方法，则自动切换为：

```python
cv2.SOLVEPNP_ITERATIVE
```

---

### 6.9 三维坐标轴可视化

位姿解算成功后，程序使用 `cv2.projectPoints()` 将三维坐标轴投影到二维图像中：

```python
projected_points, _ = cv2.projectPoints(
    axis_points, rvec, tvec, camera_matrix, dist_coeffs
)
```
<img width="692" height="443" alt="image" src="https://github.com/user-attachments/assets/6bb87b4e-a78c-4dd8-b297-95cc4418411a" />

程序绘制的坐标轴含义如下：

* 红色：X 轴
* 绿色：Y 轴
* 蓝色：Z 轴

同时，程序会在画面左上角显示目标相对于相机的平移向量：

```text
tvec: x=...mm y=...mm z=...mm
```

其中：

* `x` 表示目标中心相对于相机光心在水平方向上的偏移；
* `y` 表示目标中心相对于相机光心在竖直方向上的偏移；
* `z` 表示目标到相机的深度距离。

---

### 6.10 实验结果

本实验成功完成了以下内容：

1. 使用棋盘格图片完成相机标定；
2. 成功生成并保存 `camera_params.npz`；
3. 使用真实矩形目标完成角点检测；
4. 成功调用 `cv2.solvePnP()` 解算目标三维位姿；
5. 成功在画面中绘制 X、Y、Z 三维坐标轴；
6. 成功保存位姿解算结果视频。

相机标定过程视频：

[点击查看相机标定与内参计算过程](solvepnp_pose/一键标定计算内参数.mp4)

solvePnP 位姿解算结果视频：

[点击查看 solvePnP 位姿解算结果](solvepnp_pose/solvepnp_result.mp4)

三维位姿展示视频：

[点击查看三维位姿展示视频](solvepnp_pose/展现物体的三维位姿情况.mp4)

---

### 6.11 实验注意事项

1. 相机标定图片采集和 solvePnP 主程序运行时，摄像头分辨率必须保持一致。本实验统一设置为 `1280 × 720`。
2. 如果更换摄像头，需要重新运行 `采集标定照片.py` 和 `一键标定计算内参.py`，重新生成 `camera_params.npz`。
3. 如果更换矩形目标，需要重新测量矩形真实尺寸，并修改 `RECT_W` 和 `RECT_H`。
4. `object_points` 和 `image_points` 的四个点顺序必须一一对应，否则三维坐标轴方向可能异常。
5. 如果程序提示找不到 `camera_params.npz`，需要确认该文件是否与 `物体的三维位姿情况展示.py` 位于同一目录。
6. 如果摄像头无法打开，可以尝试将 `cv2.VideoCapture(0)` 中的 `0` 改为 `1` 或其他摄像头编号。
7. 由于矩形检测依赖图像阈值和轮廓筛选，运行时需要尽量保证目标轮廓清晰、背景干扰较少。

---

### 6.12 实验问题与改进方向

本实验目前可以完成基础的相机标定与矩形目标三维位姿解算，但仍有一些可以继续改进的地方：

1. 当前矩形检测主要依赖自适应阈值和轮廓筛选，在光照变化较大或背景复杂时鲁棒性仍可提升。
2. 可以进一步优化角点检测方法，提高 `imagePoints` 的稳定性。
3. 可以对 `tvec` 结果进行滤波，减少视频中坐标轴抖动。
4. 可以加入更稳定的目标识别标记，例如 ArUco Marker 或 AprilTag。
5. 后续可以进一步学习 RoboMaster 中装甲板识别、目标预测、云台控制和自动瞄准相关内容，将位姿解算与实际机器人视觉任务结合。

---

## 7. 项目运行说明

如果想完整运行本项目，可以按照以下顺序执行：

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 运行颜色分割实验
cd color_segmentation
python color_segmentation.py

# 3. 运行最小框选与多边形拟合实验
cd ../contour_polygon
python contour_polygon.py

# 4. 进入 solvePnP 实验目录
cd ../solvepnp_pose

# 5. 采集棋盘格标定图片
python 采集标定照片.py

# 6. 计算相机内参并生成 camera_params.npz
python 一键标定计算内参.py

# 7. 运行 solvePnP 物体三维位姿解算
python 物体的三维位姿情况展示.py
```

如果已经完成相机标定，并且目录下已经存在 `camera_params.npz`，则可以直接运行：

```bash
cd solvepnp_pose
python 物体的三维位姿情况展示.py
```

---

## 8. 调试记录与问题总结

### 8.1 OpenCV 图像窗口显示问题

在 Ubuntu / PyCharm 环境下运行 `cv2.imshow()` 时，可能会出现 Qt、Wayland 或字体相关提示。部分提示不影响程序正常运行。如果窗口无法正常显示，可以检查：

1. Python 解释器是否选择正确
2. `opencv-python` 是否安装在当前解释器环境中
3. 图片或视频路径是否正确
4. 是否在支持图形界面的环境中运行

### 8.2 文件路径问题

本项目中图片、视频均使用相对路径读取。如果运行时报错找不到文件，需要确认当前工作目录是否为对应实验文件夹。

### 8.3 solvePnP 稳定性问题

solvePnP 对角点检测顺序、真实尺寸设置和相机内参比较敏感。若出现坐标轴方向异常或抖动较大，需要重点检查：

1. 四个图像角点顺序是否正确
2. `objectPoints` 和 `imagePoints` 是否一一对应
3. 真实矩形尺寸是否填写准确
4. 相机内参是否与当前摄像头匹配
5. 目标是否为真实平面物体，而不是屏幕显示内容

---

## 9. AI 辅助与 Debug 记录

本项目允许使用生成式 AI 辅助学习和调试。本人在完成过程中主要使用 AI 辅助理解以下内容：

1. OpenCV 环境配置问题
2. HSV 阈值调整思路
3. findContours、boundingRect、approxPolyDP 等函数理解
4. solvePnP 中 objectPoints、imagePoints、cameraMatrix、distCoeffs 的含义
5. 相机标定中棋盘格内角点、重投影误差和畸变参数的含义
6. 程序报错与运行路径问题排查

相关对话记录、调试记录和问题总结已整理在：

```text
debug_logs/
```

---

## 10. 项目收获

通过本次视觉组招新考核项目，我主要完成了以下学习：

1. 熟悉了 OpenCV 的基本图像读取、显示、保存流程
2. 理解了 BGR、RGB、HSV 等颜色空间的区别
3. 掌握了基于阈值和掩膜的颜色分割方法
4. 学习了轮廓检测、最小外接矩形和多边形拟合方法
5. 初步理解了相机内参、畸变参数和相机标定的作用
6. 初步完成了基于 solvePnP 的目标物体三维位姿解算
7. 学会了将实验代码、运行结果、调试记录和演示视频整理到开源仓库中

本项目仍有很多可以改进的地方，例如增强光照变化下的鲁棒性、优化角点排序算法、提高视频实时处理稳定性等。后续希望能继续深入学习 RoboMaster 视觉任务中的目标检测、装甲板识别、位姿解算、目标预测和自动瞄准等内容。

---

## 11. 作者信息

* 姓名：巩皓怡
* 学校：北京交通大学
* 专业：人工智能
* 方向意向：RoboMaster 视觉组
