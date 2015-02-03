import os
from os import listdir
import csv

# Change this to wherever the IES files are located
mypath="/Users/DeMates/Documents/Luminaires/Sample ies files"

# Change this to the path of the output file
output_file = '/Users/DeMates/Documents/Luminaires/Othervalues.csv'

#listing all the filenames in the directory
list_of_filenames=listdir(mypath)

# List with the header names that we care about in the right order
header_names = ['file_name', 'TILT', 'NUMBER_LAMP', 'LUMEN_LAMP', 'WIDTH', 'LENGTH', 'HEIGHT', 'BALLAST_FACTOR', 'INPUTT_WATTS']

for filename in list_of_filenames:

    # Dictionary for keeping track of whether or not a particular header is present in the current
    # IES file being processed
    header_found = {'file_name':False,'TILT':False,'NUMBER_LAMP':False,'LUMEN_LAMP':False, 'WIDTH': False, 'LENGTH': False, 'HEIGHT': False,'BALLAST_FACTOR':False,'INPUTT_WATTS':False}

    # Dictionary that will hold the values associated with each header
    # Initialized to empty strings
    header_value = {'file_name':'','TILT':'','NUMBER_LAMP':'','LUMEN_LAMP':'', 'WIDTH':'', 'LENGTH':'', 'HEIGHT':'', 'BALLAST_FACTOR':'','INPUTT_WATTS':''}

    #Open IES file for processing
    my_file = open(str(mypath+'/'+filename))
    file_contents = my_file.read()

    #break into everything below 'Tilt'

    break_at_tilt = file_contents.split('TILT')[1]
        #breaking all the values under tilt into their own lines
    break_at_line = break_at_tilt.split('\r\n')


    #indexing each line, spaces are recognized in index, but ok for now

    for i in range(len(break_at_line)):
        list_values = break_at_line[i]
        split_values = list_values.split(' ')
        print split_values

    # The header values dictionary should be populated.
    # Now we need to turn that dictionary into a csv line in the correct order
    output_string = ''
    for index in range(len(header_names)):

        #Don't want a comma at the end of the last element
        if index == len(header_names)-1:
            output_string += header_value[header_names[index]]
        else:
            output_string += header_value[header_names[index]] + ','
    #print output_string

    writer= csv.writer(open(output_file,'a'), delimiter=',')
    writer.writerow([output_string])
    my_file.close()
