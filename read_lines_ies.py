#reading one ies file (but goal is to loop through multiple, writing to file with defined columns)
my_file = open("/Users/DeMates/Google Drive/SFO Group Files/Projects/FEMP EEPP/Luminaires/Undetermined/20352.ies")
file_contents = my_file.read()


#Creating a list in the order of the column headers
column_names = ['file_name','IESNA','TEST','DATE','ISSUEDATE','MANUFAC','LUMCAT','LUMINAIRE','LAMP','BALLAST','DISTRIBUTION','OTHER','MORE']

#creating file_name variable to link to dictionary
file_name = my_file.name

#spliting file into lines
lines = file_contents.split('\n')
#creating list of values we want from ies files
ies_file=[]

#appending file name to list
ies_file.append(file_name)

#appending first line
my_file.seek(0)
IESNA = my_file.readline()
ies_file.append(IESNA)

#grabbing the lines we want, but I can't get it to recognize first line (IESA) though that is separated with :
for line in lines:
    if '[' in line:
        split_line = line.split(']')
        value = split_line[1]
        header = split_line[0]
        header = header[1:]

        for column in column_names:
            if column == header:
                ies_file.append(value)

output_str = ''
for i in range(len(ies_file)):
    ies_file[i] = ies_file[i].rstrip('\n')
    ies_file[i] = ies_file[i].rstrip('\r')

    if i == 0:
        output_str = output_str +  str(ies_file[i])
    else:
        output_str = output_str + ',' +  str(ies_file[i])

print output_str
f= open("/Users/DeMates/Documents/Luminaires/Fields_template.csv","w")
f.write(output_str)
f.close()
