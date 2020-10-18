"""
RANSAC Algorithm Problem
(Due date: Oct. 23, 3 P.M., 2019)
The goal of this task is to fit a line to the given points using RANSAC algorithm, and output
the names of inlier points and outlier points for the line.

Do NOT modify the code provided to you.
Do NOT use ANY API provided by opencv (cv2) and numpy (np) in your code.
Do NOT import ANY library (function, module, etc.).
You can use the library random
Hint: It is recommended to record the two initial points each time, such that you will Not 
start from this two points in next iteration.
"""
import random
def solution(input_points, t, d, k):
    """
    :param input_points:
           t: t is the perpendicular distance threshold from a point to a line
           d: d is the number of nearby points required to assert a model fits well, you may not need this parameter
           k: k is the number of iteration times
           Note that, n for line should be 2
           (more information can be found on the page 90 of slides "Image Features and Matching")
    :return: inlier_points_name, outlier_points_name
    inlier_points_name and outlier_points_name is two list, each element of them is str type.
    For example: If 'a','b' is inlier_points and 'c' is outlier_point.
    the output should be two lists of ['a', 'b'], ['c'].
    Note that, these two lists should be non-empty.
    """
    # TODO: implement this function.
    temp=[]
    point_list=[]
    inliers=[]
    outliers=[]
    model=[]
    for k in range(k):
        #Choosing the two points randomly
        point1=random.choice(input_points)
        point2=random.choice(input_points)
        if point1==point2:
            continue
        print("Point1", point1)
        print("Point2", point2)
        temp.append(point1['name'])
        temp.append(point2['name'])
        print(point_list)
        if sorted(temp) not in point_list:
            point_list.append(sorted(temp))
            a = point2['value'][1] - point1['value'][1] 
            b = point1['value'][0] - point2['value'][0]  
            c = -1 * (a*(point1['value'][0]) + b*(point1['value'][1]) )
            if(b<0 and c>0):  
              print("The line passing through points point 1 and point 2 is:", a ,"x",b,"y+",c,"=0","\n") 
            elif(b>0 and c<0 ):
                print("The line passing through points point 1 and point 2 is:", a ,"x+",b,"y",c ,"=0","\n")
            elif(b>0 and c>0 ):
                print("The line passing through points point 1 and point 2 is:", a ,"x+",b,"y+",c,"=0","\n")
            else: 
              print("The line passing through points point 1 and point 2 is: ",a ,"x",b,"y",c ,"=0","\n") 
            distance_den=(a**2+b**2)**0.5
            inliers.append(point1['name'])
            inliers.append(point2['name'])
            print(sorted(temp))
            model_error=0
            for i in input_points:
                if i['name'] not in sorted(temp):
                    distance_num = abs(a*(i['value'][0]) + b*(i['value'][1]) + c)
                    distance=distance_num/distance_den
                    print(distance)
                    if distance <= t:
                        inliers.append(i['name'])
                        model_error=model_error+distance
                    else: 
                        outliers.append(i['name'])
        if len(inliers)>= (d+2):
            model.append({'inliers':inliers,'outliers':outliers,'error':model_error/(len(inliers)-2)})
        temp=[]
        inliers=[]
        outliers=[]
        print(model)
    print(model)
    prev_min_val=0
    ind=0
    for j in model:
        curr_min_val=j['error']
        if prev_min_val ==0:
            prev_min_val=curr_min_val
        if curr_min_val < prev_min_val and prev_min_val!=0:
            ind=model.index(j)
            prev_min_val=curr_min_val
    print(model[ind])
    return sorted(model[ind]['inliers']),sorted(model[ind]['outliers'])
        
    #raise NotImplementedError


if __name__ == "__main__":
    input_points = [{'name': 'a', 'value': (0.0, 1.0)}, {'name': 'b', 'value': (2.0, 1.0)},
                    {'name': 'c', 'value': (3.0, 1.0)}, {'name': 'd', 'value': (0.0, 3.0)},
                    {'name': 'e', 'value': (1.0, 2.0)}, {'name': 'f', 'value': (1.5, 1.5)},
                    {'name': 'g', 'value': (1.0, 1.0)}, {'name': 'h', 'value': (1.5, 2.0)}]
    t = 0.5
    d = 3
    k = 100
    inlier_points_name, outlier_points_name = solution(input_points, t, d, k)  # TODO
    print(inlier_points_name)
    print(outlier_points_name)
    assert len(inlier_points_name) + len(outlier_points_name) == 8  
    f = open('./results/task1_result.txt', 'w')
    f.write('inlier points: ')
    for inliers in inlier_points_name:
        f.write(inliers + ',')
    f.write('\n')
    f.write('outlier points: ')
    for outliers in outlier_points_name:
        f.write(outliers + ',')
    f.close()



