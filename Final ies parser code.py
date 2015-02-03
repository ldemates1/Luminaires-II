import os
from os import listdir
import csv

# Change this to wherever the IES files are located
mypath="/Users/DeMates/Google Drive/SFO Group Files/Projects/FEMP EEPP/Luminaires/Commercial_Suspended"

# Change this to the path of the output file
output_file = '/Users/DeMates/Documents/Luminaires/Commercial_Suspended01232015.csv'

#listing all the filenames in the directory
list_of_filenames=listdir(mypath)

# List with the header names that we care about in the right order
header_names = ['file_name','IESNA','TEST','DATE','ISSUEDATE','MANUFAC','LUMCAT', 'LAMPCAT', 'LUMINAIRE','LAMP','BALLAST','DISTRIBUTION', '_MOUNTING', 'TILT', 'NUMBER_LAMP', 'LUMEN_LAMP', 'WIDTH', 'LENGTH', 'HEIGHT', 'BALLAST_FACTOR','INPUTT_WATTS','OTHER','MORE']

for filename in list_of_filenames:

    # Dictionary for keeping track of whether or not a particular header is present in the current
    # IES file being processed
    header_found = {'file_name':False,'IESNA':False,'TEST':False,'DATE':False,'ISSUEDATE':False,'MANUFAC':False,'LUMCAT':False, 'LAMPCAT':False, 'LUMINAIRE':False,'LAMP':False,'BALLAST':False,'DISTRIBUTION':False, '_MOUNTING':False, 'TILT':False, 'NUMBER_LAMP':False,'LUMEN_LAMP':False,'WIDTH':False, 'LENGTH':False, 'HEIGHT':False, 'BALLAST_FACTOR':False, 'INPUTT_WATTS':False, 'OTHER':False,'MORE':False}

    # Dictionary that will hold the values associated with each header
    # Initialized to empty strings
    header_value = {'file_name':'','IESNA':'','TEST':'','DATE':'','ISSUEDATE':'','MANUFAC':'','LUMCAT':'', 'LAMPCAT':'', 'LUMINAIRE':'','LAMP':'','BALLAST':'','DISTRIBUTION':'','_MOUNTING':'','TILT':'','NUMBER_LAMP':'','LUMEN_LAMP':'','WIDTH':'','LENGTH':'','HEIGHT':'','BALLAST_FACTOR':'','INPUTT_WATTS':'', 'OTHER':'','MORE':''}

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
        # If a line starts with a bracket, then it might contain a relevant value
        if '[' in line:
            # Split the line into header and value, and take out return characters
            # Using rstrip to remove the return characters, and lstrip to remove
            # preceeding whitespace from the value
            line_content = line.split(']')

            # If there are two elements
            if(len(line_content) > 1):
                line_header = line_content[0].split('[')

                if(len(line_header) > 1):

                    line_header = line_header[1].rstrip('[\r\n')

                    line_value = line_content[1].rstrip('[\r\n').lstrip(' ')

                    #print line_header + ' ' + line_value

                    # Now we can check if the header is one that we care about
                    # If so, put it into the header_value dictionary, and update the relevant
                    # Header found element
                    if line_header in header_names:

                        # We'll include a check here to see if a header value is already present.
                        # Some headers may appear multiple times in a single IES file. We'll combine those
                        # Values into a single value
                        if header_found[line_header] == False:
                            header_value[line_header] = line_value
                            header_found[line_header] = True
                        # This is the vase for multiple of the same header
                        else:
                            header_value[line_header] = header_value[line_header] + ' ' + line_value
                else:
                    pass
            else:
                pass
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
