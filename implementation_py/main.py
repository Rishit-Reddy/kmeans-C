# main.py

"""
Main script for K-Means clustering.
Handles user input, orchestrates the clustering process, manages output, and optionally visualizes the results.
"""

import sys
import argparse
from file_io import read_data, write_output
from kmeans import initialize_centroids, get_initial_centroids_user_input, kmeans

def get_number_of_clusters(max_k):
    """
    Prompts the user to enter the number of clusters (k).

    Parameters:
        max_k (int): Maximum allowable value for k.

    Returns:
        int: Number of clusters.
    """
    while True:
        try:
            k = int(input("Enter the number of clusters (k): "))
            if 1 <= k <= max_k:
                return k
            else:
                print(f"Please enter an integer between 1 and {max_k}.")
        except ValueError:
            print("Invalid input. Please enter a positive integer.")

def get_initial_centroids(data, k):
    """
    Determines initial centroids either randomly or via user input.

    Parameters:
        data (list of list of float): The dataset.
        k (int): Number of clusters.

    Returns:
        list of list of float: Initial centroids.
    """
    while True:
        choice = input("Do you want to input initial centroids? (y/n): ").strip().lower()
        if choice == 'y':
            return get_initial_centroids_user_input(data, k)
        elif choice == 'n':
            return initialize_centroids(data, k)
        else:
            print("Invalid choice. Please enter 'y' or 'n'.")

def main():
    """
    Main function to execute the K-Means clustering and optionally visualize the results.
    """
    parser = argparse.ArgumentParser(description="K-Means Clustering Implementation")
    parser.add_argument('-v', '--visualize', action='store_true', help='Visualize the clustering results after completion')
    args = parser.parse_args()

    input_filename = 'kmeans-data.txt'
    output_filename = 'kmeans-output.txt'

    # Step 1: Read data
    try:
        data = read_data(input_filename)
        print(f"Successfully read {len(data)} data points from '{input_filename}'.")
    except Exception as e:
        print(e)
        sys.exit(1)

    # Step 2: Get number of clusters
    k = get_number_of_clusters(len(data))
    print(f"Number of clusters (k): {k}")

    # Step 3: Get initial centroids
    initial_centroids = get_initial_centroids(data, k)
    print("Initial centroids:")
    for idx, centroid in enumerate(initial_centroids, start=1):
        print(f"  Centroid {idx}: {centroid}")

    # Step 4: Perform K-Means clustering
    cluster_assignments, final_centroids = kmeans(data, k, initial_centroids)

    # Step 5: Write output
    try:
        write_output(output_filename, data, cluster_assignments)
        print(f"K-Means clustering completed. Results are in '{output_filename}'.")
    except Exception as e:
        print(e)
        sys.exit(1)

    # Optional: Print final centroids
    print("Final centroids:")
    for idx, centroid in enumerate(final_centroids, start=1):
        print(f"  Centroid {idx}: {centroid}")

    # Step 6: Visualize if flag is set
    if args.visualize:
        print("Visualizing the clustering results...")
        try:
            import subprocess
            subprocess.run([sys.executable, 'visualization.py'], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error during visualization: {e}")
        except FileNotFoundError:
            print("Error: 'visualization.py' not found.")
        except Exception as e:
            print(f"An unexpected error occurred during visualization: {e}")

if __name__ == "__main__":
    main()
