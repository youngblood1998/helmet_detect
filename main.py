from sift_flann import SiftFlann
import cv2
import time


if __name__ == '__main__':
    pwd = "./data/templates/"
    img_arr = ["b1", "b2", "g1", "o1", "o2", "w1"]
    temp_arr = [pwd+img+".jpg" for img in img_arr]
    start = time.time()
    match = cv2.imread("./data/matches/w1-2.bmp")

    sift = SiftFlann(min_match_count=5, resize_times=0.3)
    result, angle = sift.match(temp_arr, match)
    print(time.time()-start)
    print(result, angle)
