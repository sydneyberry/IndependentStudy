import os
import pandas as pd
import csv as csv

files_loc = 'C:\\Users\\Sydney\\Documents\\College\\IndependentStudy'

def prep_files(input_location):
    for root, dirs, files in os.walk(input_location):
        for file_name in files:
            if file_name.find("ready_") == -1:
                new_name = "ready_" + file_name
                dataframe = pd.read_csv(input_location + "\\" + file_name, header=None)
                dataframe = dataframe[0]
                dataframe.to_csv(input_location + "\\ready_data\\" + new_name, index=False, header=None)

                #os.remove(input_location + "\\" + file_name)

def combine_files(input_location, output_location):
    mega_file = output_location + "/compiled_data.csv"
    csv_files = os.listdir(input_location)

    if os.path.exists(mega_file):
        os.remove(mega_file)

    mega = open(mega_file, 'w+', newline='')
    writer = csv.writer(mega)

    for csv_file in csv_files:
        #if not csv_file == "megafile.csv":
        reader = csv.reader(open(input_location + "\\" + csv_file))
        for row in reader:
            writer.writerow(row)
            #    writer.writerow(row)
    mega.close()

#OLD:

def split_file():
    mega_file = files_loc + "/megafile"
    csv_files = os.listdir(files_loc)
    count = 1
    rowCount = 0

    reader = csv.reader(open(mega_file + ".csv"))

    for csv_file in csv_files:
        newName = mega_file + "_" + str(count) + ".csv"
        newFile = open(newName, 'w+', newline='')
        writer = csv.writer(newFile)
        for row in reader:
            rowCount = rowCount + 1
            writer.writerow(row)
            if rowCount == 50000:
                rowCount = 0
                count = count + 1

def sydney_you_dummy(new_data_location, compiled_data_location):
    if os.path.exists(compiled_data_location + "/megafile.csv"):
        os.remove(compiled_data_location + "/megafile.csv")
    for root, dirs, files in os.walk(new_data_location):
        for file_name in files:
            dataframe = pd.read_csv(new_data_location + "\\" + file_name, header=None)
            rows, col = dataframe.shape
            if col == 2:
                # new_name = "ready_" + file_name
                print(file_name)
                dataframe = dataframe[0]
                dataframe.to_csv(new_data_location + "\\" + file_name, header=None)
                os.remove(new_data_location + "\\" + file_name)


# mega_file = open(files_location + "\\megaFile.csv", "w+")
#
# for root, dirs, files in os.walk(files_location):
#     tmp = pd.DataFrame()    # empty dataframe
#     for file_name in files:
#         if not file_name == "megaFile.csv":
#             df = pd.read_csv(files_location + "\\" + file_name, header=None)
#             df = df[0]
#             tmp = tmp.append(df)
#     tmp.to_csv(files_location + "\\megaFile.csv", header=None)

def random_func():
    row_total = 0
    for root, dirs, files in os.walk(files_loc):
        for file_name in files:
            if file_name.find("mega") == -1:
                dataframe = pd.read_csv(files_loc + "\\" + file_name, header=None)
                rows, col = dataframe.shape
                print(rows)
                row_total = row_total + rows
    print(row_total)