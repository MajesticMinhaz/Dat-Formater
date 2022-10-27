import re
from typing import Iterator


class DatFileFormat:
    def __init__(self, file_path: str):
        self.file_path = file_path

        self.emp_id_pattern = re.compile(pattern=r".*(emp_id:)[\s]+[1-9].+")
        self.errnr_pattern = re.compile(pattern=r".*(errnr:)[\s]+[1-9].+")
        self.log_one_pattern = re.compile(pattern=r"^t_log1.*")
        self.actual_data_pattern = re.compile(pattern=r".*(zusdat:)[\s]+[0-9]")

        self.current_errnr = None
        self.need_check = False

        self.product_id_pattern = re.compile(
            r"(.+)(pos_id[:\s]+)([0-9]+).+(t_id[:\s]+)([0-9]+).+(tll_id[:\s]+)([0-9]+).+(zeit[:\s]+)(["
            r"A-Za-z0-9:\s]+).+(emp_id[:\s]+)([0-9]+).+(kat[:\s]+)([0-9]+).+(errnr[:\s]+)([0-9]+).+(zusdat[:\s]+)(["
            r"0-9.]+)(\s+)(.+)(,)$")
        self.product_quantity_pattern = re.compile(
            r"^(.+)(pos_id[:\s]+)([0-9]+).+(t_id[:\s]+)([0-9]+).+(tll_id[:\s]+)([0-9]+).+(zeit[:\s]+)(["
            r"A-Za-z0-9:\s]+).+(emp_id[:\s]+)([0-9]+).+(kat[:\s]+)([0-9]+).+(errnr[:\s]+)([0-9]+).+(zusdat[:\s]+)(["
            r"0-9.]+)([\s@]+)([0-9.]+)([\sA*]+)([0-9.]+)(\s+)([A*])(\s+)(,)$")

    def read_file(self) -> Iterator[str]:
        all_row_data = []

        try:
            with open(file=self.file_path, mode="r") as read_file:
                file_lines = iter(read_file.readlines())

            for file_line in file_lines:
                log_one_line = file_line.strip()
                log_one_matched = re.fullmatch(self.log_one_pattern, string=log_one_line)

                if log_one_matched:
                    emp_id_line = next(file_lines).strip()
                    emp_id_matched = re.match(self.emp_id_pattern, emp_id_line)

                    errnr_matched = re.match(self.errnr_pattern, emp_id_line)
                    actual_data_matched = re.match(self.actual_data_pattern, emp_id_line)

                    if emp_id_line.__contains__("INVOICE"):
                        self.need_check = True
                    elif emp_id_line.__contains__("TOTAL"):
                        self.need_check = False

                    if self.need_check and emp_id_matched and actual_data_matched and errnr_matched:
                        combine_line = log_one_line + emp_id_line
                        all_row_data.append(combine_line)
                    else:
                        pass
                else:
                    continue
        except FileNotFoundError as file_not_found:
            print(file_not_found)

        return iter(all_row_data)

    def format_file(self, file_data: Iterator[str]) -> Iterator[str]:
        all_row_data_list = []

        for line in file_data:
            product_id_line = line.strip()
            product_id_matched = re.match(self.product_id_pattern, product_id_line)

            if product_id_matched:
                product_quantity_line = next(file_data).strip()
                product_quantity_matched = re.match(self.product_quantity_pattern, product_quantity_line)

                if product_quantity_matched:
                    single_line = ""
                    single_line += ("pos_id=" + product_id_matched.group(3).strip() + "<>")
                    single_line += ("t_id=" + product_id_matched.group(5).strip() + "<>")

                    single_line += ("tll_id=" + product_id_matched.group(7).strip() + "<>")
                    single_line += ("zeit=" + product_id_matched.group(9).strip() + "<>")
                    single_line += ("emp_id=" + product_id_matched.group(11).strip() + "<>")
                    single_line += ("kat=" + product_id_matched.group(13).strip() + "<>")
                    single_line += ("errnr=" + product_id_matched.group(15).strip() + "<>")
                    single_line += ("product_id=" + product_id_matched.group(17).strip() + "<>")
                    single_line += ("product_name=" + product_id_matched.group(19).strip() + "<>")

                    single_line += ("product_quantity=" + product_quantity_matched.group(17).strip() + "<>")
                    single_line += ("product_price=" + product_quantity_matched.group(19).strip() + "<>")
                    single_line += ("total_cost=" + product_quantity_matched.group(21).strip() + "<>")
                    single_line += ("product_status=" + product_quantity_matched.group(23).strip())
                    all_row_data_list.append(single_line.strip())
                else:
                    # print("Skip Start")
                    # print(product_id_line + product_quantity_line)
                    # print("skip end")
                    pass
            else:
                if product_id_line.strip() == "":
                    continue
                else:
                    print("Not passed", product_id_line)

        return iter(all_row_data_list)

