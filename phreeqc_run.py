import os
from phreeqc_model import phreeqcModel
from file_management import Input_file
from pathlib import Path
from queries_db import Db_connection
import numpy as np
import sys
import subprocess

#Which model
model_id = 1#int(sys.argv[1])

#creating input file
my_new_file = Input_file(model_id)
my_new_file.start_input_file()

#Creating connection with the database
dbc = Db_connection()
connection = dbc.connect()






#all_rules = query_id.all_rule_ids()


# rule_ids =[]
# rule_counts = [amount_of_rules]
# rule_counter = 2
# while rule_counter <= amount_of_rules
#
#
# query_rules.rule_id = rule_id
# amount_of_rules = query_rules.count_rule()

# #Create the input sheet
# cmd = f'python phreeqc_de_punt_rules.py {model_id}'
# p = subprocess.Popen(cmd,shell=True)
# p.wait()
#
# #Run phreeqc
# chemModel = phreeqcModel()
#
# #assing the executable and database
# phPath = "C:\\Program Files\\USGS\\phreeqc-3.7.0-15749-x64"
# chemModel.phBin = os.path.join(phPath,"bin\\phreeqc.bat")
# chemModel.phDb = os.path.join(phPath, "database\\Stimela.dat")
# chemModel.phDb
#
# #setting up in and output files
# chemModel.inputFile = Path("input/phreeqc_de_punt_input.in")
# chemModel.outputFile = Path("output/phreeqc_de_punt_output.out")
# chemModel.inputFile
#
# chemModel.runModel()
# os.remove("input/working_solution_input_sheet.in")