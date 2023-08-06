'''Exceptions module.'''


class DimensionMatrixError(Exception):
    '''
        Exception raised for errors when the matrix has zero columns
        or zero rows.
    '''

    def __init__(self,
                 dimension='row',
                 message='The matrix needs to have at least one'):
        self.message = message
        super().__init__(self.message)
        self.dimension = dimension

    def __str__(self):
        return f'{self.message} {self.dimension}.'


class AddSubtractionMatrixError(Exception):
    '''
        Exception raised for errors when the matrices to be added or subracted
        do not have the same dimensions
    '''

    def __init__(self,
                 message='The matrices needs to have the same dimension'):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}.'


class MultiplicationMatrixError(Exception):
    '''
        Exception raised for errors when the matrices to be multiplied have
        the wrong dimensions
    '''

    def __init__(self,
                 message='The first matrix needs to have the number of '
                 'columns equals to the second matrix number of rows'):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}.'
