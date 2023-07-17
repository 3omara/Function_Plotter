import pytest
from PySide2.QtWidgets import QApplication
from app import MainWindow
import numpy as np

@pytest.fixture
def app_init(qtbot):
    test_app = MainWindow()
    qtbot.addWidget(test_app)
    return test_app

def test_function_validation_with_addition(app_init):
    terms = ["x", "+", "x"]
    signs = [1, 1, 1, 1, 1, 1, 1]
    res_terms, res_signs = app_init.validate_state_machine("++x +++x")
    assert np.array_equal(terms, res_terms) and np.array_equal(signs, res_signs)

def test_function_validation_with_subtraction(app_init):
    terms = ["x", "-", "x"]
    signs = [-1, 1, 1, 1, 1, 1, 1]
    res_terms, res_signs = app_init.validate_state_machine("-x ---+x")
    assert np.array_equal(terms, res_terms) and np.array_equal(signs, res_signs)

def test_function_validation_with_exponent(app_init):
    terms = ["x", "^", "2"]
    signs = [1, 1, 1]
    res_terms, res_signs = app_init.validate_state_machine("x^2")
    assert np.array_equal(terms, res_terms) and np.array_equal(signs, res_signs)

def test_function_validation_with_negative_exponent(app_init):
    terms = ["x", "^", "2"]
    signs = [1, 1, -1, 1]
    res_terms, res_signs = app_init.validate_state_machine("x^-2")
    assert np.array_equal(terms, res_terms) and np.array_equal(signs, res_signs)

def test_function_validation_with_multiplication(app_init):
    terms = ["x", "^", "2", "*", "8", "*", "x"]
    signs = [1, 1, 1, 1, -1, 1, 1, 1]
    res_terms, res_signs = app_init.validate_state_machine("x^2 * -8 * x")
    assert np.array_equal(terms, res_terms) and np.array_equal(signs, res_signs)

def test_function_validation_with_division(app_init):
    terms = ["x", "^", "2", "/", "8", "/", "x"]
    signs = [1, 1, 1, 1, -1, 1, 1, 1]
    res_terms, res_signs = app_init.validate_state_machine("x^2 / -8 / x")
    assert np.array_equal(terms, res_terms) and np.array_equal(signs, res_signs)