import csv
from datetime import datetime
import os
import sys

if len(sys.argv) != 2:
  print "Usage: python sort_all_people_by_time.py <people_dir>"
  sys.exit(0)
  

people_dir = sys.argv[1]
if not os.path.exists(people_dir):
  print "ERROR: directory '%s' doesn't exist" %people_dir
  sys.exit(0)

print "Sorting all rows in all files in %s by test date" %(people_dir)

data = []
csv.field_size_limit(1000000000)

for filename in os.listdir(people_dir):
  person_filename = os.path.join(people_dir, filename)
  person_file = open(person_filename)
  
  reader = csv.reader(person_file)
  headers = reader.next()
  time_ind = headers.index('Test Date')

  all_rows = [row for row in reader]
  print "Read in %d rows for %s" %(len(all_rows), filename)
  all_rows.sort(key = lambda row: row[time_ind])
  print "Sorted rows by time"
  person_file.close()
  
  person_file = open(person_filename, 'w')
  writer = csv.writer(person_file)
  writer.writerow(headers)
  for row in all_rows:
    writer.writerow(row)
  person_file.close()
  print "Wrote all rows back to disk"
  
  














