import cv2 as cv
import numpy as np


def create_rgb_hist(image):
   h, w, c = image.shape
   # 创建一个（16*16*16,1）的初始矩阵，作为直方图矩阵
   # 16*16*16的意思为三通道每通道有16个bins
   rgbhist = np.zeros([16 * 16 * 16, 1], np.float32)
   bsize = 256 / 16
   for row in range(h):
      for col in range(w):
         b = image[row, col, 0]
         g = image[row, col, 1]
         r = image[row, col, 2]
         # 人为构建直方图矩阵的索引，该索引是通过每一个像素点的三通道值进行构建
         index = int(b / bsize) * 16 * 16 + int(g / bsize) * 16 + int(r / bsize)
         # 该处形成的矩阵即为直方图矩阵
         rgbhist[int(index), 0] += 1
   return rgbhist

def hist_compare(image1, image2):
   # 创建第一幅图的rgb三通道直方图（直方图矩阵）
   hist1 = create_rgb_hist(image1)
   # 创建第二幅图的rgb三通道直方图（直方图矩阵）
   hist2 = create_rgb_hist(image2)
   # 进行三种方式的直方图比较
   match = cv.compareHist(hist1, hist2, cv.HISTCMP_CORREL)
   return match