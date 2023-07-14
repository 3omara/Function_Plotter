import numpy as np
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
        # text entry
        self.equation_text = QLineEdit("x^2")
        self.equation_text.setPlaceholderText("Enter your equation here")
        self.equation_text.setAlignment(Qt.AlignCenter)
        # button
        self.button = QPushButton("Plot")
        self.button.clicked.connect(self.plot_button_clicked)

        root_layout = QVBoxLayout()

        eq_layout = QHBoxLayout()
        eq_layout.addWidget(self.equation_text)
        eq_layout.addWidget(self.button)
        root_layout.addLayout(eq_layout)

        self.min_x = QLineEdit("-10")
        self.min_x.setAlignment(Qt.AlignCenter)
        self.min_x.setFixedWidth(100)
        self.max_x = QLineEdit("10")
        self.max_x.setFixedWidth(100)
        self.max_x.setAlignment(Qt.AlignCenter)
        left_angle_bracket = QLabel("<")
        left_angle_bracket.setFixedSize(QSize(10, 10))
        right_angle_bracket = QLabel("<")
        right_angle_bracket.setFixedSize(QSize(10, 10))
        x_label = QLabel("x")
        x_label.setFixedSize(QSize(10, 10))

        x_layout = QHBoxLayout()
        x_layout.addWidget(self.min_x)
        x_layout.addWidget(left_angle_bracket)
        x_layout.addWidget(x_label)
        x_layout.addWidget(right_angle_bracket)
        x_layout.addWidget(self.max_x)
        x_layout.setSpacing(0)
        root_layout.addLayout(x_layout)

        # canvas
        grid = QGridLayout()
        fig = Figure(figsize=(7, 5), dpi=100)
        ax = fig.add_subplot(111)
        # ax.set_xticks(np.arange(-10, 11, 1))
        # ax.set_yticks(np.arange(-5, 101, 5))
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        x = np.linspace(-10, 10, 100)
        y = self.equation_solver(["x", "^", "2"], [1, 1, 1], x)
        ax.grid()
        ax.plot(x, y)
        self.canvas = FigureCanvas(fig)
        grid.addWidget(self.canvas, 0, 0)
        root_layout.addWidget(self.canvas)

        container = QWidget()
        container.setLayout(root_layout)
        self.setCentralWidget(container)
    
    def plot_button_clicked(self):
        equation = self.equation_text.text()
        terms, signs = self.validate_state_machine(equation)
        if terms == "Syntax error":
            self.user_message("Syntax error")
            return
        min_x = self.min_x.text()
        max_x = self.max_x.text()
        sample_size = (int(max_x) - int(min_x))*100
        x = np.linspace(int(min_x), int(max_x), sample_size)
        y = self.equation_solver(terms, signs, x)
        if y == -1:
            return
        fig = Figure(figsize=(7, 5), dpi=100)
        ax = fig.add_subplot(111)
        max_range2 = max((int(max_x)), y[-1])
        max_range1 = min((int(min_x)), y[0])
        ax.set_xlim([max_range1, max_range2])
        ax.set_ylim([max_range1, max_range2])
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.grid()
        ax.plot(x, y)       
        self.layout().itemAt(0).widget().layout().itemAt(2).widget().deleteLater()
        canvas = FigureCanvas(fig)
        self.layout().itemAt(0).widget().layout().addWidget(canvas)
        canvas.draw()

    
    def equation_solver(self, terms, signs, x_values):
        y = []
        print("signs: {}".format(signs))
        print("terms: {}".format(terms))
        order = []
        for i in range(len(terms)):
            if terms[i] == '^':
                order.append(i)
        for i in range(len(terms)):
            if terms[i] == '*' or terms[i] == '/':
                order.append(i)
        for i in range(len(terms)):
            if terms[i] == '+' or terms[i] == '-':
                order.append(i)
        
        shifts = np.zeros(len(order))
        for i in range(len(order)):
            for j in range(i):
                if order[j] < order[i]:
                    shifts[i] += 2
        order = [int(x - y) for x, y in zip(order, shifts)]
        print("order: {}".format(order))
        for i in x_values:
            temp = terms.copy()
            for j in range(len(terms)):
                if temp[j] == 'x':
                    temp[j] = i * signs[j]
                else:
                    try:
                        temp[j] = float(temp[j]) * signs[j]
                    except ValueError:
                        pass
            for op in order:
                if temp[op] == '^':
                    temp[op-1] = float(temp[op-1]) ** float(temp[op+1])
                elif temp[op] == '*':
                    temp[op-1] = float(temp[op-1]) * float(temp[op+1])
                elif temp[op] == '/':
                    temp[op-1] = float(temp[op-1]) / float(temp[op+1])
                elif temp[op] == '+':
                    temp[op-1] = float(temp[op-1]) + float(temp[op+1])
                elif temp[op] == '-':
                    temp[op-1] = float(temp[op-1]) - float(temp[op+1])
                temp.pop(op)
                temp.pop(op)
            # print('i: {}, res: {}'.format(i, temp[0]))
            y.append(temp[0])
                
        
        return y
    
    def validate_state_machine(self, equation):
        states = {
            0: {'-': 0, '+': 0, 'x': 2, 'num': 2},
            1: {'-': 1, '+': 1, 'x': 2, 'num': 2},
            2: {'-': 1, '+': 1, '^': 3, '*': 3, '/': 3},
            3: {'-': 1, '+': 1, 'x': 2, 'num': 2},
        }
        current_state = 0
        equation = "".join(equation.split())
        terms = re.split(r'([-/+*^])', equation)
        terms = [x for x in terms if x != '']
        signs = np.ones(len(terms))
        i = 0
        length = len(terms)
        while i < length:
            print("state: {}".format(current_state))
            term = terms[i]
            print("i: {}, term: {}".format(i, term))
            try:
                float(term)
                transition = 'num'
            except ValueError:
                transition = term
            if transition not in states[current_state]:
                print(terms)
                print("transition: {}".format(transition))
                return "Syntax error", -1
            print("terms: {}".format(terms))
            if current_state == 0:
                if term == '+':
                    terms.pop(i)
                    i -= 1
                elif term == '-':
                    terms.pop(i)
                    signs[i] *= -1
                    i -= 1
            else:
                if (terms[i] == '+' and terms[i-1] == '-') or (terms[i] == '-' and terms[i-1] == '+'):
                    terms[i] = '-'
                    terms.pop(i-1)
                    i -= 1
                elif (terms[i] == '-' and terms[i-1] == '-') or (terms[i] == '+' and terms[i-1] == '+'):
                    terms[i] = '+'
                    terms.pop(i-1)
                    i -= 1
                elif (terms[i-1] == '*' or terms[i-1] == '/' or terms[i-1] == '^') and terms[i] == '-':
                    terms.pop(i)
                    signs[i] *= -1
                    i -= 1
                elif (terms[i-1] == '*' or terms[i-1] == '/' or terms[i-1] == '^') and terms[i] == '+':
                    terms.pop(i)
                    i -= 1
            current_state = states[current_state][transition]
            length = len(terms)
            i += 1

        return terms, signs


        

    
    def user_message(self, message):
        dialog = QMessageBox(self)
        dialog.setWindowTitle("Error")
        dialog.setText(message)    
        button = dialog.exec_()


        

            
            

window = MainWindow()

window.show()
app.exec_()