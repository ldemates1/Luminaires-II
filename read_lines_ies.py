#reading one ies file (but goal is to loop through multiple, writing to file with defined columns)
my_file = open("/Users/DeMates/Google Drive/SFO Group Files/Projects/FEMP EEPP/Luminaires/Undetermined/20352.ies")
file_contents = my_file.read()


#Creating a list in the order of the column headers
column_names = ['file_name','IESNA','TEST','DATE','ISSUEDATE','MANUFAC','LUMCAT','LUMINAIRE','LAMP','BALLAST','DISTRIBUTION','OTHER','MORE']

#creating file_name variable to link to dictionary
file_name = my_file.name

#spliting file into lines
lines = file_contents.split('\n')

#grabbing the lines we want, but I can't get it to recognize first line (IESA) though that is separated with :
for line in lines:
    if '[' in line:
        split_line = line.split(']')
        value = split_line[1]
        header = split_line[0]
        header = header[1:]
if header in column_names:
    column_names.append(value)
    print column_names

#accessing the csv I created with the dictionary keys, add wr?
template_file = open("/Users/DeMates/Google Drive/SFO Group Files/Projects/FEMP EEPP/Luminaires/Fields_template.csv")
template_contents = template_file.read()

#filling in dictionary with values from ies files
        if header in column_names:
            print value





#added file name to data 1 which will hopefully be string with all needed data (worked-yay), still not recognizing IESNA though!
data_1= file_name +','+ raw_data_string

#accessing the csv I created with the dictionary keys, add wr?
template_file = open("/Users/DeMates/Google Drive/SFO Group Files/Projects/FEMP EEPP/Luminaires/Fields_template.csv")
template_contents = template_file.read()



#closing file, I think will be key to moving to next file
my_file.close()
