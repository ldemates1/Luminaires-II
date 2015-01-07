#approach: open one file, read first line, and identify other data we want by taking only lines that start with [

#reading one ies file
my_file = open("/Users/DeMates/Google Drive/SFO Group Files/Projects/FEMP EEPP/Luminaires/Undetermined/20352.ies")
file_contents = my_file.read()

#Create a template dictionary
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

#turn dictionary into string, but can't figure out how to get it in the order as template, \r is line break so good its in there right?
s=str(template_dict)
print s
