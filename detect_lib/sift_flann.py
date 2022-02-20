import numpy as np
import cv2
from detect_lib.calculate_area import CalArea


class SiftFlann:
    def __init__(self, min_match_count=10, resize_times=0.3, max_matches=500, flann_index_kdtree=0,
                 trees=5, checks=50, k=2, ratio=0.9):
        self.min_match_count = min_match_count  # 最小匹配数
        self.resize_times = resize_times    # 大小变换的倍数，越小越快越不准
        self.max_matches = max_matches  # 最大特征点数
        self.flann_index_kdtree = flann_index_kdtree
        self.trees = trees  # 树的遍历次数，越大越准，但费时
        self.checks = checks
        self.k = k  # 匹配取前k个
        self.ratio = ratio  # 距离比例

    def sift_flann(self, im1, im2):
        # # 大小变换
        # im1 = cv2.resize(im1, dsize=None, fx=self.resize_times, fy=self.resize_times, interpolation=cv2.INTER_LINEAR)
        # im2 = cv2.resize(im2, dsize=None, fx=self.resize_times, fy=self.resize_times, interpolation=cv2.INTER_LINEAR)
        # 直方图归一化，应对白色的头盔
        cv2.normalize(im1, im1, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
        cv2.normalize(im2, im2, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
        # 转换成黑白
        img1 = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
        if len(im2.shape) == 3:
            img2 = cv2.cvtColor(im2, cv2.COLOR_RGB2GRAY)
        else:
            img2 = im2

        # 初始化SIFT特征检测器
        sift = cv2.SIFT_create(self.max_matches)

        # 使用特征检测器找特征点和描述子
        kp1, des1 = sift.detectAndCompute(img1, None)
        kp2, des2 = sift.detectAndCompute(img2, None)

        # 初始化一个FLANN匹配器
        index_params = dict(algorithm=self.flann_index_kdtree, trees=self.trees)
        search_params = dict(checks=self.checks)    # or pass empty dictionary
        flann = cv2.FlannBasedMatcher(index_params, search_params)

        if des2 == None:
            return 0, [], None

        # 执行匹配
        matches = flann.knnMatch(des1, des2, k=self.k)

        # 选出好的匹配结果进行保存
        good = []
        for m, n in matches:
            if m.distance < self.ratio * n.distance:
                good.append(m)

        # 判断匹配上的点是否符合要求
        if len(good) > self.min_match_count:
            # 分别取出匹配成功的queryImage的所有关键点 src_pts 以及trainImage的所有关键点 dst_pts
            src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
            dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
            # 使用findHomography并结合RANSAC算法，避免一些错误的点对结果产生影响
            M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
            if M is None:
                print("M is None")
                print("-" * 50)
                return 0, [], None
            h, w = img1.shape
            # 创建一个queryImage的四个点轮廓图
            pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
            # 对这个轮廓图执行透视变换
            print(M)
            dst = np.int32(cv2.perspectiveTransform(pts, M))
        else:
            # 匹配上的点太少
            dst = []
            M = None
            print("Not enough matches are found - %d/%d" % (len(good), self.min_match_count))
        print("-"*50)

        return len(good), dst, M

    def match(self, path_arr, im2):
        # 最多的匹配点个数
        max_matches = 0
        best_match = None
        draw_point = []
        best_path = None
        angles = []
        # 读取被匹配的图片
        im2 = cv2.resize(im2, dsize=None, fx=self.resize_times, fy=self.resize_times, interpolation=cv2.INTER_LINEAR)
        # 在模板中找最佳匹配
        for path in path_arr:
            # 读取并调整大小
            im1 = cv2.imread(path, cv2.IMREAD_COLOR)
            im1 = cv2.resize(im1, dsize=None, fx=self.resize_times, fy=self.resize_times,
                             interpolation=cv2.INTER_LINEAR)
            # 模板图片的宽高和面积
            im1_height = np.shape(im1)[0]
            im1_width = np.shape(im1)[1]
            area1 = im1_width * im1_height
            # 匹配点个数、框的四个点、变换矩阵
            matches, dst, matrix = self.sift_flann(im1, im2)
            # print(dst[2][0][0])
            # 匹配点太少的话直接跳过
            if len(dst) == 0:
                # print(1)
                continue
            # 计算匹配框的面积
            cal = CalArea()
            area2 = cal.get_point_area([dst[0][0], dst[1][0], dst[2][0], dst[3][0]])
            # im2_width = abs(dst[0][0][1]-dst[2][0][0])
            # im2_height = abs(dst[0][0][1]-dst[2][0][1])
            # print(area1, area2)
            # i/f (im2_width < 0.5*im1_width or im2_height < 0.5*im1_height) \
            #         or ((im2_width > 2*im1_width or im2_height > 2*im1_height)):
            #     print(2)
            #     continue
            # 面积不合适直接跳过
            if area2 < 0.8*area1 or area2 > 1.2*area1:
                # print(2)
                continue
            # 选择最好的匹配
            if matches > max_matches:
                max_matches = matches
                best_match = im1    # 最好的模板
                draw_point = dst    # 最好匹配的框
                best_path = path    # 最好模板的路径
                angles = cal.rotationMatrix_to_eulerAngles(matrix)  # 角度
        if best_match is None:
            print("匹配不到该物体")
            return None, []
        # 把匹配的框画进去，并表示出来
        # im2 = cv2.polylines(im2, [np.int32(draw_point)], True, (255, 0, 0), 3, cv2.LINE_AA)
        # cv2.imshow("template", best_match)
        # cv2.imshow("result", im2)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # 返回模板路径和角度
        return best_path, angles[2]
