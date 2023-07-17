import pytest
from PySide2.QtWidgets import QApplication
from app import MainWindow

@pytest.fixture
def app_init(qtbot):
    test_app = MainWindow()
    qtbot.addWidget(test_app)
    return test_app

def test_dialog_when_no_function_entered(app_init, qtbot):
    app_init.equation_text.setText("")
    app_init.button.click()
    assert app_init.dialog.text() == "Please enter a function to plot!"

def test_dialog_when_invalid_function_entered(app_init, qtbot):
    app_init.equation_text.setText("x+*2")
    app_init.button.click()
    assert app_init.dialog.text() == "Syntax error!"

def test_dialog_when_no_x_range_entered(app_init, qtbot):
    app_init.min_x.setText("")
    app_init.max_x.setText("")
    app_init.button.click()
    assert app_init.dialog.text() == "Please enter a valid range!"

def test_dialog_when_invalid_x_range_entered(app_init, qtbot):
    app_init.min_x.setText("a")
    app_init.max_x.setText("b")
    app_init.button.click()
    assert app_init.dialog.text() == "The range must be a number!"

def test_dialog_when_x_range_is_reversed(app_init, qtbot):
    app_init.min_x.setText("10")
    app_init.max_x.setText("1")
    app_init.button.click()
    assert app_init.dialog.text() == "The range must be in ascending order!"




    
