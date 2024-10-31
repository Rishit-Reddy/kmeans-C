// kmeans.h

#ifndef KMEANS_H
#define KMEANS_H

#include <stdio.h>
#include <stdlib.h>
#include <math.h>

//Structure for a point
typedef struct {
    double x;
    double y;
} Point;

//Functions
Point* readData(char *filename, int *numPoints);
void initCentroids(Point *points, Point *centroids, int numPoints, int k);
double calcDistance(Point p1, Point p2);
void assignClusters(Point *points, Point *centroids, int *clusters, int numPoints, int k);
void updateCentroids(Point *points, Point *centroids, int *clusters, int numPoints, int k);
void kMeans(Point *points, Point *centroids, int *clusters, int numPoints, int k);
void writeOutput(char *filename, Point *points, int *clusters, int numPoints);

#endif
