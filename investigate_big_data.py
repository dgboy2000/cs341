import csv
import sys

if len(sys.argv) != 2:
  print "Usage: python investigate_big_data.py <csv filename>"
  sys.exit(0)

# csv.field_size_limit(1000000000)
# reader = csv.reader(open(sys.argv[1]), dialect='excel')
# headers = reader.next()

def load_headers():
  header_filename = 'flextronics_processed.csv'
  try:
    headers = csv.reader(open(header_filename)).next()
    num_headers = len(headers)
    return headers
  except:
    print "Couldn't extact headers from %s" %header_filename
    sys.exit(0)

reader = csv.reader(open(sys.argv[1]))

headers = load_headers()
header_uniques = dict([(header,set()) for header in headers])
header_empties = dict([(header,0) for header in headers])

data = []
num_rows = 0
num_bad_rows = 0
num_headers = len(headers)

# for row in reader:
try:
  for row in reader:
    if len(row) < num_headers:
      num_bad_rows += 1
      continue

    for ind,header in enumerate(headers):
      val = row[ind]
      if val:
        header_uniques[header].add(val)
      else:
        header_empties[header] += 1
      
    num_rows += 1
    if num_rows % 100000 == 0:
      print "Processed %d rows" %num_rows
except:
  print "Error after processing %d rows with %d bad rows; moving on" %(num_rows, num_bad_rows)
  
print "Read %d rows of data" %num_rows
print "Here are the headers:\n%s" %str(headers)

for field in headers:
  print "Found %d %s with %f%% empty" %(len(header_uniques[field]), field, 100*header_empties[field]/num_rows)














