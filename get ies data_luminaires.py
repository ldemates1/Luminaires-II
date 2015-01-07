my_file = open("/Users/DeMates/Google Drive/SFO Group Files/Projects/FEMP EEPP/Luminaires/Undetermined/*.ies")
")
file_contents = my_file.read()
print(file_contents)



#module to quickly write a loop over standard input or a list of files.
my_file = open("/Users/DeMates/Google Drive/SFO Group Files/Projects/FEMP EEPP/Luminaires/Undetermined/20352.ies")
import fileinput
for line in fileinput.input() :
    fileinput.filename()





#to read the filename, which i would like to save and include in final csv: fileinput.filename()

#to close current file: fileinput.nextfile() Close the current file so that the next iteration will read the first line from /
#the next file (if any); lines not read from the file will not count towards the cumulative line count."
