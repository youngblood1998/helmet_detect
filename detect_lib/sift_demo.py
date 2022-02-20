import numpy as np
import cv2
import time

start = time.time()

# 最小匹配数
MIN_MATCH_COUNT = 10

# 读取图片并转换成黑白图
im1 = cv2.imread('./data_color/templates/o1.bmp', cv2.IMREAD_COLOR)  # trainImage
im2 = cv2.imread('./data_color/matches/o1-1.bmp', cv2.IMREAD_COLOR)  # queryImage
im1 = cv2.resize(im1, dsize=None, fx=0.3, fy=0.3, interpolation=cv2.INTER_LINEAR)
im2 = cv2.resize(im2, dsize=None, fx=0.3, fy=0.3, interpolation=cv2.INTER_LINEAR)
# 直方图归一化，应对白色的头盔
cv2.normalize(im1, im1, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
cv2.normalize(im2, im2, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
img1 = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
img2 = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)


# 初始化SIFT特征检测器
sift = cv2.SIFT_create(500)


# 使用特征检测器找特征点和描述子
kp1, des1 = sift.detectAndCompute(img1, None)
kp2, des2 = sift.detectAndCompute(img2, None)
# print("kp1: {}, kp2: {}".format(len(kp1), len(kp2)))

# 这里显示前做一次拷贝，避免影响最后使用
im1_copy = im1.copy()
cv2.drawKeypoints(im1_copy, kp1, im1_copy, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
cv2.imshow("kp1", im1_copy)

im2_copy = im2.copy()
cv2.drawKeypoints(im2_copy, kp2, im2_copy, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
cv2.imshow("kp2", im2_copy)

# 初始化一个FLANN匹配器和一个BF匹配器
#   FLANN匹配器
FLANN_INDEX_KDTREE = 0
index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)  # 指定索引中的树应该递归遍历的次数。值越高，精度越高，但是也越耗时
search_params = dict(checks=50) # or pass empty dictionary
flann = cv2.FlannBasedMatcher(index_params, search_params)


# 执行匹配
matches = flann.knnMatch(des1, des2, k=2)

# 选出好的匹配结果进行保存
good = []
for m, n in matches:
    if m.distance < 0.9 * n.distance:
        good.append(m)

if len(good) > MIN_MATCH_COUNT:
    # 分别取出匹配成功的queryImage的所有关键点 src_pts 以及trainImage的所有关键点 dst_pts
    src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
    # 使用findHomography并结合RANSAC算法，避免一些错误的点对结果产生影响
    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
    # 转成一行多列的。描述了对应索引位置的匹配结果是否在结果区域内
    matchesMask = mask.ravel().tolist()

    h, w = img1.shape
    # 创建一个queryImage的四个点轮廓图
    pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
    # 对这个轮廓图执行透视变换
    dst = cv2.perspectiveTransform(pts, M)
    # 将透视变换后的点连成封闭的线框绘制到trainImage上。
    im2 = cv2.polylines(im2, [np.int32(dst)], True, (255, 0, 0), 3, cv2.LINE_AA)

else:
    print("Not enough matches are found - %d/%d" % (len(good), MIN_MATCH_COUNT))
    matchesMask = None

draw_params = dict(matchColor=(0, 255, 0),  # draw matches in green color
                   singlePointColor=None,
                   matchesMask=matchesMask,  # draw only inliers只绘制掩膜区域以内的匹配
                   flags=2)

print(time.time()-start)

img3 = cv2.drawMatches(im1, kp1, im2, kp2, good, None, **draw_params)
cv2.imshow('matches', img3)
cv2.waitKey(0)