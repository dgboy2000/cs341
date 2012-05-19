import csv
import sys

if len(sys.argv) != 2:
  print "Usage: python investigate_big_data.py <csv filename>"
  sys.exit(0)

data = []
reader = csv.reader(open(sys.argv[1]))
headers = reader.next()

header_uniques = dict([header,set() for header in headers])
header_empties = dict([header,0 for header in headers])

num_rows = 0

for row in reader:
  row_len = len(row)
  for ind,header in enumerate(headers):
    val = row[ind] if row_len > ind else None
    if val is not None:
      header_uniques[header].add(val)
    else:
      header_empties[header] += 1
      
  num_rows += 1
  if num_rows % 100000 == 0:
    print "Processed %d rows" %num_rows
  
print "Read %d rows of data" %num_rows
print "Here are the headers:\n%s" %str(headers)

for field in headers:
  print "Found %d %s with %f%% empty" %(len(header_uniques[field]), field, 100*header_empties[field]/num_rows)














