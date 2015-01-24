import os
from os import listdir
import csv

mypath="/Users/DeMates/Google Drive/SFO Group Files/Projects/FEMP EEPP/Luminaires/Commercial_Suspended"

output_file = '/Users/DeMates/Documents/Luminaires/Commercial_Suspended_List of Headers.csv'

list_of_filenames=listdir(mypath)

for filename in list_of_filenames:
    #Open IES file for processing
    my_file = open(str(mypath+'/'+filename))
    file_contents = my_file.read()

    lines = file_contents.split('\n')

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

                    #ATTEMPT 1: creating list and count of only unique headers
                    def unique_headers(line_header):
                        keys = []
                        for e in line_value:
                            if e not in keys:
                                keys.append(e)
                        return keys
                        print keys
                        print len(keys)


    # exporting the list of unique headers to csv
                    writer= csv.writer(open(output_file,'a'), delimiter=',')
                    writer.writerow([keys])
                    my_file.close()
