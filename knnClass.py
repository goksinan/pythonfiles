#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  9 17:23:53 2018

@author: sinan
"""
import numpy as np
import random
import matplotlib.pyplot as plt
import scipy.stats as ss

def distance(p1, p2):
    """Finds the distance between two points"""
    return np.sqrt(np.sum(np.power(p2-p1,2)))

p1 = np.array([1,1])
p2 = np.array([2,3])

print(distance(p1, p2))


def majority_vote(votes):
    vote_counts = {}
    for vote in votes:
        if vote in vote_counts:
            vote_counts[vote] += 1
        else:
            vote_counts[vote] = 1
            
    winners = []
    max_count = max(vote_counts.values())
    for vote, count in vote_counts.items():
        if vote_counts[vote] == max_count:
            winners.append(vote)
        
    return random.choice(winners)

votes = [1,1,1,2,2,3,3,1,1,3,3,3,4,5,6]

winner = majority_vote(votes)


points = np.array([[1,1],[1,2],[1,3],[2,1],[2,2],[2,3],[3,1],[3,2],[3,3]])
p = np.array([2.5,2])

plt.plot(points[:,0], points[:,1], 'bo')
plt.plot(p[0], p[1], 'r*')
plt.show()


def find_nearest_neighbors(p, points, k=2):
    distances = np.zeros(points.shape[0])
    for i in range(len(distances)):
        distances[i] = distance(p, points[i])
    ind = np.argsort(distances)
    return ind[:k]


def knn_predict(p, points, outcomes, k=5):
    ind = find_nearest_neighbors(p, points, k)
    return majority_vote(outcomes[ind])
    
outcomes = np.array([0,0,0,0,1,1,1,1,1])
    
def generate_synthetic_data(n=50):
    """Create two sets of points from bivariate normal distribution"""
    points = np.concatenate((ss.norm(0,1).rvs((n,2)), ss.norm(1,1).rvs((n,2))), axis=0)
    outcomes = np.concatenate((np.repeat(0,n), np.repeat(1,n)), axis=0)
    return (points, outcomes)
    
n = 20
(points, outcomes) = generate_synthetic_data(n)
plt.figure()
plt.plot(points[:n,0], points[:n,1], "bo")
plt.plot(points[n:,0], points[n:,1], "ro")
plt.show()


def make_prediction_grid(predictors, outcomes, limits, h, k):
    """xx"""
    (x_min, x_max, y_min, y_max) = limits
    xs = np.arange(x_min, x_max, h)
    ys = np.arange(y_min, y_max, h)
    xx, yy = np.meshgrid(xs,  ys)
    
    prediction_grid = np.zeros(xx.shape, dtype=int)
    for i,x in enumerate(xs):
        for j,y in enumerate(ys):
            p = np.array([x,y])
            prediction_grid[j,i] = knn_predict(p, predictors, outcomes, k)
            
    return (xx, yy, prediction_grid)
            

predictors, outcomes = generate_synthetic_data()

k = 25; filename = 'knn_predict_5.pdf'; limits = (-3,4,-3,4); h = 0.1;
(xx, yy, prediction_grid) = make_prediction_grid(predictors, outcomes, limits, h, k)
plot_prediction_grid(xx, yy, prediction_grid, filename)








