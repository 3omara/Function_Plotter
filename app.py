import numpy as np
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import re

from PySide2.QtCore import QSize, Qt
from PySide2.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QVBoxLayout, QWidget, QHBoxLayout, QLabel, QGridLayout

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

        container = QWidget()
        container.setLayout(root_layout)
        self.setCentralWidget(container)

    def plot_button_clicked(self):
        return
    
    def equation_solver(self, equation, x_values):
        y = []
        terms = re.split(r'([-/+*^])', equation)
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
                    

        print("order: ", order)

        for i in x_values:
            terms = re.split(r'([-/+*^])', equation)
            for j in range(len(terms)):
                if terms[j] == 'x':
                    terms[j] = i
            for op in order:
                if terms[op] == '^':
                    terms[op-1] = float(terms[op-1]) ** float(terms[op+1])
                elif terms[op] == '*':
                    terms[op-1] = float(terms[op-1]) * float(terms[op+1])
                elif terms[op] == '/':
                    terms[op-1] = float(terms[op-1]) / float(terms[op+1])
                elif terms[op] == '+':
                    terms[op-1] = float(terms[op-1]) + float(terms[op+1])
                elif terms[op] == '-':
                    terms[op-1] = float(terms[op-1]) - float(terms[op+1])
                terms.pop(op)
                terms.pop(op)
            print('i: {}, res: {}'.format(i, terms[0]))
            y.append(terms[0])
                
        
        return y
            
            

window = MainWindow()

window.show()
app.exec_()