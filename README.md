# BNGU 北京校区视觉组招新考核项目

## 1. 项目简介

本仓库为 BNGU 北京校区视觉组招新考核项目，主要基于 Python + OpenCV 完成计算机视觉基础任务复现与实践，包括：

1. OpenCV 颜色分割实验
2. OpenCV 最小框选与多边形拟合实验
3. 相机标定与 solvePnP 物体位姿解算实验

项目重点围绕图像预处理、HSV 颜色空间分割、轮廓检测、最小外接矩形、多边形拟合、相机内参使用以及目标物体三维姿态估计展开。通过本项目，我初步熟悉了视觉任务从图像输入、特征提取、目标筛选到结果可视化的完整流程。

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

# 实验三：基于 OpenCV 的相机标定与三维位姿解算 (solvePnP)

## 1. 实验目的

本实验旨在通过计算机视觉技术，实现对目标物体在真实三维空间中的绝对位姿估计。核心流程包括：利用张正友标定法获取相机内参（焦距、光学中心）与畸变系数，随后利用 `cv2.solvePnP` 算法结合相机内参，计算已知物理尺寸目标（100x70mm 矩形）相对于相机光心的平移向量（tvec）与旋转向量（rvec），并将其三维坐标系可视化。

## 2. 工程目录结构

提交的文件包含以下核心代码及生成产物：

* **`采集标定照片.py`**: 负责在 1280x720 强制分辨率下，实时采集并保存多角度的棋盘格标定图像至本地。
* **`一键标定计算内参.py`**: 读取采集好的图像集，利用 `cv2.calibrateCamera` 提取亚像素角点并解算相机内参矩阵与畸变系数，保存为 `.npz` 文件。
* **`物体的三维位姿情况展示.py`**: 主功能程序。读取保存的相机内参，实时检测 100x70mm 矩形角点，利用 PnP 算法进行空间测距定位，并在图像上渲染 X、Y、Z 三维坐标轴。
* **`camera_params.npz`**: 标定成功后生成的相机物理参数文件（核心数据）。
* **`calibration_images/`**: 存放用于相机标定的多角度棋盘格原始照片集。
* **`棋盘格标定图.png`**: 用于打印的原始棋盘格图片（物理测量单格边长为 25.0mm）。
* **`solvepnp_result.mp4` & `一键标定计算内参数.mp4`**: 实验过程及最终位姿解算可视化效果的屏幕录制视频。

## 3. 实验关键步骤说明

1. **准备阶段**：打印 `棋盘格标定图.png`，并用高精度直尺测量单个黑色方块的物理边长，确认其为 25.0mm。
2. **数据采集**：运行 `采集标定照片.py`，手持棋盘格在不同深度、不同倾角下拍摄了 20 余张标定照片。
3. **内参求解**：运行 `一键标定计算内参.py`。程序成功提取角点并完成解算，终端输出显示**总平均重投影误差为 0.0391 px**，远低于 0.5 px 的标准阈值，证明标定过程极度精准，并将数据固化至 `camera_params.npz`。
4. **位姿估计 (PnP)**：运行 `物体的三维位姿情况展示.py`。程序成功加载内参，精准框选画面中的目标矩形。输出的 `tvec` 数据中：

   * **X, Y** 代表目标中心偏离镜头正中心（光轴）的物理坐标偏差。
   * **Z** 代表目标距离镜头的光学深度（即真实物理距离）。
   * 实验验证表明，测算出的 Z 轴距离与实际卷尺测量距离高度吻合。

## 4. 环境依赖

* Python 3.x
* OpenCV (`pip install opencv-python`)
* NumPy (`pip install numpy`)

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

## 11. 作者信息

* 姓名：巩皓怡
* 学校：北京交通大学
* 专业：人工智能
* 方向意向：RoboMaster 视觉组
