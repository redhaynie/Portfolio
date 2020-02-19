classification
import pickle
import random
import math
import copy
import sys
import pdb
import matplotlib.pyplot as plt
from KNN_Data import *

LAST_NAME = "Haynie"


def visualize_data(data, cluster_centers_file):
  fig = plt.figure(1, figsize=(4,3))
  f = open(cluster_centers_file, 'rb')
  centers = pickle.load(f)
  f.close()

  km = KMeansClassifier()
  km._cluster_centers = centers

  colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']

  labels = []
  center_colors = []
  for pt in data:
    labels.append(colors[km.classify(pt) % len(colors)])

  for i in range(len(centers)):
    center_colors.append(colors[i])

  plt.scatter([d[0] for d in data], [d[1] for d in data], c=labels, marker='x')
  plt.scatter([c[0] for c in centers], [c[1] for c in centers], c=center_colors, marker='D')
  plt.title("K-Means Visualization")
  plt.show()

def distance(p0, p1):
    return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)

class KMeansClassifier(object):

  def __init__(self):
    self._cluster_centers = [] # List of cluster centers, each of which is a point. ex: [ [10,10], [2,1], [0,-3] ]
    self._data = [] # List of datapoints (list of immutable lists, ex:  [ (0,0), (1.,5.), (2., 3.) ] )

  def add_datapoint(self, datapoint):
    self._data.append(datapoint)

  def fit(self, k):
    # Fit k clusters to the data, by starting with k randomly selected cluster centers.
    self._cluster_centers = [] # Reset cluster centers array
    end = True
    # TODO: Initialize k cluster centers at random points
    # HINT: To choose reasonable initial cluster centers, you can set them to be in the same spot as random (different) points from the dataset
    
    for i in range(k):
    	self._cluster_centers.append(random.choice(self._data))
   

    # TODO Follow convergence procedure to find final locations for each center
    while end ==True:
      xtot=[0]*k
      ytot=[0]*k
      xynum=[0]*k
      totavgs=[]
      # TODO: Iterate through each datapoint in self._data and figure out which cluster it belongs to
      # HINT: Use self.classify(p) for each datapoint p
      for y in self._data:
      	pos = self.classify(y)
      	xynum[pos] +=1
      	xtot[pos] += y[0]
      	ytot[pos] += y[1]

      # TODO: Figure out new positions for each cluster center (should be the average position of all its points)
      totdist = 0
      for u in range(k):
      	totavgs.append([(xtot[u]/xynum[u]),(ytot[u]/xynum[u])])
      	totdist+=distance(totavgs[u],self._cluster_centers[u])


      if totdist >.001 :
        for t in range(k):
        	self._cluster_centers[t] = totavgs[t]
        
      else: 
      	end = False
      # TODO: Check to see how much the cluster centers have moved (for the stopping condition)	
      print("End of loop")
    print("End of code")


    # TODO Add each of the 'k' final cluster_centers to the model (self._cluster_centers)

  def classify(self,p):
    # Given a data point p, figure out which cluster it belongs to and return that cluster's ID (its index in self._cluster_centers)
    closest_cluster_index = 0
    mindistval = []
    # TODO Find nearest cluster center, then return its index in self._cluster_centers
    for i in range(len(self._cluster_centers)):
    	if i == 0:
    		mindistval = self._cluster_centers[i]

    	else:
    		if distance(self._cluster_centers[i],p) < distance(mindistval,p):
    			mindistval = self._cluster_centers[i]
    			closest_cluster_index = i
    # TODO Find nearest cluster center, then return its index in self._cluster_centers

    return closest_cluster_index

class KNNClassifier(object):

  def __init__(self):
    self._data = [] # list of (datapoint, label) tuples
  
  def clear_data(self):
    # Removes all data stored within the model
    self._data = []

  def add_labeled_datapoint(self, data_point, label):
    # Adds a labeled datapoint tuple onto the object's _data member
    self._data.append((data_point, label))
  
  def classify_datapoint(self, data_point, k):
    label_counts = {} # Dictionary mapping "label" => vote count
    best_label = None
    label_dist = {} #dictionary adding up distances
    # Perform k_nearest_neighbor classification, setting best_label to the majority-vote label for k-nearest points
    #TODO: Find the k nearest points in self._data to data_point
    temp = [0]*k
    listtemp = [0]*k
    first = True
    for i in self._data :
    	tempdist = distance(data_point, i[0]) #find distance between given data point and data point
    	for j in range(k): #loop through saved data points
	    	if tempdist < temp[j] or temp[j] == 0: #if the new data point is less than the distance in list
	    		temp[j] = tempdist
	    		listtemp[j] = i
	    		
	    		break
    #TODO: Populate label_counts with the number of votes each label got from the k nearest points

    for d in range(len(listtemp)):
    	if listtemp[d][1] not in label_counts.keys():
    		label_counts[listtemp[d][1]] = 1
    		label_dist[listtemp[d][1]]= temp[d]

    	else:
    		label_counts[listtemp[d][1]]+= 1
    		label_dist[listtemp[d][1]]+= temp[d]
    #TODO: Make sure to scale the weight of the vote each point gets by how far away it is from data_point
    #      Since you're just taking the max at the end of the algorithm, these do not need to be normalized in any way
    maxcount = 0
    mindist=sys.maxsize
    for i in label_counts:
    	if label_counts[i] > maxcount:
    		maxcount = label_counts[i]
    		best_label = i
    	if label_dist[i]<mindist:
    		mindist = label_counts[i]
    		best_label = i
    end = ["#"] *40

    return best_label



def print_and_save_cluster_centers(classifier, filename):
  for idx, center in enumerate(classifier._cluster_centers):
    print("  Cluster %d, center at: %s" % (idx, str(center)))


  f = open(filename,'wb')
  pickle.dump(classifier._cluster_centers, f)
  f.close()

def read_data_file(filename):
  f = open(filename)
  data_dict = pickle.load(f)
  f.close()

  return data_dict['data'], data_dict['labels']

def read_hw_data():
  global hw_data
  data_dict = pickle.loads(hw_data)
  return data_dict['data'], data_dict['labels']

def main():
  global LAST_NAME
  # read data file
  #data, labels = read_data_file('hw3_data.pkl')

  # load dataset
  data, labels = read_hw_data()

  # data is an 'N' x 'M' matrix, where N=number of examples and M=number of dimensions per example
  # data[0] retrieves the 0th example, a list with 'M' elements, one for each dimension (xy-points would have M=2)
  # labels is an 'N'-element list, where labels[0] is the label for the datapoint at data[0]


  ########## PART 1 ############
  # perform K-means clustering
  kMeans_classifier = KMeansClassifier()
  for datapoint in data:
    kMeans_classifier.add_datapoint(datapoint) # add data to the model

  kMeans_classifier.fit(4) # Fit 4 clusters to the data

  # plot results
  print('\n'*2)
  print("K-means Classifier Test")
  print('-'*40)
  print("Cluster center locations:")
  print_and_save_cluster_centers(kMeans_classifier, "hw3_kmeans_" + LAST_NAME + ".pkl")

  print('\n'*2)


  ########## PART 2 ############
  print("K-Nearest Neighbor Classifier Test")
  print('-'*40)

  # Create and test K-nearest neighbor classifier
  kNN_classifier = KNNClassifier()
  k = 2

  correct_classifications = 0
  # Perform leave-one-out cross validation (LOOCV) to evaluate KNN performance
  for holdout_idx in range(len(data)):
    # Reset classifier
    kNN_classifier.clear_data()

    for idx in range(len(data)):
      if idx == holdout_idx: continue # Skip held-out data point being classified

      # Add (data point, label) tuples to KNNClassifier
      kNN_classifier.add_labeled_datapoint(data[idx], labels[idx])

    guess = kNN_classifier.classify_datapoint(data[holdout_idx], k) # Perform kNN classification
    if guess == labels[holdout_idx]: 
      correct_classifications += 1.0
  
  print("kNN classifier for k=%d" % k)
  print("Accuracy: %g" % (correct_classifications / len(data)))
  print('\n'*2)

  visualize_data(data, 'hw3_kmeans_' + LAST_NAME + '.pkl')


if __name__ == '__main__':
  main()
