import os, sys, math

# first run: cat 2wireTestData.csv|awk -F, '{print NR $27}'|grep IW > IW_LINES

f=open('IW_LINES', 'r')
D=dict()
for line in f.readlines():
  num, garbage = line.split()
  D[num] = 1
f.close()

for line in open('2wireTestData.csv', 'r'):
  data = line.split(',')
  if data[0] in D:
    print line,

