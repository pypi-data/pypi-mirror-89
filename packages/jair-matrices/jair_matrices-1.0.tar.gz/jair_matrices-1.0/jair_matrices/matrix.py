''' Matrix class '''
from jair_matrices.exceptions import DimensionMatrixError, \
    AddSubtractionMatrixError, MultiplicationMatrixError


class Matrix:

    def __init__(self, matrix):
        '''
        Matrix class to realize addition, subtraction, multiplication and
        transpose operation.
        The matrix has to have at least one column and one row.

        Parameters
        --------
        matrix: List
            A two dimensional list
        '''
        self.matrix = matrix

        if len(self.matrix) == 0:
            raise DimensionMatrixError('row')
        self.rows = len(matrix)

        try:
            self.cols = len(matrix[0])
        except Exception as e:
            raise e

        if self.cols == 0:
            raise DimensionMatrixError('col')

    def add(self, matrix_2):
        '''
        Add two matrix

        Parameters
        --------
        matrix_2: Matrix
            The matrix that will be added

        Returns
        --------
        Matrix
            The resulting matrix
        '''
        if self.rows != matrix_2.rows or self.cols != matrix_2.cols:
            raise AddSubtractionMatrixError()

        added_matrix = [[0 for i in range(self.cols)]
                        for j in range(self.rows)]
        for row in range(self.rows):
            for col in range(self.cols):
                added_matrix[row][col] = \
                    self.matrix[row][col] + matrix_2.matrix[row][col]

        return Matrix(added_matrix)

    def subtraction(self, matrix_2):
        '''
        Subtract two matrix

        Parameters
        --------
        matrix_2: Matrix
            The matrix that will be subtracted

        Returns
        --------
        Matrix
            The resulting matrix
        '''
        if self.rows != matrix_2.rows or self.cols != matrix_2.cols:
            raise AddSubtractionMatrixError()

        sub_matrix = [[0 for i in range(self.cols)] for j in range(self.rows)]
        for row in range(self.rows):
            for col in range(self.cols):
                sub_matrix[row][col] = \
                    self.matrix[row][col] - matrix_2.matrix[row][col]

        return Matrix(sub_matrix)

    def _get_mult_element_result(self, row_list, matrix_2, col_index):
        '''
        Auxiliar function to realize the matrix multiplication.
        The goal of this function is to multiply the row from the first matrix
        with the elements from the column of the second matrix.

        Parameters
        --------
        row_list: List
            The row of the first matrix
        matrix_2: Matrix
            The matrix that will be subtracted
        col_index: Integer
            The column index of the second matrix

        Returns
        --------
        Integer
            The resulting element
        '''
        result_ele = 0
        for index, row_ele in enumerate(row_list):
            result_ele += row_ele * matrix_2.matrix[index][col_index]

        return result_ele

    def multiplication(self, matrix_2):
        '''
        Multiplication of two matrices

        Parameters
        --------
        matrix_2: Matrix
            The matrix that will be multiplied

        Returns
        --------
        Matrix
            The resulting matrix
        '''
        if self.cols != matrix_2.rows:
            raise MultiplicationMatrixError()

        mult_matrix = \
            [[0 for i in range(matrix_2.cols)] for j in range(self.rows)]
        for row in range(self.rows):
            for col in range(matrix_2.cols):
                mult_matrix[row][col] = self._get_mult_element_result(
                    self.matrix[row], matrix_2, col)

        return Matrix(mult_matrix)

    def transpose(self):
        '''
        Transpose the matrix

        Returns
        --------
        Matrix
            The transposed matrix
        '''
        trans_matrix = [[0 for i in range(self.rows)]
                        for j in range(self.cols)]
        for row in range(self.rows):
            for col in range(self.cols):
                trans_matrix[col][row] = self.matrix[row][col]

        return Matrix(trans_matrix)
