import cv2
import numpy as np


# 画虚线
def drawline(img, pt1, pt2, color, thickness=1, style='dotted', gap=20):
   dist = ((pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2) ** .5
   pts = []
   for i in np.arange(0, dist, gap):
      r = i / dist
      x = int((pt1[0] * (1 - r) + pt2[0] * r) + .5)
      y = int((pt1[1] * (1 - r) + pt2[1] * r) + .5)
      p = (x, y)
      pts.append(p)

   if style == 'dotted':
      for p in pts:
         cv2.circle(img, p, thickness, color, -1)
   else:
      s = pts[0]
      e = pts[0]
      i = 0
      for p in pts:
         s = e
         e = p
         if i % 2 == 1:
            cv2.line(img, s, e, color, thickness)
         i += 1

# 将图片划分成num×num的网格
def drawgrid(img, num):
   for i in range(1, num):
      drawline(img, (int(img.shape[1] * i / num), 0), (int(img.shape[1] * i / num), img.shape[0]), (0, 255, 0), 1, "")
      drawline(img, (0, int(img.shape[0] * i / num)), (img.shape[1], int(img.shape[0] * i / num)), (0, 255, 0), 1, "")