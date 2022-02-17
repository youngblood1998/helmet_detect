# from calculate_area import CalArea
#
#
# cal = CalArea()
# print(cal.get_point_area([[0, 5], [0, 10], [5, 10], [5, 5]]))

#-------------------------------------------------------------------

# import numpy as np
# import math
#
# def isRotationMatrix(R):
#     Rt = np.transpose(R)
#     shouldBeIdentity = np.dot(Rt, R)
#     I = np.identity(3, dtype=R.dtype)
#     n = np.linalg.norm(I - shouldBeIdentity)
#     return n < 1e-6
#
#
# def rotationMatrixToEulerAngles(R):
#     # assert(isRotationMatrix(R))
#
#     sy = math.sqrt(R[0, 0] * R[0, 0] + R[1, 0] * R[1, 0])
#
#     singular = sy < 1e-6
#
#     if not singular:
#         x = math.atan2(R[2, 1], R[2, 2])
#         y = math.atan2(-R[2, 0], sy)
#         z = math.atan2(R[1, 0], R[0, 0])
#     else:
#         x = math.atan2(-R[1, 2], R[1, 1])
#         y = math.atan2(-R[2, 0], sy)
#         z = 0
#
#     return np.array([x, y, z])
#
#
# R = np.array([[ 2.67281837e-02, -9.04387480e-01,  2.80697554e+02],
#  [ 2.21957342e-02, -7.45233723e-01,  2.31218281e+02],
#  [ 9.60548946e-05, -3.22252443e-03,  1.00000000e+00]])
#
# print(rotationMatrixToEulerAngles(R))

#---------------------------------------------------------------------------------

# from calculate_area import CalArea
# import numpy as np
#
# R = np.array([[ 2.67281837e-02, -9.04387480e-01,  2.80697554e+02],
#  [ 2.21957342e-02, -7.45233723e-01,  2.31218281e+02],
#  [ 9.60548946e-05, -3.22252443e-03,  1.00000000e+00]])
#
# cal = CalArea()
# print(cal.rotationMatrix_to_eulerAngles(R))

#--------------------------------------------------------------------------

import cv2
import numpy as np

img = cv2.imread('data_color/matches/w1-1.bmp')
cv2.normalize(img, img, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
img = cv2.resize(img, dsize=None, fx=0.1, fy=0.1, interpolation=cv2.INTER_LINEAR)

h, w, d = img.shape
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 0, 255)

# 200 代表应该检测到的行的最小长度
lines = cv2.HoughLines(edges, 1, np.pi / 180, 60)

for i in range(len(lines)):
 for rho, theta in lines[i]:
  a = np.cos(theta)
  b = np.sin(theta)
  x0 = a * rho
  y0 = b * rho
  x1 = int(x0 + w * (-b))
  y1 = int(y0 + w * (a))
  x2 = int(x0 - w * (-b))
  y2 = int(y0 - w * (a))

  cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
cv2.imshow("edges", edges)
cv2.imshow("lines", img)
cv2.waitKey()
cv2.destroyAllWindows()

#-------------------------------------------------------

# import cv2
# import numpy as np
#
# img = cv2.imread('data_color/matches/o1-2.bmp')
# cv2.normalize(img, img, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
# img = cv2.resize(img, dsize=None, fx=0.1, fy=0.1, interpolation=cv2.INTER_LINEAR)
#
# gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
# edges = cv2.Canny(gray,50,150)
#
#
# #最低线段的长度，小于这个值的线段被抛弃
# minLineLength = 50
#
# #线段中点与点之间连接起来的最大距离，在此范围内才被认为是单行
# maxLineGap =5
#
# #100阈值，累加平面的阈值参数，即：识别某部分为图中的一条直线时它在累加平面必须达到的值，低于此值的直线将被忽略。
# lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength, maxLineGap)
#
# for i in range(len(lines)):
#     for x1,y1,x2,y2 in lines[i]:
#         cv2.line(img, (x1,y1), (x2,y2), (0,255,0), 2)
#
# cv2.imshow("edges",edges)
# cv2.imshow("lines", img)
# cv2.waitKey()
# cv2.destroyAllWindows()

#------------------------------------------------------------

# import cv2
# import math
#
# img=cv2.imread("data_color/matches/b1-1.bmp.bmp")
# cv2.normalize(img, img, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
# img = cv2.resize(img, dsize=None, fx=0.1, fy=0.1, interpolation=cv2.INTER_LINEAR)
#
# img=cv2.blur(img,(1,1))
# imgray=cv2.Canny(img,50,250,3)#Canny边缘检测，参数可更改
# #cv2.imshow("0",imgray)
# ret,thresh = cv2.threshold(imgray,127,255,cv2.THRESH_BINARY)
# contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)#contours为轮廓集，可以计算轮廓的长度、面积等
# for cnt in contours:
#     if len(cnt)>50:
#         S1=cv2.contourArea(cnt)
#         ell=cv2.fitEllipse(cnt)
#         S2 =math.pi*ell[1][0]*ell[1][1]
#         if (S1/S2)>0.2 :#面积比例，可以更改，根据数据集。。。
#             img = cv2.ellipse(img, ell, (0, 255, 0), 2)
#             print(str(S1) + "    " + str(S2)+"   "+str(ell[0][0])+"   "+str(ell[0][1]))
# cv2.imshow("0",img)
# cv2.waitKey(0)
