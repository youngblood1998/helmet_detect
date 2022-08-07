from cv2 import cv2
import numpy as np

def concate_image(image, transformed_image):
   h0,w0=image.shape[0],image.shape[1]  #cv2 读取出来的是h,w,c
   h1,w1=transformed_image.shape[0],transformed_image.shape[1]
   h=max(h0,h1)
   w=max(w0,w1)
   org_image=np.ones((h,w,3),dtype=np.uint8)*255
   trans_image=np.ones((h,w,3),dtype=np.uint8)*255

   org_image[:h0,:w0,:]=image[:,:,:]
   trans_image[:h1,:w1,:]=transformed_image[:,:,:]
   all_image = np.hstack((org_image[:,:w0,:], trans_image[:,:w1,:]))
   return all_image