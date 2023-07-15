import numpy as np
import math
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import re

from PySide2.QtCore import QSize, Qt
from PySide2.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QVBoxLayout, QWidget, QHBoxLayout, QLabel, QGridLayout, QMessageBox

app = QApplication([])

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Function Plotter")
        self.setFixedSize(QSize(800, 650))
        # A widget for entering the user function
        self.equation_text = QLineEdit("x^2") # default function
        self.equation_text.setPlaceholderText("Enter your equation here")
        self.equation_text.setAlignment(Qt.AlignCenter)

        # A button to plot the function when the user is ready
        self.button = QPushButton("Plot")
        self.button.clicked.connect(self.plot_button_clicked)

        root_layout = QVBoxLayout()

        # function text entry and plot button are laid out horizontally
        eq_layout = QHBoxLayout()
        eq_layout.addWidget(self.equation_text)
        eq_layout.addWidget(self.button)
        # function entry layout is added to the vertical root layout 
        root_layout.addLayout(eq_layout)

        # x range entry
        self.min_x = QLineEdit("-10") # default minimum x
        self.min_x.setAlignment(Qt.AlignCenter)
        self.min_x.setFixedWidth(100)
        self.max_x = QLineEdit("10") # default maximum x
        self.max_x.setFixedWidth(100)
        self.max_x.setAlignment(Qt.AlignCenter)
        left_angle_bracket = QLabel("<")
        left_angle_bracket.setFixedSize(QSize(10, 10))
        right_angle_bracket = QLabel("<")
        right_angle_bracket.setFixedSize(QSize(10, 10))
        x_label = QLabel("x")
        x_label.setFixedSize(QSize(10, 10))

        # x range entry is laid out horizontally
        x_layout = QHBoxLayout()
        x_layout.addWidget(self.min_x)
        x_layout.addWidget(left_angle_bracket)
        x_layout.addWidget(x_label)
        x_layout.addWidget(right_angle_bracket)
        x_layout.addWidget(self.max_x)
        x_layout.setSpacing(0)
        # x range entry layout is added to the vertical root layout
        root_layout.addLayout(x_layout)

        # canvas view to display the plot
        fig = Figure(figsize=(7, 5), dpi=75)
        ax = fig.add_subplot(111)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        # preparing the canvas with a default plot of x^2
        x = np.linspace(-10, 10, 100) # generate 100 x values between -10 and 10
        y = self.equation_solver(["x", "^", "2"], [1, 1, 1], x) # generate 100 y values for x^2
        ax.grid() # add grid lines
        ax.plot(x, y) # plot the function
        # add the canvas to the root layout
        self.canvas = FigureCanvas(fig)
        root_layout.addWidget(self.canvas)

        container = QWidget()
        container.setLayout(root_layout)
        self.setCentralWidget(container)
    
    # function responsible for plotting the user function
    def plot_button_clicked(self):
        equation = self.equation_text.text()
        min_x = self.min_x.text()
        max_x = self.max_x.text()

        if equation == "":
            self.user_message("Please enter a function to plot!")
            return
        if min_x == "" or max_x == "":
            self.user_message("Please enter a valid range!")
            return
        try:
            float(min_x)
            float(max_x)
        except ValueError:
            self.user_message("The range must be a number!")
            return
        if float(min_x) >= float(max_x):
            self.user_message("Max x must be greater than min x!")
            return
        terms, signs = self.validate_state_machine(equation)
        if terms == "Syntax error":
            self.user_message("Syntax error!")
            return

        sample_size = (float(max_x) - float(min_x))/((float(max_x) - float(min_x))*100)
        x = np.arange(float(min_x), float(max_x), sample_size)
        y = self.equation_solver(terms, signs, x)
        if y == -1:
            return
        fig = Figure(figsize=(7, 5), dpi=75)
        ax = fig.add_subplot(111)
        # max_range = max((float(max_x)), y[-1])
        # max_range = max(max_range, y[0])
        # min_range = min((float(min_x)), y[0])
        # min_range = min(min_range, y[-1])
        # ax.set_xlim([min_range, max_range])
        # ax.set_ylim([min_range, max_range])
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.grid()
        ax.plot(x, y)       
        self.layout().itemAt(0).widget().layout().itemAt(2).widget().deleteLater()
        canvas = FigureCanvas(fig)
        self.layout().itemAt(0).widget().layout().addWidget(canvas)
        canvas.draw()
    
    # function responsible for solving the user function and generating y values
    def equation_solver(self, terms, signs, x_values):
        y = [] # list of y values
        order = [] # list of operators in the order of operations
        
        # exponentiation is done first and is therefore added to the list first
        for i in range(len(terms)): 
            if terms[i] == '^':
                order.append(i)
        # multiplication and division are done second and are therefore added to the list second
        for i in range(len(terms)): 
            if terms[i] == '*' or terms[i] == '/':
                order.append(i)
        # addition and subtraction are done last and are therefore added to the list last
        for i in range(len(terms)): 
            if terms[i] == '+' or terms[i] == '-':
                order.append(i)
        
        # the order list is modified to account for the fact that the list will be modified 
        # since calculated terms will be popped from the list and the list will be shift accordingly 
        shifts = np.zeros(len(order))
        for i in range(len(order)):
            for j in range(i):
                if order[j] < order[i]:
                    # for every operator before the current operator, the index of the current operator will be shifted by 2 
                    shifts[i] += 2 
        order = [int(x - y) for x, y in zip(order, shifts)]

        for i in x_values:
            zero_division = False # flag to check for division by zero
            temp = terms.copy() # temporary list to be modified
            for j in range(len(terms)):
                if temp[j] == 'x': 
                    # replace x with the current x value multiplied by the sign of the term
                    temp[j] = i * signs[j]
                else:
                    try:
                        # replace the term with itself multiplied by the corresponding sign
                        temp[j] = float(temp[j]) * signs[j]
                    except ValueError:
                        pass
            # solve the equation using the order of operations
            for op in order:
                if temp[op] == '^':
                    # save the result of the operation in the first term of the operation
                    temp[op-1] = float(temp[op-1]) ** float(temp[op+1])
                elif temp[op] == '*':
                    temp[op-1] = float(temp[op-1]) * float(temp[op+1])
                elif temp[op] == '/':
                    if temp[op+1] == 0: # check for division by zero
                        zero_division = True
                        break
                    temp[op-1] = float(temp[op-1]) / float(temp[op+1])
                elif temp[op] == '+':
                    temp[op-1] = float(temp[op-1]) + float(temp[op+1])
                elif temp[op] == '-':
                    temp[op-1] = float(temp[op-1]) - float(temp[op+1])
                # remove the operator and the second term of the operation from the list
                temp.pop(op)
                temp.pop(op)

            if zero_division:
                # if division by zero occurs, add a nan value to the list
                y.append(float('nan'))
            else:
                y.append(temp[0])
                
        
        return y
    
    # function responsible for validating the user function syntax 
    # and generating a list of terms and signs to be used in the equation solver
    def validate_state_machine(self, equation):
        # state machine to validate the syntax of the user function
        states = {
            0: {'-': 0, '+': 0, 'x': 2, 'num': 2},
            1: {'-': 1, '+': 1, 'x': 2, 'num': 2},
            2: {'-': 1, '+': 1, '^': 3, '*': 3, '/': 3},
            3: {'-': 1, '+': 1, 'x': 2, 'num': 2},
        }
        current_state = 0 # initial state
        equation = "".join(equation.split()) # remove all whitespaces
        terms = re.split(r'([-/+*^])', equation) # split the equation into terms and operators
        terms = [x for x in terms if x != ''] # remove empty strings
        signs = np.ones(len(terms)) # list of signs for each term
        i = 0
        length = len(terms)
        while i < length:
            term = terms[i]
            try:
                # check if the term is a number
                float(term)
                transition = 'num'
            except ValueError:
                # if the term is not a number, its transition is its value
                transition = term
            # check if the transition is valid
            if transition not in states[current_state]:
                return "Syntax error", -1

            if current_state == 0:
                # remove the term if it is a plus sign
                if term == '+':
                    terms.pop(i)
                    i -= 1
                # remove the negative sign and reverse the sign of the next term
                elif term == '-':
                    terms.pop(i)
                    signs[i] *= -1
                    i -= 1
            else:
                # a plus sign after or before a minus sign is equivalent to a minus sign
                if (terms[i] == '+' and terms[i-1] == '-') or (terms[i] == '-' and terms[i-1] == '+'):
                    terms[i] = '-'
                    terms.pop(i-1)
                    i -= 1
                # two minus signs or two plus signs are equivalent to a plus sign
                elif (terms[i] == '-' and terms[i-1] == '-') or (terms[i] == '+' and terms[i-1] == '+'):
                    terms[i] = '+'
                    terms.pop(i-1)
                    i -= 1
                # a minus sign after a multiplication, division or exponentiation sign is removed 
                # and the sign of the next term is reversed
                elif (terms[i-1] == '*' or terms[i-1] == '/' or terms[i-1] == '^') and terms[i] == '-':
                    terms.pop(i)
                    signs[i] *= -1
                    i -= 1
                # a plus sign after a multiplication, division or exponentiation sign is removed
                elif (terms[i-1] == '*' or terms[i-1] == '/' or terms[i-1] == '^') and terms[i] == '+':
                    terms.pop(i)
                    i -= 1
            # update the current state
            current_state = states[current_state][transition]
            # update the length of the list to account for the terms that were removed
            length = len(terms)
            i += 1

        return terms, signs

    # function responsible for displaying error messages
    def user_message(self, message):
        dialog = QMessageBox(self)
        dialog.setWindowTitle("Error")
        dialog.setText(message)    
        dialog.exec_()

window = MainWindow()

window.show()
app.exec_()