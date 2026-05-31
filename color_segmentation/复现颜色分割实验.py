# 导入 OpenCV 库，后面所有 cv2.xxx 的函数都来自这个库
import cv2

# 读取当前运行目录下名为 test.png 的图片
# OpenCV 读取图片时默认格式是 BGR，不是 RGB
img_bgr = cv2.imread("text.png")

# 判断图片是否读取失败
# 如果路径不对、文件名不对、图片不存在，img_bgr 就会是 None
if img_bgr is None:
    # 在控制台输出提示信息，告诉用户图片读取失败
    print("图片读取失败，请检查 test.png 是否在当前运行目录下")

    # 退出程序，不再继续往下执行
    # 因为图片都没读到，后面的颜色转换肯定会报错
    exit()

# 将 BGR 颜色空间的图片转换为 HSV 颜色空间
# BGR 更适合计算机存储，HSV 更适合做颜色筛选
img_hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)

# 将 HSV 图像拆分成三个单独的通道
# img_h 表示 H 通道：色相，决定颜色种类，比如红色、黄色、蓝色
# img_s 表示 S 通道：饱和度，决定颜色鲜艳程度
# img_v 表示 V 通道：亮度，决定颜色明暗程度
img_h, img_s, img_v = cv2.split(img_hsv)

# 对 H 色相通道进行范围筛选
# 这个范围大概对应偏黄色区域，不同图片需要根据目标颜色调整
# 满足条件的位置在 mask_h 中变成白色 255，不满足的位置变成黑色 0
mask_h = cv2.inRange(img_h, 150, 179)

# 对 S 饱和度通道进行范围筛选
# 饱和度越高，颜色越鲜艳；这样可以过滤掉灰白、暗淡的区域
# 满足条件的位置变成白色 255，不满足的位置变成黑色 0
mask_s = cv2.inRange(img_s, 40, 255)

# 对 V 亮度通道进行范围筛选
# 这样可以过滤掉太暗的区域
# 满足条件的位置变成白色 255，不满足的位置变成黑色 0
mask_v = cv2.inRange(img_v, 50, 255)

# 将 H 通道筛选结果和 S 通道筛选结果进行按位与操作
# 只有同时满足 H 范围和 S 范围的像素才会被保留下来
# 也就是：既是目标颜色，又有足够饱和度
mask_h_and_s = cv2.bitwise_and(mask_h, mask_s)

# 再将上一步结果和 V 通道筛选结果进行按位与操作
# 只有同时满足 H、S、V 三个条件的像素才会被保留下来
# 最终得到完整的目标区域掩膜 mask
mask = cv2.bitwise_and(mask_h_and_s, mask_v)

# 使用最终的 mask 掩膜从原图中提取目标区域
# mask 中白色区域对应的原图内容会被保留
# mask 中黑色区域对应的原图内容会被变成黑色
img_out = cv2.bitwise_and(img_bgr, img_bgr, mask=mask)

# 弹出一个窗口显示处理后的图片
# 窗口名字叫 img，显示内容是 img_out
cv2.imshow("img", img_out)

# 将处理后的图片保存到当前运行目录下
# 保存文件名为 img_out.png
cv2.imwrite("img_out.png", img_out)

# 等待键盘按键
# 参数 0 表示无限等待，直到用户按下任意键
# 如果没有这一句，图片窗口可能会一闪而过
cv2.waitKey(0)

# 关闭所有 OpenCV 创建的窗口
cv2.destroyAllWindows()