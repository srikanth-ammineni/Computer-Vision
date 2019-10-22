"""
Image Stitching Problem
(Due date: Oct. 23, 3 P.M., 2019)
The goal of this task is to stitch two images of overlap into one image.
To this end, you need to find feature points of interest in one image, and then find
the corresponding ones in another image. After this, you can simply stitch the two images
by aligning the matched feature points.
For simplicity, the input two images are only clipped along the horizontal direction, which
means you only need to find the corresponding features in the same rows to achieve image stiching.
"""
import cv2
import numpy as np
import random

def solution(left_img, right_img):
    """
    :param left_img:
    :param right_img:
    :return: you need to return the result image which is stitched by left_img and right_img
    """
    #Converting images to Grayscale
    left_img_gray = cv2.cvtColor(left_img,cv2.COLOR_BGR2GRAY)
    right_img_gray = cv2.cvtColor(right_img,cv2.COLOR_BGR2GRAY)
    
    #Finding sift-key points and descriptors for left and right images
    sift= cv2.xfeatures2d.SIFT_create()
    kp1,des1 = sift.detectAndCompute(right_img_gray,None)
    kp2,des2 = sift.detectAndCompute(left_img_gray,None)
    
    #Computing distances between every descriptor in one image and every descriptor in the other image.
    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks = 50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1,des2,k=2)
    
    #Selecting the top best matches for each descriptor of an image.
    good=[]
    for match1,match2 in matches:
        if match1.distance < 0.5 * match2.distance:
            good.append(match1)
            
    #calculating the homography matrix using RANSAC
    MIN_MATCH_COUNT = 10
    if len(good) > MIN_MATCH_COUNT:
        ptsA = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        ptsB = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
        H, status = cv2.findHomography(ptsA, ptsB, cv2.RANSAC,5.0)
        
    #Stiching the image using warp perspective
    result = cv2.warpPerspective(right_img, H,
			(left_img.shape[1] + right_img.shape[1], left_img.shape[0]+right_img.shape[0]))
    result[0:left_img.shape[0], 0:left_img.shape[1]] = left_img
    
    #Removing the black region from the resultant image
    result_gray = cv2.cvtColor(result,cv2.COLOR_BGR2GRAY)
    _,thresh = cv2.threshold(result_gray,1,255,cv2.THRESH_BINARY)
    _,contours,hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnt = contours[0]
    x,y,w,h = cv2.boundingRect(cnt)
    result = result[y:y+h,x:x+w]
    
    return result

if __name__ == "__main__":
    left_img = cv2.imread('left.jpg')
    right_img = cv2.imread('right.jpg')
    result_image = solution(left_img, right_img)
    cv2.imwrite('results/task2_result.jpg',result_image)



