from sift_flann import SiftFlann
import cv2


if __name__ == '__main__':
    pwd = "./data_color/templates/"
    img_arr = ["b1", "b2", "g1", "o1", "o2", "w1"]
    temp_arr = [pwd+img+".bmp" for img in img_arr]
    match = cv2.imread("./data_color/matches/w1-1.bmp")

    sift = SiftFlann(min_match_count=5, resize_times=0.3)
    sift.match(temp_arr, match)
