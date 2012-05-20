import csv
from datetime import datetime
import sys

if len(sys.argv) != 2:
  print "Usage: python personal_efficiency.py <csv filename>"
  sys.exit(0)

data = []
csv.field_size_limit(1000000000)
reader = csv.reader(open(sys.argv[1]))
headers = reader.next()

header_uniques = dict([(header,set()) for header in headers])
header_empties = dict([(header,0) for header in headers])

num_rows = 0

part_ind = headers.index('PartNumber')
test_ind = headers.index('TestStation')
person_ind = headers.index('EmpName')
time_ind = headers.index('Test Date')

data = {}

for row in reader:
  row_len = len(row)
  
  part = row[part_ind]
  test = row[test_ind]
  person = row[person_ind]
  time = datetime.strptime(row[time_ind], '%m/%d/%y %H:%M')
  
  if test not in data:
    data[test] = {}
  test_data = data[test]
  
  if part not in test_data:
    test_data[part] = {}
  part_data = test_data[part]
  
  if person not in part_data:
    part_data[person] = []
  part_data[person].append(time)
      
  num_rows += 1
  if num_rows % 100000 == 0:
    print "Processed %d rows" %num_rows
  
print "Read %d rows of data" %num_rows
print "Here are the headers:\n%s" %str(headers)

for field in headers:
  print "Found %d %s with %f%% empty" %(len(header_uniques[field]), field, 100*header_empties[field]/num_rows)














