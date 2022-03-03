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

# import cv2
# import numpy as np
#
# img = cv2.imread('data_color/matches/w1-1.bmp')
# cv2.normalize(img, img, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
# img = cv2.resize(img, dsize=None, fx=0.1, fy=0.1, interpolation=cv2.INTER_LINEAR)
#
# h, w, d = img.shape
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# edges = cv2.Canny(gray, 0, 255)
#
# # 200 代表应该检测到的行的最小长度
# lines = cv2.HoughLines(edges, 1, np.pi / 180, 60)
#
# for i in range(len(lines)):
#  for rho, theta in lines[i]:
#   a = np.cos(theta)
#   b = np.sin(theta)
#   x0 = a * rho
#   y0 = b * rho
#   x1 = int(x0 + w * (-b))
#   y1 = int(y0 + w * (a))
#   x2 = int(x0 - w * (-b))
#   y2 = int(y0 - w * (a))
#
#   cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
# cv2.imshow("edges", edges)
# cv2.imshow("lines", img)
# cv2.waitKey()
# cv2.destroyAllWindows()

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

#-------------------------------------------------------------------------------------------------------

# from ImageConvert import *
# from MVSDK import *
# from camera_lib import enumCameras, openCamera, closeCamera, setLineTriggerConf, setExposureTime
# import time
# import numpy
# import cv2
#
# g_isStop=0
#
# def test_callback(frame, userInfo):
#
#     if (g_isStop == 1):
#         return
#
#     nRet = frame.contents.valid(frame)
#     if (nRet != 0):
#         print("frame is invalid!")
#         # 释放驱动图像缓存资源
#         frame.contents.release(frame)
#         return
#
#     print("BlockId = %d userInfo = %s" % (frame.contents.getBlockId(frame), c_char_p(userInfo).value))
#
#     imageParams = IMGCNV_SOpenParam()
#     imageParams.dataSize = frame.contents.getImageSize(frame)
#     imageParams.height = frame.contents.getImageHeight(frame)
#     imageParams.width = frame.contents.getImageWidth(frame)
#     imageParams.paddingX = frame.contents.getImagePaddingX(frame)
#     imageParams.paddingY = frame.contents.getImagePaddingY(frame)
#     imageParams.pixelForamt = frame.contents.getImagePixelFormat(frame)
#
#     # 将裸数据图像拷出
#     imageBuff = frame.contents.getImage(frame)
#     userBuff = c_buffer(b'\0', imageParams.dataSize)
#     memmove(userBuff, c_char_p(imageBuff), imageParams.dataSize)
#
#     # 释放驱动图像缓存资源
#     frame.contents.release(frame)
#
#     # 如果图像格式是 Mono8 直接使用
#     if imageParams.pixelForamt == EPixelType.gvspPixelMono8:
#         grayByteArray = bytearray(userBuff)
#         cvImage = numpy.array(grayByteArray).reshape(imageParams.height, imageParams.width)
#     else:
#         # 转码 => BGR24
#         rgbSize = c_int()
#         rgbBuff = c_buffer(b'\0', imageParams.height * imageParams.width * 3)
#
#         nRet = IMGCNV_ConvertToBGR24(cast(userBuff, c_void_p), \
#                                      byref(imageParams), \
#                                      cast(rgbBuff, c_void_p), \
#                                      byref(rgbSize))
#
#         colorByteArray = bytearray(rgbBuff)
#         cvImage = numpy.array(colorByteArray).reshape(imageParams.height, imageParams.width, 3)
#     cv2.imwrite("./image/image.bmp", cvImage)
#
# frameCallbackFuncEx = callbackFuncEx(test_callback)
#
# def demo():
#     # 发现相机
#     cameraCnt, cameraList = enumCameras()
#     if cameraCnt is None:
#         return -1
#
#     # 显示相机信息
#     for index in range(0, cameraCnt):
#         camera = cameraList[index]
#         print("\nCamera Id = " + str(index))
#         print("Key           = " + str(camera.getKey(camera)))
#         print("vendor name   = " + str(camera.getVendorName(camera)))
#         print("Model  name   = " + str(camera.getModelName(camera)))
#         print("Serial number = " + str(camera.getSerialNumber(camera)))
#
#     camera = cameraList[0]
#
#     # 打开相机
#     nRet = openCamera(camera)
#     if (nRet != 0):
#         print("openCamera fail.")
#         return -1;
#
#     # 创建流对象
#     streamSourceInfo = GENICAM_StreamSourceInfo()
#     streamSourceInfo.channelId = 0
#     streamSourceInfo.pCamera = pointer(camera)
#
#     streamSource = pointer(GENICAM_StreamSource())
#     nRet = GENICAM_createStreamSource(pointer(streamSourceInfo), byref(streamSource))
#     if (nRet != 0):
#         print("create StreamSource fail!")
#         return -1
#
#     # 注册拉流回调函数
#     userInfo = b"jay"
#     nRet = streamSource.contents.attachGrabbingEx(streamSource, frameCallbackFuncEx, userInfo)
#     if (nRet != 0):
#         print("attachGrabbingEx fail!")
#         # 释放相关资源
#         streamSource.contents.release(streamSource)
#         return -1
#
#     # 设置曝光时间
#     nRet = setExposureTime(camera, 200)
#     if (nRet != 0):
#         print("set ExposureTime fail")
#         # 释放相关资源
#         streamSource.contents.release(streamSource)
#         return -1
#
#     # 设置外触发
#     nRet = setLineTriggerConf(camera)
#     if (nRet != 0):
#         print("set LineTriggerConf fail!")
#         # 释放相关资源
#         streamSource.contents.release(streamSource)
#         return -1
#     else:
#         print("set LineTriggerConf success!")
#
#     # 开始拉流
#     nRet = streamSource.contents.startGrabbing(streamSource, c_ulonglong(0), \
#                                                c_int(GENICAM_EGrabStrategy.grabStrartegySequential))
#     if (nRet != 0):
#         print("startGrabbing fail!")
#         # 释放相关资源
#         streamSource.contents.release(streamSource)
#         return -1
#
#     # 自由拉流 x 秒
#     time.sleep(60)
#     global g_isStop
#     g_isStop = 1
#
#     # 反注册回调函数
#     nRet = streamSource.contents.detachGrabbingEx(streamSource, frameCallbackFuncEx, userInfo)
#     if (nRet != 0):
#         print("detachGrabbingEx fail!")
#         # 释放相关资源
#         streamSource.contents.release(streamSource)
#         return -1
#
#     # 停止拉流
#     nRet = streamSource.contents.stopGrabbing(streamSource)
#     if (nRet != 0):
#         print("stopGrabbing fail!")
#         # 释放相关资源
#         streamSource.contents.release(streamSource)
#         return -1
#
#     # 关闭相机
#     nRet = closeCamera(camera)
#     if (nRet != 0):
#         print("closeCamera fail")
#         # 释放相关资源
#         streamSource.contents.release(streamSource)
#         return -1
#
#     # 释放相关资源
#     streamSource.contents.release(streamSource)
#
#     return 0
#
#
# if __name__ == "__main__":
#
#     nRet = demo()
#     if nRet != 0:
#         print("Some Error happend")
#     print("--------- Demo end ---------")
#     # 3s exit
#     time.sleep(0.2)

#------------------------------------------------------------------

# from detect_lib.sift_flann import SiftFlann
# import cv2
# import time
#
#
# if __name__ == '__main__':
#     pwd = "./data/templates/"
#     img_arr = ["b1", "b2", "g1", "o1", "o2", "w1"]
#     temp_arr = [pwd+img+".jpg" for img in img_arr]
#     start = time.time()
#     match = cv2.imread("./data/matches/b2-2.bmp")
#
#     sift = SiftFlann(min_match_count=5, resize_times=0.1)
#     result, angle = sift.match(temp_arr, match)
#     print(time.time()-start)
#     print(result, angle)

#----------------------------------------------------------------
# a = {'l': 1}
# for j in a:
#    print(type(j))

#--------------------------------------------------------------
# from camera_lib import enumCameras
#
# print(enumCameras())

#---------------------------------------------------------------
# import numpy as np
# import cv2
# import time
#
# # 读取图片并转换成黑白图
# im1 = cv2.imread('./data_color/templates/o1.bmp', cv2.IMREAD_COLOR)  # trainImage
# print(im1.shape)
#
#
# start = time.time()
# for i in range(1, 11):
#    di = i*0.1
#    img1 = cv2.resize(im1, dsize=None, fx=di, fy=di, interpolation=cv2.INTER_LINEAR)
#    # 直方图归一化，应对白色的头盔
#    cv2.normalize(img1, img1, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
#    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
#
#    # 初始化SIFT特征检测器
#    sift = cv2.SIFT_create(500)
#
#    # 使用特征检测器找特征点和描述子
#    kp1, des1 = sift.detectAndCompute(img1, None)
#    # print(type(kp1[1]), type(des1))
#    # print(kp1, des1.shape)
#    # print('--'*20)
#
#    # print(des1)
#    # print(type(des1[1][1]))
#    str1 = des1.tobytes()
#    print(type(str1))
#    des2 = np.frombuffer(str1, dtype=np.float32)
#    des2 = np.reshape(des2, (-1, 128))
#    # print(des2)
#    # print('--'*20)
# print(time.time()-start)

#--------------------------------------------------------------

# import numpy as np
# import datetime
# import cv2
# import time
# from PyQt5.QtSql import QSqlDatabase, QSqlQuery
#
# db = QSqlDatabase.addDatabase("QSQLITE")
# db.setDatabaseName('./helmetDB.db3')
# db.open()
#
# # 读取图片并转换成黑白图
# im1 = cv2.imread('./data_color/templates/o1.bmp', cv2.IMREAD_COLOR)  # trainImage
#
# di = 0.1
# img1 = cv2.resize(im1, dsize=None, fx=di, fy=di, interpolation=cv2.INTER_LINEAR)
# # 直方图归一化，应对白色的头盔
# cv2.normalize(img1, img1, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
# img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
#
# # 初始化SIFT特征检测器
# sift = cv2.SIFT_create(500)
#
# # 使用特征检测器找特征点和描述子
# kp1, des1 = sift.detectAndCompute(img1, None)
# # print(type(kp1[1]), type(des1))
# # print(kp1, des1.shape)
# # print('--'*20)
#
# # print(des1)
# # print(type(des1[1][1]))
# # str1 = des1.tobytes()
# # print(type(str1))
# # des2 = np.frombuffer(str1, dtype=np.float32)
# # des2 = np.reshape(des2, (-1, 128))
#
# im2 = im1.tobytes()
# str1 = des1.tobytes()
#
# query = QSqlQuery()
# insert_sql = 'insert into helmet values (?,?,?,?,?,?,?,?)'
# query.prepare(insert_sql)
# query.addBindValue('TSA52')
# query.addBindValue("绿")
# query.addBindValue('M')
# query.addBindValue(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
# query.addBindValue(im2)
# query.addBindValue(im1.shape[1])
# query.addBindValue(im1.shape[0])
# query.addBindValue(str1)
# query.exec_()
#
# db.close()

#-------------------------------------------
# import datetime
#
# print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

#-----------------------------------------------------
# import numpy as np
# import datetime
# import cv2
# import time
# from PyQt5.QtSql import QSqlDatabase, QSqlQuery
# import sqlite3
#
#
# # 读取图片并转换成黑白图
# im1 = cv2.imread('./data_color/templates/o1.bmp', cv2.IMREAD_COLOR)  # trainImage
#
# conn = sqlite3.connect('helmetDB.db3')
# cursor = conn.cursor()
#
# sql = 'INSERT into helmet values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
#
# x = ['SQH4-s', 'L', '绿', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),im1.shape[1], im1.shape[0], im1]
#
# for i in range(1, 11):
#    di = 0.1*i
#    img1 = cv2.resize(im1, dsize=None, fx=di, fy=di, interpolation=cv2.INTER_LINEAR)
#    # 直方图归一化，应对白色的头盔
#    cv2.normalize(img1, img1, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
#    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
#
#    # 初始化SIFT特征检测器
#    sift = cv2.SIFT_create(500)
#
#    # 使用特征检测器找特征点和描述子
#    kp1, des1 = sift.detectAndCompute(img1, None)
#
#    x.append(des1)
#
# for i in x:
#    print(type(i))
# cursor.execute(sql, x)
# conn.commit()
# cursor.close()
# conn.close()

#-------------------------------------------------------------------

# import sqlite3
# import cv2
# import numpy as np
#
# conn = sqlite3.connect('helmetDB.db3')
# cursor = conn.cursor()
# result = cursor.execute('SELECT * from helmet where model="AAA"')
# all = result.fetchall()
#
# for record in all:
#    img = np.frombuffer(record[6], dtype=np.uint8)
#    print(len(img))
#    img = np.reshape(img, (1668, 1924))
#    des = np.frombuffer(record[8], dtype=np.float32)
#    des = np.reshape(des, (-1, 128))
#    print(des)
# cv2.imshow('1', img)
# cv2.waitKey()
# cv2.destroyAllWindows()

#------------------------------------------
a = "0.01000"
print(float(a))