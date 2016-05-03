#!/usr/bin/python
import random, copy


class KMeans:
    
    range_min = 0
    range_max = 20
    
    def __init__(self,attr_dict):
        
        #initial centroid coordinates
        self.cent_x = attr_dict["cords_x"]
        self.cent_y = attr_dict["cords_y"]
        self.cent_z = attr_dict["cords_z"]
        
        self.cl_cnt = attr_dict["cl_cnt"]  #how many clusters
        self.dim = attr_dict["dim"]
        
        if attr_dict["empty"]:
            self.randomCentroids() #in case none were given
        
        #point values
        self.points_x = attr_dict["points_x"]
        self.points_y = attr_dict["points_y"]
        self.points_z = attr_dict["points_z"]
        
        self.points_cnt = len(self.points_x)
        
        #cluster members - each point has a number of cluster it's in
        self.cl_members = []
        for i in range(0,self.points_cnt):
            self.cl_members.append(0)  #initially all points go to cluster 0
            
        print self.cl_members
        print self.cent_x
        print self.cent_y
        print self.cent_z
        
    
    
    
    #if no specific coords given, we generate them at random
    def randomCentroids(self):

        #let's generate random positions for centroids
        for c in range(0,self.cl_cnt):
            x = random.randint(KMeans.range_min,KMeans.range_max)
            y = random.randint(KMeans.range_min,KMeans.range_max) 
            
            self.cent_x[c] = x
            self.cent_y[c] = y
            
            if self.dim == 3:
                z = random.randint(KMeans.range_min,KMeans.range_max)
                self.cent_z[c] = z
                    
        
        