import csv
from datetime import datetime
import os
import sys

if len(sys.argv) != 3:
  print "Usage: python extract_columns.py <raw_data_file> <reduced_data_file>"
  sys.exit(0)
  

raw_data_file = sys.argv[1]
clean_data_file = sys.argv[2]
if not os.path.exists(raw_data_file):
  print "ERROR: raw data file '%s' doesn't exist" %raw_data_file
  sys.exit(0)

header_filename = 'flextronics_processed.csv'
try:
  headers = csv.reader(open(header_filename)).next()
  num_headers = len(headers)
except:
  print "Couldn't extact headers from %s" %header_filename
  sys.exit(0)

cols_to_extract = ['Master Id', 'PartNumber', 'Test Date', 'TestStation', 'EmpName']
inds_to_extract = [headers.index(col) for col in cols_to_extract]
emp_ind = headers.index('EmpName')
date_ind = headers.index('Test Date')
print "Extracting the following columns from %s:\n%s" %(raw_data_file, "\n".join(cols_to_extract))

csv.field_size_limit(1000000000)

reader = csv.reader(open(raw_data_file))
num_rows = 0
num_bogus_rows = 0
num_dup_rows = 0

writer = csv.writer(open(clean_data_file, 'w'))
writer.writerow(cols_to_extract)

seen_data = set() # empname:time

for row in reader:
  row_len = len(row)
  if row_len < num_headers:
    num_bogus_rows += 1
    continue
    
  uniq_str = "%s:%s" %(row[emp_ind], row[date_ind])
  if uniq_str in seen_data:
    num_dup_rows += 1
    continue
  seen_data.add(uniq_str)
  
  filtered_row = [row[ind] for ind in inds_to_extract]
  writer.writerow(filtered_row)
      
  num_rows += 1
  if num_rows % 100000 == 0:
    print "Processed %d rows" %num_rows
  
print "Read %d rows of data, skipped %d bogus rows, %d duplicate rows" %(num_rows, num_bogus_rows, num_dup_rows)















