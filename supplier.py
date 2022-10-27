import os
import re
import configparser


config = configparser.ConfigParser()

if not os.path.exists(path=os.path.join(os.getcwd(), "config.ini")):
    config['DEFAULT'] = {
        "Input_Dat_Path": os.path.join(os.getcwd(), "data.dat"),
        "Output_Json_Path": os.getcwd(),
        "Output_CSV_Path": os.getcwd(),
        "Specific_Zeit": True,
        "Zeit": "2022-10-11",
        "Interval_Minutes": 5,
        "Export_JSON": True,
        "Export_CSV": True,
    }
    with open("config.ini", 'w') as config_file:
        config.write(config_file)
else:
    config.read(filenames=os.path.join(os.getcwd(), "config.ini"))


time_regex = re.compile(r"[0-9][0-9]:[0-9][0-9]:[0-9][0-9]")
date_regex = re.compile(r"[0-3][0-9]")
year_regex = re.compile(r"20[0-2][0-9]")

month_number_dict = {
    "jan": 1,
    "feb": 2,
    "mar": 3,
    "apr": 4,
    "may": 5,
    "jun": 6,
    "jul": 7,
    "aug": 8,
    "sep": 9,
    "oct": 10,
    "nov": 11,
    "dec": 12
}
