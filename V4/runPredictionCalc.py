"""
Author - Matthew Hughes
Initial Comment Date - 27/02/2022

Description:    Generates a new instance of the savings and investment prediction 
                calculator.

"""

# Load the top level dependencies of the calculator.
from totalSavInvPredictionCalc import Ui_TabWidget
from PyQt5 import QtWidgets
conda list -e > requirements.txt
# Generate an instance of the savings and investment calculator app.
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)    
    ui = Ui_TabWidget()
    TabWidget = QtWidgets.QTabWidget()
    ui.setupUi(TabWidget)
    ui.show()
    sys.exit(app.exec_())
