#importing one ies files as csv

import csv
results = []
with (open('/Users/DeMates/Google Drive/SFO Group Files/Projects/FEMP EEPP/Luminaires/Undetermined/20352.ies', newline=' ') as inputfile:
  reader = csv.DictReader(csvfile)
  for row in csv.reader(inputfile):
    results.append(row)



    print column['IESNA'], column['TEST'], column['ISSUEDATE'], column['MANUFAC'], column['LUMCAT'], column['LUMINAIRE'], column['LAMP'], column['BALLAST'], column['OTHER']
