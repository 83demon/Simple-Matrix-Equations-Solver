import PySimpleGUI as sg
from Parser import Parser
from Solver import Solver
import numpy as np
import matplotlib.pyplot as plt


class GUI:
    def __init__(self):
        self._default_dim_value = 2
        self.title = "Simple Matrix Equation Solver"
        self._greeting_text = """Hi! This is a simple matrix equation solver. \n
                                    Please write down height and width of your matrix:"""
        self._input_matrix_text = "Please, write down your matrix data."
        self._input_b_vector_text = "Please, write down your b vector data."
        self._result_text = "Your result is:"
        self.layout = [[sg.Text(self._greeting_text)],
                       [sg.Input(default_text=self._default_dim_value),sg.Input(default_text=self._default_dim_value)],
                       [sg.Submit()]]
        self._m_n = None
        self._m = None
        self._n = None
        self._marker_width = 3
        self._input_box_size = (6,1)
        self._default_value = '0'
        self.color = 'forestgreen'
        self.handler()

    def _first_run(self):
        self.window = sg.Window(self.title, self.layout)
        event, self._m_n = self.window.read()
        self._m = int(self._m_n[0])
        self._n = int(self._m_n[1])
        sg.popup(f'You entered: \nHeight: {self._m}\t Width: {self._n}')
        self.window.close()

    def _construct_matrix_input(self):
        self.layout = [[sg.Text(self._input_matrix_text)]]
        for i in range(int(self._m)):
            temp = [sg.Input(size=self._input_box_size,default_text=self._default_value) for _ in range(int(self._n))]
            self.layout.append(temp)
        self.layout.append([sg.Submit()])
        self.window = sg.Window(self.title, self.layout)
        event, self.raw_matrix = self.window.read()
        #print("You entered:", self.raw_matrix)
        self.window.close()

    def _construct_b_vector_input(self):
        self.layout = [[sg.Text(self._input_b_vector_text)]]
        for i in range(int(self._m)):
            temp = [sg.Input(size=self._input_box_size,default_text=self._default_value)]
            self.layout.append(temp)
        self.layout.append([sg.Submit()])
        self.window = sg.Window(self.title, self.layout)
        event, self.raw_b_vector = self.window.read()
        #print("You entered:", self.raw_b_vector)
        self.window.close()

    def _show_result(self, solution, pinv_matrix, epsilon, has_invert, unity_check):
        self.layout = [[sg.Text(self._result_text)]]
        for i in range(int(self._n)):
            temp = [sg.Text(size=self._input_box_size,text=f"{solution[key][i]}") for key in solution.keys()]
            self.layout.append(temp)

        self.layout.append([sg.Text("")])
        k=1
        for v in solution.keys():
            self.layout.append([sg.Text("v"+str(k)+": " + " ".join([str(v[i]) for i in range(self._n)]))])
            k+=1
        self.layout.append([sg.Text(f"Pseudo incerse matrix is:")])

        #pseudo inverse matrix has shape (n,m) while original one has shape of (m,n)
        for i in range(self._n):
            self.layout.append([sg.Text(" ".join([str(pinv_matrix[i][j]) for j in range(self._m)]))])
        self.layout.append([sg.Text(f"Epsilon^2: {epsilon[0][0]}")])
        self.layout.append([sg.Text(f"There is only one solution: {unity_check}")])
        self.layout.append([sg.CloseButton("Bye!"),sg.Button("Show Visualisation")])
        self.window = sg.Window(self.title, self.layout)

        while True:

            event, values = self.window.read()

            if event == 'Show Visualisation':
                self._show_graphs(solution, unity_check)

            if event == sg.WIN_CLOSED:
                break

        self.window.close()

    def _show_graphs(self,solution,unity_flag):
        if self._n==2 or self._n==3:
            xs = []
            ys = []
            if self._n == 2:
                if unity_flag:
                    for v in solution.values():
                        xs = v[0]
                        ys = v[1]
                        break
                else:
                    for v in solution.values():
                        xs.append(v[0])
                        ys.append(v[1])
                plt.scatter(x=xs, y=ys,linewidths=self._marker_width,c=self.color)
                plt.show()
            if self._n == 3:
                xs = []
                ys = []
                zs = []
                fig = plt.figure()
                ax = fig.add_subplot(projection='3d')
                if unity_flag:
                    for v in solution.values():
                        xs = v[0]
                        ys = v[1]
                        zs = v[2]
                        break
                else:
                    for v in solution.values():
                        xs.append(v[0])
                        ys.append(v[1])
                        zs.append(v[2])

                ax.scatter(xs=xs,ys=ys,zs=zs,linewidths=self._marker_width,c=self.color)
                plt.show()
        else:

            visualize_window = sg.Window('Whoops...',[[sg.Text(f"Teach me to visualize plots in {self._n} dimensions")],
                                   [sg.CloseButton("I'll teach you"),sg.CloseButton("I'm done.")]])
            while True:

                event, values = visualize_window.read()

                if event == sg.WIN_CLOSED:
                    break
            visualize_window.close()

    def handler(self):
        self._first_run()
        if 1<=self._n<=13 and 1<=self._m<=25:
            self._construct_matrix_input()
            self._construct_b_vector_input()
            parser = Parser(self._m,self._n,self.raw_matrix,self.raw_b_vector)
            solver = Solver(*parser.main())
            solution, pinv_matrix, eps, has_invert, unity_check = solver.main()
            self._show_result(solution, pinv_matrix, eps, has_invert, unity_check)
        elif self._n<=0 or self._m <=0:
            raise ValueError(f'Cannot construct matrix with shape {self._m,self._n}')

        else:
            console_input = read_from_console(self._m, self._n)
            solver = Solver(*console_input)
            solution, pinv_matrix, eps, has_invert, unity_check = solver.main()
            console_output(solution, pinv_matrix, eps, has_invert, unity_check)
            self._show_graphs(solution,unity_check)




def read_from_console(m,n):
    print(f"Enter a {(m,n)} matrix data separated by whitespace:\n")
    matrix_data = []
    for i in range(m):
        temp = input().split(" ")
        if temp[-1] == "":
            temp.pop()
        if len(temp)!=n:
            raise ValueError(f"You entered {len(temp)} values")
        matrix_data.append(temp)


    print(f"Enter a {(m,1)} b vector data separated by whitespace:\n")
    b = input().split(" ")
    matrix = np.array(matrix_data,dtype=np.float32)
    b_vector = np.array(b,dtype=np.float32)
    b_vector = b_vector[:,np.newaxis]


    return matrix, b_vector


def console_output(solution, pinv_matrix, eps, has_invert, unity_check):
    print("Your solution:\n")
    for k,v in solution.items():
        print(f"{k} :\n{v}")
    print()
    print("Pseudo inverted matrix is:\n")
    for i in range(pinv_matrix.shape[0]):
       print(f"{' '.join(str(pinv_matrix[i][j]) for j in range(pinv_matrix.shape[1]))}")
    print()
    print(f'Epsilon^2 is: {eps}')
    print(f'There is only one solution: {unity_check}')
    print()




