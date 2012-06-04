from collections import Counter
import csv
from datetime import datetime
import os
import sys

if len(sys.argv) != 2:
  print "Usage: python estimate_job_times.py <people_dir>"
  sys.exit(0)
  

people_dir = sys.argv[1]
if not os.path.exists(people_dir):
  print "ERROR: directory '%s' doesn't exist" %people_dir
  sys.exit(0)

print "Estimating the times of each test station from personnel jobs in %s" %(people_dir)

data = []
csv.field_size_limit(1000000000)

station_total_times = Counter()
station_num_jobs = Counter()

for filename in os.listdir(people_dir):
  person_filename = os.path.join(people_dir, filename)
  person_file = open(person_filename)
  
  reader = csv.reader(person_file)
  headers = reader.next()
  station_ind = headers.index('TestStation')
  time_ind = headers.index('Test Date')
  
  num_rows = 0
  num_ignored_jobs = 0

  last_station = None
  last_time = None
  for row in reader:
    num_rows += 1
    station = row[station_ind]
    time = datetime.strptime(row[time_ind], '%Y-%m-%d %H:%M:%S.%f')
    if station == last_station and time.date() == last_time.date():
      station_total_times[station] += (time - last_time).total_seconds()
      station_num_jobs[station] += 1
    else:
      num_ignored_jobs += 1
    
    last_station = station
    last_time = time
    
  print "Read in %d rows for %s and ignored %d jobs" %(num_rows, filename, num_ignored_jobs)

print "Here are the average times per station:"
for station,total_time in station_total_times.iteritems():
  print "%s: %f" %(station, total_time / station_num_jobs[station])
  
  














