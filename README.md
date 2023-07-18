# Function_Plotter

## Description

This simple function plotter can plot any valid functions in one variable. The GUI is written in PySide2 and the plotting is done using matplotlib. The user can enter the function in the top text box and indicate the range of the x variable in the below text boxes. The program will then plot the function in the specified range. The plot could look strange due to scaling issues. The program supports the following operations: +, -, *, /, ^. The program performs the operations in the PEMDAS order. Two consecutive positive or negative signs are reduced to a single positive sign while neigbouring heterogeneous signs are reduced to a negative sign. The program has a scale check button used to adjust the scale of the plot. To illustrate, if this button is checked, the same ranges will be used for the y and x-axis of the plot ensuring the plot is to scale. While unchecked, the plot can look weird since the scale of the y-axis is different from that of the x-axis.    

After the user enters the function and the range, the program will do the following:

* First, the program validates the dunction using the **validate_state_machine()** function This function uses a state machine to validate the function entered by the user. It returns a list of tokens and another list of signs. The tokens array contains the tokens in the function if the function is valid; otherwise, it returns a string: "Syntax Error". The FSM is shown below:
![ISM drawio](https://github.com/3omara/Function_Plotter/assets/61950995/6fdd0c51-2296-4d2a-976e-598a92c4a34e)

* Second, the program uses the **equation_solver()** function to solve the user function using the resulting tokens and signs from the previous step. It orders the operations in the PEMDAS order before iterating through the tokens multiplying each token by its sign. Any division by zero substitutes the corresponding y value with nan. The function only returns a list of y values.
* Finally, the program plots the function using the **plot_button_clicked()** function. It uses the resulting y values from the previous step and plots them against the x values in the specified range using matplotlib.

## Running the program

Run the program by running the app.py file:

```bash
python app.py
```

## Snapshots

Default plot:
![image](https://github.com/3omara/Function_Plotter/assets/61950995/281b550f-e0f9-45f1-b514-5d3df80b4eeb)


Dialog message when no function is entered:
![image](https://github.com/3omara/Function_Plotter/assets/61950995/c78e2fc9-53ec-4e07-a84c-2711a2cde8ff)


Dialog message when entering an invalid function:
![image](https://github.com/3omara/Function_Plotter/assets/61950995/b4c602ab-3d61-40cf-bde8-99d494fb4b33)


Dialog message when the range is not entered or only partially so:
![image](https://github.com/3omara/Function_Plotter/assets/61950995/58671b8e-a329-467e-92b1-d3d7604208ff)


Dialog message when the range is reversed:
![image](https://github.com/3omara/Function_Plotter/assets/61950995/4c55f7b1-52e2-487a-9b89-bcd8199035bd)


Successful examples:


![image](https://github.com/3omara/Function_Plotter/assets/61950995/f2fb0c92-e964-43ee-8818-dc923ec0e505)


![image](https://github.com/3omara/Function_Plotter/assets/61950995/d75f4d09-07f7-483b-86b7-3fe9babf6fb0)


![image](https://github.com/3omara/Function_Plotter/assets/61950995/7aa91f7e-9c62-4b3a-a73c-6a4d4e1e62e7)


Note: for this image, the scale button is checked. 
![image](https://github.com/3omara/Function_Plotter/assets/61950995/25aed72a-eea6-4719-836b-be76d23c59b1)





