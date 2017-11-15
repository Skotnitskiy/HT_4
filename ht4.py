import re

f_log = open("openerp-server.log", "r")
lines = f_log.readlines()
date_time_ptrn = "[0-9]+-\d\d-\d\d \d\d:\d\d:\d\d"
errors_ptrn = "(ERROR)(.*)"
warnings_ptrn = "(WARNING)(.*)"
criticals_ptrn = "(CRITICAL)(.*)"

def get_errors():
    err_dict = {"Marker": "ERROR"}
    dt_tm_list = []
    text_list = []
    for line in lines:
        l_err = re.search(errors_ptrn, line)
        l_date = re.search(date_time_ptrn, line)
        if l_err is not None:
            dt_tm_list.append(l_date.group())
            text_list.append(l_err.group().split("ERROR")[1])
    err_dict.update({"DateTime":dt_tm_list})
    err_dict.update({"Text":text_list})
    return err_dict

print(get_errors())