
import cv2

img = cv2.imread("yingkuangshi.png")

if img is None:
    print("图片读取失败，请检查图片文件名或路径是否正确")
else:
    cv2.namedWindow("test", cv2.WINDOW_NORMAL)
    cv2.imshow("test", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()