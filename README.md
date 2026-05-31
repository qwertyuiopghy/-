# BNGU 北京校区视觉组招新考核项目

## 1. 项目简介

本仓库为 **BNGU 北京校区视觉组招新考核** 的个人完成项目，主要基于 **Python + OpenCV** 完成视觉基础实验复现与拓展实践。

项目内容包括：

1. OpenCV 颜色分割实验
2. OpenCV 最小框选与多边形拟合实验
3. 基于视频的装甲板灯条识别拓展实验
4. 相机标定与 solvePnP 物体三维位姿解算实验
5. OpenCV / PyCharm / Ubuntu 视觉环境验证

本项目围绕图像读取、HSV 颜色空间分割、掩膜构建、轮廓检测、最小外接矩形、多边形拟合、相机内参计算、畸变参数保存以及目标位姿解算等内容展开。通过本次考核，我初步完成了从图像输入、视觉特征提取、目标筛选、参数调试到结果可视化的视频/图像处理流程。

---

## 2. 完成情况总览

| 模块 | 完成内容 | 结果文件 |
|---|---|---|
| 环境配置与测试 | 完成 PyCharm、OpenCV、Ubuntu/VMware 环境配置与基础图像显示测试 | `视觉环境测试/text.py`、`VMware软件安装图片.png` |
| 颜色分割 | 基于 HSV 阈值完成目标颜色区域提取 | `color_segmentation/img_out.png`、`复现颜色分割实验.mp4` |
| 最小框选与多边形拟合 | 完成轮廓检测、目标筛选、最小框选与结果可视化 | `1_Contours_Pro.png`、`2_FinalBox_Pro.png` |
| 装甲板视频识别拓展 | 对视频中的灯条目标进行实时检测、配对与框选 | `contour_polygon/装甲板 视频识别/Result_Output.mp4` |
| 相机标定 | 采集棋盘格图像并计算相机内参和畸变参数 | `solvepnp_pose/camera_params.npz` |
| solvePnP 位姿解算 | 对真实矩形目标进行三维位姿解算并绘制坐标轴 | `solvepnp_pose/solvepnp_result.mp4` |

---

## 3. 开发环境

### 3.1 系统与工具

- 操作系统：Windows / Ubuntu 22.04
- IDE：PyCharm
- Python：Python 3.x
- 主要依赖：
  - `opencv-python`
  - `numpy`

### 3.2 依赖安装

```bash
pip install opencv-python numpy
```

如果使用虚拟环境，可以按如下方式创建并安装依赖：

```bash
python -m venv .venv
```

Windows：

```bash
.venv\Scripts\activate
pip install opencv-python numpy
```

Linux / Ubuntu：

```bash
source .venv/bin/activate
pip install opencv-python numpy
```

---

## 4. 仓库结构

```text
.
├── README.md
├── LICENSE
├── .gitignore
├── BNGU招新报名表.pdf
├── VMware软件安装图片.png
│
├── 视觉环境测试/
│   ├── text.py
│   └── yingkuangshi.png
│
├── color_segmentation/
│   ├── text.png
│   ├── img_out.png
│   ├── 复现颜色分割实验.py
│   └── 复现颜色分割实验.mp4
│
├── contour_polygon/
│   ├── test3.png
│   ├── 1_Contours_Pro.png
│   ├── 2_FinalBox_Pro.png
│   ├── OpenCV最小框选与多边形拟合.py
│   └── 装甲板 视频识别/
│       ├── 2.py
│       ├── 实验测试原视频.mp4
│       ├── 装甲板识别视频.mp4
│       └── Result_Output.mp4
│
└── solvepnp_pose/
    ├── 采集标定照片.py
    ├── 一键标定计算内参.py
    ├── 物体的三维位姿情况展示.py
    ├── camera_params.npz
    ├── 棋盘格示意图.png
    ├── 一键标定计算内参数.mp4
    ├── 展现物体的三维位姿情况.mp4
    ├── solvepnp_result.mp4
    └── calibration_images/
        ├── img_0.jpg
        ├── img_1.jpg
        ├── img_2.jpg
        └── ...
```

说明：

- `视觉环境测试/`：用于验证 OpenCV 是否能够正常读取和显示图像。
- `color_segmentation/`：颜色分割实验代码、输入图片、输出图片和运行视频。
- `contour_polygon/`：最小框选与多边形拟合实验代码与结果图。
- `contour_polygon/装甲板 视频识别/`：基于视频的装甲板灯条识别拓展实验。
- `solvepnp_pose/`：相机标定、相机内参保存、solvePnP 位姿解算与结果视频。
- `camera_params.npz`：相机标定后保存的相机内参矩阵和畸变参数。
- `BNGU招新报名表.pdf`：个人报名表。

---

## 5. 快速运行说明

> 本项目中部分程序使用相对路径读取图片或视频，建议进入对应文件夹后再运行程序。

### 5.1 运行颜色分割实验

```bash
cd color_segmentation
python 复现颜色分割实验.py
```

运行后会显示颜色分割结果，并生成：

```text
img_out.png
```

### 5.2 运行最小框选与多边形拟合实验

```bash
cd contour_polygon
python OpenCV最小框选与多边形拟合.py
```

运行后可查看轮廓检测结果图和最终框选结果图：

```text
1_Contours_Pro.png
2_FinalBox_Pro.png
```

### 5.3 运行装甲板视频识别拓展实验

```bash
cd "contour_polygon/装甲板 视频识别"
python 2.py
```

运行过程中：

- 按空格键：暂停 / 继续播放，方便调节参数；
- 按 `q` 键：退出程序；
- 程序会将处理后的视频保存为：

```text
Result_Output.mp4
```

### 5.4 运行相机标定与 solvePnP 实验

进入 solvePnP 实验目录：

```bash
cd solvepnp_pose
```

采集棋盘格标定图片：

```bash
python 采集标定照片.py
```

计算相机内参：

```bash
python 一键标定计算内参.py
```

运行物体三维位姿解算：

```bash
python 物体的三维位姿情况展示.py
```

如果当前目录下已经存在 `camera_params.npz`，可以直接运行位姿解算程序。

---

## 6. 环境配置与 OpenCV 测试

### 6.1 实验目标

在正式完成视觉任务前，先对本地视觉环境进行测试，确认 Python 解释器、OpenCV 库、图片路径和图像显示功能均可正常使用。

### 6.2 文件位置

```text
视觉环境测试/
├── text.py
└── yingkuangshi.png
```

### 6.3 核心思路

程序通过 `cv2.imread()` 读取本地图片，并使用 `cv2.imshow()` 显示图像。如果图像能够正常弹出，说明 OpenCV 基础环境配置成功。

### 6.4 运行方式

```bash
cd 视觉环境测试
python text.py
```

如果图片无法读取，需要重点检查：

1. 当前工作目录是否正确；
2. 图片文件名是否和代码中一致；
3. Python 解释器是否安装了 `opencv-python`；
4. 是否在支持图形界面的环境中运行。

---

## 7. 实验一：OpenCV 颜色分割

### 7.1 实验目标

本实验复现 OpenCV 颜色分割任务，目标是从输入图片 `text.png` 中提取指定颜色区域，并保存处理结果。实验采用 HSV 颜色空间进行阈值筛选，相比直接使用 BGR/RGB 空间，HSV 更适合按照颜色种类、饱和度和亮度对目标进行分离。

### 7.2 文件位置

```text
color_segmentation/
├── text.png
├── img_out.png
├── 复现颜色分割实验.py
└── 复现颜色分割实验.mp4
```

### 7.3 处理流程

```text
读取 text.png
→ 判断图片是否成功读取
→ BGR 转 HSV
→ 分离 H、S、V 三个通道
→ 分别设置 H/S/V 阈值
→ 使用 cv2.inRange 生成掩膜
→ 使用 bitwise_and 融合掩膜
→ 提取目标颜色区域
→ 显示并保存结果 img_out.png
```

### 7.4 核心阈值设置

```python
mask_h = cv2.inRange(img_h, 150, 179)
mask_s = cv2.inRange(img_s, 40, 255)
mask_v = cv2.inRange(img_v, 50, 255)
```

其中：

- `H` 通道用于筛选目标颜色范围；
- `S` 通道用于过滤灰白、低饱和区域；
- `V` 通道用于过滤过暗区域。

最终通过：

```python
mask_h_and_s = cv2.bitwise_and(mask_h, mask_s)
mask = cv2.bitwise_and(mask_h_and_s, mask_v)
img_out = cv2.bitwise_and(img_bgr, img_bgr, mask=mask)
```

保留同时满足 H、S、V 三个条件的目标像素。

### 7.5 实验结果

原始图片：

![颜色分割原图](<color_segmentation/text.png>)

分割结果：

![颜色分割结果](<color_segmentation/img_out.png>)

运行视频：

[查看颜色分割实验运行视频](<color_segmentation/复现颜色分割实验.mp4>)

### 7.6 问题总结与改进方向

1. HSV 阈值需要根据实际图片颜色和光照条件手动调整。
2. 当背景中存在相近颜色时，仅依靠颜色阈值容易产生误检。
3. 后续可以加入形态学开运算、闭运算减少噪声。
4. 可以增加滑动条动态调参功能，提高调试效率。

---

## 8. 实验二：OpenCV 最小框选与多边形拟合

### 8.1 实验目标

本实验完成目标区域的轮廓检测、最小外接矩形框选和多边形拟合。主要目标是利用 OpenCV 从图像中提取目标轮廓，并通过面积、形状、长宽比和多边形顶点等特征过滤非目标区域。

### 8.2 文件位置

```text
contour_polygon/
├── test3.png
├── 1_Contours_Pro.png
├── 2_FinalBox_Pro.png
└── OpenCV最小框选与多边形拟合.py
```

### 8.3 处理流程

```text
读取输入图像
→ 图像预处理
→ 二值化处理
→ findContours 查找轮廓
→ contourArea 过滤面积异常轮廓
→ boundingRect / minAreaRect 绘制外接框
→ approxPolyDP 进行多边形拟合
→ 根据形状条件筛选目标
→ 输出轮廓图和最终框选图
```

### 8.4 关键函数

| 函数 | 作用 |
|---|---|
| `cv2.findContours()` | 查找二值图像中的轮廓 |
| `cv2.contourArea()` | 计算轮廓面积，用于过滤小噪声或过大区域 |
| `cv2.boundingRect()` | 得到普通外接矩形 |
| `cv2.minAreaRect()` | 得到可旋转的最小外接矩形 |
| `cv2.approxPolyDP()` | 对轮廓进行多边形拟合 |
| `cv2.drawContours()` | 绘制检测出的轮廓或外接框 |

### 8.5 实验结果

输入图像：

![多边形拟合输入图](<contour_polygon/test3.png>)

轮廓检测结果：

![轮廓检测结果](<contour_polygon/1_Contours_Pro.png>)

最终框选结果：

![最终框选结果](<contour_polygon/2_FinalBox_Pro.png>)

### 8.6 问题总结与改进方向

1. 仅依靠轮廓面积进行筛选容易误检，需要结合形状特征进一步过滤。
2. 多边形拟合中 `epsilon` 参数会影响拟合精度，过大可能丢失细节，过小可能保留噪声。
3. 复杂背景下可以先进行颜色分割或亮度阈值处理，再进行轮廓检测。
4. 后续可进一步结合目标几何约束，提高筛选稳定性。

---

## 9. 拓展实验：基于视频的装甲板灯条识别

### 9.1 实验目标

在完成基础最小框选与多边形拟合后，本项目进一步尝试对视频中的装甲板灯条进行检测。该部分主要通过颜色分割、轮廓筛选、灯条长宽比判断、角度约束和灯条配对，实现对装甲板区域的动态框选。

### 9.2 文件位置

```text
contour_polygon/装甲板 视频识别/
├── 2.py
├── 实验测试原视频.mp4
├── 装甲板识别视频.mp4
└── Result_Output.mp4
```

### 9.3 处理流程

```text
读取视频
→ 逐帧旋转校正画面方向
→ BGR 转 HSV
→ 根据蓝色灯条颜色范围构建 mask
→ 形态学闭运算连接灯条区域
→ findContours 查找候选轮廓
→ 通过面积和长宽比筛选灯条
→ 根据中心距离、倾斜角度、长度差异进行灯条配对
→ 绘制绿色灯条框和红色装甲板框
→ 实时显示并保存处理后视频
```

### 9.4 调试设计

程序中加入了 OpenCV 滑动条调参面板：

```text
Halo Brightness
Halo Saturation
Min Area
Min Aspect Ratio
Max Aspect Ratio
Armor Max Width
```

运行时可以按空格暂停画面，调节参数后继续播放。这样能够在不同光照、不同视频帧下观察阈值和筛选条件对识别结果的影响。

### 9.5 运行方式

```bash
cd "contour_polygon/装甲板 视频识别"
python 2.py
```

操作说明：

- 空格键：暂停 / 继续；
- `q` 键：退出；
- 输出视频：`Result_Output.mp4`。

### 9.6 实验结果

输入视频：

[查看实验测试原视频](<contour_polygon/装甲板 视频识别/实验测试原视频.mp4>)

输出视频：

[查看装甲板识别输出视频](<contour_polygon/装甲板 视频识别/Result_Output.mp4>)

### 9.7 问题总结与改进方向

1. 视频中灯条亮度变化会影响 HSV 阈值稳定性。
2. 杂光区域可能被误认为灯条，需要进一步加强几何约束。
3. 当前配对逻辑主要依赖手工规则，后续可结合装甲板宽高比例、灯条角度一致性和历史帧跟踪优化。
4. 可以加入 Kalman 滤波或简单时序跟踪，减少检测框抖动。

---

## 10. 实验三：相机标定与 solvePnP 物体三维位姿解算

### 10.1 实验目标

本实验完成相机标定与真实矩形目标的三维位姿解算。实验首先使用棋盘格图片对摄像头进行标定，得到相机内参矩阵和畸变参数；随后选取真实世界中的矩形目标，检测矩形四个角点，并结合相机内参使用 `cv2.solvePnP()` 求解目标相对于相机的旋转向量和平移向量，最后将三维坐标轴投影到图像中，实现物体三维姿态可视化。

本实验使用真实纸面矩形目标进行检测，没有使用手机屏幕显示的矩形，也没有使用他人拍摄的图片，从而保证目标具有真实物理尺寸，满足 solvePnP 位姿解算要求。

### 10.2 文件位置

```text
solvepnp_pose/
├── 采集标定照片.py
├── 一键标定计算内参.py
├── 物体的三维位姿情况展示.py
├── camera_params.npz
├── 棋盘格示意图.png
├── 一键标定计算内参数.mp4
├── 展现物体的三维位姿情况.mp4
├── solvepnp_result.mp4
└── calibration_images/
    ├── img_0.jpg
    ├── img_1.jpg
    ├── img_2.jpg
    └── ...
```

### 10.3 相机标定流程

```text
采集棋盘格图片
→ 棋盘格角点检测
→ 亚像素角点优化
→ cv2.calibrateCamera 计算相机内参
→ 计算重投影误差
→ 保存 camera_params.npz
```

运行采集程序：

```bash
python 采集标定照片.py
```

运行内参计算程序：

```bash
python 一键标定计算内参.py
```

标定程序使用的棋盘格参数：

```python
CHECKERBOARD = (9, 6)
SQUARE_SIZE = 25.0
```

其中：

- `CHECKERBOARD = (9, 6)` 表示棋盘格内角点数量为 9 × 6；
- `SQUARE_SIZE = 25.0` 表示每个棋盘格小方块边长为 25 mm。

本次实验中，程序成功生成了：

```text
camera_params.npz
```

该文件保存了：

- `camera_matrix`：相机内参矩阵；
- `dist_coeffs`：相机畸变参数。

本次标定的平均重投影误差约为：

```text
0.0391 px
```

重投影误差越小，说明标定结果越稳定。本次误差较小，说明棋盘格角点检测和相机标定结果较为可靠。

### 10.4 solvePnP 位姿解算流程

```text
读取 camera_params.npz
→ 打开摄像头
→ 检测真实矩形目标轮廓
→ approxPolyDP 拟合四边形
→ 对四个角点排序
→ 构建 objectPoints 和 imagePoints
→ 调用 cv2.solvePnP 求解 rvec/tvec
→ 调用 cv2.projectPoints 投影三维坐标轴
→ 显示并保存位姿结果视频
```

运行：

```bash
python 物体的三维位姿情况展示.py
```

### 10.5 真实目标尺寸与 3D 点定义

本实验中，真实矩形目标尺寸设置为：

```python
RECT_W = 100.0
RECT_H = 70.0
```

单位为 mm。

程序中将矩形中心定义为物体坐标系原点，矩形所在平面为 `z = 0`：

```python
object_points = np.array([
    [-RECT_W / 2, -RECT_H / 2, 0],
    [ RECT_W / 2, -RECT_H / 2, 0],
    [ RECT_W / 2,  RECT_H / 2, 0],
    [-RECT_W / 2,  RECT_H / 2, 0],
], dtype=np.float32)
```

检测到的图像角点会按照：

```text
左上角 → 右上角 → 右下角 → 左下角
```

进行排序，以保证 `objectPoints` 与 `imagePoints` 一一对应。

### 10.6 solvePnP 核心代码

```python
calibration = np.load(CALIBRATION_FILE)
camera_matrix = calibration["camera_matrix"].astype(np.float32)
dist_coeffs = calibration["dist_coeffs"].astype(np.float32)

success, rvec, tvec = cv2.solvePnP(
    object_points,
    image_points,
    camera_matrix,
    dist_coeffs,
    flags=flags,
)
```

其中：

- `object_points`：真实世界中的 3D 点坐标；
- `image_points`：图像中的 2D 像素点坐标；
- `camera_matrix`：相机内参矩阵；
- `dist_coeffs`：畸变系数；
- `rvec`：旋转向量；
- `tvec`：平移向量。

由于本实验目标是平面矩形，程序优先使用：

```python
cv2.SOLVEPNP_IPPE
```

若当前 OpenCV 版本不支持，则切换到：

```python
cv2.SOLVEPNP_ITERATIVE
```

### 10.7 三维坐标轴可视化

位姿解算成功后，使用 `cv2.projectPoints()` 将三维坐标轴投影到二维图像中：

```python
projected_points, _ = cv2.projectPoints(
    axis_points,
    rvec,
    tvec,
    camera_matrix,
    dist_coeffs
)
```

画面中的坐标轴含义：

- 红色：X 轴；
- 绿色：Y 轴；
- 蓝色：Z 轴。

程序同时会显示目标相对于相机的平移向量：

```text
tvec: x=...mm y=...mm z=...mm
```

其中：

- `x`：目标中心相对于相机光心的水平偏移；
- `y`：目标中心相对于相机光心的竖直偏移；
- `z`：目标到相机的深度距离。

### 10.8 实验结果

棋盘格示意图：

![棋盘格示意图](<solvepnp_pose/棋盘格示意图.png>)

相机标定与内参计算过程：

[查看相机标定过程视频](<solvepnp_pose/一键标定计算内参数.mp4>)

三维位姿展示过程：

[查看三维位姿展示视频](<solvepnp_pose/展现物体的三维位姿情况.mp4>)

solvePnP 位姿解算结果：

[查看 solvePnP 结果视频](<solvepnp_pose/solvepnp_result.mp4>)

### 10.9 注意事项

1. 相机标定和 solvePnP 主程序运行时，应尽量保持摄像头分辨率一致。
2. 更换摄像头后，需要重新采集棋盘格图片并重新生成 `camera_params.npz`。
3. 更换矩形目标后，需要重新测量真实尺寸，并修改 `RECT_W` 和 `RECT_H`。
4. `objectPoints` 和 `imagePoints` 的四个点顺序必须严格对应，否则坐标轴方向可能异常。
5. 如果程序找不到 `camera_params.npz`，需要确认该文件是否与主程序位于同一目录。
6. 如果摄像头无法打开，可以尝试将 `cv2.VideoCapture(0)` 中的 `0` 改为其他摄像头编号。

### 10.10 问题总结与改进方向

1. 矩形检测依赖图像阈值和轮廓筛选，复杂背景下稳定性仍可提升。
2. 可以进一步优化角点检测方法，降低坐标轴抖动。
3. 可以对 `tvec` 结果加入滤波，提高视频显示稳定性。
4. 后续可以尝试 ArUco Marker 或 AprilTag，提高标记检测鲁棒性。
5. 后续希望将位姿解算与 RoboMaster 装甲板识别、目标预测和云台控制进一步结合。

---

## 11. 调试记录与问题总结

### 11.1 文件路径问题

本项目中多处使用相对路径读取图片或视频。如果运行时报错找不到文件，需要确认当前工作目录是否为对应实验文件夹。

例如颜色分割实验需要在：

```bash
cd color_segmentation
```

后运行程序，否则 `cv2.imread("text.png")` 可能读取失败。

### 11.2 OpenCV 窗口显示问题

在 Ubuntu / PyCharm 环境下运行 `cv2.imshow()` 时，可能出现 Qt、Wayland 或字体相关提示。部分提示不影响程序运行；如果窗口无法显示，需要检查：

1. 当前环境是否支持图形界面；
2. Python 解释器是否选择正确；
3. `opencv-python` 是否安装到当前解释器中；
4. 是否误用了其它虚拟环境或 Conda 环境。

### 11.3 HSV 阈值调试问题

颜色分割和灯条识别都对 HSV 阈值比较敏感。光照变化、曝光变化和背景干扰都会影响识别效果。后续可通过滑动条调参、形态学处理和几何约束提升稳定性。

### 11.4 solvePnP 稳定性问题

solvePnP 对以下因素较敏感：

1. 相机内参是否准确；
2. 真实物体尺寸是否测量正确；
3. 四个图像角点顺序是否正确；
4. 检测到的角点是否稳定；
5. 目标是否为真实世界中的平面物体。

如果出现坐标轴方向错误或抖动较大，需要优先检查 `objectPoints` 和 `imagePoints` 的对应关系。

---

## 12. AI 辅助说明

在本项目完成过程中，我使用生成式 AI 辅助进行学习、排错和 README 整理，主要包括：

1. OpenCV 环境配置问题排查；
2. HSV 阈值范围理解与调试思路整理；
3. `findContours`、`boundingRect`、`minAreaRect`、`approxPolyDP` 等函数理解；
4. 视频处理中的路径、旋转、保存和窗口显示问题排查；
5. 相机标定中棋盘格内角点、相机内参、畸变参数、重投影误差的理解；
6. solvePnP 中 `objectPoints`、`imagePoints`、`cameraMatrix`、`distCoeffs`、`rvec`、`tvec` 的含义理解；
7. 项目 README 结构整理和表达优化。

AI 主要用于辅助理解和调试，最终代码均已在本地运行验证，并将运行结果图片或视频提交到仓库中。

---

## 13. 项目收获

通过本次视觉组招新考核，我主要完成了以下学习：

1. 熟悉了 OpenCV 的图像读取、显示、保存和视频处理流程；
2. 理解了 BGR、RGB、HSV 颜色空间的区别；
3. 掌握了基于阈值和掩膜的颜色分割方法；
4. 学习了轮廓检测、最小外接矩形和多边形拟合方法；
5. 初步完成了基于视频的灯条检测和装甲板区域框选；
6. 初步理解了相机标定、相机内参和畸变参数的作用；
7. 初步完成了基于 solvePnP 的真实物体三维位姿解算；
8. 学会了将代码、运行结果、调试记录和演示视频整理到开源仓库中。

目前项目仍有很多可以继续优化的地方，例如增强复杂光照下的鲁棒性、优化视频检测稳定性、减少 solvePnP 坐标轴抖动等。后续希望继续深入学习 RoboMaster 视觉任务中的装甲板识别、目标预测、位姿解算和自动瞄准等内容。

---

## 14. 作者信息

- 姓名：巩皓怡
- 学号：24201034
- 学校：北京交通大学
- 专业：人工智能
- 方向意向：RoboMaster 视觉组
