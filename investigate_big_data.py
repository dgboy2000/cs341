import csv
import sys

if len(sys.argv) != 2:
  print "Usage: python investigate_big_data.py <csv filename>"
  sys.exit(0)

# csv.field_size_limit(1000000000)
# reader = csv.reader(open(sys.argv[1]), dialect='excel')
# headers = reader.next()

data_file = open(sys.argv[1])
headers = data_file.readline()
headers = headers.rstrip()
headers = headers.split()

header_uniques = dict([(header,set()) for header in headers])
header_empties = dict([(header,0) for header in headers])

data = []
num_rows = 0

# for row in reader:
try:
  for row in data_file.xreadlines():
    row_len = len(row)
    for ind,header in enumerate(headers):
      val = row[ind] if row_len > ind else None
      if val:
        header_uniques[header].add(val)
      else:
        header_empties[header] += 1
      
    num_rows += 1
    if num_rows % 100000 == 0:
      print "Processed %d rows" %num_rows
except:
  print "Error after processing %d rows; moving on" %num_rows
    
data_file.close()
  
print "Read %d rows of data" %num_rows
print "Here are the headers:\n%s" %str(headers)

for field in headers:
  print "Found %d %s with %f%% empty" %(len(header_uniques[field]), field, 100*header_empties[field]/num_rows)














