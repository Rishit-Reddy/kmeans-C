# kmeans.py

"""
Module: kmeans
Implements the K-Means clustering algorithm.
"""

import random
from utils import euclidean_distance

def initialize_centroids(data, k):
    """
    Randomly selects k unique data points as initial centroids.

    Parameters:
        data (list of list of float): The dataset.
        k (int): Number of clusters.

    Returns:
        list of list of float: Initial centroids.
    
    Raises:
        ValueError: If k is greater than the number of data points.
    """
    if k > len(data):
        raise ValueError("Number of clusters 'k' cannot exceed number of data points.")
    return random.sample(data, k)

def get_initial_centroids_user_input(data, k):
    """
    Prompts the user to input initial centroids.

    Parameters:
        data (list of list of float): The dataset.
        k (int): Number of clusters.

    Returns:
        list of list of float: User-specified initial centroids.
    
    Raises:
        ValueError: If user inputs invalid coordinates.
    """
    centroids = []
    print("Enter the initial centroids:")
    for i in range(k):
        while True:
            try:
                x = float(input(f"  Centroid {i+1} - Enter x-coordinate: "))
                y = float(input(f"  Centroid {i+1} - Enter y-coordinate: "))
                centroids.append([x, y])
                break
            except ValueError:
                print("  Invalid input. Please enter numeric values for coordinates.")
    return centroids

def assign_clusters(data, centroids):
    """
    Assigns each data point to the nearest centroid.

    Parameters:
        data (list of list of float): The dataset.
        centroids (list of list of float): Current centroids.

    Returns:
        list of int: Cluster index for each data point.
    """
    cluster_assignments = []
    for point in data:
        distances = [euclidean_distance(point, centroid) for centroid in centroids]
        min_distance_index = distances.index(min(distances))
        cluster_assignments.append(min_distance_index)
    return cluster_assignments

def calculate_new_centroids(data, cluster_assignments, k):
    """
    Recalculates centroids as the mean of all points assigned to each cluster.

    Parameters:
        data (list of list of float): The dataset.
        cluster_assignments (list of int): Current cluster assignments.
        k (int): Number of clusters.

    Returns:
        list of list of float: Updated centroids.
    """
    new_centroids = []
    for cluster_index in range(k):
        cluster_points = [point for point, assignment in zip(data, cluster_assignments) if assignment == cluster_index]
        if cluster_points:
            x_mean = sum(point[0] for point in cluster_points) / len(cluster_points)
            y_mean = sum(point[1] for point in cluster_points) / len(cluster_points)
            new_centroids.append([x_mean, y_mean])
        else:
            # If a cluster has no points, reinitialize its centroid randomly
            new_centroids.append(random.choice(data))
    return new_centroids

def kmeans(data, k, initial_centroids, max_iterations=100):
    """
    Performs K-Means clustering on the dataset.

    Parameters:
        data (list of list of float): The dataset.
        k (int): Number of clusters.
        initial_centroids (list of list of float): Initial centroids.
        max_iterations (int): Maximum number of iterations to prevent infinite loops.

    Returns:
        tuple:
            list of int: Final cluster assignments.
            list of list of float: Final centroids.
    """
    centroids = initial_centroids
    for iteration in range(max_iterations):
        cluster_assignments = assign_clusters(data, centroids)
        new_centroids = calculate_new_centroids(data, cluster_assignments, k)
        # Check for convergence (if centroids do not change)
        if all(euclidean_distance(c1, c2) < 1e-4 for c1, c2 in zip(centroids, new_centroids)):
            print(f"Converged after {iteration+1} iterations.")
            break
        centroids = new_centroids
    else:
        print(f"Reached maximum iterations ({max_iterations}).")
    return cluster_assignments, centroids
