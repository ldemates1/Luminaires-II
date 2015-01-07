"""I need to access data from individual ies files then aggregate data as csv with one row for each ies file.
Do not need all data from ies files but would like csv to have the following columns
(all are delimited rows in ies files except for file_name which would be the actual file name): file_name, [IESNA],[TEST],[ISSUEDATE],[MANUFAC],[LUMCAT], [LAMCAT], [LUMINAIRE],[LAMP],[BALLAST],[OTHER]
Not all files have same delimited rows so if easier to just grab all, that is fine too
All my attempts below to access one ies file.
"""

#"""Attempt1 works just to open file (this is the only thing I can get to work, but not scalable to overall project because thousands
of files...)"""

my_file = open("/Users/DeMates/Google Drive/SFO Group Files/Projects/FEMP EEPP/Luminaires/Undetermined/20352.ies")
file_contents = my_file.read()
print(file_contents)

#Attempt2 doesn't work-using ascii package I downloaded to try and merge first then convert to csv, but said I needed numpy. tried to install numpy but says already there

my_file = open("/Users/DeMates/Google Drive/SFO Group Files/Projects/FEMP EEPP/Luminaires/Undetermined/20352.ies")
from astropy.io import ascii
data = ascii.read('my_file')

#Attempt3 doesn't work-trying to open with csv reader, gets stuck on the reader = csv.DictReader(my_file). Maybe because it isn't actually a csv?

import csv
with open(/Users/DeMates/Google Drive/SFO Group Files/Projects/FEMP EEPP/Luminaires/Undetermined/20352.ies, "rb)" as my_file:
  reader = csv.DictReader(my_file):
  for line in reader:
    print line

#Attempt4 doesn't work -nothing happens. other way to open using csv reader

import csv

with open('/Users/DeMates/Google Drive/SFO Group Files/Projects/FEMP EEPP/Luminaires/Undetermined/20352.ies', 'r') as my_file:
  for line in my_file:
    print line


#Attempt to read specific rows of ies file recognizing [] as the delimiter, but I dont know if this really helps me even, still
need to aggregate and get into csv

my_file = open("/Users/DeMates/Google Drive/SFO Group Files/Projects/FEMP EEPP/Luminaires/Undetermined/20352.ies")
file_contents = my_file.read()
def load_sections(my_file):
  with open(my_file,'r') as infile:
    line = ' '
    while True:
      while not line.startswith('[]'):
        line = next(infile)
        continue
      entry = {}
      for line in infile:
        line = line.strip()
        if not line: break

        key, value = map(str.strip, line.split(], 1))
        entry[key] = value

      yield entry
  for section in load_sections(my_file):
    print section


#writing to csv
import csv
def csv_writer(data,path):
with open(path, "wb") as csv_file:
  writer = csv.writer(csv.file, delimiter=',')
  for line in data:
    writer.writecol(line)
