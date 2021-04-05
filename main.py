import csv

import file_prep
import data_prep
import pandas as pd

files_location = 'C:\\Users\\Sydney\\Documents\\College\\IndependentStudy'
new_data_location = 'C:\\Users\\Sydney\\Documents\\College\\IndependentStudy\\uncompiled_data'
compiled_data_location = 'C:\\Users\\Sydney\\Documents\\College\\IndependentStudy\\compiled_data'
split_data_location = 'C:\\Users\\Sydney\\Documents\\College\\IndependentStudy\\compiled_data\\split_labeled_data'

data_prep.make_json_file(split_data_location)

