from detect_lib.sift_flann import SiftFlann
from ImageConvert import *
from MVSDK import *
from camera_lib import enumCameras, openCamera, closeCamera, setLineTriggerConf, setExposureTime
import time
import numpy
import cv2

g_isStop=0

def test_callback(frame, userInfo):

    if (g_isStop == 1):
        return

    nRet = frame.contents.valid(frame)
    if (nRet != 0):
        print("frame is invalid!")
        # 释放驱动图像缓存资源
        frame.contents.release(frame)
        return

    print("BlockId = %d userInfo = %s" % (frame.contents.getBlockId(frame), c_char_p(userInfo).value))

    imageParams = IMGCNV_SOpenParam()
    imageParams.dataSize = frame.contents.getImageSize(frame)
    imageParams.height = frame.contents.getImageHeight(frame)
    imageParams.width = frame.contents.getImageWidth(frame)
    imageParams.paddingX = frame.contents.getImagePaddingX(frame)
    imageParams.paddingY = frame.contents.getImagePaddingY(frame)
    imageParams.pixelForamt = frame.contents.getImagePixelFormat(frame)

    # 将裸数据图像拷出
    imageBuff = frame.contents.getImage(frame)
    userBuff = c_buffer(b'\0', imageParams.dataSize)
    memmove(userBuff, c_char_p(imageBuff), imageParams.dataSize)

    # 释放驱动图像缓存资源
    frame.contents.release(frame)

    # 如果图像格式是 Mono8 直接使用
    if imageParams.pixelForamt == EPixelType.gvspPixelMono8:
        grayByteArray = bytearray(userBuff)
        cvImage = numpy.array(grayByteArray).reshape(imageParams.height, imageParams.width)
    else:
        # 转码 => BGR24
        rgbSize = c_int()
        rgbBuff = c_buffer(b'\0', imageParams.height * imageParams.width * 3)

        nRet = IMGCNV_ConvertToBGR24(cast(userBuff, c_void_p), \
                                     byref(imageParams), \
                                     cast(rgbBuff, c_void_p), \
                                     byref(rgbSize))

        colorByteArray = bytearray(rgbBuff)
        cvImage = numpy.array(colorByteArray).reshape(imageParams.height, imageParams.width, 3)
    # cv2.imwrite("./image/image.bmp", cvImage)

    # 检测
    pwd = "./data/templates/"
    img_arr = ["b1", "b2", "g1", "o1", "o2", "w1"]
    temp_arr = [pwd + img + ".jpg" for img in img_arr]
    start = time.time()
    sift = SiftFlann(min_match_count=5, resize_times=0.3)
    result, angle = sift.match(temp_arr, cvImage)
    print(time.time() - start)
    print(result, angle)

frameCallbackFuncEx = callbackFuncEx(test_callback)

def demo():
    # 发现相机
    cameraCnt, cameraList = enumCameras()
    if cameraCnt is None:
        return -1

    # 显示相机信息
    for index in range(0, cameraCnt):
        camera = cameraList[index]
        print("\nCamera Id = " + str(index))
        print("Key           = " + str(camera.getKey(camera)))
        print("vendor name   = " + str(camera.getVendorName(camera)))
        print("Model  name   = " + str(camera.getModelName(camera)))
        print("Serial number = " + str(camera.getSerialNumber(camera)))

    camera = cameraList[0]

    # 打开相机
    nRet = openCamera(camera)
    if (nRet != 0):
        print("openCamera fail.")
        return -1;

    # 创建流对象
    streamSourceInfo = GENICAM_StreamSourceInfo()
    streamSourceInfo.channelId = 0
    streamSourceInfo.pCamera = pointer(camera)

    streamSource = pointer(GENICAM_StreamSource())
    nRet = GENICAM_createStreamSource(pointer(streamSourceInfo), byref(streamSource))
    if (nRet != 0):
        print("create StreamSource fail!")
        return -1

    # 注册拉流回调函数
    userInfo = b"jay"
    nRet = streamSource.contents.attachGrabbingEx(streamSource, frameCallbackFuncEx, userInfo)
    if (nRet != 0):
        print("attachGrabbingEx fail!")
        # 释放相关资源
        streamSource.contents.release(streamSource)
        return -1

    # 设置曝光时间
    nRet = setExposureTime(camera, 200)
    if (nRet != 0):
        print("set ExposureTime fail")
        # 释放相关资源
        streamSource.contents.release(streamSource)
        return -1

    # # 设置触发延迟时间
    # nRet = setTriggerDelay(camera, 1000000)
    # if (nRet != 0):
    #     print("set setTriggerDelay fail!")
    #     # 释放相关资源
    #     streamSource.contents.release(streamSource)
    #     return -1
    # else:
    #     print("set setTriggerDelay success!")

    # 设置外触发
    nRet = setLineTriggerConf(camera, 1000000)
    if (nRet != 0):
        print("set LineTriggerConf fail!")
        # 释放相关资源
        streamSource.contents.release(streamSource)
        return -1
    else:
        print("set LineTriggerConf success!")

    # 开始拉流
    nRet = streamSource.contents.startGrabbing(streamSource, c_ulonglong(0), \
                                               c_int(GENICAM_EGrabStrategy.grabStrartegySequential))
    if (nRet != 0):
        print("startGrabbing fail!")
        # 释放相关资源
        streamSource.contents.release(streamSource)
        return -1

    # 自由拉流 x 秒
    time.sleep(60)
    global g_isStop
    g_isStop = 1

    # 反注册回调函数
    nRet = streamSource.contents.detachGrabbingEx(streamSource, frameCallbackFuncEx, userInfo)
    if (nRet != 0):
        print("detachGrabbingEx fail!")
        # 释放相关资源
        streamSource.contents.release(streamSource)
        return -1

    # 停止拉流
    nRet = streamSource.contents.stopGrabbing(streamSource)
    if (nRet != 0):
        print("stopGrabbing fail!")
        # 释放相关资源
        streamSource.contents.release(streamSource)
        return -1

    # 关闭相机
    nRet = closeCamera(camera)
    if (nRet != 0):
        print("closeCamera fail")
        # 释放相关资源
        streamSource.contents.release(streamSource)
        return -1

    # 释放相关资源
    streamSource.contents.release(streamSource)

    return 0


if __name__ == "__main__":

    nRet = demo()
    if nRet != 0:
        print("Some Error happend")
    print("--------- Demo end ---------")
    # 3s exit
    time.sleep(0.2)