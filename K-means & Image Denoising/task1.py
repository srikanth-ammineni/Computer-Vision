"""
K-Means Segmentation Problem
(Due date: Nov. 25, 11:59 P.M., 2019)
The goal of this task is to segment image using k-means clustering.

Do NOT modify the code provided to you.
Do NOT import ANY library or API besides what has been listed.
Hint: 
Please complete all the functions that are labeled with '#to do'. 
You are allowed to add your own functions if needed.
You should design you algorithm as fast as possible. To avoid repetitve calculation, you are suggested to depict clustering based on statistic histogram [0,255]. 
You will be graded based on the total distortion, e.g., sum of distances, the less the better your clustering is.
"""


import utils
import numpy as np
import json
import time


def kmeans(img,k):
    """
    Implement kmeans clustering on the given image.
    Steps:
    (1) Random initialize the centers.
    (2) Calculate distances and update centers, stop when centers do not change.
    (3) Iterate all initializations and return the best result.
    Arg: Input image;
         Number of K. 
    Return: Clustering center values;
            Clustering labels of all pixels;
            Minimum summation of distance between each pixel and its center.  
    """
    #Flattening the image and finding unique pixels so that centers will be initialized from it
    flat_img=np.ndarray.flatten(img)  
    unique_pixels=np.unique(flat_img)
    unique_pixels=np.flip(unique_pixels)
    length=unique_pixels.shape[0]
    initial_indice_c1=0
    initial_indice_c2=1
    centroidList=[]
    sumList=[]
    iteration_count=0
    clusterassignmentsList=[]
    #Loop for all initializations
    while initial_indice_c1 < length-1:
        iteration_count+=1
        print("Iteration:",iteration_count)
        indices=[initial_indice_c1,initial_indice_c2] 
        
        #Centroid Initialization
        centroids =np.take(unique_pixels,indices) 
        if initial_indice_c2<length-1:
            initial_indice_c2+=1
        elif initial_indice_c1 < length-1:
            initial_indice_c1+=1
            initial_indice_c2=initial_indice_c1+1
        img=img.astype(int)
        centroids_old=np.zeros(centroids.shape)
        
        #Loop for clustering to converge
        while (centroids_old != centroids).any():
             centroids_old = centroids.copy()
             #Finding distances between each pixel and the center
             d1=abs(img-centroids[0])
             d2=abs(img-centroids[1])
             
             #Assigning pixels to their respective clusters based on absolute distances
             closest_centroid = np.greater_equal(d1,d2)
             cluster_assignment=np.where(closest_centroid==False, 1, closest_centroid)
             cluster_assignment=np.where(closest_centroid==True, 2, cluster_assignment)
             
             #Recalculating the cluster centers by taking the mean
             sum1=np.sum(img[cluster_assignment==1])
             sum2=np.sum(img[cluster_assignment==2])
             count1=np.size(img[cluster_assignment==1])
             count2=np.size(img[cluster_assignment==2])
             
             #Calculating sum of distance between each pixel and its center. 
             distanceSum=np.sum(d1[cluster_assignment==1])+np.sum(d2[cluster_assignment==2])
             centroids=np.array([int(sum1/count1),int(sum2/count2)])
             
        #Storing centroids, Distance sum, Cluster Assignment for each iteration
        centroidList.append(centroids)
        sumList.append(distanceSum)
        clusterassignmentsList.append(cluster_assignment)
        
    #Finding the centroids, Cluster Assignment which gave the minimum summation    
    min_sum=min(sumList)
    index=sumList.index(min_sum)
    cluster_assignment=clusterassignmentsList[index]
    centroids=centroidList[index]
    return (centroids,cluster_assignment,int(min_sum))

def visualize(centers,labels):
    """
    Convert the image to segmentation map replacing each pixel value with its center.
    Arg: Clustering center values;
         Clustering labels of all pixels. 
    Return: Segmentation map.
    """
    result=labels
    result=np.where(labels==1, centers[0], labels)
    result=np.where(labels==2, centers[1], result)
    result=result.astype("uint8")
    return result
if __name__ == "__main__":
    img = utils.read_image('lenna.png')
    k = 2
    start_time = time.time()
    centers, labels, sumdistance = kmeans(img,k)
    result = visualize(centers, labels)
    end_time = time.time()
    running_time = end_time - start_time
    centers = centers.tolist()
    with open('results/task1.json', "w") as jsonFile:
        jsonFile.write(json.dumps({"centers":centers, "distance":sumdistance, "time":running_time}))
    utils.write_image(result, 'results/task1_result.jpg')




