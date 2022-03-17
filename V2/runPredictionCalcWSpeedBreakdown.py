"""
Author - Matthew Hughes
Initial Comment Date - 02/03/2022

Description:    Performs time analysis on the prediction calculator.

"""

# import module
from totalSavInvPredictionCalc import Ui_TabWidget
from PyQt5 import QtWidgets
import os
# Set a variable equal to the current working directory that this file is in.

module_dir = os.getcwd()

# Generate a variable equal to the location of the test dataset.
test_path = module_dir + "\\timer_stats\\calc_speeds.prof"

# Generate an instance of the savings and investment calculator app.
if __name__ == "__main__":
    import sys
    import cProfile, pstats
    profiler = cProfile.Profile()
    profiler.enable()
    app = QtWidgets.QApplication(sys.argv)    
    ui = Ui_TabWidget()
    TabWidget = QtWidgets.QTabWidget()
    ui.setupUi(TabWidget)
    ui.show()
    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('cumtime') 
    stats.dump_stats(test_path)
    stats.print_stats(50)
    sys.exit(app.exec_())

# pip install snakeviz 
# snakeviz directory_to_prof_file
# snakeviz D:\OneDrive\pred_calc_fileset\timer_stats\calc_speeds.prof
# for convenient vizualisation