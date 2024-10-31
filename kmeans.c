/*
    Todo: 
    Initialize centroids
    Assign points to clusters
    Update centroids based on cluster assignments
    Iterate until convergence or max iterations
*/

#include "kmeans.h"

Point* readData(char *filePath, int *pointCount) {
    FILE *filePtr = fopen(filePath, "r");
    if (filePtr == NULL) {
        printf("Cannot open file.\n");
        return NULL;
    }

    int tempCount = 0;
    char buffer[100];
    while (fgets(buffer, sizeof(buffer), filePtr)) {
        tempCount++;
    }
    rewind(filePtr); //Reset file pointer

    Point *loadedPoints = (Point *)malloc(tempCount * sizeof(Point));
    if (loadedPoints == NULL) {
        printf("Memory error.\n");
        fclose(filePtr);
        return NULL;
    }

    int index = 0;
    while (fgets(buffer, sizeof(buffer), filePtr)) {
        sscanf(buffer, "%lf %lf", &loadedPoints[index].x, &loadedPoints[index].y);
        index++;
    }

    fclose(filePtr);
    *pointCount = tempCount;
    return loadedPoints;
}

void initCentroids(Point *sourcePoints, Point *initialCentroids, int totalPoints, int numClusters) {
    for (int i = 0; i < numClusters; i++) {
        initialCentroids[i] = sourcePoints[i]; 
    }
}

double calcDistance(Point a, Point b) {
    double diffX = a.x - b.x;
    double diffY = a.y - b.y;
    return sqrt(diffX * diffX + diffY * diffY);
}

void assignClusters(Point *dataPoints, Point *currentCentroids, int *clusterMapping, int totalPoints, int numClusters) {

    /*
        Assign each point to the closest centroid using distance 
    */

    for (int i = 0; i < totalPoints; i++) {
        double minDist = calcDistance(dataPoints[i], currentCentroids[0]);
        int assignedCluster = 0;
        for (int j = 1; j < numClusters; j++) {
            double dist = calcDistance(dataPoints[i], currentCentroids[j]);
            if (dist < minDist) {
                minDist = dist;
                assignedCluster = j;
            }
        }
        clusterMapping[i] = assignedCluster;
    }
}

// Update centroids based on cluster assignments
void updateCentroids(Point *dataPoints, Point *currentCentroids, int *clusterMapping, int totalPoints, int numClusters) {
    int *pointCounts = (int *)calloc(numClusters, sizeof(int));
    Point *centroidSums = (Point *)calloc(numClusters, sizeof(Point));

    /* 
        Calculate sum of points assigned to each cluster
        Calculate new centroids
    */

    for (int i = 0; i < totalPoints; i++) {
        int currentCluster = clusterMapping[i];
        centroidSums[currentCluster].x += dataPoints[i].x;
        centroidSums[currentCluster].y += dataPoints[i].y;
        pointCounts[currentCluster]++;
    }

    for (int j = 0; j < numClusters; j++) {
        if (pointCounts[j] > 0) {
            currentCentroids[j].x = centroidSums[j].x / pointCounts[j];
            currentCentroids[j].y = centroidSums[j].y / pointCounts[j];
        }
    }

    free(pointCounts);
    free(centroidSums);
}

// Write output to file
void writeOutput(char *outputFile, Point *dataPoints, int *clusterMapping, int totalPoints) {
    FILE *outPtr = fopen(outputFile, "w");

    if (outPtr == NULL) {
        printf("Cannot write to file.\n");
        return;
    }

    // Write each point with its cluster assignment
    for (int i = 0; i < totalPoints; i++) {
        fprintf(outPtr, "%lf %lf %d\n", dataPoints[i].x, dataPoints[i].y, clusterMapping[i]);
    }

    fclose(outPtr);
}

void kMeans(Point *dataPoints, Point *currentCentroids, int *clusterMapping, int totalPoints, int numClusters) {
    /* 
        Initialize cluster assignments
        Update centroids
        Check for convergence
    */
    int hasChanged;
    int maxIterations = 0;
    do {
        hasChanged = 0;
        assignClusters(dataPoints, currentCentroids, clusterMapping, totalPoints, numClusters);

        Point *prevCentroids = (Point *)malloc(numClusters * sizeof(Point));
        for (int i = 0; i < numClusters; i++) {
            prevCentroids[i] = currentCentroids[i];
        }

        updateCentroids(dataPoints, currentCentroids, clusterMapping, totalPoints, numClusters);

        for (int i = 0; i < numClusters; i++) {
            if (calcDistance(prevCentroids[i], currentCentroids[i]) > 0.0001) {
                hasChanged = 1;
                break;
            }
        }

        free(prevCentroids);
        maxIterations++;
    } while (hasChanged && maxIterations < 100);
}
