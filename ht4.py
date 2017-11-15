import re

f_log = open("openerp-server.log", "r")
lines = f_log.readlines()
date_time_ptrn = "[0-9]+-\d\d-\d\d \d\d:\d\d:\d\d"
markers_list = ["WARNING", "ERROR", "CRITICAL"]
warnings_ptrn = "("+markers_list[0]+")(.*)"
errors_ptrn = "("+markers_list[1]+")(.*)"
criticals_ptrn = "("+markers_list[2]+")(.*)"

def get_messages(type, pattern):
    result = {"Marker": type}
    dt_tm_list = []
    text_list = []
    lines_ids_list = []
    line_count = 0
    for line in lines:
        l_mess = re.search(pattern, line)
        l_date = re.search(date_time_ptrn, line)
        line_count += 1
        if l_mess is not None:
            dt_tm_list.append(l_date.group())
            text_list.append(l_mess.group().split(type)[1])
            lines_ids_list.append(line_count)
    result.update({"DateTime":dt_tm_list})
    result.update({"Text":text_list})
    result.update({"LineId":lines_ids_list})
    return result
print(get_messages(markers_list[1], errors_ptrn))