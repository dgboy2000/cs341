import csv

data = []
reader = csv.reader(open('flextronics_processed.csv'))
headers = reader.next()
for row in reader:
  row_hash = {}
  for ind,val in enumerate(row):
    row_hash[headers[ind]] = val
  data.append(row_hash)
  
print "Read %d rows of data" %len(data)
print "Here are the headers:\n%s" %str(headers)

def count_uniques(data, field):
  field_vals = set()
  for row in data:
    try:
      field_vals.add(row[field])
    except:
      pass
  return len(field_vals)
  
def count_empties(data, field):
  num_empties = 0
  for row in data:
    if field not in row or not row[field]:
      num_empties += 1
  return num_empties

num_rows = float(len(data))
for field in headers:
  try:
    print "Found %d %s with %f%% empty" %(count_uniques(data, field), field, 100*count_empties(data, field)/num_rows)
  except:
    print "Exception counting %s field" %field














