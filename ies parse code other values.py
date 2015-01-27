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

    # Get the file name
    header_value['file_name'] = filename
    header_found['file_name'] = True

    # Creating the IESNA variable to link to list
    my_file.seek(0)
    IESNA = my_file.readline().rstrip('\r\n')
    header_value['IESNA'] = IESNA
    header_found['IESNA'] = True

    # Now we need to loop through and find the other headers that we're interested in
    # First, make a list where each element is a line in the file
    lines = file_contents.split('\n')
    # Now, we can go through the list line by line and extract the header values

    for line in lines:
        # If line contains TILT, want to break into header and value with =
        if 'TILT' in line:
            # Split the line into header and value, and take out return characters
            # Using rstrip to remove the return characters, and lstrip to remove
            # preceeding whitespace from the value

            tilt_line_content = line.split('=')

            #Getting the tilt value
            if(len(tilt_line_content) > 1):
                tilt_line_value = tilt_line_content[1].split('=')

                tilt_line_value = tilt_line_content[1].rstrip('[\r\n').lstrip(' ')
                print tilt_line_value

                #Adding tilt value to disctionary
                header_value['TILT'] = tilt_line_value
                header_found['TILT'] = True

                #this gets me next line from the top but not after the tilt line
                next_line = my_file.next()
                print next_line

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