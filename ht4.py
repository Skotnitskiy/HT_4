import re
import csv

import os

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

markers_list = ["WARNING", "ERROR", "CRITICAL"]
date_time_ptrn = "[0-9]+-\d\d-\d\d \d\d:\d\d:\d\d"
warnings_ptrn = markers_list[0] + "(.*)"
errors_ptrn = markers_list[1] + "(.*)"
criticals_ptrn = markers_list[2] + "(.*)"

patterns_list = [warnings_ptrn, errors_ptrn, criticals_ptrn]
csv_all_data_columns = ["LineId", "Marker", "DateTime", "Description"]
csv_unique_data_columns = ["Count", "Marker", "DateTime", "Description"]

dtm_list = []
t_list = []
m_list = []


def get_messages(message_type, log_pattern):
    result = []
    line_count = 0
    for line in lines:
        l_mess = re.search(log_pattern, line)
        l_date = re.search(date_time_ptrn, line)
        line_count += 1
        if l_mess is not None:
            result.append({csv_all_data_columns[0]: line_count})
            result.append({csv_all_data_columns[1]: message_type})
            result.append({csv_all_data_columns[2]: l_date.group().strip()})
            result.append({csv_all_data_columns[3]: l_mess.group().split(message_type)[1].strip()})
            m_list.append(message_type)
            dtm_list.append(l_date.group().strip())
            t_list.append(l_mess.group().split(message_type)[1].strip())
    return result


def write_dict_to_csv(csv_file, csv_columns, dict_data):
    with open(csv_file, 'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        writer.writerows(dict_data)


messages_list = []
for marker, pattern in zip(markers_list, patterns_list):
    messages_list.append(get_messages(marker, pattern))

# write to file all data
for message in messages_list:
    write_dict_to_csv(all_data_csv_path, csv_all_data_columns, message)

unique_descriptions = []
unique_result = []

unique_warn_count = 0
unique_err_count = 0
unique_crit_count = 0

duplicate_warn_count = 0
duplicate_err_count = 0
duplicate_crit_count = 0

all_data_count = 0

for marker, date_time, description in zip(m_list, dtm_list, t_list):
    if description not in unique_descriptions:
        unique_descriptions.append(description)
        if marker == "WARNING":
            unique_warn_count += 1
        elif marker == "ERROR":
            unique_err_count += 1
        elif marker == "CRITICAL":
            unique_crit_count += 1
        unique_result.append({csv_unique_data_columns[0]: "*"})
        unique_result.append({csv_unique_data_columns[1]: marker})
        unique_result.append({csv_unique_data_columns[2]: date_time})
        unique_result.append({csv_unique_data_columns[3]: description})
    all_data_count += 1


write_dict_to_csv(unique_csv_path, csv_unique_data_columns, unique_result)

print("Unique:", len(unique_descriptions), "warnings:", unique_warn_count,
      "errors:", unique_err_count, "criticals:", unique_crit_count)
print("All data:", all_data_count)
