import csv
import matplotlib.pyplot as plt
import numpy as np

fname = "./CCRB-Complaint-Data_202007271729/allegations_202007271729.csv"

# READ IN RAW DATA
data_years = {} # year -> entry
MOS_ID = 0
YEAR = 7
FADO_TYPE = -6 # one of Force, offensive language, discourtesy, abuse of authority
with open(fname, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        # ['unique_mos_id', 'first_name', 'last_name', 'command_now', 'shield_no', 'complaint_id', 'month_received', 'year_received', 'month_closed', 'year_closed', 'command_at_incident', 'rank_abbrev_incident', 'rank_abbrev_now', 'rank_now', 'rank_incident', 'mos_ethnicity', 'mos_gender', 'mos_age_incident', 'complainant_ethnicity', 'complainant_gender', 'complainant_age_incident', 'fado_type', 'allegation', 'precinct', 'contact_reason', 'outcome_description', 'board_disposition']
        try:
            year = int(row[YEAR])
            data_years.setdefault(year, []).append(row)
        except:
            continue


print("YEAR / NUM COMPLAINTS / NUM FALSE REPORTS")
def count_false_reports(entries):
    return sum("Substantiated" not in x[-1] for x in entries)
for year, entries in sorted(data_years.items()):
    print(year, len(entries), count_false_reports(entries))

# NUMBER OF REPORTS PER OFFICER
id_complaints = {}
for entries in data_years.values():
    for entry in entries:
        id_num = entry[MOS_ID]
        id_complaints[id_num] = id_complaints.get(id_num, 0) + 1


vals = list(id_complaints.values())
def num_in_range(lo, hi, vals):
    return sum(lo <= x <= hi for x in vals)
x = [num_in_range(1, 4, vals), num_in_range(5, 9, vals), num_in_range(10, 14, vals), num_in_range(15, float("inf"), vals)]
x = [num_in_range(1, 3, vals), num_in_range(4, float("inf"), vals)]


# Reports of force
print("YEAR / NUM COMPLAINTS FORCE / NUM FALSE REPORTS")
def filter_reports(entries):
    return [entry for entry in entries if entry[FADO_TYPE] == "Force"]
def count_false_reports(entries):
    return sum("Substantiated" not in x[-1] for x in entries)
for year, entries in sorted(data_years.items()):
    entries = filter_reports(entries)
    print(year, len(entries), count_false_reports(entries))
