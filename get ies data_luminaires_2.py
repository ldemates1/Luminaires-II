import os
from os import listdir
import csv

mypath="/Users/DeMates/Google Drive/SFO Group Files/Projects/FEMP EEPP/Luminaires/Undetermined"

#printing how many files in that folder, just to check path is correct
isfile=os.path.isfile
join=os.path.join
number_of_files = sum(1 for item in os.listdir(mypath) if isfile(join(mypath, item)))


#listing all the filenames in the directory
list_of_filenames=listdir(mypath)


for filename in list_of_filenames:
        my_file = open(str(mypath+'/'+filename))
        file_contents = my_file.read()

#Creating a list in the order of the column headers, want to export in this order
        column_names = ['file_name','IESNA','TEST','DATE','ISSUEDATE','MANUFAC','LUMCAT','LUMINAIRE','LAMP','BALLAST','DISTRIBUTION','OTHER','MORE']

#creating file_name variable to link to column_names list
        file_name = my_file.name

#creating list of values we want from ies files
        ies_file=[]

#appending file name to list
        ies_file.append(file_name)

#spliting file into lines
        lines = file_contents.split('\n')

#creating the IESNA variable to link to column_names list
        my_file.seek(0)
        IESNA = my_file.readline()
        ies_file.append(IESNA)

#grabbing the lines we want and putting 'Not Available for' headers that are not in columns_names
        headers = []
        values= []

        for line in lines:
            if '[' in line:
                split_line = line.split(']')
                value = (split_line[1])
                header = split_line[0]
                header = (header[1:])
#trying to create the 'headers' and 'values' lists to grab from to add to ies_file. lists are capturing the data
                headers.append(header)
                values.append(value)

            for i in range(len(headers)):
                value = values[i]

            else:
                value = "Not available"


        for column in column_names:
            ies_file.append(value)

#taking out line breaks and putting into string so can delimit in right places
        output_str = ''
        for i in range(len(ies_file)):
            ies_file[i] = ies_file[i].rstrip('\n')
            ies_file[i] = ies_file[i].rstrip('\r')
            if i == 0:
                output_str = output_str + str(ies_file[i])
            else:
                output_str = output_str + ',' + str(ies_file[i])


        writer= csv.writer(open('/Users/DeMates/Documents/Luminaires/Fields_template2.csv','a'), delimiter=',')
        writer.writerow([output_str])
        my_file.close()
