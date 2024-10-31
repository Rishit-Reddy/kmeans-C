# file_io.py

"""
Module: file_io
Handles reading input data and writing output results for K-Means clustering.
"""

def read_data(filename):
    """
    Reads 2D data points from a file.

    Parameters:
        filename (str): Path to the input data file.

    Returns:
        list of list of float: A list containing data points as [x, y].
    
    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file contains invalid data.
    """
    data = []
    try:
        with open(filename, 'r') as file:
            for line_num, line in enumerate(file, start=1):
                stripped_line = line.strip()
                if not stripped_line:
                    continue  # Skip empty lines
                # Adjust the splitter if commas are used
                if ',' in stripped_line:
                    parts = stripped_line.split(',')
                else:
                    parts = stripped_line.split()
                if len(parts) != 2:
                    raise ValueError(f"Invalid data format on line {line_num}: '{line.strip()}'")
                try:
                    x, y = float(parts[0]), float(parts[1])
                    data.append([x, y])
                except ValueError:
                    raise ValueError(f"Non-numeric data on line {line_num}: '{line.strip()}'")
        if not data:
            raise ValueError("Input file is empty.")
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: '{filename}' not found.")
    except Exception as e:
        raise e

def write_output(filename, data, cluster_assignments):
    """
    Writes the clustering results to an output file.

    Parameters:
        filename (str): Path to the output file.
        data (list of list of float): Original data points.
        cluster_assignments (list of int): Cluster index for each data point.
    
    Raises:
        Exception: If there's an issue writing to the file.
    """
    try:
        with open(filename, 'w') as file:
            file.write("x\ty\tcluster\n")
            for point, cluster in zip(data, cluster_assignments):
                file.write(f"{point[0]}\t{point[1]}\t{cluster}\n")
    except Exception as e:
        raise Exception(f"Error writing to '{filename}': {e}")
