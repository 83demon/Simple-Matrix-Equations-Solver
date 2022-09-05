from Solver import Solver
import numpy as np

A = np.array([[1,2],[3,4]])
b = np.array([[10],[4]])
print(b.shape,A.shape)
nu_list = [(1,2),(0,0),(2,2)]
solver = Solver(A,b,nu_list)
solution, eps, has_invert, unity_flag = solver.main()
for k, v in solution.items():
    print(k,v)
print(eps,has_invert, unity_flag)


##TO DO: show eps, two flags, graphs and txt file