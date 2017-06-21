"""Convert probility matrix to adjency matrix"""
import random
import numpy as np

def to_adjency_matrix(probability_matrix):
    """
    Converts the probability matrix to an adjency matrix

    Keyword arguments:
    probability_matrix -- a numpy matrix

    NOTE: For each element in the matrix, this will generate a random
    number between 0 and 1. If the random number is
    less than the element, replace the element with 1.
    If the random number is greater than
    or equal to the element, replace the element with 0

    Returns:
    The resulting adjency matrix
    """

    for item in np.nditer(probability_matrix, op_flags=['readwrite']):
        random_number = random.random()
        if random_number < item:
            item[...] = 1
        else:
            item[...] = 0

    return probability_matrix
