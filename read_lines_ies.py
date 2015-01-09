#reading one ies file (but goal is to loop through multiple, writing to file with defined columns)
my_file = open("/Users/DeMates/Google Drive/SFO Group Files/Projects/FEMP EEPP/Luminaires/Undetermined/20352.ies")
file_contents = my_file.read()

#Creating a template dictionary, these are column headers on template
template_dict = {'file_name':'','IESNA':'','TEST':'','DATE':'','ISSUEDATE':'','MANUFAC':'','LUMCAT':'','LUMINAIRE':'','LAMP':'','BALLAST':'', 'DISTRIBUTION':'','OTHER':'', 'MORE':'',}

#spliting file into lines
lines = file_contents.split('\n')

#grabbing the lines we want, but I can't get it to recognize first line (IESA) though that is separated with :
for line in lines:
    if '[' in line:
        split_line = line.split(']')
        value = split_line[1]
        header = split_line[0]
        header = header[1:]
#filling in dictionary with values from ies files
        if header in template_dict:
            template_dict[header] = value

#trying to get the first line recognized (only line we want without the [. Tried so many ways- I dont get why not pickup in the IESNA)
    if ':' in line:
        split_line_2 = line.split(':')
        value_2 = split_line_2[1]
        header_2 = split_line_2[0]
        header_2 = header_2[1:]
    if header_2 in template_dict:
            template_dict[header] = value_2

#creating file_name variable to link to dictionary
file_name = my_file.name

#transfering dictionairy to string
raw_data_string=str(template_dict)

#added file name to data 1 which will hopefully be string with all needed data (worked-yay), still not recognizing IESNA though!
data_1= file_name +','+ raw_data_string

print data_1

#accessing the csv I created with the dictionary keys, add wr?
template_file = open("/Users/DeMates/Google Drive/SFO Group Files/Projects/FEMP EEPP/Luminaires/Fields_template.csv")
template_contents = template_file.read()

#trying to say that if in dictionary then write data to file
def data_2(data_1,template_contents)
    if key in data_1 == template contents:


#closing file, I think will be key to moving to next file
my_file.close()
