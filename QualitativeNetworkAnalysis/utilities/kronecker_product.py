
def compute_kronecker_product(matrix, power, decimalplaces):
    """
    Computes the kroneker product of the given nxn matrix

    Keyword arguments:
    matrix -- the nxn matrix
    power -- the number of times to multiply the matrix by itself
    decimalplaces -- the number of decimal places to round values to

    NOTE: A 2x2 matrix with exponent = 3 generates a 256x256 matrix
    Using exponent > 3 is likely to cause an out of memory exception

    Returns:
    The resulting matrix
    """
    interim_matrix = []
    sub_matrix = []
    kronecker_matrix = matrix

    for multiplier in range(power):

        count = len(kronecker_matrix)
        for elem1 in kronecker_matrix:
            counter = 0
            check = 0
            while check < count:
                for num1 in elem1:
                    for num2 in kronecker_matrix[counter]:
                        sub_matrix.append(round(num1 * num2, decimalplaces))
                counter += 1
                interim_matrix.append(sub_matrix)
                sub_matrix = []
                check += 1

        kronecker_matrix = interim_matrix
        interim_matrix = []
        multiplier += 1

    return kronecker_matrix
