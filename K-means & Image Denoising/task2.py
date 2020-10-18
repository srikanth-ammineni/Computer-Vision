"""
Denoise Problem
(Due date: Nov. 25, 11:59 P.M., 2019)
The goal of this task is to denoise image using median filter.

Do NOT modify the code provided to you.
Do NOT import ANY library or API besides what has been listed.
Hint: 
Please complete all the functions that are labeled with '#to do'. 
You are suggested to use utils.zero_pad.
"""


import utils
import numpy as np
import json

def median_filter(img):
    """
    Implement median filter on the given image.
    Steps:
    (1) Pad the image with zero to ensure that the output is of the same size as the input image.
    (2) Calculate the filtered image.
    Arg: Input image. 
    Return: Filtered image.
    """
    padded_img=utils.zero_pad(img, 1, 1)
    result=np.zeros((img.shape[0],img.shape[1]),dtype="uint8")
    array=np.zeros((3, 3))
    for r in range(0, len(padded_img[0])-2): #rows
        for c in range(0, len(padded_img[1])-2):#columns 
            for i in range (0, 3):
                for j in range (0, 3): 
                    array[i][j]=padded_img[i+r][j+c]
            result[r][c]=np.median(array)
            array=np.zeros((3, 3))
    return result

def mse(img1, img2):
    """
    Calculate mean square error of two images.
    Arg: Two images to be compared.
    Return: Mean square error.
    """    
    diff=0
    for m in range(0,img1.shape[0]):
        for n in range(0,img2.shape[1]):
            diff+=(img1[m][n]-img2[m][n])**2       
    mse=diff/(img1.shape[0]*img1.shape[1])
    return mse

if __name__ == "__main__":
    img = utils.read_image('lenna-noise.png')
    gt = utils.read_image('lenna-denoise.png')
    result = median_filter(img)
    error = mse(gt, result)
    with open('results/task2.json', "w") as file:
        json.dump(error, file)
    utils.write_image(result,'results/task2_result.jpg')


