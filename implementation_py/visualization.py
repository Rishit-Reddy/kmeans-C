# visualization.py

"""
Module: visualization
Reads the clustering results from 'kmeans-output.txt' and visualizes them using matplotlib.
"""

import matplotlib.pyplot as plt
import sys
import os

def read_output(filename):
    """
    Reads the clustering results from the output file.
    
    Parameters:
        filename (str): Path to the output file.
    
    Returns:
        tuple:
            list of list of float: Data points as [x, y].
            list of int: Cluster assignments.
    """
    data = []
    cluster_assignments = []
    try:
        with open(filename, 'r') as file:
            header = file.readline()  # Skip header
            for line_num, line in enumerate(file, start=2):
                stripped_line = line.strip()
                if not stripped_line:
                    continue  # Skip empty lines
                parts = stripped_line.split()
                if len(parts) != 3:
                    print(f"Warning: Invalid format on line {line_num}: '{line.strip()}'")
                    continue
                try:
                    x, y, cluster = float(parts[0]), float(parts[1]), int(parts[2])
                    data.append([x, y])
                    cluster_assignments.append(cluster)
                except ValueError:
                    print(f"Warning: Non-numeric data on line {line_num}: '{line.strip()}'")
                    continue
        if not data:
            print("Error: No valid data found in the output file.")
            sys.exit(1)
        return data, cluster_assignments
    except FileNotFoundError:
        print(f"Error: '{filename}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading '{filename}': {e}")
        sys.exit(1)

def plot_clusters(data, cluster_assignments, k):
    """
    Plots the clustered data points.
    
    Parameters:
        data (list of list of float): Data points as [x, y].
        cluster_assignments (list of int): Cluster index for each data point.
        k (int): Number of clusters.
    """
    # Create a color map
    colors = plt.cm.get_cmap('tab20', k)

    # Plot each cluster
    for cluster_index in range(k):
        cluster_points = [point for point, assignment in zip(data, cluster_assignments) if assignment == cluster_index]
        if not cluster_points:
            continue  # Skip empty clusters
        x_coords = [point[0] for point in cluster_points]
        y_coords = [point[1] for point in cluster_points]
        plt.scatter(x_coords, y_coords, s=30, color=colors(cluster_index), label=f'Cluster {cluster_index}')
    
    plt.title('K-Means Clustering Results')
    plt.xlabel('X-coordinate')
    plt.ylabel('Y-coordinate')
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    """
    Main function to execute the visualization.
    """
    output_filename = 'kmeans-output.txt'
    
    # Check if the output file exists
    if not os.path.exists(output_filename):
        print(f"Error: '{output_filename}' does not exist. Please run the clustering first.")
        sys.exit(1)
    
    # Read the output file
    data, cluster_assignments = read_output(output_filename)
    
    # Determine the number of clusters
    k = max(cluster_assignments) + 1  # Assuming clusters are labeled from 0 to k-1
    
    # Plot the clusters
    plot_clusters(data, cluster_assignments, k)

if __name__ == "__main__":
    main()
