"""
Author - Matthew Hughes
Initial Comment Date - 27/02/2022

Description:    A set of classes holding the functionality of the 
                totalSavInvPredictionCalc.

"""

from PyQt5 import QtWidgets, QtChart
from PyQt5.QtCore import QAbstractTableModel, Qt
from pyqtgraph.Qt import QtCore, QtGui
import json
import os
import datetime
import pandas as pd
import numpy as np
import ftfy
import pickle
import os.path
import pyqtgraph


# tmp =datetime.datetime.strptime("21/12/2008", "%d/%m/%Y").strftime("%Y-%m-%d")
# tmp =datetime.datetime.strptime("21/12/2008", "%d/%m/%Y").date()

# Define a method for converting a pandas dataframe to a table.
class pandasModel(QAbstractTableModel):

    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None

# Set a seried of self-contained functions that do note require separate classes.
class relevantFunctions():
    
    def loadDefaultValues(self):
        
        # Set a variable equal to the current working directory that this file is in.
        module_dir = os.getcwd()

        # Generate a variable equal to the location of the defaults dataset.
        defaults_path = module_dir + "\\default_values\\calc_defaults.txt"
                
        # Set a path to the default full savings calculation set including month and period end flags
        full_sav_1 = module_dir + "\\default_values\\sav_defaults_full_fields.pkl"

        # Define a variable for the user defined path
        self.user_path = module_dir + "\\user_inputs\\user_defined_parameters.txt"
               
        # Set a path to the default full savings calculation set including month and period end flags
        self.full_sav_2 = module_dir + "\\user_inputs\\sav_defaults_full_fields.pkl"
        
        # Create investment paths
        self.full_inv_path_1 = module_dir + "\\default_values\\inv_defaults_full_fields.pkl"
        self.full_inv_path_2 = module_dir + "\\user_inputs\\inv_defaults_full_fields.pkl"
        
        # Create user real-life stats paths
        self.month_rt_path = module_dir + "\\user_inputs\\month_table.txt"
        self.year_rt_path = module_dir + "\\user_inputs\\year_table.txt"
        
                
        # Create empty dictionaries to house user change flags and a check dictionary to compare to
        self.user_changes_month = {}
        self.user_changes_year = {}
        self.user_check_dic_m = {}
        self.user_check_dic_y = {}
        
        # Dynamically set the savings load path
        if os.path.isfile(self.full_sav_2):
            full_sav = self.full_sav_2
        else:
            full_sav = full_sav_1
            
        # Dynamically set the investment table load path
        if os.path.isfile(self.full_inv_path_2):
            full_inv = self.full_inv_path_2
        else:
            full_inv = self.full_inv_path_1
        
        # Load the defaults values as a dictionary
        with open(defaults_path, 'r') as defaults:
            temp_def_dict = defaults.read()
        def_dict = json.loads(temp_def_dict)
        
        # If they exist load the user defined values as a dictionary
        try:
            with open(self.user_path, 'r') as user_inp:
                temp_user_dict = user_inp.read()
            user_dict = json.loads(temp_user_dict)
        
        # Otherwise create an empty user dictionary
        except:
            user_dict = {"def_final_fy": [],
                              "def_init_contrib_date":[] ,
                              "def_init_contrib_freq": [],
                              "def_init_sav_contrib": [],
                              "def_sav_int_rt": [],
                              "def_pre_inv_sav_goal": [],
                              "def_init_sav":[] ,
                              "def_pg_contrib":[] ,
                              "def_psg_inv_contrib": [],
                              "def_inv_int_rt": [],
                              "def_init_inv":[] }
    
        # Create an empty dictionary to fill a new instance of the app 
        self.df_fill_parameters = {}
        
        # Generate an aggregate dataframe from the user defined and default values, defaulting to empty if both are empty.
        for key in user_dict:
            self.df_fill_parameters[key] = user_dict[key] or def_dict[key] or []
            
        # If the start date is unfilled set the starting date to the current system date
        if not self.df_fill_parameters["def_init_contrib_date"]:
            self.df_fill_parameters["def_init_contrib_date"] = datetime.datetime.today().strftime('%d/%m/%Y')
        
        # If the optional arguments are empty, initialise them with their appropriate values.
        if not self.df_fill_parameters["def_init_sav"]:
            self.df_fill_parameters["def_init_sav"] = '0'
        
        if not self.df_fill_parameters["def_pg_contrib"]:
            self.df_fill_parameters['def_pg_contrib'] = str(int(self.df_fill_parameters['def_init_sav_contrib']) - int(self.df_fill_parameters['def_psg_inv_contrib']))
        
        if not self.df_fill_parameters['def_init_inv']:
            self.df_fill_parameters['def_init_inv'] = '0'
        
        # Hard code further defaults in case they did not load properly
        if not self.df_fill_parameters['def_final_fy']:
            self.df_fill_parameters['def_final_fy'] = '2045'
        
        if not self.df_fill_parameters["def_init_contrib_freq"]:
            self.df_fill_parameters["def_init_contrib_freq"] = 'fortnightly'
        
        if not self.df_fill_parameters["def_init_sav_contrib"]:
            self.df_fill_parameters["def_init_sav_contrib"] = '500'

        if not self.df_fill_parameters["def_sav_int_rt"]:
            self.df_fill_parameters["def_sav_int_rt"] = '0.9'
            
        if not self.df_fill_parameters["def_pre_inv_sav_goal"]:
            self.df_fill_parameters["def_pre_inv_sav_goal"] = '75000'
            
        if not self.df_fill_parameters["def_psg_inv_contrib"]:
            self.df_fill_parameters["def_psg_inv_contrib"] = '300'

        if not self.df_fill_parameters["def_inv_int_rt"]:
            self.df_fill_parameters["def_inv_int_rt"] = '5.0'

        # create a copy of the df_fill_parameters to check for changes later
        self.checking_fill_parameters = self.df_fill_parameters.copy()
        
        # Load default savings tables if they exist
        try:
            with open(full_sav, 'rb') as file:
                self.overall_dates = pickle.load(file)
                self.output_sav_table = self.overall_dates[['Date', 'Overall Contribution ($)', 'Overall Interest ($)', 'Savings Value ($)']]
                
                # Create copies of the imported tables to test for changes when deciding if saving is needed
                self.test_overall_dates = self.overall_dates.copy()
                self.test_output_sav_table = self.output_sav_table.copy()
        except:
            pass
        
        # Load default investment tables if they exist
        try:
            with open(full_inv, 'rb') as file:
                self.df_inv = pickle.load(file)
                self.df_inv_disp = self.df_inv[self.df_inv['Overall Interest ($)'] > 0] 
                
                # Create copies of the imported tables to test for changes when deciding if saving is needed
                self.test_df_inv = self.df_inv.copy()
                self.test_df_inv_disp = self.df_inv_disp.copy()
        except:
            pass
        
        # If the user monthly and year tables exist, load them
        if os.path.isfile(self.month_rt_path):
            with open(self.month_rt_path, 'r') as file:
                self.month_table_array = np.loadtxt(file)
            self.user_month_table_flag = 1
            self.test_month_table_array = self.month_table_array.copy()
        else:
            self.user_month_table_flag = 0
        
        # If the user monthly and year tables exist, load them
        if os.path.isfile(self.year_rt_path):
            with open(self.year_rt_path, 'r') as file:
                self.year_table_array = np.loadtxt(file)
            self.user_year_table_flag = 1
            self.test_year_table_array = self.year_table_array.copy()
        else:
            self.user_year_table_flag = 0
        
    # Set a date range based on the df_fill_parameters library.
    def dateRange(self):
        
        # retrieve the starting date from the library.
        st_date = datetime.datetime.strptime(self.df_fill_parameters['def_init_contrib_date'], "%d/%m/%Y").date()
    
        # Generate the end date from the initialisation library.
        end_date = datetime.date((int(self.df_fill_parameters['def_final_fy']) + 1), 1, 1)
        
        # Set the number of days per interval
        if self.df_fill_parameters["def_init_contrib_freq"].lower() == 'fortnightly':
            date_div = 14
        elif self.df_fill_parameters["def_init_contrib_freq"].lower() == 'weekly':
            date_div = 7
        elif self.df_fill_parameters["def_init_contrib_freq"].lower() == 'monthly':
            date_div = 30.44
            
        # Determine the number of fortnights between the two values
        fortnights = int((end_date - st_date).days / date_div)
        
        # Generate a date list of each date two weeks from the last
        date_list = [datetime.datetime.strptime(self.df_fill_parameters['def_init_contrib_date'], "%d/%m/%Y")]
        
        # Create a list of dates two weeks apart
        for fortnight in range(1, fortnights):
            date_list.append((st_date + datetime.timedelta(date_div * fortnight)))
        
        # Create a fortnight flag of the same length as the existing list
        fortnight_flag = np.ones(len(date_list))
        
        # Create a dictionary from the dates and flags
        fortnight_dic = {'Date': date_list, 'fortnight_flag': fortnight_flag}
        
        # Generate a dataframe containing the dates and flags
        df_biweekly = pd.DataFrame(fortnight_dic)
        
        # A built-in process handles month-end dates well
        month_ends = [*pd.date_range(start = st_date, end = end_date, freq = 'M').to_pydatetime()]
        month_ends = [day.date() for day in month_ends]
        mon_flag = np.ones(len(month_ends))
        month_dic = {'Date': month_ends, 'month_end_flag': mon_flag}
        df_monthly = pd.DataFrame(month_dic)
        
        # Make sure the date columns are of the same type and consist of dates
        df_biweekly['Date'] = pd.to_datetime(df_biweekly.Date, format='%Y-%m-%d %H:%M:%S').dt.date
        df_monthly['Date'] = pd.to_datetime(df_monthly.Date, format='%Y-%m-%d %H:%M:%S').dt.date
        
        # Determine dates that are both end of month and fortnightly dates
        shared_dates = pd.merge(df_biweekly, 
                                     df_monthly, 
                                     how = 'left',
                                     on = 'Date')
        
        # Remove shared entries from the monthly list
        df_monthly = df_monthly[~df_monthly.Date.isin(shared_dates.Date)]
        
        # Join the compiled date sets into an overall set of DataFrame of dates, with appropriate flags.
        frames = [shared_dates, df_monthly]
        self.overall_dates = pd.concat(frames).drop_duplicates(keep=False)
        
        # Set the nan entries to 0
        self.overall_dates = self.overall_dates.fillna(0)
        
        # Order the set of dates by date
        self.overall_dates = self.overall_dates.sort_values(by = ['Date'])
   
    # Create a function to calculate the expected change to savings over time
    def firstSavingsGrowth(self):
        
        # Determine the savings contribution through direct contributions for an initial FIRST PASS:
        # Set a theoretical max contribution and prelim_int column
         # Set the first-pass contribution. This is set to the maximum and is refined in subsequent passes.
         self.overall_dates['Max Contribution ($)'] = self.df_fill_parameters["def_init_sav_contrib"]
         self.overall_dates.loc[self.overall_dates['fortnight_flag'].eq(0), 'Max Contribution ($)'] = 0
         
         # Generate some temporary variables which are used to generate first estimates of variables
         init_doll = [int(self.df_fill_parameters["def_init_sav"])]
         first_int = [0]
         self.contrib_var = self.overall_dates['Max Contribution ($)'].to_numpy()
         self.date_diff = ((self.overall_dates['Date'] - self.overall_dates['Date'].shift(1)).dt.days).to_numpy()
         
         for row in range(1, self.overall_dates.shape[0]):
             init_doll.append(self.contrib_var[row - 1] + init_doll[row - 1])
             first_int.append(round(init_doll[row]*(1 + ((float(self.df_fill_parameters["def_sav_int_rt"]) / 100) / 365))**(self.date_diff[row]) - init_doll[row], 2)) 
             
         self.overall_dates['first_interest'] = first_int
         
         # Run the second pass of the total generation
         
    def secSavingsGrowth(self):
        
        # Create a manual second pass variable set since this is a special case too
        grouping_df = self.overall_dates[['Date', 'first_interest']]
        grouper = pd.to_datetime(self.overall_dates['Date']).dt.to_period("M")
        # Create a grouped df to lookup in
        grouped_times = grouping_df.groupby(grouper).sum().reset_index()
         
        # Create numpy versions of columns for processing
        date_vec_lookup = grouper.to_numpy()
        # Set a cumulative total variable
        self.cum_tot_p_n = [int(self.df_fill_parameters["def_init_sav"])]
        month_flag = self.overall_dates['month_end_flag'].to_numpy()
        contrib_var_n = [self.contrib_var[0]]
        self.interest_n = [0]
        
        # Calculate the first passes grand total
        for row in range(1, self.overall_dates.shape[0]):
            if month_flag[row - 1] == 1:
                iter_date_lu = date_vec_lookup[row - 1]
                interest = round(float(grouped_times['first_interest'][grouped_times.Date == iter_date_lu]), 2)
                self.cum_tot_p_n.append(self.cum_tot_p_n[row - 1] + self.contrib_var[row - 1] + interest)

            else:
                self.cum_tot_p_n.append(self.cum_tot_p_n[row - 1] + self.contrib_var[row - 1])  
          
        # Set the second pass contribution and interest based on if the first pass cumulative total is more than the limit set previously                  
        for row in range(1, self.overall_dates.shape[0]):
              if float(self.cum_tot_p_n[row]) < int(self.df_fill_parameters["def_pre_inv_sav_goal"]):
                  contrib_var_n.append(int(self.df_fill_parameters["def_init_sav_contrib"]))
                  self.interest_n.append(round(self.cum_tot_p_n[row]*(1 + ((float(self.df_fill_parameters["def_sav_int_rt"]) / 100) / 365))**(self.date_diff[row]) - self.cum_tot_p_n[row], 2)) 
              else:
                  if self.contrib_var[row] == 0:
                      contrib_var_n.append(0)
                      self.interest_n.append(round(self.cum_tot_p_n[row]*(1 + ((float(self.df_fill_parameters["def_sav_int_rt"]) / 100) / 365))**(self.date_diff[row]) - self.cum_tot_p_n[row], 2)) 
        
                  else:
                      contrib_var_n.append(int(self.df_fill_parameters['def_pg_contrib']))
                      self.interest_n.append(round(self.cum_tot_p_n[row]*(1 + ((float(self.df_fill_parameters["def_sav_int_rt"]) / 100) / 365))**(self.date_diff[row]) - self.cum_tot_p_n[row], 2)) 
        
        # Reset the interest and contribution value
        self.overall_dates['Overall Interest ($)'] = self.interest_n
        self.overall_dates['Overall Contribution ($)'] = contrib_var_n
        
        # Iterate a few times to reach an interest steady state
        for iteration in range(50):
             
            # Set the new cumulative total back to its initial value
            del self.cum_tot_p_n
            self.cum_tot_p_n = [int(self.df_fill_parameters["def_init_sav"])]
            
            # Create a manual nth-pass variable set
            grouping_df = self.overall_dates[['Date', 'Overall Interest ($)'] ]
            grouper = pd.to_datetime(self.overall_dates['Date']).dt.to_period("M")
            # Create a grouped df to lookup in
            grouped_times = grouping_df.groupby(grouper).sum().reset_index()
            # Create numpy versions of columns for processing
            date_vec_lookup = grouper.to_numpy()
            
            # Loop over the grouped data and the original
            for row in range(1, self.overall_dates.shape[0]):
                if month_flag[row - 1] == 1:
                    iter_date_lu = date_vec_lookup[row - 1]
                    interest = round(float(grouped_times['Overall Interest ($)'][grouped_times.Date == iter_date_lu]), 2)
                    self.cum_tot_p_n.append(self.cum_tot_p_n[row - 1] + contrib_var_n[row - 1] + interest)

                else:
                    self.cum_tot_p_n.append(self.cum_tot_p_n[row - 1] + contrib_var_n[row - 1])  
            
            # Now we have grouped delete the variables
            del contrib_var_n
            del self.interest_n
            
            # Create the variables again
            contrib_var_n = [self.contrib_var[0]]
            self.interest_n = [0]    
            
            # Set the nth pass contribution and interest based on if the first pass cumulative total is more than the limit set previously                  
            for row in range(1, self.overall_dates.shape[0]):
                  if float(self.cum_tot_p_n[row]) < int(self.df_fill_parameters["def_pre_inv_sav_goal"]):
                      contrib_var_n.append(int(self.df_fill_parameters["def_init_sav_contrib"]))
                      self.interest_n.append(round(self.cum_tot_p_n[row]*(1 + ((float(self.df_fill_parameters["def_sav_int_rt"]) / 100) / 365))**(self.date_diff[row]) - self.cum_tot_p_n[row], 2)) 
                  else:
                      if self.contrib_var[row] == 0:
                          contrib_var_n.append(0)
                          self.interest_n.append(round(self.cum_tot_p_n[row]*(1 + ((float(self.df_fill_parameters["def_sav_int_rt"]) / 100) / 365))**(self.date_diff[row]) - self.cum_tot_p_n[row], 2)) 
            
                      else:
                          contrib_var_n.append(int(self.df_fill_parameters['def_pg_contrib']))
                          self.interest_n.append(round(self.cum_tot_p_n[row]*(1 + ((float(self.df_fill_parameters["def_sav_int_rt"]) / 100) / 365))**(self.date_diff[row]) - self.cum_tot_p_n[row], 2)) 
            
            # Reset the interest and contribution value
            self.overall_dates['Overall Interest ($)'] = self.interest_n
            self.overall_dates['Overall Contribution ($)'] = contrib_var_n
        
        self.overall_dates['Savings Value ($)'] = self.cum_tot_p_n    
        self.output_sav_table = self.overall_dates[['Date', 'Overall Contribution ($)', 'Overall Interest ($)', 'Savings Value ($)']]
        self.test_overall_dates = self.overall_dates.copy()
        self.test_output_sav_table = self.output_sav_table.copy()
         
        # Group the table by year for plotting
        grouper = pd.to_datetime(self.output_sav_table['Date']).dt.to_period("Y")
        grouped_times = self.output_sav_table.groupby(grouper).agg({'Overall Interest ($)': 'sum', 'Savings Value ($)': 'max'}).reset_index()
         
        # Create formats for the variables
        format_mapping={'Date': '{:}', 'Overall Contribution ($)': '${:,.0f}', 'Overall Interest ($)': '${:,.2f}', 'Savings Value ($)': '${:,.2f}'}
        for key, value in format_mapping.items():
            self.output_sav_table[key] =  self.output_sav_table[key].apply(value.format)
         
        # Set savings variables and a format to set the values for the dates to date strings
        self.sav_x = [*range(grouped_times.shape[0])]
        self.sav_y = grouped_times['Savings Value ($)'].to_numpy()
        self.sav_int_y = grouped_times['Overall Interest ($)'].to_numpy()         
        format_mapping={'Date': '{:}', 'Overall Interest ($)': '${:,.2f}', 'Savings Value ($)': '${:,.2f}'}
        for key, value in format_mapping.items():
            grouped_times[key] =  grouped_times[key].apply(value.format)
        self.sav_format = [*zip(self.sav_x, grouped_times.Date.to_numpy())]
        self.sav_format_y = [*zip(self.sav_y, grouped_times['Savings Value ($)'].to_numpy())]
        self.sav_format_int_y = [*zip(self.sav_int_y, grouped_times['Overall Interest ($)'].to_numpy())]
        # Set a variable equal to the current working directory that this file is in.
        module_dir = os.getcwd()
        # Set a path to the default full savings calculation set including month and period end flags
        full_sav_1 = module_dir + "\\default_values\\sav_defaults_full_fields.pkl"
        # Dump the further outputs
        with open(full_sav_1, 'wb') as file:
            self.overall_dates.to_pickle(file)
            
    def modSecSavingsGrowth(self):
        # Create a manual second pass variable set since this is a special case too
        grouping_df = self.overall_dates[['Date', 'first_interest']]
        grouper = pd.to_datetime(self.overall_dates['Date']).dt.to_period("M")
        # Create a grouped df to lookup in
        grouped_times = grouping_df.groupby(grouper).sum().reset_index()
         
        # Create numpy versions of columns for processing
        date_vec_lookup = grouper.to_numpy()
        # Set a cumulative total variable
        self.cum_tot_p_n = [int(self.df_fill_parameters["def_init_sav"])]
        month_flag = self.overall_dates['month_end_flag'].to_numpy()
        contrib_var_n = [self.contrib_var[0]]
        self.interest_n = [0]
        
        # Calculate the first passes grand total
        for row in range(1, self.overall_dates.shape[0]):
            if month_flag[row - 1] == 1:
                iter_date_lu = date_vec_lookup[row - 1]
                interest = round(float(grouped_times['first_interest'][grouped_times.Date == iter_date_lu]), 2)
                self.cum_tot_p_n.append(self.cum_tot_p_n[row - 1] + self.contrib_var[row - 1] + interest)

            else:
                self.cum_tot_p_n.append(self.cum_tot_p_n[row - 1] + self.contrib_var[row - 1])  
          
        # Set the second pass contribution and interest based on if the first pass cumulative total is more than the limit set previously                  
        for row in range(1, self.overall_dates.shape[0]):
              if float(self.cum_tot_p_n[row]) < int(self.df_fill_parameters["def_pre_inv_sav_goal"]):
                  contrib_var_n.append(int(self.df_fill_parameters["def_init_sav_contrib"]))
                  self.interest_n.append(round(self.cum_tot_p_n[row]*(1 + ((float(self.df_fill_parameters["def_sav_int_rt"]) / 100) / 365))**(self.date_diff[row]) - self.cum_tot_p_n[row], 2)) 
              else:
                  if self.contrib_var[row] == 0:
                      contrib_var_n.append(0)
                      self.interest_n.append(round(self.cum_tot_p_n[row]*(1 + ((float(self.df_fill_parameters["def_sav_int_rt"]) / 100) / 365))**(self.date_diff[row]) - self.cum_tot_p_n[row], 2)) 
        
                  else:
                      contrib_var_n.append(int(self.df_fill_parameters['def_pg_contrib']))
                      self.interest_n.append(round(self.cum_tot_p_n[row]*(1 + ((float(self.df_fill_parameters["def_sav_int_rt"]) / 100) / 365))**(self.date_diff[row]) - self.cum_tot_p_n[row], 2)) 
        
        # Reset the interest and contribution value
        self.overall_dates['Overall Interest ($)'] = self.interest_n
        self.overall_dates['Overall Contribution ($)'] = contrib_var_n
        
        # Iterate a few times to reach an interest steady state
        for iteration in range(5):
             
            # Set the new cumulative total back to its initial value
            del self.cum_tot_p_n
            self.cum_tot_p_n = [int(self.df_fill_parameters["def_init_sav"])]
            
            # Create a manual nth-pass variable set
            grouping_df = self.overall_dates[['Date', 'Overall Interest ($)'] ]
            grouper = pd.to_datetime(self.overall_dates['Date']).dt.to_period("M")
            # Create a grouped df to lookup in
            grouped_times = grouping_df.groupby(grouper).sum().reset_index()
            # Create numpy versions of columns for processing
            date_vec_lookup = grouper.to_numpy()
            
            # Loop over the grouped data and the original
            for row in range(1, self.overall_dates.shape[0]):
                if month_flag[row - 1] == 1:
                    iter_date_lu = date_vec_lookup[row - 1]
                    interest = round(float(grouped_times['Overall Interest ($)'][grouped_times.Date == iter_date_lu]), 2)
                    self.cum_tot_p_n.append(self.cum_tot_p_n[row - 1] + contrib_var_n[row - 1] + interest)

                else:
                    self.cum_tot_p_n.append(self.cum_tot_p_n[row - 1] + contrib_var_n[row - 1])  
            
            # Now we have grouped delete the variables
            del contrib_var_n
            del self.interest_n
            
            # Create the variables again
            contrib_var_n = [self.contrib_var[0]]
            self.interest_n = [0]    
            
            # Set the nth pass contribution and interest based on if the first pass cumulative total is more than the limit set previously                  
            for row in range(1, self.overall_dates.shape[0]):
                  if float(self.cum_tot_p_n[row]) < int(self.df_fill_parameters["def_pre_inv_sav_goal"]):
                      contrib_var_n.append(int(self.df_fill_parameters["def_init_sav_contrib"]))
                      self.interest_n.append(round(self.cum_tot_p_n[row]*(1 + ((float(self.df_fill_parameters["def_sav_int_rt"]) / 100) / 365))**(self.date_diff[row]) - self.cum_tot_p_n[row], 2)) 
                  else:
                      if self.contrib_var[row] == 0:
                          contrib_var_n.append(0)
                          self.interest_n.append(round(self.cum_tot_p_n[row]*(1 + ((float(self.df_fill_parameters["def_sav_int_rt"]) / 100) / 365))**(self.date_diff[row]) - self.cum_tot_p_n[row], 2)) 
            
                      else:
                          contrib_var_n.append(int(self.df_fill_parameters['def_pg_contrib']))
                          self.interest_n.append(round(self.cum_tot_p_n[row]*(1 + ((float(self.df_fill_parameters["def_sav_int_rt"]) / 100) / 365))**(self.date_diff[row]) - self.cum_tot_p_n[row], 2)) 
            
            # Reset the interest and contribution value
            self.overall_dates['Overall Interest ($)'] = self.interest_n
            self.overall_dates['Overall Contribution ($)'] = contrib_var_n
                    
        self.overall_dates['Savings Value ($)'] = self.cum_tot_p_n    
        self.output_sav_table = self.overall_dates[['Date', 'Overall Contribution ($)', 'Overall Interest ($)', 'Savings Value ($)']]
         
        # Group the table by year for plotting
        grouper = pd.to_datetime(self.output_sav_table['Date']).dt.to_period("Y")
        grouped_times = self.output_sav_table.groupby(grouper).agg({'Overall Interest ($)': 'sum', 'Savings Value ($)': 'max'}).reset_index()
         
        # Create formats for the variables
        format_mapping={'Date': '{:}', 'Overall Contribution ($)': '${:,.0f}', 'Overall Interest ($)': '${:,.2f}', 'Savings Value ($)': '${:,.2f}'}
        for key, value in format_mapping.items():
            self.output_sav_table[key] =  self.output_sav_table[key].apply(value.format)
         
        # Set savings variables and a format to set the values for the dates to date strings
        self.sav_x = [*range(grouped_times.shape[0])]
        self.sav_y = grouped_times['Savings Value ($)'].to_numpy()
        self.sav_int_y = grouped_times['Overall Interest ($)'].to_numpy()         
        format_mapping={'Date': '{:}', 'Overall Interest ($)': '${:,.2f}', 'Savings Value ($)': '${:,.2f}'}
        for key, value in format_mapping.items():
            grouped_times[key] =  grouped_times[key].apply(value.format)
        self.sav_format = [*zip(self.sav_x, grouped_times.Date.to_numpy())]
        self.sav_format_y = [*zip(self.sav_y, grouped_times['Savings Value ($)'].to_numpy())]
        self.sav_format_int_y = [*zip(self.sav_int_y, grouped_times['Overall Interest ($)'].to_numpy())]

    
    # Define an alternative function to handle the case that we have a loaded version of the self.overall_dates and self.output_sav_table dataframes
    def savGrowthWithLoads(self):
         # Group the table by year for plotting
         grouper = pd.to_datetime(self.output_sav_table['Date']).dt.to_period("Y")
         grouped_times = self.output_sav_table.groupby(grouper).agg({'Overall Interest ($)': 'sum', 'Savings Value ($)': 'max'}).reset_index()
         
         # Create formats for the variables
         format_mapping={'Date': '{:}', 'Overall Contribution ($)': '${:,.0f}', 'Overall Interest ($)': '${:,.2f}', 'Savings Value ($)': '${:,.2f}'}
         for key, value in format_mapping.items():
             self.output_sav_table[key] =  self.output_sav_table[key].apply(value.format)
         
         # Set savings variables and a format to set the values for the dates to date strings
         self.sav_x = [*range(grouped_times.shape[0])]
         self.sav_y = grouped_times['Savings Value ($)'].to_numpy()
         self.sav_int_y = grouped_times['Overall Interest ($)'].to_numpy()
         format_mapping={'Date': '{:}', 'Overall Interest ($)': '${:,.2f}', 'Savings Value ($)': '${:,.2f}'}
         for key, value in format_mapping.items():
             grouped_times[key] =  grouped_times[key].apply(value.format)
         self.sav_format = [*zip(self.sav_x, grouped_times.Date.to_numpy())]
         self.sav_format_y = [*zip(self.sav_y, grouped_times['Savings Value ($)'].to_numpy())]
         self.sav_format_int_y = [*zip(self.sav_int_y, grouped_times['Overall Interest ($)'].to_numpy())]


    # Create an interest calculation function for first time calculation
    def invCalc(self):
        val = self.overall_dates['Overall Contribution ($)'].to_numpy()
        # Initialize variables
        init_inv = [int(self.df_fill_parameters['def_init_inv'])]
        init_int = [0]
        if int(self.df_fill_parameters["def_pre_inv_sav_goal"]) <= int(self.df_fill_parameters["def_init_sav"]):
            contrib = [int(self.df_fill_parameters["def_psg_inv_contrib"])]
        else:
            contrib = [0]
            
        # Loop over dates and calculate the interest amount, value, and total init_inv value
        for day in range(1, self.overall_dates.shape[0]):
            if val[day] == 0:
                contrib.append(0)
            elif val[day] == int(self.df_fill_parameters["def_init_sav_contrib"]):
                contrib.append(0)
            else:
                contrib.append(int(self.df_fill_parameters["def_psg_inv_contrib"]))
            interest = float(self.df_fill_parameters["def_inv_int_rt"])/100  * float(self.date_diff[day] / 365.25)
            init_int.append((init_inv[day - 1] + contrib[day - 1]) * interest)
            init_inv.append(init_inv[day - 1] + contrib[day - 1] + init_int[day])
        
        
        inv_data = {'Date': self.overall_dates.Date.to_numpy(),
                    'Overall Contribution ($)': contrib,
                    'Overall Interest ($)': init_int,
                    'Predicted Investment Value ($)': init_inv}
        # Create a dataframe from the interest values
        self.df_inv = pd.DataFrame(inv_data)
        self.df_inv_disp = self.df_inv[self.df_inv['Overall Interest ($)'] > 0]
        
        # For the case that no defaults exist save this version as it
        with open(self.full_inv_path_1, 'wb') as file:
            self.df_inv.to_pickle(file)
        
        self.test_df_inv = self.df_inv.copy()
        self.test_df_inv_disp = self.df_inv_disp.copy()
        
        # Reformat the display df
        format_mapping={'Date': '{:}', 'Overall Contribution ($)': '${:,.0f}', 'Overall Interest ($)': '${:,.2f}', 'Predicted Investment Value ($)': '${:,.2f}'}
        for key, value in format_mapping.items():
            self.df_inv_disp[key] =  self.df_inv_disp[key].apply(value.format)
        
        # Group the table by year for plotting
        grouper = pd.to_datetime(self.df_inv['Date']).dt.to_period("Y")
        grouped_times = self.df_inv.groupby(grouper).agg({'Overall Interest ($)': 'sum', 'Predicted Investment Value ($)': 'max'}).reset_index()
         
        # Set investment variables and a format to set the values for the dates to date strings
        self.inv_x = [*range(grouped_times.shape[0])]
        self.inv_y = grouped_times['Predicted Investment Value ($)'].to_numpy()
        self.inv_int_y = grouped_times['Overall Interest ($)'].to_numpy()
        format_mapping={'Date': '{:}', 'Overall Interest ($)': '${:,.2f}', 'Predicted Investment Value ($)': '${:,.2f}'}
        for key, value in format_mapping.items():
            grouped_times[key] =  grouped_times[key].apply(value.format)
        self.inv_format = [*zip(self.inv_x, grouped_times.Date.to_numpy())]
        self.inv_format_y = [*zip(self.inv_y, grouped_times['Predicted Investment Value ($)'].to_numpy())]
        self.inv_format_int_y = [*zip(self.inv_int_y, grouped_times['Overall Interest ($)'].to_numpy())]

    
    # Create an interest calculation function for rerun calculations
    def invCalcRerun(self):
        val = self.overall_dates['Overall Contribution ($)'].to_numpy()
        # Initialize variables
        init_inv = [int(self.df_fill_parameters['def_init_inv'])]
        init_int = [0]
        if int(self.df_fill_parameters["def_pre_inv_sav_goal"]) <= int(self.df_fill_parameters["def_init_sav"]):
            contrib = [int(self.df_fill_parameters["def_psg_inv_contrib"])]
        else:
            contrib = [0]
            
        # Loop over dates and calculate the interest amount, value, and total init_inv value
        for day in range(1, self.overall_dates.shape[0]):
            if val[day] == 0:
                contrib.append(0)
            elif val[day] == int(self.df_fill_parameters["def_init_sav_contrib"]):
                contrib.append(0)
            else:
                contrib.append(int(self.df_fill_parameters["def_psg_inv_contrib"]))
            interest = float(self.df_fill_parameters["def_inv_int_rt"])/100  * float(self.date_diff[day] / 365.25)
            init_int.append((init_inv[day - 1] + contrib[day - 1]) * interest)
            init_inv.append(init_inv[day - 1] + contrib[day - 1] + init_int[day])
        
        
        inv_data = {'Date': self.overall_dates.Date.to_numpy(),
                    'Overall Contribution ($)': contrib,
                    'Overall Interest ($)': init_int,
                    'Predicted Investment Value ($)': init_inv}
        # Create a dataframe from the interest values
        self.df_inv = pd.DataFrame(inv_data)
        self.df_inv_disp = self.df_inv[self.df_inv['Overall Interest ($)'] > 0]
        
        # Reformat the display df
        format_mapping={'Date': '{:}', 'Overall Contribution ($)': '${:,.0f}', 'Overall Interest ($)': '${:,.2f}', 'Predicted Investment Value ($)': '${:,.2f}'}
        for key, value in format_mapping.items():
            self.df_inv_disp[key] =  self.df_inv_disp[key].apply(value.format)
              
        # Group the table by year for plotting
        grouper = pd.to_datetime(self.df_inv['Date']).dt.to_period("Y")
        grouped_times = self.df_inv.groupby(grouper).agg({'Overall Interest ($)': 'sum', 'Predicted Investment Value ($)': 'max'}).reset_index()
         
        # Set investment variables and a format to set the values for the dates to date strings
        self.inv_x = [*range(grouped_times.shape[0])]
        self.inv_y = grouped_times['Predicted Investment Value ($)'].to_numpy()
        self.inv_int_y = grouped_times['Overall Interest ($)'].to_numpy()
        format_mapping={'Date': '{:}', 'Overall Interest ($)': '${:,.2f}', 'Predicted Investment Value ($)': '${:,.2f}'}
        for key, value in format_mapping.items():
            grouped_times[key] =  grouped_times[key].apply(value.format)
        self.inv_format = [*zip(self.inv_x, grouped_times.Date.to_numpy())]
        self.inv_format_y = [*zip(self.inv_y, grouped_times['Predicted Investment Value ($)'].to_numpy())]
        self.inv_format_int_y = [*zip(self.inv_int_y, grouped_times['Overall Interest ($)'].to_numpy())]
        
    # Create an interest calculation function for if defaults exist
    def invCalcWithLoads(self):
        # Reformat the display df
        format_mapping={'Date': '{:}', 'Overall Contribution ($)': '${:,.0f}', 'Overall Interest ($)': '${:,.2f}', 'Predicted Investment Value ($)': '${:,.2f}'}
        for key, value in format_mapping.items():
            self.df_inv_disp[key] =  self.df_inv_disp[key].apply(value.format)
        
        # Group the table by year for plotting
        grouper = pd.to_datetime(self.df_inv['Date']).dt.to_period("Y")
        grouped_times = self.df_inv.groupby(grouper).agg({'Overall Interest ($)': 'sum', 'Predicted Investment Value ($)': 'max'}).reset_index()
         
        # Set investment variables and a format to set the values for the dates to date strings
        self.inv_x = [*range(grouped_times.shape[0])]
        self.inv_y = grouped_times['Predicted Investment Value ($)'].to_numpy()
        self.inv_int_y = grouped_times['Overall Interest ($)'].to_numpy()
        format_mapping={'Date': '{:}', 'Overall Interest ($)': '${:,.2f}', 'Predicted Investment Value ($)': '${:,.2f}'}
        for key, value in format_mapping.items():
            grouped_times[key] =  grouped_times[key].apply(value.format)
        self.inv_format = [*zip(self.inv_x, grouped_times.Date.to_numpy())]
        self.inv_format_y = [*zip(self.inv_y, grouped_times['Predicted Investment Value ($)'].to_numpy())]
        self.inv_format_int_y = [*zip(self.inv_int_y, grouped_times['Overall Interest ($)'].to_numpy())]
        
    # Set a function for the re-run of variables
    def rerunParams(self):
        
        # Reset the df_fill_parameters with the current set of values
        self.saving_lib = {"def_final_fy": int(self.key_end_yr_lineEdit.text()),
                          "def_init_contrib_date":str(self.key_op_first_contrib_date_lineEdit.text()) ,
                          "def_init_contrib_freq": str(self.key_op_contrib_freq_dropdown.currentText()),
                          "def_init_sav_contrib": int(self.key_sav_cont_lineEdit_2.text()),
                          "def_sav_int_rt": float(self.key_sav_int_rt_lineEdit_2.text()),
                          "def_pre_inv_sav_goal": int(self.key_sav_goal_lineEdit_2.text()),
                          "def_init_sav": self.ke_init_sav_lineEdit_2.text() ,
                          "def_pg_contrib": self.key_cust_goal_cont_lineEdit_2.text() ,
                          "def_psg_inv_contrib": int(self.key_inv_psg_lineEdit.text()),
                          "def_inv_int_rt": float(self.key_inv_int_rt_lineEdit.text()),
                          "def_init_inv": self.key_inv_op_init_lineEdit.text()
                          }

        for key in self.saving_lib:
            self.df_fill_parameters[key] = self.saving_lib[key] or self.df_fill_parameters[key] or []
            
        # If variables exist, delete them
        try:        
            del self.df_inv
        except:
            pass
        try:        
            del self.df_inv_disp
        except:
            pass
        try:        
            del self.overall_dates
        except:
            pass
        try:        
            del self.contrib_var
        except:
            pass
        try:        
            del self.date_diff
        except:
            pass
        try:        
            del self.output_sav_table
        except:
            pass
        try:        
            del self.sav_x
        except:
            pass
        try:        
            del self.sav_y
        except:
            pass
        try:        
            del self.sav_int_y
        except:
            pass
        try:        
            del self.sav_format
        except:
            pass
        try:        
            del self.sav_format_y
        except:
            pass
        try:        
            del self.sav_format_int_y
        except:
            pass         
        
        # Run the calculations functions
        relevantFunctions.dateRange(self)
        relevantFunctions.firstSavingsGrowth(self)
        relevantFunctions.modSecSavingsGrowth(self)
        relevantFunctions.invCalcRerun(self)
        
        self.year_table_array = np.empty([self.no_years , 3])
        for row in range(self.no_years):
            for col in range(1, 3):
                self.year_table_array[row, col - 1] =  str(self.table_y_2.item(row, col).text())
        
        self.month_table_array = np.empty([self.no_months , 3])
        for row in range(self.no_months):
            for col in range(1, 3):
                self.month_table_array[row, col - 1] =  str(self.table_m_2.item(row, col).text())
    
        self.overall_dates.reset_index()
        self.df_inv.reset_index()
  
    # Set a function to calculate some yearly and monthly totals
    def genTotVals(self):
        # Generte yearly values
        sav_grouping_df = self.overall_dates[['Date', 'Savings Value ($)'] ]
        grouper = pd.to_datetime(sav_grouping_df['Date']).dt.to_period("Y")
        self.sav_year_grouped_times = sav_grouping_df.groupby(grouper).agg({'Savings Value ($)': 'max'}).reset_index()
        self.date_list_year = self.sav_year_grouped_times['Date'].to_numpy()
        inv_grouping_df = self.df_inv[['Date', 'Predicted Investment Value ($)'] ]
        grouper = pd.to_datetime(inv_grouping_df['Date']).dt.to_period("Y")
        self.inv_year_grouped_times = inv_grouping_df.groupby(grouper).agg({'Predicted Investment Value ($)': 'max'}).reset_index()
        self.no_years = len(self.inv_year_grouped_times)
        try:
            self.year_df_len = self.year_table_array.shape[0]
        except:
            pass
        
        # Generate monthly values
        grouper = pd.to_datetime(sav_grouping_df['Date']).dt.to_period("M")
        self.sav_mon_grouped_times = sav_grouping_df.groupby(grouper).agg({'Savings Value ($)': 'max'}).reset_index()
        grouper = pd.to_datetime(inv_grouping_df['Date']).dt.to_period("M")
        self.inv_mon_grouped_times = inv_grouping_df.groupby(grouper).agg({'Predicted Investment Value ($)': 'max'}).reset_index()
        self.no_months = len(self.inv_mon_grouped_times)
        self.date_list_month = self.inv_mon_grouped_times['Date'].to_numpy()
        try:
            self.month_df_len = self.month_table_array.shape[0]
        except:
            pass

        # Create a value with the final value from the savings and investment predictions.
        self.fin_sav_month = self.sav_mon_grouped_times['Savings Value ($)'].iloc[-1]
        self.fin_inv_month = self.inv_mon_grouped_times['Predicted Investment Value ($)'].iloc[-1]
        self.fin_sav_year = self.sav_year_grouped_times['Savings Value ($)'].iloc[-1]
        self.fin_inv_year = self.inv_year_grouped_times['Predicted Investment Value ($)'].iloc[-1]
        
        # Create a formatted $ value for display
        format_mapping_sav = '${:,.2f}'.format
        format_mapping_inv = '${:,.2f}'.format
        self.form_fin_sav_month =  format_mapping_sav(self.fin_sav_month)
        self.form_fin_sav_year = format_mapping_sav(self.fin_sav_year)
        self.form_fin_inv_month =  format_mapping_inv(self.fin_inv_month)
        self.form_fin_inv_year = format_mapping_inv(self.fin_inv_year)
        
    # Pie plot the total values in the appropriate widgets
    def piePlotMonth(self):
        self.donut_theo_m = QtChart.QPieSeries()
        self.donut_theo_m.setHoleSize(0.40)
         
        self.m_sav_slice = self.donut_theo_m.append("Predicted Savings ($): " + str(self.form_fin_sav_month), self.fin_sav_month)
        self.m_sav_slice.setLabelVisible(True)
        
        self.m_inv_slice = self.donut_theo_m.append("Predicted Investment ($): " + str(self.form_fin_inv_month), self.fin_inv_month)
        self.m_inv_slice.setLabelVisible(True)
        
        self.donut_theo_m.setObjectName("donut_theo_m")
    

        # Set up a chart to hold the plot
        chart = QtChart.QChart()
        chart.addSeries(self.donut_theo_m)
        chart.setAnimationOptions(QtChart.QChart.SeriesAnimations)
        chart.setTitle("Predicted End-Period Total Savings and Investment ($)")
        chart.setTheme(QtChart.QChart.ChartThemeQt)

        chartview = QtChart.QChartView(chart)

        self.tot_m_grid_layout.addWidget(chartview,0, 1, 1, 1)
        # self.setLayout(vbox)
    
    def piePlotYear(self):
        self.donut_theo_y = QtChart.QPieSeries()
        self.donut_theo_y.setHoleSize(0.40)
         
        self.y_sav_slice = self.donut_theo_y.append("Predicted Savings ($): " + str(self.form_fin_sav_year), self.fin_sav_year)
        self.y_sav_slice.setLabelVisible(True)
        
        self.y_inv_slice = self.donut_theo_y.append("Predicted Investment ($): " + str(self.form_fin_inv_year), self.fin_inv_year)
        self.y_inv_slice.setLabelVisible(True)
        
        self.donut_theo_y.setObjectName("donut_theo_m")
    

        # Set up a chart to hold the plot
        chart = QtChart.QChart()
        chart.addSeries(self.donut_theo_y)
        chart.setAnimationOptions(QtChart.QChart.SeriesAnimations)
        chart.setTitle("Predicted End-Period Total Savings and Investment ($)")
        chart.setTheme(QtChart.QChart.ChartThemeQt)

        chartview = QtChart.QChartView(chart)

        self.tot_y_grid_layout.addWidget(chartview,0, 2, 1, 1)
        # self.setLayout(vbox)
   
    # Define a function to fill known values into the user tables and make them non-editable
    def fillMonthYearTab(self):
        
        # Set the columns to consider
        col_months = [0, 1, 2, 3]
        col_years = [0, 1, 2, 3]
        
        # Set a variable to the number of months in the existing year and month np array, or to the total months/years if that doesn't exist
        try:
            no_months = self.month_df_len
        except:
            no_months = self.no_months
        
        try:
            no_years = self.year_df_len
        except:
            no_years = self.no_years
        
        if self.user_month_table_flag == 1:
                       
            for row in range(no_months):
                for col in col_months:
                    if col == 0:
                        
                        pass
                   
                    elif col == 3:
                        item = QtWidgets.QTableWidgetItem()
                        try:
                            item.setText(str(round(float(self.table_m_2.item(row, col - 1).text()) + float(self.table_m_2.item(row, col - 2).text()), 2)))
                        except:
                           item.setText(str(0.0)) 
                        item.setFlags(QtCore.Qt.ItemIsEnabled)
                        self.table_m_2.setItem(row, col, item)   
                        
                    else:
                        # Set this to the sum of the savings and interest columns
                        item = QtWidgets.QTableWidgetItem()
                        item.setText(str(round(float(self.month_table_array[row, col - 1]), 2)))
                        self.table_m_2.setItem(row, col, item)
            
            for row in range(self.no_months):
                for col in col_months:
                    if col == 0:
                        
                        item = QtWidgets.QTableWidgetItem()
                        item.setFlags(QtCore.Qt.ItemIsEnabled)
                        item.setText(str(self.date_list_month[row]))
                        self.table_m_2.setItem(row, col, item)
                        
                    else:
                        if self.table_m_2.item(row, col) is None:
                            item = QtWidgets.QTableWidgetItem()
                            item.setText(str(0.0))
                            self.table_m_2.setItem(row, col, item)
                        else:
                            pass
        else:
            for row in range(self.no_months):
                for col in col_months:
                    if col == 0:
                        
                        item = QtWidgets.QTableWidgetItem()
                        item.setFlags(QtCore.Qt.ItemIsEnabled)
                        item.setText(str(self.date_list_month[row]))
                        self.table_m_2.setItem(row, col, item)
                    elif col == 3:
                        item = QtWidgets.QTableWidgetItem()
                        item.setText(str(round(float(self.table_m_2.item(row, col - 1).text()) + float(self.table_m_2.item(row, col - 2).text()), 2)))
                        item.setFlags(QtCore.Qt.ItemIsEnabled)
                        self.table_m_2.setItem(row, col, item)
                    else:
                        # Set this to the sum of the savings and interest columns
                        item = QtWidgets.QTableWidgetItem()
                        item.setText(str(0.0))
                        self.table_m_2.setItem(row, col, item)
        
        if self.user_year_table_flag == 1:
                        
            for row in range(no_years):
                for col in col_years:
                    if col == 0:
                        
                        pass
                   
                    elif col == 3:
                        item = QtWidgets.QTableWidgetItem()
                        try:
                            item.setText(str(round(float(self.table_y_2.item(row, col - 1).text()) + float(self.table_y_2.item(row, col - 2).text()), 2)))
                        except:
                           item.setText(str(0.0)) 
                        item.setFlags(QtCore.Qt.ItemIsEnabled)
                        self.table_y_2.setItem(row, col, item)   
                        
                    else:
                        # Set this to the sum of the savings and interest columns
                        item = QtWidgets.QTableWidgetItem()
                        item.setText(str(round(float(self.year_table_array[row, col - 1]), 2)))
                        self.table_y_2.setItem(row, col, item)
            
            for row in range(self.no_years):
                for col in col_years:
                    if col == 0:
                        
                        item = QtWidgets.QTableWidgetItem()
                        item.setFlags(QtCore.Qt.ItemIsEnabled)
                        item.setText(str(self.date_list_year[row]))
                        self.table_y_2.setItem(row, col, item)
                        
                    else:
                        if self.table_y_2.item(row, col) is None:
                            item = QtWidgets.QTableWidgetItem()
                            item.setText(str(0.0))
                            self.table_y_2.setItem(row, col, item)
                        else:
                            pass
        else:
            for row in range(self.no_years):
                for col in col_years:
                    if col == 0:
                        
                        item = QtWidgets.QTableWidgetItem()
                        item.setFlags(QtCore.Qt.ItemIsEnabled)
                        item.setText(str(self.date_list_year[row]))
                        self.table_y_2.setItem(row, col, item)
                    elif col == 3:
                        item = QtWidgets.QTableWidgetItem()
                        item.setText(str(round(float(self.table_y_2.item(row, col - 1).text()) + float(self.table_y_2.item(row, col - 2).text()), 2)))
                        item.setFlags(QtCore.Qt.ItemIsEnabled)
                        self.table_y_2.setItem(row, col, item)
                    else:
                        # Set this to the sum of the savings and interest columns
                        item = QtWidgets.QTableWidgetItem()
                        item.setText(str(0.0))
                        self.table_y_2.setItem(row, col, item)
                        
        # Convert to np array for the tables if the array doesn't exist
        if self.user_month_table_flag == 0:
            self.month_table_array = np.zeros([self.no_months , 3])      
            self.user_month_table_flag = 1
            
            # If the user table does not exist save it for loading next time
            with open(self.month_rt_path, 'w') as file:     
                np.savetxt(file, self.month_table_array, fmt = '%.2f') 
        else:
            pass
            
    # Convert to np array for the tables if the array doesn't exist
        if self.user_year_table_flag == 0:
             self.year_table_array = np.zeros([self.no_years , 3]) 
             self.user_year_table_flag = 1
             
             # If the user table doesn't exist, just save it so it can be loaded next time
             with open(self.year_rt_path, 'w') as file:     
                 np.savetxt(file, self.year_table_array, fmt = '%.2f') 
        else:
             pass
         
        # Set initial flags to keep track of changes, noting that 0 = True for boolean logic
        self.changed_month_array_flag = 1
        self.changed_year_array_flag = 1
        
    # Define a month function handling item changes in the user tables
    def itemChangedByUserMonth(self):
        # Check if the item is a number (disallow if it is not) and re-adjust flags
        try:
            if self.column() == 0:
                global change_row 
                change_row = self.row()
                global change_col
                change_col = self.column()
            else:
                if self is None:
                    pass
                else:
                    test_for_numerical = float(self.text())
                    change_row = self.row()
                    change_col = self.column()
                    global res_flag
                    res_flag = 1
                
        except:
            if self.column == 0:
                pass
            else:
                if self is None:
                    pass
                else:
                    warning_msgbox = QtWidgets.QMessageBox()
                    warning_msgbox.setText("Non-numerical inputs are not accepted for plotting reasons.")
                    warning_msgbox.exec()
                    # Reset the value to it's previous value
                    self.setText(str(0.0))
                    # Flag to reset the change
                    res_flag = 0
      
    # Create a function to handle user changes at the year level
    def itemChangedByUserYear(self):
        # Check if the item is a number (disallow if it is not) and re-adjust flags
        try:
            if self.column() == 0:
                global change_row 
                change_row = self.row()
                global change_col
                change_col = self.column()
            else:
                if self is None:
                    pass
                else:
                    test_for_numerical = float(self.text())
                    change_row = self.row()
                    change_col = self.column()
                    global res_flag
                    res_flag = 1
                
        except:
            if self.column == 0:
                pass
            else:
                if self is None:
                    pass
                else:
                    warning_msgbox = QtWidgets.QMessageBox()
                    warning_msgbox.setText("Non-numerical inputs are not accepted for plotting reasons.")
                    warning_msgbox.exec()
                    # Reset the value to it's previous value
                    self.setText(str(0.0))
                    # Flag to reset the change
                    res_flag = 0

    def flagReseterMonth(self):
        try:
            if change_col == 0:
                self.changed_month_array_flag = 1
            else:
                if str(round(float(self.table_m_2.item(change_row, change_col).text()), 2)) == str(round(float(self.test_month_table_array[change_row, change_col - 1]),2)):
                    self.changed_month_array_flag = 1
                    # warning_msgbox = QtWidgets.QMessageBox()
                    # warning_msgbox.setText("The change flag value is now: " + str(self.changed_month_array_flag))
                    # warning_msgbox.exec()
                else:
                    if res_flag == 0:
                        self.changed_month_array_flag = 1
                        self.table_m_2.item(change_row, change_col).setText(str(self.month_table_array[change_row, change_col - 1]))
                        # warning_msgbox = QtWidgets.QMessageBox()
                        # warning_msgbox.setText("The change flag value is now: " + str(self.changed_month_array_flag))
                        # warning_msgbox.exec()
                    else:
                        self.changed_month_array_flag = 0
                        # For checking the value is set correctly
                        # warning_msgbox = QtWidgets.QMessageBox()
                        # warning_msgbox.setText("The change flag value is now: " + str(self.changed_month_array_flag))
                        # warning_msgbox.exec()
                
                # Add the user change flag to the change flag dictionary and use that to set the final flag value
                dic_key = str(change_row) + ":" + str(change_col)
                self.user_changes_month[dic_key] = self.changed_month_array_flag
                self.user_check_dic_m[dic_key] = 1
                # warning_msgbox = QtWidgets.QMessageBox()
                # warning_msgbox.setText("The change flag vec length is now: " + str(len(self.user_changes_month)))
                # warning_msgbox.exec()
        except:
            # Assume that bounds changed here
            self.changed_month_array_flag = 0
            dic_key = str(change_row) + ":" + str(change_col)
            self.user_changes_month[dic_key] = self.changed_month_array_flag
            self.user_check_dic_m[dic_key] = 1
            
        
        
    def flagReseterYear(self):
        try:
            if change_col == 0:
                self.changed_year_array_flag = 1
            else:
                if str(round(float(self.table_y_2.item(change_row, change_col).text()), 2)) == str(round(float(self.test_year_table_array[change_row, change_col - 1]),2)):
                    self.changed_year_array_flag = 1
                    # warning_msgbox = QtWidgets.QMessageBox()
                    # warning_msgbox.setText("The change flag value is now: " + str(self.changed_month_array_flag))
                    # warning_msgbox.exec()
                else:
                    if res_flag == 0:
                        self.changed_year_array_flag = 1
                        self.table_y_2.item(change_row, change_col).setText(str(self.year_table_array[change_row, change_col - 1]))
                        # warning_msgbox = QtWidgets.QMessageBox()
                        # warning_msgbox.setText("The change flag value is now: " + str(self.changed_month_array_flag))
                        # warning_msgbox.exec()
                    else:
                        self.changed_year_array_flag = 0
                        # For checking the value is set correctly
                        # warning_msgbox = QtWidgets.QMessageBox()
                        # warning_msgbox.setText("The change flag value is now: " + str(self.changed_month_array_flag))
                        # warning_msgbox.exec()
                
                # Add the user change flag to the change flag dictionary and use that to set the final flag value
                dic_key = str(change_row) + ":" + str(change_col)
                self.user_changes_year[dic_key] = self.changed_year_array_flag
                self.user_check_dic_y[dic_key] = 1
                # warning_msgbox = QtWidgets.QMessageBox()
                # warning_msgbox.setText("The change flag vec length is now: " + str(len(self.user_changes_month)))
                # warning_msgbox.exec()
        except:
            # If there is an out of bounds error assume that we changed axis
            self.changed_year_array_flag = 0
            dic_key = str(change_row) + ":" + str(change_col)
            self.user_changes_year[dic_key] = self.changed_year_array_flag
            self.user_check_dic_y[dic_key] = 1
            
    # Define a function settting the parameters tab plot
    def parTabPlot(self):
               
        # Calculate the total predicted savings an interest values
        pred_sav = self.overall_dates['Savings Value ($)'].to_numpy()
        pred_inv = self.df_inv['Predicted Investment Value ($)'].to_numpy()
        pred_tot = pred_sav + pred_inv
        overall_tots = self.df_inv.copy()
        overall_tots['Predicted Total Value ($)'] = pred_tot
        
        # Group the total table by year for plotting
        grouper = pd.to_datetime(overall_tots['Date']).dt.to_period("Y")
        grouped_times = overall_tots.groupby(grouper).agg({'Predicted Total Value ($)': 'max'}).reset_index()
         
        # Set investment variables and a format to set the values for the dates to date strings
        self.tot_x = [*range(grouped_times.shape[0])]
        self.tot_y = grouped_times['Predicted Total Value ($)'].to_numpy()
        # Set a format
        format_mapping={'Date': '{:}', 'Predicted Total Value ($)': '${:,.2f}'}
        for key, value in format_mapping.items():
            grouped_times[key] =  grouped_times[key].apply(value.format)
        self.tot_format = [*zip(self.tot_x, grouped_times.Date.to_numpy())]
        self.tot_format_y = [*zip(self.tot_y, grouped_times['Predicted Total Value ($)'].to_numpy())]

        # Plot the predicted investment value
        self.key_plot_widget = pyqtgraph.PlotWidget()
        self.key_plot_widget.setStyleSheet("background-color: rgb(88, 84, 129);")
        self.key_plot_widget.setObjectName("key_plot_widget")
        self.leg_kp = self.key_plot_widget.addLegend()
        self.second_plot_kp = self.key_plot_widget.plotItem
        self.key_plot_widget.setStyleSheet("background-color: rgb(88, 84, 129);")
        self.key_plot_widget.setObjectName("key_plot_widget")
        self.verticalLayout_222 = QtWidgets.QVBoxLayout(self.key_plot_widget)
        self.verticalLayout_222.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout_222.setObjectName("verticalLayout_222")
        self.verticalLayout_202 = QtWidgets.QVBoxLayout()
        self.verticalLayout_202.setObjectName("verticalLayout_202")
        self.verticalLayout_222.addLayout(self.verticalLayout_202)
        
        # Plot the savings values
        pen = pyqtgraph.mkPen(color = (163,247,181), width = 4)
        self.kp_sav_line = self.key_plot_widget.plot(x = self.sav_x, y = self.sav_y, labels = self.sav_format, pen = pen, symbol = 'o', symbolBrush = (75, 143, 140), name = "Predicted Savings Value ($)")
        self.key_plot_widget.setMouseEnabled(x = True, y = True) 
        
        # Plot the interest values
        pen = pyqtgraph.mkPen(color = (211,196,227), width = 4)
        self.inv_line_kp = pyqtgraph.PlotDataItem(x = self.inv_x, y = self.inv_y, labels = self.inv_format, pen = pen, symbol = 'o', symbolBrush = (88, 84, 129), name = "Predicted Investment Value ($)")
        self.key_plot_widget.addItem(self.inv_line_kp)
        
        # Plot the cumulative value and reset the tick marks based on the values
        pen = pyqtgraph.mkPen(color = (195,223,224), width = 4)
        self.tot_line_kp = pyqtgraph.PlotDataItem(x = self.tot_x, y = self.tot_y, labels = self.tot_format, pen = pen, symbol = 'o', symbolBrush = (109, 104, 117), name = "Predicted Total Value ($)")
        self.key_plot_widget.addItem(self.tot_line_kp)
        
        #   Pass the list in, *in* a list.
        self.ax_kp = self.key_plot_widget.getAxis('bottom')     
        self.ax2_kp = self.key_plot_widget.getAxis('left')
        self.ax_kp.setTicks([self.tot_format])
        self.ax2_kp.setTicks([self.tot_format_y])
        
        # Format the totals plot
        self.key_plot_widget.setBackground('w')
        self.key_plot_widget.showGrid(x = True, y = True)
        tickFont = QtGui.QFont()
        tickFont.setPointSize(4)
        self.key_plot_widget.getAxis('left').tickFont = tickFont
        self.key_plot_widget.setTitle("Overall Predictions with Year ($)", size="16pt")
        self.key_plot_widget.setLabel('left', 'Prediction ($)', size = '16pt')
        self.key_plot_widget.setLabel('bottom', 'Year', size = '16pt')
        font=QtGui.QFont()
        font.setPixelSize(10)
        self.key_plot_widget.getAxis("bottom").setStyle(tickFont = font)
        self.key_plot_widget.getAxis("left").setStyle(tickFont = font)
        
        self.key_plot_layout.addWidget(self.key_plot_widget)
        self.key_derived_layout.addLayout(self.key_plot_layout)
   
    # Create a function to plot user-defined values on the user-defined tabs
    def userDefPlots(self):
        
        # Use the current year to set limits for the final month plot (so it does not become overloaded with data)
        today = datetime.date.today()
        st_date = datetime.datetime.strptime(self.df_fill_parameters['def_init_contrib_date'], "%d/%m/%Y").date()
        st_year = st_date.year
        time_since_start = (int(today.year) - int(st_year)) * 12 
        
        # This is evidently the area having a problem on reloading the data
        month_array = np.add(self.month_table_array[:,0].astype(np.float), self.month_table_array[:,1].astype(np.float))  
        year_array = np.add(self.year_table_array[:,0].astype(np.float), self.year_table_array[:,1].astype(np.float))
        x_y_array = [*range(len(year_array))]
        x_m_array = [*range(len(month_array))]
        
        # Calculate the total predicted savings an interest values
        pred_sav = self.overall_dates['Savings Value ($)'].to_numpy()
        pred_inv = self.df_inv['Predicted Investment Value ($)'].to_numpy()
        pred_tot = pred_sav + pred_inv
        overall_tots = self.df_inv.copy()
        overall_tots['Predicted Total Value ($)'] = pred_tot
        
        # Group the total table by year for plotting
        grouper_1 = pd.to_datetime(overall_tots['Date']).dt.to_period("Y")
        grouped_times_1 = overall_tots.groupby(grouper_1).agg({'Predicted Total Value ($)': 'max'}).reset_index()
        
        # Group the total table by month for plotting
        grouper_2 = pd.to_datetime(overall_tots['Date']).dt.to_period("M")
        grouped_times_2 = overall_tots.groupby(grouper_2).agg({'Predicted Total Value ($)': 'max'}).reset_index()
        
        # Set investment variables and a format to set the values for the dates to date strings
        self.tot_x = [*range(grouped_times_1.shape[0])]
        self.tot_y = grouped_times_1['Predicted Total Value ($)'].to_numpy()

        # Set investment variables and a format to set the values for the dates to date strings at a month level
        self.tot_x_m = [*range(grouped_times_2.shape[0])]
        self.tot_y_m = grouped_times_2['Predicted Total Value ($)'].to_numpy()
        
        # Set a format
        format_mapping={'Date': '{:}', 'Predicted Total Value ($)': '${:,.2f}'}
        for key, value in format_mapping.items():
            grouped_times_2[key] =  grouped_times_2[key].apply(value.format)
        self.tot_format_m = [*zip(self.tot_x_m, grouped_times_2.Date.to_numpy())]
        self.tot_format_m_y = [*zip(self.tot_y_m, grouped_times_2['Predicted Total Value ($)'].to_numpy())]
        
        # Plot the predicted yearly total value with user values
        self.user_y_plot_widget = pyqtgraph.PlotWidget()
        self.user_y_plot_widget.setStyleSheet("background-color: rgb(88, 84, 129);")
        self.user_y_plot_widget.setObjectName("user_y_plot_widget")
        self.leg_user_y = self.user_y_plot_widget.addLegend()
        self.second_plot_user_y = self.user_y_plot_widget.plotItem
        self.verticalLayout_2322 = QtWidgets.QVBoxLayout(self.user_y_plot_widget)
        self.verticalLayout_2322.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout_2322.setObjectName("verticalLayout_2322")
        self.verticalLayout_2302 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2302.setObjectName("verticalLayout_2302")
        self.verticalLayout_2322.addLayout(self.verticalLayout_2302)

        # Plot the cumulative value and reset the tick marks based on the values
        pen = pyqtgraph.mkPen(color = (163,247,181), width = 4)
        try:
            self.tot_line_user_y = pyqtgraph.PlotDataItem(x = x_y_array, y = year_array, pen = pen, symbol = 'o', symbolBrush = (109, 104, 117), name = "User Total Value ($)")
            self.user_y_plot_widget.addItem(self.tot_line_user_y)
        except:
            self.tot_line_user_y = pyqtgraph.PlotDataItem(x = self.tot_x, y = np.zeros([len(self.tot_x), 1]), pen = pen, symbol = 'o', symbolBrush = (109, 104, 117), name = "User Total Value ($)")
            self.user_y_plot_widget.addItem(self.tot_line_user_y)
        
        # Plot the cumulative value and reset the tick marks based on the values
        pen = pyqtgraph.mkPen(color = (195,223,224), width = 4)
        self.tot_line_y = pyqtgraph.PlotDataItem(x = self.tot_x, y = self.tot_y, labels = self.tot_format, pen = pen, symbol = 'o', symbolBrush = (75, 143, 140), name = "Predicted Total Value ($)")
        self.user_y_plot_widget.addItem(self.tot_line_y)

        #   Pass the list in, *in* a list.
        self.ax_uy = self.user_y_plot_widget.getAxis('bottom')     
        self.ax2_uy = self.user_y_plot_widget.getAxis('left')
        self.ax_uy.setTicks([self.tot_format])
        self.ax2_uy.setTicks([self.tot_format_y])
        
        # Format the totals plot
        self.user_y_plot_widget.setBackground('w')
        self.user_y_plot_widget.showGrid(x = True, y = True)
        tickFont = QtGui.QFont()
        tickFont.setPointSize(4)
        self.user_y_plot_widget.getAxis('left').tickFont = tickFont
        self.user_y_plot_widget.setTitle("User Totals vs Overall Predictions with Year ($)", size="16pt")
        self.user_y_plot_widget.setLabel('left', 'Value ($)', size = '16pt')
        self.user_y_plot_widget.setLabel('bottom', 'Year', size = '16pt')
        font=QtGui.QFont()
        font.setPixelSize(10)
        self.user_y_plot_widget.getAxis("bottom").setStyle(tickFont = font)
        self.user_y_plot_widget.getAxis("left").setStyle(tickFont = font)
        
        self.tot_y_grid_layout.addWidget(self.user_y_plot_widget, 0, 0, 1, 1)

        # Plot the predicted monthly total value with user values
        self.user_m_plot_widget = pyqtgraph.PlotWidget()
        self.user_m_plot_widget.setStyleSheet("background-color: rgb(88, 84, 129);")
        self.user_m_plot_widget.setObjectName("user_m_plot_widget")
        self.leg_user_m = self.user_m_plot_widget.addLegend()
        self.second_plot_user_m = self.user_m_plot_widget.plotItem
        self.verticalLayout_2422 = QtWidgets.QVBoxLayout(self.user_m_plot_widget)
        self.verticalLayout_2422.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout_2422.setObjectName("verticalLayout_2422")
        self.verticalLayout_2402 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2402.setObjectName("verticalLayout_2402")
        self.verticalLayout_2422.addLayout(self.verticalLayout_2402)

        # Plot the cumulative value and reset the tick marks based on the values
        pen = pyqtgraph.mkPen(color = (163,247,181), width = 4)
        try:
            self.tot_line_user_m = pyqtgraph.PlotDataItem(x = x_m_array, y = month_array, pen = pen, symbol = 'o', symbolBrush = (109, 104, 117), name = "User Total Value ($)")
            self.user_m_plot_widget.addItem(self.tot_line_user_m)
        except:
            self.tot_line_user_m = pyqtgraph.PlotDataItem(x = self.tot_x_m, y = np.zeros([len(self.tot_x_m), 1]), pen = pen, symbol = 'o', symbolBrush = (109, 104, 117), name = "User Total Value ($)")
            self.user_m_plot_widget.addItem(self.tot_line_user_m)
        
        # Plot the cumulative value and reset the tick marks based on the values
        pen = pyqtgraph.mkPen(color = (195,223,224), width = 4)
        self.tot_line_m = pyqtgraph.PlotDataItem(x = self.tot_x_m, y = self.tot_y_m, labels = self.tot_format_m, pen = pen, symbol = 'o', symbolBrush = (75, 143, 140), name = "Predicted Total Value ($)")
        self.user_m_plot_widget.addItem(self.tot_line_m)

        #   Pass the list in, *in* a list.
        self.ax_um = self.user_m_plot_widget.getAxis('bottom')     
        self.ax2_um = self.user_m_plot_widget.getAxis('left')
        self.ax_um.setTicks([self.tot_format_m])
        self.ax2_um.setTicks([self.tot_format_m_y])
        
        # Format the totals plot
        self.user_m_plot_widget.setBackground('w')
        self.user_m_plot_widget.showGrid(x = True, y = True)
        tickFont = QtGui.QFont()
        tickFont.setPointSize(4)
        self.user_m_plot_widget.getAxis('left').tickFont = tickFont
        self.user_m_plot_widget.setTitle("User Totals vs Overall Predictions with Month and Year ($)", size="16pt")
        self.user_m_plot_widget.setLabel('left', 'Value ($)', size = '16pt')
        self.user_m_plot_widget.setLabel('bottom', 'Year', size = '16pt')
        font=QtGui.QFont()
        font.setPixelSize(10)
        self.user_m_plot_widget.getAxis("bottom").setStyle(tickFont = font)
        self.user_m_plot_widget.getAxis("left").setStyle(tickFont = font)
        self.user_m_plot_widget.setRange(xRange=[time_since_start, time_since_start + 10], yRange = [0, self.tot_y_m[time_since_start + 11]])
        
        self.tot_m_grid_layout.addWidget(self.user_m_plot_widget, 0, 0, 1, 1)
        # self.key_plot_layout.addWidget(self.user_y_plot_widget)
        # self.key_derived_layout.addLayout(self.key_plot_layout)


    # Define a rerun and re-display method
    def rerunAndRedisplay(self):
        
        # Run the base calculations again
        relevantFunctions.rerunParams(self)
        
        # Reset the savings table and plot
        sav_pred_set_new = pandasModel(self.output_sav_table)
        self.table_sav.setModel(sav_pred_set_new)
        
        # Plot the predicted savings
        # Clear the widget and re-plot
        self.plot_sav.deleteLater()
        self.plot_sav = pyqtgraph.PlotWidget()
        leg = self.plot_sav.addLegend()
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
        
        sav_int_curve = pyqtgraph.PlotDataItem(x= self.sav_x, y = self.sav_int_y, pen = pyqtgraph.mkPen(color = (211,196,227), width = 4), symbol = 'o', symbolBrush = (88, 84,129))
        self.sav_int_plot.addItem(sav_int_curve)
        leg.addItem(sav_int_curve, "Yearly Interest ($)")

        # Format the savings plot
        self.plot_sav.setBackground('w')
        self.plot_sav.showGrid(x=True, y=True)
        self.plot_sav.setTitle("Predicted Savings with Year ($)", size="16pt")
        self.plot_sav.setLabel('left', 'Savings ($)', size = '16pt')
        self.plot_sav.setLabel('bottom', 'Year', size = '16pt')
        self.plot_sav.setLabel('right', 'Interest ($ per year)', size = '16pt')

        self.pred_sav_vert_layout.addWidget(self.plot_sav)
        
        # Reset the investment table
        inv_pred_set_new = pandasModel(self.df_inv_disp)
        self.tab_inv.setModel(inv_pred_set_new)
        
        # Clear the Investment plot widget and re-plot
        self.plot_inv.deleteLater()
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
        
        # Plot the predicted totals
        # Clear the widget and re-plot
        self.key_plot_widget.deleteLater()
        relevantFunctions.parTabPlot(self)
               
        # UPDATE USER TABLES
        # Create an array to track user changes to the orginal loaded or last-entered user datasets

        self.year_table_array = np.empty([self.no_years , 3])
        for row in range(self.no_years):
            for col in range(1, 3):
                self.year_table_array[row, col - 1] =  str(self.table_y_2.item(row, col).text())
        
        self.month_table_array = np.empty([self.no_months , 3])
        for row in range(self.no_months):
            for col in range(1, 3):
                self.month_table_array[row, col - 1] =  str(self.table_m_2.item(row, col).text())
          
        # Replot the monthly and yearly pie charts
        relevantFunctions.genTotVals(self)
        self.donut_theo_y.remove(self.y_sav_slice)
        self.donut_theo_y.remove(self.y_inv_slice)
        self.y_sav_slice = self.donut_theo_y.append("Predicted Savings ($): " + str(self.form_fin_sav_year), self.fin_sav_year)
        self.y_sav_slice.setLabelVisible(True)
        
        self.y_inv_slice = self.donut_theo_y.append("Predicted Investment ($): " + str(self.form_fin_inv_year), self.fin_inv_year)
        self.y_inv_slice.setLabelVisible(True)
        
        self.donut_theo_m.remove(self.m_sav_slice)
        self.donut_theo_m.remove(self.m_inv_slice)
        self.m_sav_slice = self.donut_theo_m.append("Predicted Savings ($): " + str(self.form_fin_sav_month), self.fin_sav_month)
        self.m_sav_slice.setLabelVisible(True)
        
        self.m_inv_slice = self.donut_theo_m.append("Predicted Investment ($): " + str(self.form_fin_inv_month), self.fin_inv_month)
        self.m_inv_slice.setLabelVisible(True)
        
        # Reset the user tables
        self.table_m_2.clear()
        self.table_y_2.clear()
        # Reset the number of rows
        self.table_y_2.setRowCount(self.no_years)
        self.table_m_2.setRowCount(self.no_months)
        # Reset the column headers
        self.table_m_2.setHorizontalHeaderLabels(["Year", "Savings Total ($)", "Inv. Total ($)", "Total ($)"] )
        self.table_y_2.setHorizontalHeaderLabels(["Year", "Savings Total ($)", "Inv. Total ($)", "Total ($)"] )
        # Rerun the auto-filler
        relevantFunctions.fillMonthYearTab(self)
        
        # Plot twice to account for years potentially changing thorugh user changes
        self.year_table_array = np.empty([self.no_years , 3])
        for row in range(self.no_years):
            for col in range(1, 3):
                self.year_table_array[row, col - 1] =  str(self.table_y_2.item(row, col).text())
        
        self.month_table_array = np.empty([self.no_months , 3])
        for row in range(self.no_months):
            for col in range(1, 3):
                self.month_table_array[row, col - 1] =  str(self.table_m_2.item(row, col).text())
        relevantFunctions.fillMonthYearTab(self)

        # Plot the user monthly and yearly values
        self.user_m_plot_widget.deleteLater()
        self.user_y_plot_widget.deleteLater()
        relevantFunctions.userDefPlots(self)
        
        # Reset the displayed formulas
        _translate = QtCore.QCoreApplication.translate
        self.sav_formula.setText(_translate("TabWidget", ftfy.fix_text(u"I\u209c = P\u209c\u208b\u2081(1 +" + str(round(self.df_fill_parameters["def_sav_int_rt"]/100, 5)) + u"\u00b7 365\u207b\u00b9 )\u00b3\u2076\u2075\u1d48\u2e0d\u00b3\u2076\u2075 - P\u209c\u208b\u2081")))
        self.inv_formula.setText(_translate("TabWidget", ftfy.fix_text(u"I\u209c = P\u209c\u208b\u2081(1 + " + str(round(self.df_fill_parameters["def_inv_int_rt"]/100, 5)) + u"d / 365)")))

    # Define a method for saving user changes to the user defined parameters
    def saveUserParams(self):
        
        # Make sure the output files are up to date
        relevantFunctions.rerunParams(self)
        
        # Set the test dataframes to the current dataframes to bypass the question box on exit
        self.test_overall_dates = self.overall_dates.copy()
        self.test_output_sav_table = self.output_sav_table.copy()
        self.test_df_inv = self.df_inv.copy()
        
        # Save the user-defined parameters
        with open(self.user_path, 'w') as user_inp: 
            user_inp.write(json.dumps(self.df_fill_parameters))
        
        # Dump the further outputs
        with open(self.full_sav_2, 'wb') as file:
            self.overall_dates.to_pickle(file)
        
        # Dump the investment values
        with open(self.full_inv_path_2, 'wb') as file:
            self.df_inv.to_pickle(file)
        
        # Conditionally write the user-defined values to the user folder and reset the flags so the exit check does not trigger
        if self.user_month_table_flag == 1:
            with open(self.month_rt_path, 'w') as file:     
                np.savetxt(file, self.month_table_array, fmt = '%.2f')
            self.changed_month_array_flag = 1
            try:
                del self.test_month_table_array
            except:
                pass
            self.test_month_table_array = self.month_table_array.copy()
        
        if self.user_year_table_flag == 1:
            with open(self.year_rt_path, 'w') as file:     
                np.savetxt(file, self.year_table_array, fmt = '%.2f')
            self.changed_year_array_flag = 1
            try:
                del self.test_year_table_array
            except:
                pass
            self.test_year_table_array = self.year_table_array.copy()
        
        # Delete and reset the user changes flag dictionaries to continue checking new changes
        del self.user_changes_month
        self.user_changes_month = {}
        del self.user_changes_year
        self.user_changes_year = {}
        del self.user_check_dic_m
        self.user_check_dic_m = {}
        del self.user_check_dic_y
        self.user_check_dic_y = {}
    
    # Create a program to define closing flags
    def defineCloseFlags(self):
        # Set the user change flags
        
        self.saving_lib = {"def_final_fy": int(self.key_end_yr_lineEdit.text()),
                          "def_init_contrib_date":str(self.key_op_first_contrib_date_lineEdit.text()) ,
                          "def_init_contrib_freq": str(self.key_op_contrib_freq_dropdown.currentText()),
                          "def_init_sav_contrib": int(self.key_sav_cont_lineEdit_2.text()),
                          "def_sav_int_rt": float(self.key_sav_int_rt_lineEdit_2.text()),
                          "def_pre_inv_sav_goal": int(self.key_sav_goal_lineEdit_2.text()),
                          "def_init_sav": self.ke_init_sav_lineEdit_2.text() ,
                          "def_pg_contrib": self.key_cust_goal_cont_lineEdit_2.text() ,
                          "def_psg_inv_contrib": int(self.key_inv_psg_lineEdit.text()),
                          "def_inv_int_rt": float(self.key_inv_int_rt_lineEdit.text()),
                          "def_init_inv": self.key_inv_op_init_lineEdit.text()
                          }

        for key in self.saving_lib:
            self.df_fill_parameters[key] = self.saving_lib[key] or self.df_fill_parameters[key] or []
            
        if self.checking_fill_parameters == self.df_fill_parameters:
            self.checking_par_flag = 1
        else:
            self.checking_par_flag = 0
            
        if self.user_changes_month == self.user_check_dic_m:
            self.final_month_array_flag = 1
        else:
            self.final_month_array_flag = 0
        
        if self.user_changes_year == self.user_check_dic_y:
            self.final_year_array_flag = 1
        else:
            self.final_year_array_flag = 0
    
    # Set text and text strings.
    def retranslateUi(self, TabWidget):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("TabWidget", "TabWidget"))
        self.sav_formula_label.setText(_translate("TabWidget", "Savings Interest Formula"))
        self.sav_formula.setToolTip(_translate("TabWidget", "<html><head/><body><p><span style=\" font-size:10pt;\">Compound interest formula applied to savings, with a per-annum rate applied daily and paid monthly.</span></p></body></html>"))
        self.sav_formula.setText(_translate("TabWidget", ftfy.fix_text(u"I\u209c = P\u209c\u208b\u2081(1 +" + str(round(self.df_fill_parameters["def_sav_int_rt"]/100, 5)) + u"\u00b7 365\u207b\u00b9 )\u00b3\u2076\u2075\u1d48\u2e0d\u00b3\u2076\u2075 - P\u209c\u208b\u2081")))
        self.inv_formula_label.setText(_translate("TabWidget", "Investment Interest Formula"))
        self.inv_formula.setToolTip(_translate("TabWidget", "<html><head/><body><p><span style=\" font-size:10pt;\">Simple interest applied with a per-annum rate to investments.</span></p></body></html>"))
        self.inv_formula.setText(_translate("TabWidget", ftfy.fix_text(u"I\u209c = P\u209c\u208b\u2081(1 + " + str(round(self.df_fill_parameters["def_inv_int_rt"]/100, 5)) + u"d / 365)")))
        self.key_save_push_button.setToolTip(_translate("TabWidget", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:400;\">Save the user inputs across each tab into the local app directory for loading the next time the app is opened.</span></p></body></html>"))
        self.key_save_push_button.setText(_translate("TabWidget", "Save User Inputs"))
        self.key_rerun_push_button.setToolTip(_translate("TabWidget", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:400;\">Run predictions and calculations for predicted rates using the specified General, Savings, and Investment parameters.</span></p></body></html>"))
        self.key_rerun_push_button.setText(_translate("TabWidget", "Re-run Calculations"))
        self.mon_save_push_button.setToolTip(_translate("TabWidget", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:400;\">Save the user inputs across each tab into the local app directory for loading the next time the app is opened.</span></p></body></html>"))
        self.mon_save_push_button.setText(_translate("TabWidget", "Save User Inputs"))
        self.mon_rerun_push_button.setToolTip(_translate("TabWidget", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:400;\">Run predictions and calculations for predicted rates using the specified General, Savings, and Investment parameters.</span></p></body></html>"))
        self.mon_rerun_push_button.setText(_translate("TabWidget", "Re-run Calculations"))
        self.year_save_push_button.setToolTip(_translate("TabWidget", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:400;\">Save the user inputs across each tab into the local app directory for loading the next time the app is opened.</span></p></body></html>"))
        self.year_save_push_button.setText(_translate("TabWidget", "Save User Inputs"))
        self.year_rerun_push_button.setToolTip(_translate("TabWidget", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:400;\">Run predictions and calculations for predicted rates using the specified General, Savings, and Investment parameters.</span></p></body></html>"))
        self.year_rerun_push_button.setText(_translate("TabWidget", "Re-run Calculations"))

        self.heading_label.setText(_translate("TabWidget", "Enter Key Assumptions:"))
        self.label.setText(_translate("TabWidget", "General Parameters"))
        self.key_end_yr_label.setToolTip(_translate("TabWidget", "<html><head/><body><p><span style=\" font-weight:400;\">End year for calculation (YYYY)</span></p></body></html>"))
        self.key_end_yr_label.setText(_translate("TabWidget", "Final Year of Consideration:\n"
"(YYYY)"))
        self.key_op_contrib_freq_label.setToolTip(_translate("TabWidget", "<html><head/><body><p><span style=\" font-weight:400;\">Optional field, select weekly, fortnightly or monthly.<br/><br/> The default is fortnightly.</span></p></body></html>"))
        self.key_op_contrib_freq_label.setText(_translate("TabWidget", "Custom Contribution Frequency:\n"
"(Optional ~ eg. weekly)"))
        self.key_op_first_contrib_label.setToolTip(_translate("TabWidget", "<html><head/><body><p><span style=\" font-weight:400;\">Optional field, fill with dd/mm/yyyy for first contribution to savings or investment.<br/><br/>Defaults to the current date if unfilled.</span></p></body></html>"))
        self.key_op_first_contrib_label.setText(_translate("TabWidget", "First Contribution Date:\n"
"(Optional ~ dd/mm/yyyy)"))
        self.key_end_yr_lineEdit.setToolTip(_translate("TabWidget", "<html><head/><body><p>End year for calculation, format YYYY.</p></body></html>"))
        self.key_end_yr_lineEdit.setText(_translate("TabWidget", str(self.df_fill_parameters["def_final_fy"])))
        self.key_op_first_contrib_date_lineEdit.setToolTip(_translate("TabWidget", "<html><head/><body><p>Optional field, fill with dd/mm/yyyy for first contribution to savings or investment.<br/><br/>Defaults to the current date if unfilled.</p></body></html>"))
        self.key_op_first_contrib_date_lineEdit.setText(_translate("TabWidget", str(self.df_fill_parameters["def_init_contrib_date"])))
        self.key_op_contrib_freq_dropdown.setToolTip(_translate("TabWidget", "<html><head/><body><p><span style=\" font-weight:400;\">Optional field, select weekly, fortnightly or monthly.<br/><br/> The default is fortnightly.</span></p></body></html>"))
        self.key_op_contrib_freq_dropdown.setCurrentText(str(self.df_fill_parameters["def_init_contrib_freq"]))
        self.sav_par_label_2.setText(_translate("TabWidget", "Savings Parameters"))
        self.key_sav_cont_label_2.setToolTip(_translate("TabWidget", "<html><head/><body><p><span style=\" font-weight:400;\">Unformatted number for the fornightly $ contributed to savings.</span></p></body></html>"))
        self.key_sav_cont_label_2.setText(_translate("TabWidget", "Initial Savings Contribution:\n"
"($ per Fortnight)"))
        self.key_sav_interest_rt_label_2.setToolTip(_translate("TabWidget", "<html><head/><body><p><span style=\" font-weight:400;\">Expected yearly compound interest p.a. across the period under examination (unformatted float). <br/><br/>Assumed to be applied to savings account as a per-annum rate compounded daily and paid monthly.</span></p></body></html>"))
        self.key_sav_interest_rt_label_2.setText(_translate("TabWidget", "Savings Interest Rate:\n"
"(% p.a.)"))
        self.key_sav_goal_label_2.setToolTip(_translate("TabWidget", "<html><head/><body><p><span style=\" font-weight:400;\">Amount of savings planned prior to commencing investment contributions, as an unformatted number.</span></p></body></html>"))
        self.key_sav_goal_label_2.setText(_translate("TabWidget", "Pre-Investment Savings Goal:\n"
"($ prior to commencing investing)"))
        self.key_op_init_sav_label_2.setToolTip(_translate("TabWidget", "<html><head/><body><p><span style=\" font-weight:400;\">Optional initial savings amount as an unformatted number.<br/><br/>Assumed to be 0 if unfilled.</span></p></body></html>"))
        self.key_op_init_sav_label_2.setText(_translate("TabWidget", "Initial Savings:\n"
"(Optional ~ $)"))
        self.key_op_pg_cont_label_2.setToolTip(_translate("TabWidget", "<html><head/><body><p><span style=\" font-weight:400;\">Optional post savings goal fortnightly contribution to savings as an unformatted number.</span></p><p><br/></p><p><span style=\" font-weight:400;\">Assumed to be $200 per fortnight if unfilled.</span></p></body></html>"))
        self.key_op_pg_cont_label_2.setText(_translate("TabWidget", "Custom Post-Goal Contribution:\n"
"(Optional ~ $ per Fortnight)"))
        self.key_sav_cont_lineEdit_2.setToolTip(_translate("TabWidget", "<html><head/><body><p>Unformatted number for the fornightly $ contributed to savings.</p></body></html>"))
        self.key_sav_cont_lineEdit_2.setText(_translate("TabWidget", str(self.df_fill_parameters["def_init_sav_contrib"])))
        self.key_sav_int_rt_lineEdit_2.setToolTip(_translate("TabWidget", "<html><head/><body><p>Expected yearly compound interest p.a. across the period under examination (unformatted float). <br/><br/>Assumed to be applied to savings account as a per-annum rate compounded daily and paid monthly.</p></body></html>"))
        self.key_sav_int_rt_lineEdit_2.setText(_translate("TabWidget", str(self.df_fill_parameters["def_sav_int_rt"])))
        self.key_sav_goal_lineEdit_2.setToolTip(_translate("TabWidget", "<html><head/><body><p>Amount of savings planned prior to commencing investment contributions, as an unformatted number.</p></body></html>"))
        self.key_sav_goal_lineEdit_2.setText(_translate("TabWidget", str(self.df_fill_parameters["def_pre_inv_sav_goal"])))
        self.ke_init_sav_lineEdit_2.setToolTip(_translate("TabWidget", "<html><head/><body><p>Optional initial savings amount as an unformatted number.<br/><br/>Assumed to be 0 if unfilled.</p></body></html>"))
        self.ke_init_sav_lineEdit_2.setText(_translate("TabWidget", str(self.df_fill_parameters["def_init_sav"])))
        self.key_cust_goal_cont_lineEdit_2.setToolTip(_translate("TabWidget", "<html><head/><body><p>Optional post savings goal fortnightly contribution to savings as an unformatted number.</p><p><br/></p><p>Assumed to be $200 per contribution period if unfilled.</p></body></html>"))
        self.key_cust_goal_cont_lineEdit_2.setText(_translate("TabWidget", str(self.df_fill_parameters["def_pg_contrib"])))
        self.inv_par_label.setText(_translate("TabWidget", "Investment Parameters"))
        self.key_inv_psg_label.setToolTip(_translate("TabWidget", "<html><head/><body><p><span style=\" font-weight:400;\">Unformatted number for the fornightly $ contributed to investments after reaching the specified savings goal.</span></p></body></html>"))
        self.key_inv_psg_label.setText(_translate("TabWidget", "Post-Savings Goal Contribution:\n"
"($ per Fortnight)"))
        self.key_inv_int_rt_label.setToolTip(_translate("TabWidget", "<html><head/><body><p><span style=\" font-weight:400;\">Expected yearly simple interest across the period under examination (unformatted float). </span></p></body></html>"))
        self.key_inv_int_rt_label.setText(_translate("TabWidget", "Investment Interest Rate:\n"
"(% p.a.)"))
        self.key_op_init_inv_label.setToolTip(_translate("TabWidget", "<html><head/><body><p><span style=\" font-weight:400;\">Optional initial investment amount as an unformatted number.<br/><br/>Assumed to be 0 if unfilled.</span></p></body></html>"))
        self.key_op_init_inv_label.setText(_translate("TabWidget", "Initial Investment:\n"
"(Optional ~ $)"))
        self.key_inv_psg_lineEdit.setToolTip(_translate("TabWidget", "<html><head/><body><p>Unformatted number for the fornightly $ contributed to investments after reaching the specified savings goal.</p></body></html>"))
        self.key_inv_psg_lineEdit.setText(_translate("TabWidget", str(self.df_fill_parameters["def_psg_inv_contrib"])))
        self.key_inv_int_rt_lineEdit.setToolTip(_translate("TabWidget", "<html><head/><body><p>Expected yearly simple interest across the period under examination (unformatted float). </p></body></html>"))
        self.key_inv_int_rt_lineEdit.setText(_translate("TabWidget", str(self.df_fill_parameters["def_inv_int_rt"])))
        self.key_inv_op_init_lineEdit.setToolTip(_translate("TabWidget", "<html><head/><body><p>Optional initial investment amount as an unformatted number.<br/><br/>Assumed to be 0 if unfilled.</p></body></html>"))
        self.key_inv_op_init_lineEdit.setText(_translate("TabWidget", str(self.df_fill_parameters["def_init_inv"])))
        self.setTabText(self.indexOf(self.key_assumptions), _translate("TabWidget", "Key Assumptions"))
        self.table_m_2.setToolTip(_translate("TabWidget", "<html><head/><body><p>Enter savings fields for pre-filled month and year to plot progress.</p><p>Format: Unformatted Number</p></body></html>"))
        item = self.table_m_2.horizontalHeaderItem(0)
        item.setText(_translate("TabWidget", "Year"))
        # item = self.table_m_2.horizontalHeaderItem(1)
        # item.setText(_translate("TabWidget", "Month"))
        item = self.table_m_2.horizontalHeaderItem(1)
        item.setText(_translate("TabWidget", "Savings Total ($)"))
        item = self.table_m_2.horizontalHeaderItem(2)
        item.setText(_translate("TabWidget", "Inv. Total ($)"))
        item = self.table_m_2.horizontalHeaderItem(3)
        item.setText(_translate("TabWidget", "Total ($)"))
        __sortingEnabled = self.table_m_2.isSortingEnabled()
        self.table_m_2.setSortingEnabled(False)
        self.table_m_2.setSortingEnabled(__sortingEnabled)
        self.setTabText(self.indexOf(self.tot_m), _translate("TabWidget", "Total: Month to Month"))
        self.table_y_2.setToolTip(_translate("TabWidget", "<html><head/><body><p>Enter savings fields for pre-filled year to plot progress.</p><p>Format: Unformatted Number</p></body></html>"))
        item = self.table_y_2.horizontalHeaderItem(0)
        item.setText(_translate("TabWidget", "Year"))
        item = self.table_y_2.horizontalHeaderItem(1)
        item.setText(_translate("TabWidget", "Savings Total ($)"))
        item = self.table_y_2.horizontalHeaderItem(2)
        item.setText(_translate("TabWidget", "Inv. Total ($)"))
        item = self.table_y_2.horizontalHeaderItem(3)
        item.setText(_translate("TabWidget", "Total ($)"))
        __sortingEnabled = self.table_y_2.isSortingEnabled()
        self.table_y_2.setSortingEnabled(False)
        self.table_y_2.setSortingEnabled(__sortingEnabled)
        self.setTabText(self.indexOf(self.tot_y), _translate("TabWidget", "Total: Year to Year"))
        self.setTabText(self.indexOf(self.pred_sav), _translate("TabWidget", "Predicted Savings Year to Year"))
        self.setTabText(self.indexOf(self.pred_inv), _translate("TabWidget", "Predicted Investment Year to Year"))
