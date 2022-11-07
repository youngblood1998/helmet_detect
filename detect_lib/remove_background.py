import cv2 as cv
import numpy as np


def calc_diff(pixel, bg_color):
   return (pixel[0] - bg_color[0]) ** 2 + (pixel[1] - bg_color[1]) ** 2 + (pixel[2] - bg_color[2]) ** 2

def FillHole(mask):
   image, contours, hierarchy = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
   len_contour = len(contours)
   contour_list = []
   for i in range(len_contour):
      drawing = np.zeros_like(mask, np.uint8)  # create a black image
      img_contour = cv.drawContours(drawing, contours, i, (255, 255, 255), -1)
      contour_list.append(img_contour)

   out = sum(contour_list)
   return out

def remove_bg(bg_color, threshold, img):

   img = cv.blur(img, (7,7))
   # logo = cv.cvtColor(logo, cv.COLOR_BGR2BGRA)  # 将图像转成带透明通道的BGRA格式
   h, w = img.shape[0:2]
   binary = np.zeros((h, w), dtype=np.uint8)
   for i in range(h):
      for j in range(w):
         if calc_diff(img[i][j], bg_color) >= threshold:
            # # 若果logo[i][j]为背景，将其颜色设为黑色
            binary[i][j] = 255
         else:
            binary[i][j] = 0

   binary = FillHole(binary)
   area = np.count_nonzero(binary)
   return area, binary
