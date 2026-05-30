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
│   ├── solvepnp.py
│   ├── camera_calibration.py
│   ├── input/
│   └── output/
├── assets/
│   ├── images/
│   └── videos/
└── debug_logs/
```

说明：

* `color_segmentation/`：颜色分割实验代码与结果
* `contour_polygon/`：最小框选与多边形拟合实验代码与结果
* `solvepnp_pose/`：相机标定与 solvePnP 位姿解算实验代码与结果
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

## 6. 实验三：相机标定与 solvePnP 位姿解算

### 6.1 实验目标

本实验主要完成对真实世界目标物体的位姿解算。实验中使用真实纸面矩形作为检测目标，通过识别矩形四个角点，结合相机内参矩阵和畸变参数，使用 `cv2.solvePnP()` 求解目标相对于相机的旋转向量和平移向量，并通过坐标轴投影实现三维姿态可视化。

### 6.2 注意事项

本实验使用的目标为真实世界中的纸面矩形，不使用手机屏幕显示的矩形，也不使用他人拍摄的照片作为目标。这样可以保证目标物体具有真实的空间尺度，便于进行位姿解算。

### 6.3 核心思路

主要流程如下：

```text
准备真实矩形目标
→ 获取或设置相机内参 cameraMatrix
→ 设置畸变参数 distCoeffs
→ 检测矩形四个角点 imagePoints
→ 根据真实尺寸定义 objectPoints
→ 使用 cv2.solvePnP 求解 rvec 和 tvec
→ 使用 cv2.projectPoints 投影三维坐标轴
→ 在图像/视频中绘制姿态坐标轴
→ 保存结果视频
```

### 6.4 相机内参

本实验使用的相机内参矩阵格式如下：

```python
cameraMatrix = np.array([
    [fx, 0, cx],
    [0, fy, cy],
    [0, 0, 1]
], dtype=np.float32)
```

畸变参数格式如下：

```python
distCoeffs = np.array([k1, k2, p1, p2, k3], dtype=np.float32)
```

如果畸变较小，也可以先将畸变参数近似设置为 0 进行实验：

```python
distCoeffs = np.zeros((5, 1), dtype=np.float32)
```

### 6.5 运行方式

进入对应目录：

```bash
cd solvepnp_pose
python solvepnp.py
```

### 6.6 运行结果

检测目标图像：

![solvePnP 输入图像](assets/images/solvepnp_input.png)

三维坐标轴可视化结果：

![solvePnP 位姿解算结果](assets/images/solvepnp_result.png)

输出视频：

```text
solvepnp_pose/output/solvepnp_result.mp4
```

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

# 4. 运行 solvePnP 位姿解算实验
cd ../solvepnp_pose
python solvepnp.py
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
5. 程序报错与运行路径问题排查

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
7. 学会了将实验代码、运行结果、调试记录整理到开源仓库中

本项目仍有很多可以改进的地方，例如增强光照变化下的鲁棒性、优化角点排序算法、提高视频实时处理稳定性等。后续希望能继续深入学习 RoboMaster 视觉任务中的目标检测、装甲板识别、位姿解算、目标预测和自动瞄准等内容。

---

## 11. 作者信息

* 姓名：巩皓怡
* 学校：北京交通大学
* 专业：人工智能
* 方向意向：RoboMaster 视觉组
