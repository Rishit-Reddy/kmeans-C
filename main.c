/*
    Todo: 
    1. Read the file
    2. user input: Clusters
    3. user input: Centroids (if yes)
    4. kMeans (kmeans.c)
    5. Write output to file
*/

#include "kmeans.h"

int main() {
    int totalPoints;
    Point *dataPoints = readData("kmeans-data.txt", &totalPoints);
    if (dataPoints == NULL) {
        return 1;
    }

    int numClusters;
    printf("Enter number of clusters: ");
    scanf("%d", &numClusters);

    if (numClusters <= 0 || numClusters > totalPoints) {
        printf("Invalid number of clusters.\n");
        free(dataPoints);
        return 1;
    }

    Point *initialCentroids = (Point *)malloc(numClusters * sizeof(Point));
    int *pointClusters = (int *)malloc(totalPoints * sizeof(int));
    if (initialCentroids == NULL || pointClusters == NULL) {
        printf("Memory error.\n");
        free(dataPoints);
        return 1;
    }

    char centroidChoice;
    printf("Input initial centroids? (y/n): ");
    scanf(" %c", &centroidChoice);

    if (centroidChoice == 'y' || centroidChoice == 'Y') {
        for (int i = 0; i < numClusters; i++) {
            printf("Enter centroid %d (x y): ", i + 1);
            scanf("%lf %lf", &initialCentroids[i].x, &initialCentroids[i].y);
        }
    } else {
        initCentroids(dataPoints, initialCentroids, totalPoints, numClusters);
    }

    kMeans(dataPoints, initialCentroids, pointClusters, totalPoints, numClusters);

    writeOutput("kmeans-output.txt", dataPoints, pointClusters, totalPoints);
    printf("Output written to output.txt.\n");

    free(dataPoints);
    free(initialCentroids);
    free(pointClusters);
    return 0;
}
