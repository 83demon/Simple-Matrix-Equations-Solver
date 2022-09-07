import numpy as np

class Parser:
    def __init__(self,m,n,matrix,b):
        self.m = int(m)
        self.n = int(n)
        self.raw_matrix = matrix
        self.raw_b = b
        self.matrix = np.zeros((self.m,self.n))
        self.b = np.zeros((self.m,1))

    def _parse_matrix(self):
        for i in range(self.m*self.n):
            self.matrix[i//self.n,i%self.n] = float(self.raw_matrix[i])

    def _parse_b_vector(self):
        for i in range(self.m):
            self.b[i] = float(self.raw_b[i])

    def main(self):
        self._parse_matrix()
        self._parse_b_vector()
        return self.matrix, self.b