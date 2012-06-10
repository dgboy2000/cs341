from collections import Counter
import csv
from datetime import datetime
import os
import sys

if len(sys.argv) != 2:
  print "Usage: python count_part_number_job_diversity.py <data_file>"
  sys.exit(0)
  

data_file = sys.argv[1]
if not os.path.exists(data_file):
  print "ERROR: data file '%s' doesn't exist" %data_file
  sys.exit(0)

print "Computing the diversity of people working on each product and test station in %s" %(data_file)

data = []
csv.field_size_limit(1000000000)

station_to_person_counter = {}
station_to_part_to_person_counter = {}
person_to_stations = {}
person_to_parts = {}

reader = csv.reader(open(data_file))
headers = reader.next()
print "Headers are:\n%s" %"\n".join(headers)

part_ind = headers.index('PartNumber')
person_ind = headers.index('EmpName')
station_ind = headers.index('TestStation')

num_rows = 0

for row in reader:
  station = row[station_ind]
  if station not in station_to_person_counter:
    station_to_person_counter[station] = Counter()
    station_to_part_to_person_counter[station] = {}
  person_counter = station_to_person_counter[station]
  part_to_person_counter = station_to_part_to_person_counter[station]
  
  part = row[part_ind]
  if part not in part_to_person_counter:
    part_to_person_counter[part] = Counter()
  part_person_counter = part_to_person_counter[part]

  person = row[person_ind]
  if person not in person_to_stations:
    person_to_stations[person] = set()
    person_to_parts[person] = set()
  
  person_to_stations[person].add(station)
  person_to_parts[person].add(part)
  person_counter[person] += 1
  part_person_counter[person] += 1

  num_rows += 1
  if num_rows % 100000 == 0:
    print "Processed %d rows" %num_rows
  
print "Read in %d rows for %s" %(num_rows, data_file)

print "Here are the employee job counts per station:"
for station,person_counter in station_to_person_counter.iteritems():
  for person,job_count in person_counter.iteritems():
    print "%s: %s (%d jobs)" %(station, person, job_count)

print "Number of stations per employee:"
for person,stations in person_to_stations.iteritems():
  print "%s: %d" %(person, len(stations))
  
print "Number of parts per employee:"
for person,parts in person_to_stations.iteritems():
  print "%s: %d" %(person, len(parts))

print "Number of employees per station:"
for station,person_counter in station_to_person_counter.iteritems():
  print "%s: %d" %(station,len(person_counter))

print "Here are the Herfindahl indices for each station:"
for station,person_counter in station_to_person_counter.iteritems():
  num_jobs = sum(person_counter.values())
  hi = sum([cnt**2 for cnt in person_counter.itervalues()]) / float(num_jobs ** 2)
  print "%s: %f" %(station, hi)
  
for station,part_to_person in station_to_part_to_person_counter.iteritems():
  for part,person_counter in part_to_person.iteritems():
    print "%d people worked on '%s' at '%s'" %(len(person_counter), part, station)













