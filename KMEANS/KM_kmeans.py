#!/usr/bin/python
import random, copy
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cm

class KMeans:
    
    range_min = 0
    range_max = 20
    tolerance = 0.01
    
    def __init__(self,attr_dict):  
        
        self.points_cnt = len(attr_dict["points_x"]) #how many points
        self.cl_cnt = attr_dict["cl_cnt"]           #how many clusters
        self.dim = attr_dict["dim"]                 #dimension
        
        #initial centroid coordinates
        self.cent_x = attr_dict["cords_x"]
        self.cent_y = attr_dict["cords_y"]
        self.cent_z = attr_dict["cords_z"]
        
        if attr_dict["empty"]:
            self.randomCentroids() #in case none were given
        
        #list of numpy arrays reprezenting centroids in given dimension
        #print "creating centroids"
        #print "their cnt is: " + str(self.cl_cnt)
        self.centroids = self.initializePoints(self.cl_cnt,self.cent_x,
                                            self.cent_y,self.cent_z)
        
        #point coordinates
        self.points_x = attr_dict["points_x"]
        self.points_y = attr_dict["points_y"]
        self.points_z = attr_dict["points_z"]
        
        #list of numpy arrays reprezenting points in given dimension
        #print "creating points"
        #print "their cnt is: " + str(self.points_cnt)
        self.points = self.initializePoints(self.points_cnt,self.points_x,
                                            self.points_y,self.points_z)
        
        
        self.cl_points = []            #list of lists of points belonging to the respective cluster
        
        for i in range(0,self.cl_cnt): #creating list for each cluster
            self.cl_points.append([])
        
        #cluster members - each point has a number of cluster it's in
        #it's to create their indexes in the cl_members list
        self.cl_members = []
        for i in range(0,self.points_cnt):
            self.cl_members.append(0)  #initially all points go to cluster 0
            
        
    
    
    
    ###--------------------------------
    ###-----POINT INITIALIZATION-------
    ###--------------------------------
    
    #CREATES NUMPY ARRAY REPREZENTATION OF GIVEN POINTS
    #picks whether 2D or 3D
    def initializePoints(self,cnt,cord_x,cord_y,cord_z):
        
        if self.dim == 2:
            return self.initializePoints2D(cnt,cord_x,cord_y)
        
        else:
            return self.initializePoints3D(cnt,cord_x,cord_y,cord_z)
    
    #2D VARIANT
    def initializePoints2D(self,cnt,cord_x,cord_y):
        
        points = []
        
        for i in range(0,cnt):
            x = float(cord_x[i])
            y = float(cord_y[i])
            #print "coords"
            #print x
            #print y
            point = np.array([x,y])
            #print "creating point"
            #print point
            points.append(point)
            
        return points
    
    
    #3D VARIANT
    def initializePoints3D(self,cnt,cord_x,cord_y,cord_z):
        
        points = []
        
        for i in range(0,cnt):
            x = float(cord_x[i])
            y = float(cord_y[i])
            z = float(cord_z[i])
            point = np.array([x,y,z])
            points.append(point)
            
        return points
    
    #INITIALIZE CENTROIDS AT RANDOM COORDINATES
    #if no specific coords given, we generate them at random
    def randomCentroids(self):

        #let's generate random positions for centroids
        for c in range(0,self.cl_cnt):
            x = random.random() * KMeans.range_max
            y = random.random() * KMeans.range_max 
            
            self.cent_x[c] = x
            self.cent_y[c] = y
            
            if self.dim == 3:
                z = random.random() * KMeans.range_max
                self.cent_z[c] = z
                
                
                
    ###-------------------------------------
    ###--------ALGORITHM SECTION------------
    ###-------------------------------------
     
     
    #FOR EACH POINT FINDS THE CLOSEST CLUSTER
    def findMyCluster(self):
        
        self.cleanClusterLists() 
         
        for i in range(0,self.points_cnt):
            point = self.points[i]             
            self.shortest = -1
            
            #print "I have point"
            #print point
             
            for j in range(0,self.cl_cnt):
                centroid = self.centroids[j]
                #print "I have centroid"
                #print centroid
                 
                #gets euclide distance of the two points
                dist = np.linalg.norm(point-centroid)
                #print "euclide is: " + str(dist)
                
                #print str(dist) + " < " + str(self.shortest)
                #print dist < self.shortest
                if self.shortest == -1 or dist < self.shortest:
                    #print "we set it as shortest"
                    self.shortest = dist
                    #print "shortest should be dist now"
                    self.cl_members[i] = j #point i is in cluster j for now
                    #print "cl members updated to: " + str(j)
                     
        #now each point in self.cl_members has index of cluster it belongs to
        #what remains is to update the cluster point lists:
        self.sortInClusters()
    
    
    #CLEANS LISTS OF CLUSTER POINTS
    #so we can sort points anew in each cycle
    def cleanClusterLists(self):
        
        for i in range(self.cl_cnt):
            self.cl_points[i] = []
            
     
    #UPDATES LISTS OF POINTS BELONGING TO EACH CLUSTER
    def sortInClusters(self):
         
        for i in range(0,self.points_cnt):
            cluster = self.cl_members[i]
            self.cl_points[cluster].append(i)
             
             
    #COUNTS NEW CENTROID POSITIONS        
    def newCentroidPositions(self):
        
        #print "old centroids"
        #print self.centroids
         
        changeFlag = False
         
        for i in range(0,self.cl_cnt):             
            
            #setting proper starting sum
            if self.dim == 2:
                sum_points = np.array([0.0,0.0])
            else:
                sum_points = np.array([0.0,0.0,0.0])
            
            
            #first we add all points on all their dimensions
            for p in self.cl_points[i]:
                sum_points = sum_points + self.points[p]
            
                        
            #no points for this cluster, nothing to count
            if len(self.cl_points[i]) == 0:
                continue
            
            #then we divide the sum by the cnt of points
            #to get the average => new cluster position
            new_position = sum_points / len(self.cl_points[i])
             
            #if there is a change to the previous position, we set the flag
            #print "old position"
            #print self.centroids[i]
            #print "new position"
            #print new_position
            
            diff = np.linalg.norm(self.centroids[i]-new_position)
            if not diff < KMeans.tolerance:
               self.centroids[i] = new_position               
               changeFlag = True
        
        #print self.cl_points
        #print "new centroids"
        #print self.centroids
        return changeFlag #false if no change happened
         
     
     
    ###-----------------------
    ###-------PLOTTING--------
    ###-----------------------
     
    #PLOTS POINTS AND CENTROIDS IN DIFFERENT COLORS
    #calls either 2D plot or 3D plot
    def plotPoints(self):
         
        if self.dim == 2:
            self.plotPoints2D()
        else:
            self.plotPoints3D()
            
            
    #2D PLOTTING        
    def plotPoints2D(self):
        colors = cm.rainbow(np.linspace(0, 1, self.cl_cnt))
       
        for c in range(self.cl_cnt):
            centroid = self.centroids[c]
            x = []
            y = []
            cluster_size = len(self.cl_points[c])
            
            #for each point assorted to the cluster
            for p in range(cluster_size):
                index = self.cl_points[c][p] #index of the point
                point = self.points[index]
                #print point
                x.append(point[0])
                y.append(point[1])
            
            clrs = cm.rainbow(np.linspace(0, 1, self.cl_cnt))
            plt.scatter(x, y, color=clrs[c], marker='o')
            plt.scatter(centroid[0], centroid[1], color=clrs[c], marker='*', s = 50)
        
        plt.show()
     
    
    #3D PLOTTING        
    def plotPoints3D(self): 
        colors = cm.rainbow(np.linspace(0, 1, self.cl_cnt))
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        
        for c in range(self.cl_cnt):
            centroid = self.centroids[c]
            x = []
            y = []
            z = []
            cluster_size = len(self.cl_points[c])
            
            #for each point assorted to the cluster
            for p in range(cluster_size):
                index = self.cl_points[c][p] #index of the point
                point = self.points[index]
                #print point
                x.append(point[0])
                y.append(point[1])
                z.append(point[2])
            
            clrs = cm.rainbow(np.linspace(0, 1, self.cl_cnt)) #colors
            
            ax.scatter(x, y, z, color=clrs[c], marker='o')
            ax.scatter(centroid[0], centroid[1], centroid[2],
                       color=clrs[c], marker='*', s = 50)
        print "I'm here"
        plt.show()
     
             
    ###------------------------
    ###----------START---------
    ###------------------------
    def start(self):
        
        flag = True
         
        while(flag):
            
            self.findMyCluster() #sorting points in cluster
            self.plotPoints()
            
            flag = self.newCentroidPositions()
            print self.cl_points

        #raw_input("Press Enter to continue...")
        
         
        
                    
        
        