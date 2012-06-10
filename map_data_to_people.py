import csv
from datetime import datetime
import os
import sys

if len(sys.argv) != 3:
  print "Usage: python map_data_to_people.py <csv filename> <target_dir>"
  sys.exit(0)
  
data_filename = sys.argv[1]
target_dir = sys.argv[2]
print "Mapping all data in %s to individual personnel files in %s" %(data_filename, target_dir)

if not os.path.exists(target_dir):
  os.mkdir(target_dir)

data = []
csv.field_size_limit(1000000000)

reader = csv.reader(open(data_filename))
headers = reader.next()

num_headers = len(headers)
num_rows = 0
num_bogus_rows = 0

part_ind = headers.index('PartNumber')
test_ind = headers.index('TestStation')
person_ind = headers.index('EmpName')
time_ind = headers.index('Test Date')

data = {}
person_to_writer = {}

for row in reader:
  row_len = len(row)
  if row_len < num_headers:
    num_bogus_rows += 1
    continue
  
  # part = row[part_ind]
  # test = row[test_ind]
  try:
    person = row[person_ind]
  except:
    import pdb;pdb.set_trace()
  # time = datetime.strptime(row[time_ind], '%m/%d/%y %H:%M') # change format: '2012-04-20 07:17:11.647'
  
  if person not in person_to_writer:
    person_to_writer[person] = csv.writer(open(os.path.join(target_dir, person.translate(None, ' ')), 'w'))
    person_to_writer[person].writerow(headers)
  
  person_to_writer[person].writerow(row)
  
      
  num_rows += 1
  if num_rows % 100000 == 0:
    print "Processed %d rows" %num_rows
  
print "Read %d rows of data" %num_rows
print "Here are the headers:\n%s" %str(headers)
print "Found %d unique employees:\n%s" %(len(person_to_writer), "\n".join(person_to_writer.keys()))














