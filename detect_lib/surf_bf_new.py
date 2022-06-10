# import numpy
import copy

import numpy as np
import cv2
from detect_lib.calculate_area import CalArea
from detect_lib.hist_compare import hist_compare


class SurfBf:
    def __init__(self, min_match_count=10, resize_times=0.3, max_matches=500, flann_index_kdtree=0,
                 trees=5, checks=50, k=2, ratio=0.9, hist2=0.8, area=1.25):
        self.min_match_count = min_match_count  # 最小匹配数
        self.resize_times = resize_times    # 大小变换的倍数，越小越快越不准
        self.max_matches = max_matches  # 最大特征点数
        self.flann_index_kdtree = flann_index_kdtree
        self.trees = trees  # 树的遍历次数，越大越准，但费时
        self.checks = checks
        self.k = k  # 匹配取前k个
        self.ratio = ratio  # 距离比例
        self.hist2 = hist2  # 颜色对比度
        self.area = area    # 面积匹配度


    def surf_bf(self, im1, kp1, des1, im2):
        # # 大小变换
        # im1 = cv2.resize(im1, dsize=None, fx=self.resize_times, fy=self.resize_times, interpolation=cv2.INTER_LINEAR)
        # im2 = cv2.resize(im2, dsize=None, fx=self.resize_times, fy=self.resize_times, interpolation=cv2.INTER_LINEAR)
        # 直方图归一化，应对白色的头盔
        # cv2.normalize(im1, im1, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
        # cv2.normalize(im2, im2, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
        # # 转换成黑白
        # img1 = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
        # # img2 = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)
        if len(im2.shape) == 3:
            img2 = cv2.cvtColor(im2, cv2.COLOR_RGB2GRAY)
        else:
            img2 = im2
            # img2 = copy.deepcopy(im2)

        # 限制对比度的自适应阈值均衡化
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        img2 = clahe.apply(img2)
        #
        # 初始化SURF特征检测器
        surf = cv2.xfeatures2d.SURF_create()
        #
        # # 使用特征检测器找特征点和描述子
        # kp1, des1 = sift.detectAndCompute(img1, None)
        kp2, des2 = surf.detectAndCompute(img2, None)

        # 初始化一个FLANN匹配器
        # index_params = dict(algorithm=self.flann_index_kdtree, trees=self.trees)
        # search_params = dict(checks=self.checks)    # or pass empty dictionary
        # flann = cv2.FlannBasedMatcher(index_params, search_params)

        # 初始化一个BF匹配器
        bf = cv2.BFMatcher()

        if des2 is None:
            print("没有描述子")
            return 0, [], None

        # 执行匹配
        # matches = flann.knnMatch(des1, des2, k=self.k)
        matches = bf.knnMatch(des1, des2, k=self.k)

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
                print("没有转换矩阵")
                # print("-" * 50)
                return 0, [], None
            h, w = im1.shape[0], im1.shape[1]
            # 创建一个queryImage的四个点轮廓图
            pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
            # 对这个轮廓图执行透视变换
            # print(M)
            dst = np.int32(cv2.perspectiveTransform(pts, M))

            # 截取图片做颜色对比
            p_0 = dst[0][0]
            p_1 = dst[1][0]
            p_2 = dst[2][0]
            p_3 = dst[3][0]
            min_y = int((p_1[1] + p_2[1]) / 2)
            max_y = int((p_0[1] + p_3[1]) / 2)
            min_x = int((p_2[0] + p_3[0]) / 2)
            max_x = int((p_0[0] + p_1[0]) / 2)
            resize = round(0.05/self.resize_times, 2)

            im2_h, im2_w = im2.shape[0], im2.shape[1]
            x_1 = min(min_x, max_x) if min(min_x, max_x) >= 0 else 0
            x_2 = max(min_x, max_x) if max(min_x, max_x) <= im2_w else im2_w
            y_1 = min(min_y, max_y) if min(min_y, max_y) >= 0 else 0
            y_2 = max(min_y, max_y) if max(min_y, max_y) <= im2_h else im2_h
            # 特殊情况过滤
            if x_2-x_1<10 or y_2-y_1<10:
                print("截取图过小", x_2-x_1, y_2-y_1)
                return 0, [], None
            # if min(min_x, max_x) < 0 or min(min_y, max_y) < 0 or max(min_x, max_x) > im2_w or min(min_y, max_y) > im2_h:
            #     print("有点在图外")
            #     print(min_x, min_y, max_x, max_y)
            #     return 0, [], None
            # if max(min_y, max_y)-min(min_y, max_y)<10 or max(min_x, max_x)-min(min_x, max_x)<10:
            #     print("截取图过小")
            #     print(max(min_y, max_y)-min(min_y, max_y), max(min_x, max_x)-min(min_x, max_x))
            #     return 0, [], None
            resize_im2 = cv2.resize(im2[y_1:y_2, x_1:x_2, :], dsize=None, fx=resize, fy=resize, interpolation=cv2.INTER_LINEAR)
            resize_im1 = cv2.resize(im1, dsize=None, fx=resize, fy=resize, interpolation=cv2.INTER_LINEAR)
            # print(hist_compare(resize_im2, resize_im1))
            if hist_compare(resize_im2, resize_im1) < self.hist2:
                print("颜色不匹配："+str(hist_compare(resize_im2, resize_im1)))
                return 0, [], None
        else:
            print("对应点太少："+str(len(good)))
            # 匹配上的点太少
            dst = []
            M = None
        #     print("Not enough matches are found - %d/%d" % (len(good), self.min_match_count))
        # print("-"*50)

        return len(good), dst, M


    def match(self, temp_arr, im2):
        # 最多的匹配点个数
        # max_matches = 0
        min_area_ratio = 1
        best_match = None
        draw_point = []
        best_temp = None
        angles = []
        # 读取被匹配的图片
        # print(im2.shape)
        im2 = cv2.resize(im2, dsize=None, fx=self.resize_times, fy=self.resize_times, interpolation=cv2.INTER_LINEAR)
        # 在模板中找最佳匹配
        for temp in temp_arr:
            print("模板" + temp['model'] + temp['size'])
            # 读取并调整大小
            im1 = temp["image"]
            # print(im1.shape)
            im1 = cv2.resize(im1, dsize=None, fx=self.resize_times, fy=self.resize_times,
                             interpolation=cv2.INTER_LINEAR)
            # 模板图片的宽高和面积
            # im1_height = np.shape(im1)[0]
            # im1_width = np.shape(im1)[1]
            # area1 = im1_width * im1_height
            # 匹配点个数、框的四个点、变换矩阵
            matches, dst, matrix = self.surf_bf(im1, temp["kp"], temp["des"], im2)
            # print(dst[2][0][0])
            # 匹配点太少的话直接跳过
            if len(dst) == 0:
                # print(1)
                continue
            # 计算两边中点连线长度
            point0 = (int((dst[0][0][0] + dst[1][0][0])/2), int((dst[0][0][1] + dst[1][0][1])/2))
            point1 = (int((dst[2][0][0] + dst[3][0][0])/2), int((dst[2][0][1] + dst[3][0][1])/2))
            cal = CalArea()
            length2 = cal.get_distance(point0, point1)

            # # 计算匹配框的面积
            # cal = CalArea()
            # area2 = cal.get_point_area([dst[0][0], dst[1][0], dst[2][0], dst[3][0]])
            # print(dst, area2)
            # im2_width = abs(dst[0][0][0]-dst[2][0][0])
            # im2_height = abs(dst[0][0][1]-dst[2][0][1])
            # print(area1, area2)
            # i/f (im2_width < 0.5*im1_width or im2_height < 0.5*im1_height) \
            #         or ((im2_width > 2*im1_width or im2_height > 2*im1_height)):
            #     print(2)
            #     continue
            # 面积不合适直接跳过
            # if area2 < 0.8*area1 or area2 > 1.25*area1:
            #     print("面积不匹配")
            #     continue
            # if area2 < (1.0/self.area)*area1 or area2 > (self.area)*area1:
            #     print("面积不匹配")
            #     continue

            # 将模板数组中所有同名同颜色的进行交叉比对
            for temp_cmp in temp_arr:
                if temp_cmp["model"] == temp["model"] and temp_cmp["color"] == temp["color"]:
                    print(temp_cmp["model"] + temp_cmp["size"] + ":")
                    # 计算宽度
                    im1_width = temp_cmp["width"] * self.resize_times

                    if length2 < (1.0 / self.area) * im1_width or length2 > (self.area) * im1_width:
                        print("长度不匹配")
                        continue

                    # area_ratio = float(abs(area2-area1))/area2
                    area_ratio = float(abs(length2-im1_width))/length2
                    print(length2, im1_width, area_ratio)
                    # 选择最好的匹配
                    if area_ratio < min_area_ratio:
                        min_area_ratio = area_ratio
                        best_match = temp_cmp["image"]  # 最好的模板
                        draw_point = dst  # 最好匹配的框
                        best_temp = temp_cmp  # 最好模板的路径
                        angles = cal.rotationMatrix_to_eulerAngles(matrix)  # 角度
        print("-"*20)
            # # 选择最好的匹配
            # if matches > max_matches:
            #     max_matches = matches
            #     best_match = im1    # 最好的模板
            #     draw_point = dst    # 最好匹配的框
            #     best_temp = temp    # 最好模板的路径
            #     angles = cal.rotationMatrix_to_eulerAngles(matrix)  # 角度
        if best_match is None:
            print("匹配不到该物体")
            return None, 0, [], 0, 0, 0
        # 把匹配的框画进去，并表示出来
        im2 = cv2.polylines(im2, [np.int32(draw_point)], True, (255, 0, 0), 3, cv2.LINE_AA)
        im2 = cv2.line(im2, point0, point1, (0, 0, 255), 3)
        # cv2.imshow("template", best_match)
        # cv2.imshow("result", im2)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # 返回模板路径和角度
        direction = 0 if (angles[2] < np.pi/2 and angles[2] > -np.pi/2) else 1
        x, y = int((draw_point[0][0][1]+draw_point[1][0][1]+draw_point[2][0][1]+draw_point[3][0][1])/4), \
               int((draw_point[0][0][0]+draw_point[1][0][0]+draw_point[2][0][0]+draw_point[3][0][0])/4)
        return best_temp, direction, im2, angles[2], x, y
