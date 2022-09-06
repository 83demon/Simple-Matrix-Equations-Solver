import numpy as np


class Solver:

    def __init__(self, matrix, vector_column, nu: list = None):
        self.m = matrix.shape[0]  # height
        self.n = matrix.shape[1]  # width
        self.A = matrix
        self.b = vector_column
        self._nu_set_length = 5
        self._nu_low = -10
        self._nu_high = 10
        if nu is None:
            self.nu_values = []
            self._init_nu()
            self.solution = dict()
        else:
            self.nu_values = nu
            self.solution = {nu: np.zeros((self.n, 1)) for nu in self.nu_values}  # dict of vector x for every nu
        self.A_inv = None  # pseudo inverse of self.matrix
        self.epsilon = np.array([[0]])  # accuracy
        self._has_invert = None
        self._unity_flag = None  # flag to indicate unity of the solution
        self.ndigits=3

    def _init_nu(self):
        for _ in range(self._nu_set_length):
            self.nu_values.append(tuple(np.random.randint(self._nu_low,self._nu_high,(1,self.n))[0]))

    def _translate_tuple_to_ndarray_n_transpore(self, key):
        """Translates from tuple of shape (1,m) to ndarray of shape (m,1)"""
        a = np.array(key)
        a=a[:,np.newaxis]
        return a

    def _compute_inverse(self):
        if self._has_invert:
            self.A_inv = np.linalg.inv(self.A)
        else:
            self.A_inv = np.linalg.pinv(self.A)

    def _check_for_inverse(self):
        """Checks whether matrix has an inverse one"""
        return self.m == self.n and np.linalg.det(self.A) != 0

    def _check_for_unity(self):
        """Checks a solution for unity"""
        return np.linalg.det(self.A.T @ self.A) > 0

    def _calculate_accuracy(self):
        if not self._has_invert:
            self.epsilon = self.b.T @ self.b - self.b.T @ self.A @ self.A_inv @ self.b

    def _solve(self):
        for nu in self.nu_values:
            nu_val = self._translate_tuple_to_ndarray_n_transpore(nu)

            matrix_product = self.A_inv @ self.A
            #matrix_product[np.isclose(matrix_product, 0)] = 0
            temp = nu_val - matrix_product @ nu_val
            #temp[np.isclose(temp, 0)] = 0
            self.solution[nu] = np.round(self.A_inv @ self.b + temp,decimals=self.ndigits)

    def main(self):
        self._has_invert = self._check_for_inverse()
        self._unity_flag = self._check_for_unity()
        self._compute_inverse()
        self._calculate_accuracy()
        self._solve()
        return self.solution, self.epsilon, self._has_invert, self._unity_flag
