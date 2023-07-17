import pytest
from PySide2.QtWidgets import QApplication
from app import MainWindow
import numpy as np

@pytest.fixture
def app_init(qtbot):
    test_app = MainWindow()
    qtbot.addWidget(test_app)
    return test_app

@pytest.fixture
def x():
    return np.linspace(-10, 10, 100)

def test_equation_solver_with_addition(x, app_init):
    y = x + x
    terms = ["x", "+", "x"]
    signs = [1, 1, 1, 1, 1, 1, 1]
    res_y = app_init.equation_solver(terms, signs, x)
    assert np.array_equal(y, res_y)

def test_function_validation_with_subtraction(x, app_init):
    y = -x - x
    terms = ["x", "-", "x"]
    signs = [-1, 1, 1, 1, 1, 1, 1]
    res_y = app_init.equation_solver(terms, signs, x)
    assert np.array_equal(y, res_y)

def test_function_validation_with_exponent(x, app_init):
    y = x**2
    terms = ["x", "^", "2"]
    signs = [1, 1, 1]
    res_y = app_init.equation_solver(terms, signs, x)
    assert np.array_equal(y, res_y)

def test_function_validation_with_negative_exponent(x, app_init):
    y = x**-2
    terms = ["x", "^", "2"]
    signs = [1, 1, -1, 1]
    res_y = app_init.equation_solver(terms, signs, x)
    assert np.array_equal(y, res_y)

def test_function_validation_with_multiplication(x, app_init):
    y = x**2 * -8 * x
    terms = ["x", "^", "2", "*", "8", "*", "x"]
    signs = [1, 1, 1, 1, -1, 1, 1, 1]
    res_y = app_init.equation_solver(terms, signs, x)
    assert np.array_equal(y, res_y)
    

def test_function_validation_with_division(x, app_init):
    y = x**2 / -8
    terms = ["x", "^", "2", "/", "8"]
    signs = [1, 1, 1, 1, -1, 1]
    res_y = app_init.equation_solver(terms, signs, x)
    assert np.array_equal(y, res_y)
