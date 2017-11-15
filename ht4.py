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

def get_warnings():
    warn_dict = {"Marker": "WARNING"}
    dt_tm_list = []
    text_list = []
    for line in lines:
        l_warn = re.search(warnings_ptrn, line)
        l_date = re.search(date_time_ptrn, line)
        if l_warn is not None:
            dt_tm_list.append(l_date.group())
            text_list.append(l_warn.group().split("WARNING")[1])
    warn_dict.update({"DateTime":dt_tm_list})
    warn_dict.update({"Text":text_list})
    return warn_dict

def get_criticals():
    critical_dict = {"Marker": "CRITICAL"}
    dt_tm_list = []
    text_list = []
    for line in lines:
        l_crit = re.search(criticals_ptrn, line)
        l_date = re.search(date_time_ptrn, line)
        if l_crit is not None:
            dt_tm_list.append(l_date.group())
            text_list.append(l_crit.group().split("CRITICAL")[1])
    critical_dict.update({"DateTime":dt_tm_list})
    critical_dict.update({"Text":text_list})
    return critical_dict

def get_messages(type, pattern):
    result = {"Marker": type}
    dt_tm_list = []
    text_list = []
    for line in lines:
        l_mess = re.search(pattern, line)
        l_date = re.search(date_time_ptrn, line)
        if l_mess is not None:
            dt_tm_list.append(l_date.group())
            text_list.append(l_mess.group().split(type)[1])
    result.update({"DateTime":dt_tm_list})
    result.update({"Text":text_list})
    return result
print((get_messages("ERROR", errors_ptrn)))

