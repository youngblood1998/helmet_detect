class CalArea:
    def get_distance(self, point0, point1):
        distance = ((point0[0] - point1[0])**2 + (point0[1] - point1[1])**2)**0.5
        return distance

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
