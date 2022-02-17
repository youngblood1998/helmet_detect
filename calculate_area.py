import math
import numpy as np

class CalArea:
    # 获得两点距离
    def get_distance(self, point0, point1):
        distance = ((point0[0] - point1[0])**2 + (point0[1] - point1[1])**2)**0.5
        return distance

    # 获得四个点围成的面积
    def get_point_area(self, points):
        d01 = self.get_distance(points[0], points[1])
        d12 = self.get_distance(points[1], points[2])
        d23 = self.get_distance(points[2], points[3])
        d30 = self.get_distance(points[3], points[0])
        d13 = self.get_distance(points[1], points[3])
        k1 = (d01 + d30 + d13) / 2.0
        k2 = (d12 + d23 + d13) / 2.0
        # print(d01, d12, d23, d30, d13)
        s1 = (k1*(k1 - d01)*(k1 - d30)*(k1 - d13))**0.5
        s2 = (k2*(k2 - d12)*(k2 - d23)*(k2 - d13))**0.5
        return s1 + s2

    # 变换矩阵转欧拉角
    def rotationMatrix_to_eulerAngles(self, R):
        sy = math.sqrt(R[0, 0] * R[0, 0] + R[1, 0] * R[1, 0])
        singular = sy < 1e-6
        if not singular:
            x = math.atan2(R[2, 1], R[2, 2])
            y = math.atan2(-R[2, 0], sy)
            z = math.atan2(R[1, 0], R[0, 0])
        else:
            x = math.atan2(-R[1, 2], R[1, 1])
            y = math.atan2(-R[2, 0], sy)
            z = 0
        return np.array([x, y, z])
