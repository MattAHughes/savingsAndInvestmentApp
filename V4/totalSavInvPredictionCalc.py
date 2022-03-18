"""
Author - Matthew Hughes
Initial Comment Date - 27/02/2022

Description:    Specifies the parameters of the app that are loaded on the 
                instantiation of a new version of the app.

"""
# Import the pyqt core modules. Note key functions are stored in a sub-module for brevity.
from PyQt5 import QtChart, QtWidgets
from PyQt5.QtWidgets import QTableView, QMessageBox, QTabWidget, QComboBox
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph
import totSavPredCalcFuncs
import sys

class Ui_TabWidget(QTabWidget):
    
    # Define a custom close event for if user changes took place.
    def closeEvent(self, event):
        
        # Create closing flags
        totSavPredCalcFuncs.relevantFunctions.defineCloseFlags(self)   
        
        # Test for unsaved user changes
        if self.test_overall_dates.equals(self.overall_dates) and self.test_df_inv.equals(self.df_inv) and self.final_year_array_flag == 1 and self.final_month_array_flag == 1 and self.checking_par_flag == 1:
            # A little rough, but send the message close signal to the system in the case that nothing has changed.
            reply = QMessageBox.Close
            if reply == QMessageBox.Close:
                event.accept()
        else:
            self.messagebox = QMessageBox()
            
            # Create a question box.
            reply = self.messagebox.question(self, 'Save Changes?', 'Would you like to save your changes and exit, close the program, or cancel back to the application?', QMessageBox.Save | QMessageBox.Cancel | QMessageBox.Close)
            
            # Use the question response to determine program action.
            if reply == self.messagebox.Save:
                self.messagebox.setIcon(self.messagebox.Information)
                totSavPredCalcFuncs.relevantFunctions.saveUserParams(self)
                event.accept()
            elif reply == self.messagebox.Close:
                event.accept()
            else:
                event.ignore()
          
    # Define the core layout of the GUI.
    def setupUi(self, TabWidget):

               
        # Load the default and user defined values. Note these functions are separated for ease of speed benchmarking.
        totSavPredCalcFuncs.relevantFunctions.loadDefaultValues(self)
        
        # Conditionally run calculations or load defaults in order of preference
        try:
            # First try both being loadable files
            totSavPredCalcFuncs.relevantFunctions.savGrowthWithLoads(self)
            # Calculate Investment predictions
            totSavPredCalcFuncs.relevantFunctions.invCalcWithLoads(self)
            # Generate total values
            totSavPredCalcFuncs.relevantFunctions.genTotVals(self)

        except:
            try:
                # Next try only savings growth being loadable
                totSavPredCalcFuncs.relevantFunctions.savGrowthWithLoads(self)
                # Calculate Investment predictions
                totSavPredCalcFuncs.relevantFunctions.invCalc(self)
                # Generate total values
                totSavPredCalcFuncs.relevantFunctions.genTotVals(self)

            except:
                # Finally neither could be loaded, so recalculate the tables
                # Create a dataframe of dates to be calculated on
                totSavPredCalcFuncs.relevantFunctions.dateRange(self)
                
                # Create the inital values calculation
                totSavPredCalcFuncs.relevantFunctions.firstSavingsGrowth(self)
                
                # Perform the second values calculation
                totSavPredCalcFuncs.relevantFunctions.secSavingsGrowth(self)
                
                # Calculate Investment predictions
                totSavPredCalcFuncs.relevantFunctions.invCalc(self)
                
                # Generate total values
                totSavPredCalcFuncs.relevantFunctions.genTotVals(self)
        
        # Set an initial regular expression that can be used to restrict entries
        # in a field to date values
        self.date_regexp = QtCore.QRegExp("(0[1-9]|[12][0-9]|3[01])/(0[1-9]|[1][0-2])/(19[0-9][0-9]|20[0-9][0-9])")
        
        # Create the inital tab widget.
        self.setObjectName("TabWidget")
        self.resize(1135, 959)
        self.setMinimumSize(QtCore.QSize(715, 0))
        self.setAutoFillBackground(False)
        
        # Set the general background colour.
        self.setStyleSheet("background-color: rgb(210, 219, 240);")
        
        
        # Create the key assumptions tab and its layout.
        self.key_assumptions = QtWidgets.QWidget()
        self.key_assumptions.setObjectName("key_assumptions")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.key_assumptions)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.key_derived_layout = QtWidgets.QVBoxLayout()
        self.key_derived_layout.setSpacing(0)
        
        # KEY ASSUMPTIONS TAB:
        # Create a container for the overall derived objects frrom the assumptions.
        self.key_derived_layout.setObjectName("key_derived_layout")
        self.key_plot_layout = QtWidgets.QVBoxLayout()
        
        # Create a layout for the plot of savings etc in the derived layout.
        self.key_plot_layout.setObjectName("key_plot_layout")
        
        # Add a widget for holding an interactive plot
        totSavPredCalcFuncs.relevantFunctions.parTabPlot(self)
        
        # Add a formula widget.
        self.key_formula_widget = QtWidgets.QWidget(self.key_assumptions)
        self.key_formula_widget.setStyleSheet("background-color: rgb(109, 104, 117);")
        self.key_formula_widget.setObjectName("key_formula_widget")
        self.verticalLayout_24 = QtWidgets.QVBoxLayout(self.key_formula_widget)
        self.verticalLayout_24.setObjectName("verticalLayout_24")
        self.key_formula_layout = QtWidgets.QVBoxLayout()
        self.key_formula_layout.setObjectName("key_formula_layout")
        self.verticalLayout_25 = QtWidgets.QVBoxLayout()
        self.verticalLayout_25.setObjectName("verticalLayout_25")
        
        # Adds and customises savings formula label.
        self.sav_formula_label = QtWidgets.QLabel(self.key_formula_widget)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(109, 104, 117))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(109, 104, 117))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(109, 104, 117))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(109, 104, 117))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(109, 104, 117))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(109, 104, 117))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(109, 104, 117))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(109, 104, 117))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(109, 104, 117))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.sav_formula_label.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.sav_formula_label.setFont(font)
        self.sav_formula_label.setObjectName("sav_formula_label")
        self.verticalLayout_25.addWidget(self.sav_formula_label)
        
        # Adds and customised the savings formula
        self.sav_formula = QtWidgets.QLabel(self.key_formula_widget)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(109, 104, 117))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(109, 104, 117))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(109, 104, 117))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(109, 104, 117))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(109, 104, 117))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(109, 104, 117))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(109, 104, 117))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(109, 104, 117))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(109, 104, 117))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.sav_formula.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Palatino Linotype")
        font.setPointSize(12)
        self.sav_formula.setFont(font)
        self.sav_formula.setObjectName("sav_formula")
        self.verticalLayout_25.addWidget(self.sav_formula)
        
        # Add and customise the investment formula label
        self.inv_formula_label = QtWidgets.QLabel(self.key_formula_widget)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(109, 104, 117))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(109, 104, 117))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(109, 104, 117))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(109, 104, 117))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(109, 104, 117))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(109, 104, 117))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(109, 104, 117))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(109, 104, 117))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(109, 104, 117))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.inv_formula_label.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.inv_formula_label.setFont(font)
        self.inv_formula_label.setObjectName("inv_formula_label")
        self.verticalLayout_25.addWidget(self.inv_formula_label)
        
        # Add and customise the investment formula
        self.inv_formula = QtWidgets.QLabel(self.key_formula_widget)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(109, 104, 117))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(109, 104, 117))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(109, 104, 117))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(109, 104, 117))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(109, 104, 117))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(109, 104, 117))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(109, 104, 117))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(109, 104, 117))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(109, 104, 117))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.inv_formula.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Palatino Linotype")
        font.setPointSize(12)
        self.inv_formula.setFont(font)
        self.inv_formula.setObjectName("inv_formula")
        self.verticalLayout_25.addWidget(self.inv_formula)
        self.key_formula_layout.addLayout(self.verticalLayout_25)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_26 = QtWidgets.QVBoxLayout()
        self.verticalLayout_26.setObjectName("verticalLayout_26")
        
        # Add the save button and customise it
        self.key_save_push_button = QtWidgets.QPushButton(self.key_formula_widget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.key_save_push_button.setFont(font)
        self.key_save_push_button.setStyleSheet("QPushButton {\n"
"color: #333;\n"
"border: 2px solid #555;\n"
"border-radius: 20px;\n"
"border-style: outset;\n"
"background: qradialgradient(\n"
"cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
"radius: 1.35, stop: 0 #fff, stop: 1 #888\n"
");\n"
"padding: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"background: qradialgradient(\n"
"cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
"radius: 1.35, stop: 0 #fff, stop: 1 #bbb\n"
");\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"border-style: inset;\n"
"background: qradialgradient(\n"
"cx: 0.4, cy: -0.1, fx: 0.4, fy: -0.1,\n"
"radius: 1.35, stop: 0 #fff, stop: 1 #ddd\n"
");\n"
"}")
        self.key_save_push_button.setIconSize(QtCore.QSize(16, 16))
        self.key_save_push_button.setObjectName("key_save_push_button")
        self.verticalLayout_26.addWidget(self.key_save_push_button)
        self.horizontalLayout_3.addLayout(self.verticalLayout_26)
        self.verticalLayout_27 = QtWidgets.QVBoxLayout()
        self.verticalLayout_27.setObjectName("verticalLayout_27")
        
        # Add and customise the re-run calculations push button
        self.key_rerun_push_button = QtWidgets.QPushButton(self.key_formula_widget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.key_rerun_push_button.setFont(font)
        self.key_rerun_push_button.setStyleSheet("QPushButton {\n"
"color: #333;\n"
"border: 2px solid #555;\n"
"border-radius: 20px;\n"
"border-style: outset;\n"
"background: qradialgradient(\n"
"cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
"radius: 1.35, stop: 0 #fff, stop: 1 #888\n"
");\n"
"padding: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"background: qradialgradient(\n"
"cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
"radius: 1.35, stop: 0 #fff, stop: 1 #bbb\n"
");\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"border-style: inset;\n"
"background: qradialgradient(\n"
"cx: 0.4, cy: -0.1, fx: 0.4, fy: -0.1,\n"
"radius: 1.35, stop: 0 #fff, stop: 1 #ddd\n"
");\n"
"}")
        self.key_rerun_push_button.setIconSize(QtCore.QSize(16, 16))
        self.key_rerun_push_button.setObjectName("key_rerun_push_button")
        self.verticalLayout_27.addWidget(self.key_rerun_push_button)
        self.horizontalLayout_3.addLayout(self.verticalLayout_27)
        self.key_formula_layout.addLayout(self.horizontalLayout_3)
        self.key_formula_layout.setStretch(0, 3)
        self.key_formula_layout.setStretch(1, 1)
        self.verticalLayout_24.addLayout(self.key_formula_layout)
        self.key_derived_layout.addWidget(self.key_formula_widget)
        self.key_derived_layout.setStretch(0, 5)
        self.key_derived_layout.setStretch(1, 3)
        self.gridLayout_7.addLayout(self.key_derived_layout, 0, 2, 1, 1)
        
        # Set a space for background colour for the user entry of data.
        self.key_entered_col_widget = QtWidgets.QWidget(self.key_assumptions)
        self.key_entered_col_widget.setStyleSheet("")
        self.key_entered_col_widget.setObjectName("key_entered_col_widget")
        self.verticalLayout_23 = QtWidgets.QVBoxLayout(self.key_entered_col_widget)
        self.verticalLayout_23.setContentsMargins(-1, 0, 3, 0)
        self.verticalLayout_23.setSpacing(2)
        self.verticalLayout_23.setObjectName("verticalLayout_23")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.heading_label = QtWidgets.QLabel(self.key_entered_col_widget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.heading_label.setFont(font)
        self.heading_label.setObjectName("heading_label")
        self.verticalLayout_3.addWidget(self.heading_label)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        
        # Set up the various elements of the general user entered parameters box.
        self.gen_out_border_widget = QtWidgets.QWidget(self.key_entered_col_widget)
        self.gen_out_border_widget.setStyleSheet("background-color: rgb(58, 58, 58);")
        self.gen_out_border_widget.setObjectName("gen_out_border_widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.gen_out_border_widget)
        self.verticalLayout_2.setContentsMargins(1, 1, 1, 1)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gen_inner_border_widet = QtWidgets.QWidget(self.gen_out_border_widget)
        self.gen_inner_border_widet.setStyleSheet("background-color: rgb(163, 247, 181);")
        self.gen_inner_border_widet.setObjectName("gen_inner_border_widet")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.gen_inner_border_widet)
        self.verticalLayout_6.setContentsMargins(3, 1, 4, 4)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label = QtWidgets.QLabel(self.gen_inner_border_widet)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout_5.addWidget(self.label)
        spacerItem1 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_5.addItem(spacerItem1)
        self.verticalLayout_6.addLayout(self.verticalLayout_5)
        self.key_gen_layout = QtWidgets.QHBoxLayout()
        self.key_gen_layout.setObjectName("key_gen_layout")
        self.key_gen_label_layout = QtWidgets.QVBoxLayout()
        self.key_gen_label_layout.setObjectName("key_gen_label_layout")
        self.key_end_yr_label = QtWidgets.QLabel(self.gen_inner_border_widet)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.key_end_yr_label.setFont(font)
        self.key_end_yr_label.setFrameShape(QtWidgets.QFrame.HLine)
        self.key_end_yr_label.setFrameShadow(QtWidgets.QFrame.Raised)
        self.key_end_yr_label.setObjectName("key_end_yr_label")
        self.key_gen_label_layout.addWidget(self.key_end_yr_label)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.key_gen_label_layout.addItem(spacerItem2)
        self.key_op_first_contrib_label = QtWidgets.QLabel(self.gen_inner_border_widet)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.key_op_first_contrib_label.setFont(font)
        self.key_op_first_contrib_label.setFrameShape(QtWidgets.QFrame.HLine)
        self.key_op_first_contrib_label.setFrameShadow(QtWidgets.QFrame.Raised)
        self.key_op_first_contrib_label.setObjectName("key_op_first_contrib_label")
        self.key_gen_label_layout.addWidget(self.key_op_first_contrib_label)
        spacerItemx = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.key_gen_label_layout.addItem(spacerItemx)
        self.key_op_contrib_freq_label = QtWidgets.QLabel(self.gen_inner_border_widet)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.key_op_contrib_freq_label.setFont(font)
        self.key_op_contrib_freq_label.setFrameShape(QtWidgets.QFrame.HLine)
        self.key_op_contrib_freq_label.setFrameShadow(QtWidgets.QFrame.Raised)
        self.key_op_contrib_freq_label.setObjectName("key_op_contrib_freq_label")
        self.key_gen_label_layout.addWidget(self.key_op_contrib_freq_label)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.key_gen_label_layout.addItem(spacerItem3)
        self.key_gen_layout.addLayout(self.key_gen_label_layout)
        self.key_gen_lineEdit_layout = QtWidgets.QVBoxLayout()
        self.key_gen_lineEdit_layout.setObjectName("key_gen_lineEdit_layout")
        self.key_end_yr_lineEdit = QtWidgets.QLineEdit(self.gen_inner_border_widet)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.key_end_yr_lineEdit.sizePolicy().hasHeightForWidth())
        self.key_end_yr_lineEdit.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.key_end_yr_lineEdit.setFont(font)
        self.key_end_yr_lineEdit.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.key_end_yr_lineEdit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.key_end_yr_lineEdit.setObjectName("key_end_yr_lineEdit")
        self.key_end_yr_lineEdit.setValidator(QtGui.QIntValidator())
        self.key_gen_lineEdit_layout.addWidget(self.key_end_yr_lineEdit)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.key_gen_lineEdit_layout.addItem(spacerItem4)
        self.key_op_first_contrib_date_lineEdit = QtWidgets.QLineEdit(self.gen_inner_border_widet)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.key_op_first_contrib_date_lineEdit.sizePolicy().hasHeightForWidth())
        self.key_op_first_contrib_date_lineEdit.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.key_op_first_contrib_date_lineEdit.setFont(font)
        self.key_op_first_contrib_date_lineEdit.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.key_op_first_contrib_date_lineEdit.setObjectName("key_op_first_contrib_date_lineEdit")
        self.key_op_first_contrib_date_lineEdit.setValidator(QtGui.QRegExpValidator(self.date_regexp))
        self.key_gen_lineEdit_layout.addWidget(self.key_op_first_contrib_date_lineEdit)
        spacerItemy = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.key_gen_lineEdit_layout.addItem(spacerItemy)
        self.key_op_contrib_freq_dropdown = QComboBox(self.gen_inner_border_widet)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.key_op_contrib_freq_dropdown.sizePolicy().hasHeightForWidth())
        self.key_op_contrib_freq_dropdown.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.key_op_contrib_freq_dropdown.setFont(font)
        self.key_op_contrib_freq_dropdown.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.key_op_contrib_freq_dropdown.setObjectName("key_op_contrib_freq_dropdown")
        self.key_op_contrib_freq_dropdown.addItems(['Weekly', 'Fortnightly', 'Monthly'])
        self.key_op_contrib_freq_dropdown.setCurrentIndex(-1)
        self.key_gen_lineEdit_layout.addWidget(self.key_op_contrib_freq_dropdown)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.key_gen_lineEdit_layout.addItem(spacerItem5)
        self.key_gen_layout.addLayout(self.key_gen_lineEdit_layout)
        self.verticalLayout_6.addLayout(self.key_gen_layout)
        self.verticalLayout_2.addWidget(self.gen_inner_border_widet)
        self.verticalLayout_3.addWidget(self.gen_out_border_widget)
        self.verticalLayout_23.addLayout(self.verticalLayout_3)
        
        # Setup box for user entered savings parameters.
        self.outer_sav_border_widget = QtWidgets.QWidget(self.key_entered_col_widget)
        self.outer_sav_border_widget.setStyleSheet("background-color: rgb(58, 58, 58);")
        self.outer_sav_border_widget.setObjectName("outer_sav_border_widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.outer_sav_border_widget)
        self.horizontalLayout.setContentsMargins(1, 1, 1, 1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.inner_sav_border_widget = QtWidgets.QWidget(self.outer_sav_border_widget)
        self.inner_sav_border_widget.setStyleSheet("background-color: rgb(163, 247, 181);")
        self.inner_sav_border_widget.setObjectName("inner_sav_border_widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.inner_sav_border_widget)
        self.verticalLayout.setContentsMargins(3, 1, 4, 4)
        self.verticalLayout.setObjectName("verticalLayout")
        self.key_sav_layout_2 = QtWidgets.QVBoxLayout()
        self.key_sav_layout_2.setObjectName("key_sav_layout_2")
        self.sav_par_text_layout_2 = QtWidgets.QVBoxLayout()
        self.sav_par_text_layout_2.setObjectName("sav_par_text_layout_2")
        spacerItem6 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.sav_par_text_layout_2.addItem(spacerItem6)
        self.sav_par_label_2 = QtWidgets.QLabel(self.inner_sav_border_widget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.sav_par_label_2.setFont(font)
        self.sav_par_label_2.setStyleSheet("border-bottom-color: rgb(0, 0, 0);")
        self.sav_par_label_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.sav_par_label_2.setObjectName("sav_par_label_2")
        self.sav_par_text_layout_2.addWidget(self.sav_par_label_2)
        self.key_sav_layout_2.addLayout(self.sav_par_text_layout_2)
        spacerItem7 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.key_sav_layout_2.addItem(spacerItem7)
        self.key_sav_ent_layout_2 = QtWidgets.QHBoxLayout()
        self.key_sav_ent_layout_2.setObjectName("key_sav_ent_layout_2")
        self.key_sav_ent_cat_layout_2 = QtWidgets.QVBoxLayout()
        self.key_sav_ent_cat_layout_2.setObjectName("key_sav_ent_cat_layout_2")
        self.key_sav_cont_label_2 = QtWidgets.QLabel(self.inner_sav_border_widget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.key_sav_cont_label_2.setFont(font)
        self.key_sav_cont_label_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.key_sav_cont_label_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.key_sav_cont_label_2.setObjectName("key_sav_cont_label_2")
        self.key_sav_ent_cat_layout_2.addWidget(self.key_sav_cont_label_2)
        spacerItem8 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.key_sav_ent_cat_layout_2.addItem(spacerItem8)
        self.key_sav_interest_rt_label_2 = QtWidgets.QLabel(self.inner_sav_border_widget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.key_sav_interest_rt_label_2.setFont(font)
        self.key_sav_interest_rt_label_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.key_sav_interest_rt_label_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.key_sav_interest_rt_label_2.setObjectName("key_sav_interest_rt_label_2")
        self.key_sav_ent_cat_layout_2.addWidget(self.key_sav_interest_rt_label_2)
        spacerItem9 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.key_sav_ent_cat_layout_2.addItem(spacerItem9)
        self.key_sav_goal_label_2 = QtWidgets.QLabel(self.inner_sav_border_widget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.key_sav_goal_label_2.setFont(font)
        self.key_sav_goal_label_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.key_sav_goal_label_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.key_sav_goal_label_2.setObjectName("key_sav_goal_label_2")
        self.key_sav_ent_cat_layout_2.addWidget(self.key_sav_goal_label_2)
        spacerItem10 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.key_sav_ent_cat_layout_2.addItem(spacerItem10)
        self.key_op_init_sav_label_2 = QtWidgets.QLabel(self.inner_sav_border_widget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.key_op_init_sav_label_2.setFont(font)
        self.key_op_init_sav_label_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.key_op_init_sav_label_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.key_op_init_sav_label_2.setObjectName("key_op_init_sav_label_2")
        self.key_sav_ent_cat_layout_2.addWidget(self.key_op_init_sav_label_2)
        spacerItem11 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.key_sav_ent_cat_layout_2.addItem(spacerItem11)
        self.key_op_pg_cont_label_2 = QtWidgets.QLabel(self.inner_sav_border_widget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.key_op_pg_cont_label_2.setFont(font)
        self.key_op_pg_cont_label_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.key_op_pg_cont_label_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.key_op_pg_cont_label_2.setObjectName("key_op_pg_cont_label_2")
        self.key_sav_ent_cat_layout_2.addWidget(self.key_op_pg_cont_label_2)
        spacerItem12 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.key_sav_ent_cat_layout_2.addItem(spacerItem12)
        self.key_sav_ent_layout_2.addLayout(self.key_sav_ent_cat_layout_2)
        self.key_sav_ent_val_layout_2 = QtWidgets.QVBoxLayout()
        self.key_sav_ent_val_layout_2.setObjectName("key_sav_ent_val_layout_2")
        self.key_sav_cont_lineEdit_2 = QtWidgets.QLineEdit(self.inner_sav_border_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.key_sav_cont_lineEdit_2.sizePolicy().hasHeightForWidth())
        self.key_sav_cont_lineEdit_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.key_sav_cont_lineEdit_2.setFont(font)
        self.key_sav_cont_lineEdit_2.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.key_sav_cont_lineEdit_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.key_sav_cont_lineEdit_2.setObjectName("key_sav_cont_lineEdit_2")
        self.key_sav_cont_lineEdit_2.setValidator(QtGui.QIntValidator())
        self.key_sav_ent_val_layout_2.addWidget(self.key_sav_cont_lineEdit_2)
        spacerItem13 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.key_sav_ent_val_layout_2.addItem(spacerItem13)
        self.key_sav_int_rt_lineEdit_2 = QtWidgets.QLineEdit(self.inner_sav_border_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.key_sav_int_rt_lineEdit_2.sizePolicy().hasHeightForWidth())
        self.key_sav_int_rt_lineEdit_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.key_sav_int_rt_lineEdit_2.setFont(font)
        self.key_sav_int_rt_lineEdit_2.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.key_sav_int_rt_lineEdit_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.key_sav_int_rt_lineEdit_2.setObjectName("key_sav_int_rt_lineEdit_2")
        self.key_sav_int_rt_lineEdit_2.setValidator(QtGui.QDoubleValidator())
        self.key_sav_ent_val_layout_2.addWidget(self.key_sav_int_rt_lineEdit_2)
        spacerItem14 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.key_sav_ent_val_layout_2.addItem(spacerItem14)
        self.key_sav_goal_lineEdit_2 = QtWidgets.QLineEdit(self.inner_sav_border_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.key_sav_goal_lineEdit_2.sizePolicy().hasHeightForWidth())
        self.key_sav_goal_lineEdit_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.key_sav_goal_lineEdit_2.setFont(font)
        self.key_sav_goal_lineEdit_2.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.key_sav_goal_lineEdit_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.key_sav_goal_lineEdit_2.setObjectName("key_sav_goal_lineEdit_2")
        self.key_sav_goal_lineEdit_2.setValidator(QtGui.QIntValidator())
        self.key_sav_ent_val_layout_2.addWidget(self.key_sav_goal_lineEdit_2)
        spacerItem15 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.key_sav_ent_val_layout_2.addItem(spacerItem15)
        self.ke_init_sav_lineEdit_2 = QtWidgets.QLineEdit(self.inner_sav_border_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ke_init_sav_lineEdit_2.sizePolicy().hasHeightForWidth())
        self.ke_init_sav_lineEdit_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.ke_init_sav_lineEdit_2.setFont(font)
        self.ke_init_sav_lineEdit_2.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.ke_init_sav_lineEdit_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.ke_init_sav_lineEdit_2.setObjectName("ke_init_sav_lineEdit_2")
        self.ke_init_sav_lineEdit_2.setValidator(QtGui.QIntValidator())
        self.key_sav_ent_val_layout_2.addWidget(self.ke_init_sav_lineEdit_2)
        spacerItem16 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.key_sav_ent_val_layout_2.addItem(spacerItem16)
        self.key_cust_goal_cont_lineEdit_2 = QtWidgets.QLineEdit(self.inner_sav_border_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.key_cust_goal_cont_lineEdit_2.sizePolicy().hasHeightForWidth())
        self.key_cust_goal_cont_lineEdit_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.key_cust_goal_cont_lineEdit_2.setFont(font)
        self.key_cust_goal_cont_lineEdit_2.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.key_cust_goal_cont_lineEdit_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.key_cust_goal_cont_lineEdit_2.setObjectName("key_cust_goal_cont_lineEdit_2")
        self.key_cust_goal_cont_lineEdit_2.setValidator(QtGui.QIntValidator())
        self.key_sav_ent_val_layout_2.addWidget(self.key_cust_goal_cont_lineEdit_2)
        spacerItem17 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.key_sav_ent_val_layout_2.addItem(spacerItem17)
        self.key_sav_ent_layout_2.addLayout(self.key_sav_ent_val_layout_2)
        self.key_sav_layout_2.addLayout(self.key_sav_ent_layout_2)
        self.key_sav_layout_2.setStretch(2, 30)
        self.verticalLayout.addLayout(self.key_sav_layout_2)
        self.horizontalLayout.addWidget(self.inner_sav_border_widget)
        self.verticalLayout_23.addWidget(self.outer_sav_border_widget)
        spacerItem18 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_23.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_23.addItem(spacerItem19)
        
        # Setup box for entry of user investment parameters.
        self.inv_outer_border_widget = QtWidgets.QWidget(self.key_entered_col_widget)
        self.inv_outer_border_widget.setStyleSheet("background-color: rgb(58, 58, 58);")
        self.inv_outer_border_widget.setObjectName("inv_outer_border_widget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.inv_outer_border_widget)
        self.verticalLayout_4.setContentsMargins(1, 1, 1, 1)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.inv_inner_border_widget = QtWidgets.QWidget(self.inv_outer_border_widget)
        self.inv_inner_border_widget.setStyleSheet("background-color: rgb(163, 247, 181);")
        self.inv_inner_border_widget.setObjectName("inv_inner_border_widget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.inv_inner_border_widget)
        self.horizontalLayout_2.setContentsMargins(3, 20, 4, 4)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.key_inv_layout = QtWidgets.QVBoxLayout()
        self.key_inv_layout.setObjectName("key_inv_layout")
        self.key_inv_layout_redundant = QtWidgets.QVBoxLayout()
        self.key_inv_layout_redundant.setObjectName("key_inv_layout_redundant")
        self.inv_par_text_layout = QtWidgets.QVBoxLayout()
        self.inv_par_text_layout.setObjectName("inv_par_text_layout")
        self.inv_par_label = QtWidgets.QLabel(self.inv_inner_border_widget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.inv_par_label.setFont(font)
        self.inv_par_label.setObjectName("inv_par_label")
        self.inv_par_text_layout.addWidget(self.inv_par_label)
        self.key_inv_layout_redundant.addLayout(self.inv_par_text_layout)
        spacerItem20 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.key_inv_layout_redundant.addItem(spacerItem20)
        self.key_inv_ent_layout = QtWidgets.QHBoxLayout()
        self.key_inv_ent_layout.setObjectName("key_inv_ent_layout")
        self.key_inv_labels_layout = QtWidgets.QVBoxLayout()
        self.key_inv_labels_layout.setObjectName("key_inv_labels_layout")
        self.key_inv_psg_label = QtWidgets.QLabel(self.inv_inner_border_widget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.key_inv_psg_label.setFont(font)
        self.key_inv_psg_label.setFrameShape(QtWidgets.QFrame.HLine)
        self.key_inv_psg_label.setFrameShadow(QtWidgets.QFrame.Raised)
        self.key_inv_psg_label.setObjectName("key_inv_psg_label")
        self.key_inv_labels_layout.addWidget(self.key_inv_psg_label)
        spacerItem21 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.key_inv_labels_layout.addItem(spacerItem21)
        self.key_inv_int_rt_label = QtWidgets.QLabel(self.inv_inner_border_widget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.key_inv_int_rt_label.setFont(font)
        self.key_inv_int_rt_label.setFrameShape(QtWidgets.QFrame.HLine)
        self.key_inv_int_rt_label.setFrameShadow(QtWidgets.QFrame.Raised)
        self.key_inv_int_rt_label.setObjectName("key_inv_int_rt_label")
        self.key_inv_labels_layout.addWidget(self.key_inv_int_rt_label)
        spacerItem22 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.key_inv_labels_layout.addItem(spacerItem22)
        self.key_op_init_inv_label = QtWidgets.QLabel(self.inv_inner_border_widget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.key_op_init_inv_label.setFont(font)
        self.key_op_init_inv_label.setFrameShape(QtWidgets.QFrame.HLine)
        self.key_op_init_inv_label.setFrameShadow(QtWidgets.QFrame.Raised)
        self.key_op_init_inv_label.setObjectName("key_op_init_inv_label")
        self.key_inv_labels_layout.addWidget(self.key_op_init_inv_label)
        spacerItem23 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.key_inv_labels_layout.addItem(spacerItem23)
        self.key_inv_ent_layout.addLayout(self.key_inv_labels_layout)
        self.key_inv_lineEdit_layout = QtWidgets.QVBoxLayout()
        self.key_inv_lineEdit_layout.setObjectName("key_inv_lineEdit_layout")
        self.key_inv_psg_lineEdit = QtWidgets.QLineEdit(self.inv_inner_border_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.key_inv_psg_lineEdit.sizePolicy().hasHeightForWidth())
        self.key_inv_psg_lineEdit.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.key_inv_psg_lineEdit.setFont(font)
        self.key_inv_psg_lineEdit.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.key_inv_psg_lineEdit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.key_inv_psg_lineEdit.setObjectName("key_inv_psg_lineEdit")
        self.key_inv_psg_lineEdit.setValidator(QtGui.QIntValidator())
        self.key_inv_lineEdit_layout.addWidget(self.key_inv_psg_lineEdit)
        spacerItem24 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.key_inv_lineEdit_layout.addItem(spacerItem24)
        self.key_inv_int_rt_lineEdit = QtWidgets.QLineEdit(self.inv_inner_border_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.key_inv_int_rt_lineEdit.sizePolicy().hasHeightForWidth())
        self.key_inv_int_rt_lineEdit.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.key_inv_int_rt_lineEdit.setFont(font)
        self.key_inv_int_rt_lineEdit.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.key_inv_int_rt_lineEdit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.key_inv_int_rt_lineEdit.setObjectName("key_inv_int_rt_lineEdit")
        self.key_inv_int_rt_lineEdit.setValidator(QtGui.QDoubleValidator())
        self.key_inv_lineEdit_layout.addWidget(self.key_inv_int_rt_lineEdit)
        spacerItem25 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.key_inv_lineEdit_layout.addItem(spacerItem25)
        self.key_inv_op_init_lineEdit = QtWidgets.QLineEdit(self.inv_inner_border_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.key_inv_op_init_lineEdit.sizePolicy().hasHeightForWidth())
        self.key_inv_op_init_lineEdit.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.key_inv_op_init_lineEdit.setFont(font)
        self.key_inv_op_init_lineEdit.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.key_inv_op_init_lineEdit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.key_inv_op_init_lineEdit.setObjectName("key_inv_op_init_lineEdit")
        self.key_inv_op_init_lineEdit.setValidator(QtGui.QIntValidator())
        self.key_inv_lineEdit_layout.addWidget(self.key_inv_op_init_lineEdit)
        spacerItem26 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.key_inv_lineEdit_layout.addItem(spacerItem26)
        self.key_inv_ent_layout.addLayout(self.key_inv_lineEdit_layout)
        self.key_inv_layout_redundant.addLayout(self.key_inv_ent_layout)
        self.key_inv_layout_redundant.setStretch(2, 30)
        self.key_inv_layout.addLayout(self.key_inv_layout_redundant)
        self.horizontalLayout_2.addLayout(self.key_inv_layout)
        self.verticalLayout_4.addWidget(self.inv_inner_border_widget)
        self.verticalLayout_23.addWidget(self.inv_outer_border_widget)
        self.gridLayout_7.addWidget(self.key_entered_col_widget, 0, 1, 1, 1)

        # TOTAL PER MONTH TAB:
        self.addTab(self.key_assumptions, "")
        self.tot_m = QtWidgets.QWidget()
        self.tot_m.setObjectName("tot_m")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.tot_m)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.tot_m_grid_layout = QtWidgets.QGridLayout()
        self.tot_m_grid_layout.setObjectName("tot_m_grid_layout")
        
        # Create a place for the donut plot of current user-entered totals.
        # Handled at bottom of program
        
        # Create a place for the donut plot of theoretical maximum values.
        totSavPredCalcFuncs.relevantFunctions.piePlotMonth(self)
        
        self.table_m = QtWidgets.QWidget(self.tot_m)
        self.table_m.setStyleSheet("background-color: rgb(109, 104, 117);")
        self.table_m.setObjectName("table_m")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout(self.table_m)
        self.verticalLayout_12.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        
        # Create a space to hold the month-level user-input table.
        self.table_m_layout = QtWidgets.QVBoxLayout()
        self.table_m_layout.setObjectName("table_m_layout")
        
        # Create the table itself
        self.table_m_2 = QtWidgets.QTableWidget(self.table_m)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.table_m_2.setFont(font)
        self.table_m_2.setStyleSheet("background-color: rgb(255, 255, 255);")
        
        # Set the number of rows based on the years under consideration
        self.table_m_2.setRowCount(self.no_months)
        self.table_m_2.setColumnCount(4)
        
        # Set the table information, no need to fiddle here
        self.table_m_2.setObjectName("table_m_2")
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.table_m_2.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.table_m_2.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.table_m_2.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.table_m_2.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        # self.table_m_2.setHorizontalHeaderItem(4, item)
        # item = QtWidgets.QTableWidgetItem()
        # font = QtGui.QFont()
        # font.setFamily("Arial")
        # font.setPointSize(10)
        # item.setFont(font)
        # item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        self.table_m_2.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(8)
        item.setFont(font)
        self.table_m_2.setItem(0, 4, item)
        self.table_m_layout.addWidget(self.table_m_2)
        self.verticalLayout_12.addLayout(self.table_m_layout)
        
        # Add the known
        
        self.tot_m_grid_layout.addWidget(self.table_m, 1, 0, 1, 1)
        
        # Ad a pair of buttons for reruns
        self.month_buttons_widget = QtWidgets.QWidget()
        self.tot_m_grid_layout.addWidget(self.month_buttons_widget, 1, 1, 1, 1)
        self.verticalLayout_month_buttons = QtWidgets.QVBoxLayout(self.month_buttons_widget)
        self.month_buttons_widget.setStyleSheet("background-color: rgb(163,247,181);")
        # self.plot_m = QtChart.QChartView(self.tot_m)
        # self.plot_m.setObjectName("plot_m")
        # self.verticalLayout_13 = QtWidgets.QVBoxLayout(self.plot_m)
        # self.verticalLayout_13.setContentsMargins(3, 3, 3, 3)
        # self.verticalLayout_13.setObjectName("verticalLayout_13")
        # self.plot_m_layout = QtWidgets.QVBoxLayout()
        # self.plot_m_layout.setObjectName("plot_m_layout")
        # self.verticalLayout_13.addLayout(self.plot_m_layout)
        # self.tot_m_grid_layout.addWidget(self.plot_m, 1, 1, 1, 1)
        # Add the save button and customise it
        self.mon_save_push_button = QtWidgets.QPushButton(self.month_buttons_widget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.mon_save_push_button.setFont(font)
        self.mon_save_push_button.setStyleSheet("QPushButton {\n"
"color: #333;\n"
"border: 2px solid #555;\n"
"border-radius: 20px;\n"
"border-style: outset;\n"
"background: qradialgradient(\n"
"cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
"radius: 1.35, stop: 0 #fff, stop: 1 #888\n"
");\n"
"padding: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"background: qradialgradient(\n"
"cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
"radius: 1.35, stop: 0 #fff, stop: 1 #bbb\n"
");\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"border-style: inset;\n"
"background: qradialgradient(\n"
"cx: 0.4, cy: -0.1, fx: 0.4, fy: -0.1,\n"
"radius: 1.35, stop: 0 #fff, stop: 1 #ddd\n"
");\n"
"}")
        self.mon_save_push_button.setIconSize(QtCore.QSize(16, 16))
        self.mon_save_push_button.setObjectName("mon_save_push_button")
        self.verticalLayout_month_buttons .addWidget(self.mon_save_push_button)
        
        # Add and customise the re-run calculations push button
        self.mon_rerun_push_button = QtWidgets.QPushButton(self.month_buttons_widget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.mon_rerun_push_button.setFont(font)
        self.mon_rerun_push_button.setStyleSheet("QPushButton {\n"
"color: #333;\n"
"border: 2px solid #555;\n"
"border-radius: 20px;\n"
"border-style: outset;\n"
"background: qradialgradient(\n"
"cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
"radius: 1.35, stop: 0 #fff, stop: 1 #888\n"
");\n"
"padding: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"background: qradialgradient(\n"
"cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
"radius: 1.35, stop: 0 #fff, stop: 1 #bbb\n"
");\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"border-style: inset;\n"
"background: qradialgradient(\n"
"cx: 0.4, cy: -0.1, fx: 0.4, fy: -0.1,\n"
"radius: 1.35, stop: 0 #fff, stop: 1 #ddd\n"
");\n"
"}")
        self.mon_rerun_push_button.setIconSize(QtCore.QSize(16, 16))
        self.mon_rerun_push_button.setObjectName("mon_rerun_push_button")
        self.verticalLayout_month_buttons.addWidget(self.mon_rerun_push_button)

        self.gridLayout_7.addLayout(self.key_derived_layout, 0, 2, 1, 1)

        self.gridLayout_4.addLayout(self.tot_m_grid_layout, 0, 0, 1, 1)
        self.addTab(self.tot_m, "")
        
        # TOTAL PER YEAR TAB:
        self.tot_y = QtWidgets.QWidget()
        self.tot_y.setObjectName("tot_y")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.tot_y)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.tot_y_grid_layout = QtWidgets.QGridLayout()
        self.tot_y_grid_layout.setObjectName("tot_y_grid_layout")
        
        # Ad a pair of buttons for reruns
        self.year_buttons_widget = QtWidgets.QWidget()
        self.tot_y_grid_layout.addWidget(self.year_buttons_widget, 1, 2, 1, 1)
        self.verticalLayout_year_buttons = QtWidgets.QVBoxLayout(self.year_buttons_widget)
        self.year_buttons_widget.setStyleSheet("background-color: rgb(163,247,181);")
        self.year_save_push_button = QtWidgets.QPushButton(self.year_buttons_widget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.year_save_push_button.setFont(font)
        self.year_save_push_button.setStyleSheet("QPushButton {\n"
"color: #333;\n"
"border: 2px solid #555;\n"
"border-radius: 20px;\n"
"border-style: outset;\n"
"background: qradialgradient(\n"
"cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
"radius: 1.35, stop: 0 #fff, stop: 1 #888\n"
");\n"
"padding: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"background: qradialgradient(\n"
"cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
"radius: 1.35, stop: 0 #fff, stop: 1 #bbb\n"
");\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"border-style: inset;\n"
"background: qradialgradient(\n"
"cx: 0.4, cy: -0.1, fx: 0.4, fy: -0.1,\n"
"radius: 1.35, stop: 0 #fff, stop: 1 #ddd\n"
");\n"
"}")
        self.year_save_push_button.setIconSize(QtCore.QSize(16, 16))
        self.year_save_push_button.setObjectName("mon_save_push_button")
        self.verticalLayout_year_buttons.addWidget(self.year_save_push_button)
        
        # Add and customise the re-run calculations push button
        self.year_rerun_push_button = QtWidgets.QPushButton(self.year_buttons_widget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.year_rerun_push_button.setFont(font)
        self.year_rerun_push_button.setStyleSheet("QPushButton {\n"
"color: #333;\n"
"border: 2px solid #555;\n"
"border-radius: 20px;\n"
"border-style: outset;\n"
"background: qradialgradient(\n"
"cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
"radius: 1.35, stop: 0 #fff, stop: 1 #888\n"
");\n"
"padding: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"background: qradialgradient(\n"
"cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
"radius: 1.35, stop: 0 #fff, stop: 1 #bbb\n"
");\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"border-style: inset;\n"
"background: qradialgradient(\n"
"cx: 0.4, cy: -0.1, fx: 0.4, fy: -0.1,\n"
"radius: 1.35, stop: 0 #fff, stop: 1 #ddd\n"
");\n"
"}")
        self.year_rerun_push_button.setIconSize(QtCore.QSize(16, 16))
        self.year_rerun_push_button.setObjectName("mon_rerun_push_button")
        self.verticalLayout_year_buttons.addWidget(self.year_rerun_push_button)
        
        # Plot a donut plot of the current progress year to year level.
        # Handled as the final function call in the program
        
        # Plot the theoretical end-period values in donut plot.
        totSavPredCalcFuncs.relevantFunctions.piePlotYear(self)
        
        # Create a table for year to year values.
        self.table_y = QtWidgets.QWidget(self.tot_y)
        self.table_y.setStyleSheet("background-color: rgb(109, 104, 117);")
        self.table_y.setObjectName("table_y")
        self.verticalLayout_17 = QtWidgets.QVBoxLayout(self.table_y)
        self.verticalLayout_17.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout_17.setObjectName("verticalLayout_17")
        self.table_y_layout = QtWidgets.QVBoxLayout()
        self.table_y_layout.setObjectName("table_y_layout")
        self.table_y_2 = QtWidgets.QTableWidget(self.table_y)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.table_y_2.sizePolicy().hasHeightForWidth())
        self.table_y_2.setSizePolicy(sizePolicy)
        self.table_y_2.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.table_y_2.setEditTriggers(QtWidgets.QAbstractItemView.AllEditTriggers)
        
        # Set the number of rows and columns based on the number of years under examination.
        self.table_y_2.setRowCount(self.no_years)
        self.table_y_2.setColumnCount(4)
        
        # Set table parameters, no need to interact.
        self.table_y_2.setObjectName("table_y_2")
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.table_y_2.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.table_y_2.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.table_y_2.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.table_y_2.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(8)
        item.setFont(font)
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        self.table_y_2.setItem(0, 1, item)
        self.table_y_layout.addWidget(self.table_y_2)
        self.verticalLayout_17.addLayout(self.table_y_layout)
        self.tot_y_grid_layout.addWidget(self.table_y, 1, 0, 1, 1)
        self.gridLayout_6.addLayout(self.tot_y_grid_layout, 0, 0, 1, 1)
        
        # ADD THE TOTAL PREDICTED YEAR LEVEL TAB.
        self.addTab(self.tot_y, "")
        
        # Display the predicted savings dataframe
        self.pred_sav = QtWidgets.QWidget()
        self.pred_sav.setObjectName("pred_sav")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.pred_sav)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.pred_sav_vert_layout = QtWidgets.QVBoxLayout()
        self.pred_sav_vert_layout.setObjectName("pred_sav_vert_layout")
        self.table_sav = QTableView(self.pred_sav)
        self.table_sav.setStyleSheet("background-color: rgb(163, 247,181);")
        self.table_sav.setObjectName("table_sav")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.table_sav)
        self.verticalLayout_9.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.verticalLayout_9.addLayout(self.verticalLayout_7)
        
        # Fill a dataframe for the expected investment value.
        sav_pred_set = totSavPredCalcFuncs.pandasModel(self.output_sav_table)
        self.table_sav.setModel(sav_pred_set)
        self.pred_sav_vert_layout.addWidget(self.table_sav)

        # Plot the predicted savings
        self.plot_sav = pyqtgraph.PlotWidget()
        self.leg = self.plot_sav.addLegend()
        self.second_plot_sav = self.plot_sav.plotItem
        self.plot_sav.setStyleSheet("background-color: rgb(88, 84, 129);")
        self.plot_sav.setObjectName("plot_sav")
        self.verticalLayout_14 = QtWidgets.QVBoxLayout(self.plot_sav)
        self.verticalLayout_14.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.verticalLayout_14.addLayout(self.verticalLayout_10)
        
        # Plot the dataset
        pen = pyqtgraph.mkPen(color = (163,247,181), width = 4)
        self.sav_line = self.plot_sav.plot(x = self.sav_x, y = self.sav_y, labels = self.sav_format, pen = pen, symbol = 'o', symbolBrush = (75, 143, 140), name = "Savings Value ($)")
        self.ax = self.plot_sav.getAxis('bottom')     
        self.ax2 = self.plot_sav.getAxis('left')
        #   Pass the list in, *in* a list.
        self.ax.setTicks([self.sav_format])
        self.ax2.setTicks([self.sav_format_y])
        self.plot_sav.setMouseEnabled(x = True, y = True) 
            
        # Add a second plot line on the right hand axis
        self.sav_int_plot = pyqtgraph.ViewBox()
        self.second_plot_sav.showAxis('right')     
        self.second_plot_sav.scene().addItem(self.sav_int_plot)
        self.second_plot_sav.getAxis('right').linkToView(self.sav_int_plot)
        self.sav_int_plot.setXLink(self.second_plot_sav)
        self.ax3 = self.plot_sav.getAxis('right')
        # Set the format for the new axis
        self.ax3.setTicks([self.sav_format_int_y])
        # Handle view resizing 
        def updateViews():
            ## view has resized; update auxiliary views to match
            self.sav_int_plot.setGeometry(self.second_plot_sav.vb.sceneBoundingRect())
            
            ## need to re-update linked axes since this was called
            ## incorrectly while views had different shapes.
            ## (probably this should be handled in ViewBox.resizeEvent)
            self.sav_int_plot.linkedViewChanged(self.second_plot_sav.vb, self.sav_int_plot.XAxis)
   
        updateViews()
        self.second_plot_sav.vb.sigResized.connect(updateViews)
        
        self.sav_int_curve = pyqtgraph.PlotDataItem(x= self.sav_x, y = self.sav_int_y, pen = pyqtgraph.mkPen(color = (211,196,227), width = 4), symbol = 'o', symbolBrush = (88, 84,129))
        self.sav_int_plot.addItem(self.sav_int_curve)
        self.leg.addItem(self.sav_int_curve, "Yearly Interest ($)")

        # Format the savings plot
        self.plot_sav.setBackground('w')
        self.plot_sav.showGrid(x=True, y=True)
        self.plot_sav.setTitle("Predicted Savings with Year ($)", size="16pt")
        self.plot_sav.setLabel('left', 'Savings ($)', size = '16pt')
        self.plot_sav.setLabel('bottom', 'Year', size = '16pt')
        self.plot_sav.setLabel('right', 'Interest ($ per year)', size = '16pt')

        self.pred_sav_vert_layout.addWidget(self.plot_sav)
        self.gridLayout_5.addLayout(self.pred_sav_vert_layout, 0, 0, 1, 1)
        self.addTab(self.pred_sav, "")

        # ADD TAB PREDICTED INVESTMENT VALUE
        self.pred_inv = QtWidgets.QWidget()
        self.pred_inv.setObjectName("pred_inv")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.pred_inv)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.pred_inv_vert_layout = QtWidgets.QVBoxLayout()
        self.pred_inv_vert_layout.setObjectName("pred_inv_vert_layout")
        
        # Display the investment prediction dataframe.
        self.tab_inv = QTableView(self.pred_inv)
        self.tab_inv.setStyleSheet("background-color: rgb(163, 247,181);")
        self.tab_inv.setObjectName("tab_inv")
        self.verticalLayout_21 = QtWidgets.QVBoxLayout(self.tab_inv)
        self.verticalLayout_21.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout_21.setObjectName("verticalLayout_21")
        self.verticalLayout_19 = QtWidgets.QVBoxLayout()
        self.verticalLayout_19.setObjectName("verticalLayout_19")
        self.verticalLayout_21.addLayout(self.verticalLayout_19)     
        
        # Fill a dataframe for the expected investment value.
        inv_pred_set = totSavPredCalcFuncs.pandasModel(self.df_inv_disp)
        self.tab_inv.setModel(inv_pred_set)
        self.pred_inv_vert_layout.addWidget(self.tab_inv)
        
        # Plot the predicted investment value
        self.plot_inv = pyqtgraph.PlotWidget()
        self.leg_inv = self.plot_inv.addLegend()
        self.second_plot_inv = self.plot_inv.plotItem
        self.plot_inv.setStyleSheet("background-color: rgb(88, 84, 129);")
        self.plot_inv.setObjectName("plot_inv")
        self.verticalLayout_22 = QtWidgets.QVBoxLayout(self.plot_inv)
        self.verticalLayout_22.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout_22.setObjectName("verticalLayout_22")
        self.verticalLayout_20 = QtWidgets.QVBoxLayout()
        self.verticalLayout_20.setObjectName("verticalLayout_20")
        self.verticalLayout_22.addLayout(self.verticalLayout_20)
        
        # Plot the dataset
        pen = pyqtgraph.mkPen(color = (163,247,181), width = 4)
        self.inv_line = self.plot_inv.plot(x = self.inv_x, y = self.inv_y, labels = self.inv_format, pen = pen, symbol = 'o', symbolBrush = (75, 143, 140), name = "Predicted Investment Value ($)")
        self.ax_inv = self.plot_inv.getAxis('bottom')     
        self.ax2_inv = self.plot_inv.getAxis('left')
        #   Pass the list in, *in* a list.
        self.ax_inv.setTicks([self.inv_format])
        self.ax2_inv.setTicks([self.inv_format_y])
        self.plot_inv.setMouseEnabled(x = True, y = True) 
            
        # Add a second plot line on the right hand axis
        self.inv_int_plot = pyqtgraph.ViewBox()
        self.second_plot_inv.showAxis('right')     
        self.second_plot_inv.scene().addItem(self.inv_int_plot)
        self.second_plot_inv.getAxis('right').linkToView(self.inv_int_plot)
        self.inv_int_plot.setXLink(self.second_plot_inv)
        self.ax3_inv = self.plot_inv.getAxis('right')
        # Set the format for the new axis
        self.ax3_inv.setTicks([self.inv_format_int_y])
        # Handle view resizing 
        def updateViewsInv():
            ## view has resized; update auxiliary views to match
            self.inv_int_plot.setGeometry(self.second_plot_inv.vb.sceneBoundingRect())
            
            ## need to re-update linked axes since this was called
            ## incorrectly while views had different shapes.
            ## (probably this should be handled in ViewBox.resizeEvent)
            self.inv_int_plot.linkedViewChanged(self.second_plot_inv.vb, self.inv_int_plot.XAxis)
   
        updateViewsInv()
        self.second_plot_inv.vb.sigResized.connect(updateViewsInv)
        
        self.inv_int_curve = pyqtgraph.PlotDataItem(x= self.inv_x, y = self.inv_int_y, pen = pyqtgraph.mkPen(color = (211,196,227), width = 4), symbol = 'o', symbolBrush = (88, 84,129))
        self.inv_int_plot.addItem(self.inv_int_curve)
        self.leg_inv.addItem(self.inv_int_curve, "Yearly Interest ($)")

        # Format the investment plot
        self.plot_inv.setBackground('w')
        self.plot_inv.showGrid(x=True, y=True)
        self.plot_inv.setTitle("Predicted Investment Value with Year ($)", size="16pt")
        self.plot_inv.setLabel('left', 'Predicted Investment ($)', size = '16pt')
        self.plot_inv.setLabel('bottom', 'Year', size = '16pt')
        self.plot_inv.setLabel('right', 'Interest ($ per year)', size = '16pt')


        self.pred_inv_vert_layout.addWidget(self.plot_inv)
        self.gridLayout_3.addLayout(self.pred_inv_vert_layout, 0, 0, 1, 1)
        self.addTab(self.pred_inv, "")       
        
        # Retranslate the UI
        totSavPredCalcFuncs.relevantFunctions.retranslateUi(self, TabWidget)
        self.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(TabWidget)
        
        # Activate the widow so it pops to the front upon being run
        self.activateWindow()
        
        # Set rerun and save button functionality
        self.key_rerun_push_button.clicked.connect(lambda: totSavPredCalcFuncs.relevantFunctions.rerunAndRedisplay(self))
        self.key_save_push_button.clicked.connect(lambda: totSavPredCalcFuncs.relevantFunctions.saveUserParams(self))
        self.mon_rerun_push_button.clicked.connect(lambda: totSavPredCalcFuncs.relevantFunctions.rerunAndRedisplay(self))
        self.mon_save_push_button.clicked.connect(lambda: totSavPredCalcFuncs.relevantFunctions.saveUserParams(self))
        self.year_rerun_push_button.clicked.connect(lambda: totSavPredCalcFuncs.relevantFunctions.rerunAndRedisplay(self))
        self.year_save_push_button.clicked.connect(lambda: totSavPredCalcFuncs.relevantFunctions.saveUserParams(self))
        
        # Fill the months and years into tables
        totSavPredCalcFuncs.relevantFunctions.fillMonthYearTab(self)
        
        # Add user plots
        totSavPredCalcFuncs.relevantFunctions.userDefPlots(self)
        
        # Check for item changes
        self.table_m_2.itemChanged.connect(totSavPredCalcFuncs.relevantFunctions.itemChangedByUserMonth) 
        self.table_m_2.itemChanged.connect(lambda: totSavPredCalcFuncs.relevantFunctions.flagReseterMonth(self))
        self.table_y_2.itemChanged.connect(totSavPredCalcFuncs.relevantFunctions.itemChangedByUserYear) 
        self.table_y_2.itemChanged.connect(lambda: totSavPredCalcFuncs.relevantFunctions.flagReseterYear(self))
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)    
    ui = Ui_TabWidget()
    TabWidget = QtWidgets.QTabWidget()
    ui.setupUi(TabWidget)
    ui.show()
    sys.exit(app.exec_())

