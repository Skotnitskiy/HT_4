import re
import csv

f_log = open("openerp-server.log", "r")
rep_path = "../reports/"
all_data_csv_path = rep_path + "all_data.csv"
lines = f_log.readlines()
date_time_ptrn = "[0-9]+-\d\d-\d\d \d\d:\d\d:\d\d"
markers_list = ["WARNING", "ERROR", "CRITICAL"]
warnings_ptrn = markers_list[0]+"(.*)"
errors_ptrn = markers_list[1]+"(.*)"
criticals_ptrn = markers_list[2]+"(.*)"
patterns_list = [warnings_ptrn, errors_ptrn, criticals_ptrn]
csv_all_da_columns = ["LineId", "Marker", "DateTime", "Description"]

def get_messages(type, pattern):
    result = []
    line_count = 0
    for line in lines:
        l_mess = re.search(pattern, line)
        l_date = re.search(date_time_ptrn, line)
        line_count += 1
        if l_mess is not None:
            result.append({csv_all_da_columns[0]: line_count})
            result.append({csv_all_da_columns[1]: type})
            result.append({csv_all_da_columns[2]: l_date.group().strip()})
            result.append({csv_all_da_columns[3]: l_mess.group().split(type)[1].strip()})
    return result

def write_dict_to_CSV(csv_file,csv_columns,dict_data):
        with open(csv_file, 'a') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in dict_data:
                writer.writerow(data)

messages_list = []
for marker, pattern in zip(markers_list, patterns_list):
    messages_list.append(get_messages(marker, pattern))

#write to file all data
for message in messages_list:
    write_dict_to_CSV(all_data_csv_path, csv_all_da_columns, message)
