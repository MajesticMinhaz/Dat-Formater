import csv
import re
import os
import json
from datetime import datetime
import schedule
from supplier import config
from supplier import time_regex
from supplier import date_regex
from supplier import year_regex
from supplier import month_number_dict
from datFileFormat import DatFileFormat


def task() -> None:
    current_datetime = datetime.now()
    format_datetime = current_datetime.strftime("%Y-%m-%d-%H-%M-%S-%f")

    dat_file_format = DatFileFormat(file_path=config.get(section="DEFAULT", option="input_dat_path"))
    all_data = dat_file_format.read_file()
    complete_format = dat_file_format.format_file(file_data=all_data)

    all_row_data = {"values": None}
    all_rows = []

    for line in complete_format:
        single_row = dict()
        get_list_data_list = line.split(sep="<>")

        got_date = ""

        for item in get_list_data_list:
            key, value = item.split(sep="=")

            if key.strip() == "zeit":
                date = re.search(pattern=date_regex, string=value.strip()).group()

                year = re.search(pattern=year_regex, string=value.strip()).group()

                for month in month_number_dict.keys():
                    if month in value.lower().strip():
                        month_number = month_number_dict[month]
                        got_date = f"{year}-{month_number}-{date}"
                        single_row["zeit"] = got_date
                    else:
                        continue

                _time = re.search(pattern=time_regex, string=value.strip()).group()
                single_row["time"] = _time
            else:
                single_row[key.strip()] = value.strip()

        if config.get("DEFAULT", "specific_zeit") == "True":
            if got_date == config.get("DEFAULT", "zeit"):
                all_rows.append(single_row)
            else:
                pass
        else:
            all_rows.append(single_row)
    all_row_data["values"] = all_rows

    if len(all_rows) > 0:
        data_headers = all_rows[0].keys()

        if config.get("DEFAULT", "export_json") == "True":
            with open(os.path.join(config.get("DEFAULT", "output_json_path"), f"output_{format_datetime}.json"), "w") as write_json:

                write_json.write(json.dumps(all_row_data, indent=4))
                write_json.close()
        else:
            pass

        if config.get("DEFAULT", "export_csv") == "True":
            with open(os.path.join(config.get("DEFAULT", "output_csv_path"), f"output_{format_datetime}.csv"), "w") as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=data_headers)

                writer.writeheader()

                for row in all_rows:
                    writer.writerow(row)

                csv_file.close()
        else:
            pass
    else:
        pass


schedule.every(int(config.get("DEFAULT", "interval_minutes").strip())).minutes.do(task)
while True:
    schedule.run_pending()
