# savingsAndInvestmentApp
An app to predict savings and investment growth, with visual layouts and plots as well as potential user-defined input for comparison.

This set of programs generates a GUI using PYQT5 which plots and tabulates predicted savings and investment values over time. User parameters can be input on the first three tabs, which may be saved or discarded as required.

![visuals](20220317_190556.gif)

The current version includes filtering to attempt to make sure user inputs are of the forms required for the app operation, and checks upon exit if the program registers unsaved changes across any of the user input parameters or tables.

The most recent version is V5, which includes extra inbuilt redundancies against loss or corruption of the default values files, and to the deletion of user defined and default directories, which previously would crash the program, and which corrects a logic error present in earlier versions which led to the user-contribution flag not properly being taken into account when determining the dates of savings contributions prior to reaching the user savings goal.

# This is a test to check branching functionality
