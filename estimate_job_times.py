from collections import Counter
import csv
from datetime import datetime
import os
import sys

if len(sys.argv) != 3:
  print "Usage: python estimate_job_times.py <people_dir> <output_file>"
  sys.exit(0)
  

people_dir = sys.argv[1]
output_file = sys.argv[2]
if not os.path.exists(people_dir):
  print "ERROR: directory '%s' doesn't exist" %people_dir
  sys.exit(0)

print "Estimating the times of each test station from personnel jobs in %s and writing data to %s" %(people_dir, output_file)

data = []
csv.field_size_limit(1000000000)

station_total_times = Counter()
station_num_jobs = Counter()

out_headers = ['EmpName', 'TestStation', 'PartNumber', 'NumJobs', 'TotalSecs', 'TotalSecsSq']
employee_station_part_info = {}

for person in os.listdir(people_dir):
  person_filename = os.path.join(people_dir, person)
  person_file = open(person_filename)
  
  employee_station_part_info[person] = {}
  station_part_info = employee_station_part_info[person]
  
  reader = csv.reader(person_file)
  headers = reader.next()
  master_id_ind = headers.index('Master Id')
  station_ind = headers.index('TestStation')
  part_ind = headers.index('PartNumber')
  time_ind = headers.index('Test Date')
  
  num_rows = 0
  num_ignored_jobs = 0

  last_master_id = None
  last_station = None
  last_time = None
  for row in reader:
    num_rows += 1
    
    master_id = row[master_id_ind]
    station = row[station_ind]
    part = row[part_ind]
    time = datetime.strptime(row[time_ind], '%Y-%m-%d %H:%M:%S.%f')
    
    if (station == last_station) and time.date() == last_time.date():
      secs = (time - last_time).total_seconds()
      station_total_times[station] += secs
      station_num_jobs[station] += 1
      
      if station not in station_part_info:
        station_part_info[station] = {}
      part_info = station_part_info[station]
      if part not in part_info:
        part_info[part] = {'NumJobs':0, 'TotalSecs':0.0, 'TotalSecsSq':0.0}
      info = part_info[part]
      info['NumJobs'] += 1
      info['TotalSecs'] += secs
      info['TotalSecsSq'] += secs ** 2
    else:
      num_ignored_jobs += 1
    
    last_master_id = master_id
    last_station = station
    last_time = time
    
  print "Read in %d rows for %s and ignored %d jobs" %(num_rows, filename, num_ignored_jobs)

print "Here are the average times per station:"
for station,total_time in station_total_times.iteritems():
  num_jobs = station_num_jobs[station]
  print "%s: %f seconds based on %d jobs" %(station, total_time / num_jobs, num_jobs)
  
print "Writing data to %s..." %output_file,
writer = csv.writer(open(output_file, 'w'))
writer.writerow(out_headers)
for person,station_part_info in employee_station_part_info.iteritems():
  for station,part_info in station_part_info:
    for part,info in part_info:
      writer.writerow([person, station, part, info['NumJobs'], info['TotalSecs'], info['TotalSecsSq']])
print "Done"













