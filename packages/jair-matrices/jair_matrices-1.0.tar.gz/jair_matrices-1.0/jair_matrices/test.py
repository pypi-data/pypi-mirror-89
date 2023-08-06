import unittest
from matrix import Matrix


class TestMatrixClass(unittest.TestCase):

    def test_transpose(self):
        matrix_1 = Matrix([[1, 2],
                           [3, 4],
                           [1, 1]])
        expected_matrix = [[1, 3, 1], [2, 4, 1]]
        self.assertEqual(matrix_1.transpose().matrix, expected_matrix)

    def test_multiplication(self):
        matrix_1 = Matrix([[1, 2],
                           [3, 4],
                           [1, 1]])
        matrix_2 = Matrix([[9, 8],
                           [7, 6]])
        expected_matrix = [[23, 20], [55, 48], [16, 14]]
        self.assertEqual(matrix_1.multiplication(
            matrix_2).matrix, expected_matrix)

    def test_subtraction(self):
        matrix_1 = Matrix([[1, 2], [3, 4]])
        matrix_2 = Matrix([[9, 8], [7, 6]])
        expected_matrix = [[-8, -6], [-4, -2]]
        self.assertEqual(matrix_1.subtraction(
            matrix_2).matrix, expected_matrix)

    def test_add(self):
        matrix_1 = Matrix([[1, 2], [3, 4]])
        matrix_2 = Matrix([[9, 8], [7, 6]])
        expected_matrix = [[10, 10], [10, 10]]
        self.assertEqual(matrix_1.add(
            matrix_2).matrix, expected_matrix)

    def test_add_exception(self):
        matrix_1 = Matrix([[1, 2], [3, 4]])
        matrix_2 = Matrix([[9, 8, 10], [7, 6, 10]])
        with self.assertRaises(Exception) as context:
            matrix_1.add(matrix_2)

        self.assertEqual('The matrices needs to have the same dimension.',
                         str(context.exception))

    def test_subtraction_exception(self):
        matrix_1 = Matrix([[1, 2], [3, 4]])
        matrix_2 = Matrix([[9, 8, 10], [7, 6, 10]])
        with self.assertRaises(Exception) as context:
            matrix_1.subtraction(matrix_2)

        self.assertEqual('The matrices needs to have the same dimension.',
                         str(context.exception))

    def test_multiplication_exception(self):
        matrix_1 = Matrix([[1, 2], [3, 4]])
        matrix_2 = Matrix([[9, 8, 10], [7, 6, 10], [7, 6, 10]])
        with self.assertRaises(Exception) as context:
            matrix_1.multiplication(matrix_2)

        self.assertEqual('The first matrix needs to have the number of '
                         'columns equals to the second matrix number of rows.',
                         str(context.exception))

    def test_matrix_init(self):
        with self.assertRaises(Exception) as context:
            Matrix([])

        self.assertEqual('The matrix needs to have at least one row.',
                         str(context.exception))
        with self.assertRaises(Exception) as context:
            Matrix([[]])
        self.assertEqual('The matrix needs to have at least one col.',
                         str(context.exception))


if __name__ == '__main__':
    unittest.main()
