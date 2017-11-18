import csv
import os
import re

# create dir
rep_path = "../reports/"
if not os.path.exists(rep_path):
    os.mkdir("../reports")

f_log = open("openerp-server.log", "r")
f_all_data = open(rep_path+"all_data.csv", "w")
f_unique = open(rep_path+"unique.csv", "w")

all_data_csv_path = rep_path + "all_data.csv"
unique_csv_path = rep_path + "unique.csv"
lines = f_log.readlines()

date_time_ptrn = "[0-9]+-\d\d-\d\d \d\d:\d\d:\d\d"
log_ptrn = "(WARNING|CRITICAL|ERROR)(.*)"
marker_ptrn = "(WARNING|CRITICAL|ERROR)"

csv_all_data_columns = ["LineId", "Marker", "DateTime", "Description"]
csv_unique_data_columns = ["Count", "Marker", "DateTime", "Description"]

dscr_dict = {}  # description_dict
dscr_list = []  # description_list


def get_messages(log_pattern):
    result = []
    line_count = 0
    for line in lines:
        l_mess = re.search(log_pattern, line)
        l_date = re.search(date_time_ptrn, line)
        l_marker = re.search(marker_ptrn, line)
        if l_mess is not None:
            line_count += 1
            result.append({"LineId": line_count, "Marker": l_marker.group(), "DateTime": l_date.group().strip(),
                           "Description":  l_mess.group().split(l_marker.group())[1]})
            dscr_dict.update({l_mess.group().split(l_marker.group())[1]: [l_marker.group(), l_date.group().strip()]})
            dscr_list.append(l_mess.group().split(l_marker.group())[1])

    return result


def write_dict_to_csv(csv_file, csv_columns, dict_data):
    with open(csv_file, 'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        writer.writerows(dict_data)


# write to file all_data
write_dict_to_csv(all_data_csv_path, csv_all_data_columns, get_messages(log_ptrn))

unique_result = []
description_count = 0
for deskription, key in dscr_dict.items():
    for ds in dscr_list:
        if deskription == ds:
            description_count += 1
    unique_result.append({"Count": description_count, "Marker": key[0], "DateTime": key[1], "Description": deskription})
    description_count = 0

# write to file unique data
write_dict_to_csv(unique_csv_path, csv_unique_data_columns, unique_result)
