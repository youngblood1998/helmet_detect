import cv2
import numpy as np
import time

start = time.time()

MIN_MATCH_COUNT = 10
fsize = 0.1

im1 = cv2.imread('../data_test/test/left_1.bmp', cv2.IMREAD_COLOR)
im2 = cv2.imread('../data_test/test/left_4.bmp', cv2.IMREAD_COLOR)  # queryImage
# im1 = cv2.imread('./data_color/templates/o1.bmp', cv2.IMREAD_COLOR)
# im2 = cv2.imread('./data_color/matches/o1-1.bmp', cv2.IMREAD_COLOR)  # queryImage
im1 = cv2.resize(im1, dsize=None, fx=fsize, fy=fsize, interpolation=cv2.INTER_LINEAR)
im2 = cv2.resize(im2, dsize=None, fx=fsize, fy=fsize, interpolation=cv2.INTER_LINEAR)
# cv2.normalize(im1, im1, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
# cv2.normalize(im2, im2, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
img1 = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
img2 = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)

clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
img1 = clahe.apply(img1)
img2 = clahe.apply(img2)
cv2.imshow("img1", img1)
cv2.imshow("img2", img2)

# cv2.waitKey(0)
# cv2.destroyAllWindows()
# exit(0)

# sift = cv2.xfeatures2d.SIFT_create()
# kp1, des1 = sift.detectAndCompute(img1, None)
# kp2, des2 = sift.detectAndCompute(img2, None)

# fast = cv2.FastFeatureDetector_create()
# fast.setNonmaxSuppression(True)
# brief = cv2.xfeatures2d.BriefDescriptorExtractor_create()
# kp1 = fast.detect(img1, None)
# kp2 = fast.detect(img2, None)
# kp1, des1 = brief.compute(img1, kp1)
# kp2, des2 = brief.compute(img2, kp2)

surf = cv2.xfeatures2d.SURF_create()
kp1, des1 = surf.detectAndCompute(img1, None)
kp2, des2 = surf.detectAndCompute(img2, None)

# orb = cv2.ORB_create()
# kp1, des1 = orb.detectAndCompute(img1, None)
# kp2, des2 = orb.detectAndCompute(img2, None)

print(len(kp1), len(kp2))

im1_copy = im1.copy()
cv2.drawKeypoints(im1_copy, kp1, im1_copy, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
cv2.imshow("kp1", im1_copy)

im2_copy = im2.copy()
cv2.drawKeypoints(im2_copy, kp2, im2_copy, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
cv2.imshow("kp2", im2_copy)

bf = cv2.BFMatcher()
matches = bf.knnMatch(des1, des2, k=2)

# FLANN_INDEX_KDTREE = 0
# index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
# # 指定索引中的树应该递归遍历的次数。值越高，精度越高，但是也越耗时
# search_params = dict(checks=50) # or pass empty dictionary
# # 创建Flann匹配器
# flann = cv2.FlannBasedMatcher(index_params, search_params)
# # 执行匹配
# matches = flann.knnMatch(des1, des2, k=2)

# store all the good matches as per Lowe's ratio test.
good = []
for m, n in matches:
    if m.distance < 0.7 * n.distance:
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
    print(dst)
    p_0 = dst[0][0]
    p_1 = dst[1][0]
    p_2 = dst[2][0]
    p_3 = dst[3][0]
    print(p_0, p_1, p_2, p_3)
    min_y = int((p_1[1] + p_2[1]) / 2)
    max_y = int((p_0[1] + p_3[1]) / 2)
    min_x = int((p_2[0] + p_3[0]) / 2)
    max_x = int((p_0[0] + p_1[0]) / 2)
    cv2.imshow("cut", im2[min(min_y, max_y):max(min_y, max_y),min(min_x, max_x):max(min_x, max_x),:])
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
if fsize > 0.25:
    img3 = cv2.resize(img3, dsize=None, fx=0.5, fy=0.5, interpolation=cv2.INTER_LINEAR)
cv2.imshow('matches', img3)
cv2.waitKey(0)