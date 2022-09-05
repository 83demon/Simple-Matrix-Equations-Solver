import PySimpleGUI as sg
from Parser import Parser
from Solver import Solver
import numpy as np
import matplotlib.pyplot as plt


class GUI:
    def __init__(self):
        self.title = "Simple Matrix Equation Solver"
        self._greeting_text = """Hi! This is a simple matrix equation solver. \n
                                    Please write down height and width of your matrix:"""
        self._input_matrix_text = "Please, write down your matrix data."
        self._input_b_vector_text = "Please, write down your b vector data."
        self._result_text = "Your result is:"
        self.layout = [[sg.Text(self._greeting_text)],
                       [sg.Input(),sg.Input()],
                       [sg.Submit(), sg.Cancel()]]
        self._m_n = None
        self._m = None
        self._n = None
        self._input_box_size = (6,1)
        self._default_value = '0'
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
        self.layout.append([sg.Submit(), sg.Cancel()])
        self.window = sg.Window(self.title, self.layout)
        event, self.raw_matrix = self.window.read()
        #print("You entered:", self.raw_matrix)
        self.window.close()

    def _construct_b_vector_input(self):
        self.layout = [[sg.Text(self._input_b_vector_text)]]
        for i in range(int(self._m)):
            temp = [sg.Input(size=self._input_box_size,default_text=self._default_value)]
            self.layout.append(temp)
        self.layout.append([sg.Submit(), sg.Cancel()])
        self.window = sg.Window(self.title, self.layout)
        event, self.raw_b_vector = self.window.read()
        #print("You entered:", self.raw_b_vector)
        self.window.close()

    def _show_result(self, solution, epsilon, has_invert, unity_check):
        self.layout = [[sg.Text(self._result_text)]]
        for i in range(int(self._n)):
            temp = [sg.Text(size=self._input_box_size,text=f"{solution[key][i]}") for key in solution.keys()]
            self.layout.append(temp)

        self.layout.append([sg.Text("")])
        k=1
        for v in solution.keys():
            self.layout.append([sg.Text("v"+str(k)+": " + " ".join([str(v[i]) for i in range(self._m)]))])
            k+=1
        self.layout.append([sg.CloseButton("Okay")])
        self.window = sg.Window(self.title, self.layout)
        event = self.window.read()
        self.window.close()
        pass

    def _show_graphs(self):
        pass

    def handler(self):
        self._first_run()
        self._construct_matrix_input()
        self._construct_b_vector_input()
        parser = Parser(self._m,self._n,self.raw_matrix,self.raw_b_vector)
        solver = Solver(*parser.main())
        solution, eps, has_invert, unity_check = solver.main()
        self._show_result(solution, eps, has_invert, unity_check)




gui = GUI()


