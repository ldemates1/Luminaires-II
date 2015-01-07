#reading one ies file
my_file = open("/Users/DeMates/Google Drive/SFO Group Files/Projects/FEMP EEPP/Luminaires/Undetermined/20352.ies")
file_contents = my_file.read()

#Creating a template dictionary
template_dict = {'IESNA':'','TEST':'','DATE':'','ISSUEDATE':'','MANUFAC':'','LUMCAT':'','LUMINAIRE':'','LAMP':'','BALLAST':'', 'DISTRIBUTION':'','OTHER':'', 'MORE':'',}

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

#trying to turn dictionary into string, but can't figure out how to get it in the order as template, the \r issue too
raw_data_string=str(template_dict)

#if we don't want headers -which is what discussed yesterday (doesn't work). I tried: for keys, values in template_dict(): print(values)

#added file name to data 1 which will hopefully be string with all needed data (worked-yay)
data_1= my_file.name +','+ raw_data_string

#trying to get rid of \r (doesn't work)
data_1=data_1.rstrip()
print data_1
