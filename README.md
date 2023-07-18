# Function_Plotter

## Description

This is a simple function plotter that can plot any valid functions in one variable. The GUI is written in PySide2 and the plotting is done using matplotlib. The user can enter the function in the top text box and indicate the range of the x variable in the below text boxes. The program will then plot the function in the specified range. The plot could look strange due to scaling issues. The program supports the following operations: +, -, *, /, ^. The program performs the operations in the PEMDAS order. Two consecutive positive or negative signs are reduced to a single positive sign while neigbouring heterogeneous signs are reduced to a negative sign.

After the user enters the function and the range, the program will do the following:

* First, the program validates the dunction using the **validate_state_machine()** function This function uses a state machine to validate the function entered by the user. It returns a list of tokens and another list of signs. The tokens array contains the tokens in the function if the function is valid; otherwise, it returns a string: "Syntax Error". The FSM is shown below:

* Second, the program uses the **equation_solver()** function to solve the user function using the resulting tokens and signs from the previous step. It orders the operations in the PEMDAS order before iterating through the tokens multiplying each token by its sign. Any division by zero substitutes the corresponding y value with nan. The function only returns a list of y values.
* Finally, the program plots the function using the **plot_button_clicked()** function. It uses the resulting y values from the previous step and plots them against the x values in the specified range using matplotlib.

## Running the program

Run the program by running the app.py file:

```bash
python app.py
```

## Snapshots




