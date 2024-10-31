# utils.py

"""
Module: utils
Contains utility functions for K-Means clustering.
"""

import math

def euclidean_distance(point1, point2):
    """
    Calculates the Euclidean distance between two 2D points.

    Parameters:
        point1 (list of float): First point as [x, y].
        point2 (list of float): Second point as [x, y].

    Returns:
        float: Euclidean distance between point1 and point2.
    """
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)
