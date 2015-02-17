from os import listdir
import csv

class ies_parser:
    def __init__(self, filepath, output_file):
        self.header_value = {'file_name':'','IESNA':'','TEST':'','DATE':'','ISSUEDATE':'','MANUFAC':'','LUMCAT':'', 'LAMPCAT':'', 'LUMINAIRE':'','LAMP':'','BALLAST':'','DISTRIBUTION':'','_MOUNTING':'','TILT':'','NUMBER_LAMP':'','LUMEN_LAMP':'','WIDTH':'','LENGTH':'','HEIGHT':'','BALLAST_FACTOR':'','INPUT_WATTS':'','OTHER':'','MORE':''}
        self.header_names = ['file_name','IESNA','TEST','DATE','ISSUEDATE','MANUFAC','LUMCAT', 'LAMPCAT', 'LUMINAIRE','LAMP','BALLAST','DISTRIBUTION', '_MOUNTING', 'TILT', 'NUMBER_LAMP', 'LUMEN_LAMP', 'WIDTH', 'LENGTH', 'HEIGHT', 'BALLAST_FACTOR','INPUT_WATTS','OTHER','MORE']
        self.header_found = {'file_name':False,'IESNA':False,'TEST':False,'DATE':False,'ISSUEDATE':False,'MANUFAC':False,'LUMCAT':False, 'LAMPCAT':False, 'LUMINAIRE':False,'LAMP':False,'BALLAST':False,'DISTRIBUTION':False, '_MOUNTING':False, 'TILT':False, 'NUMBER_LAMP':False,'LUMEN_LAMP':False,'WIDTH':False, 'LENGTH':False, 'HEIGHT':False, 'BALLAST_FACTOR':False, 'INPUT_WATTS':False, 'OTHER':False,'MORE':False}
        self.filepath = filepath
        self.output_file = output_file
        self.file_contents = self.read_file(self.filepath)
        self.data_below_headers = self.parse_after_headers()
        self.populate_headers()
        self.populate_non_headers()
        #self.write_to_file()

    def read_file(self, path):
        my_file = open(str(path))
        my_file.seek(0)
        IESNA = my_file.readline().rstrip('\r\n')
        self.header_value['IESNA'] = IESNA
        self.header_found['IESNA'] = True
        return my_file.read()

    def print_contents(self):
        print self.file_contents

    def print_below_headers(self):
        print self.data_below_headers

    def parse_after_headers(self):
        indexed_values = []
        #print self.filepath
        break_at_tilt = self.file_contents.split('TILT')[1]
        #breaking all the values under tilt into their own lines
        break_at_line = break_at_tilt.split('\r\n')
        #remove the 'none' line
        break_at_line = break_at_line[1:len(break_at_line)]

        for line in break_at_line:
            line_elements = line.split()
            indexed_values.append(line_elements)
        return indexed_values

    def populate_non_headers(self):
        #   Index - Value
        #   0 = NUMBER_LAMP
        #   1 = LUMEN_LAMP
        #   7 = WIDTH
        #   8 = LENGTH
        #   9 = HEIGHT
        #   10 = BALLAST_FACTOR
        #   12 = INPUT_WATTS
        self.header_value['NUMBER_LAMP'] = self.data_below_headers[0][0]
        self.header_value['LUMEN_LAMP'] = self.data_below_headers[0][1]
        self.header_value['WIDTH'] = self.data_below_headers[0][7]
        self.header_value['LENGTH'] = self.data_below_headers[0][8]
        self.header_value['HEIGHT'] = self.data_below_headers[0][9]
        self.header_value['BALLAST_FACTOR'] = self.data_below_headers[1][0]
        self.header_value['INPUT_WATTS'] = self.data_below_headers[1][2]

    def print_headers(self):
        print self.header_value

    def populate_headers(self):
        self.header_value['file_name'] = self.filepath
        self.header_found['file_name'] = True

        # Now we need to loop through and find the other headers that we're interested in
        # First, make a list where each element is a line in the file
        lines = self.file_contents.split('\n')

        # Now, we can go through the list line by line and extract the header values
        for line in lines:
            #If a line has TILT then we want that value
            if 'TILT' in line:
                # Split the line into header and value, and take out return characters
                # Using rstrip to remove the return characters, and lstrip to remove
                # preceeding whitespace from the value

                tilt_line_content = line.split('=')

                #Getting the tilt value
                if(len(tilt_line_content) > 1):
                    tilt_line_value = tilt_line_content[1].split('=')

                    tilt_line_value = tilt_line_content[1].rstrip('[\r\n').lstrip(' ')

                    #Adding tilt value to disctionary
                    self.header_value['TILT'] = tilt_line_value
                    self.header_found['TILT'] = True

            # If a line starts with a bracket, then it might contain a relevant value
            elif '[' in line:
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
                        if line_header in self.header_names:

                            # We'll include a check here to see if a header value is already present.
                            # Some headers may appear multiple times in a single IES file. We'll combine those
                            # Values into a single value
                            if self.header_found[line_header] == False:
                                self.header_value[line_header] = line_value
                                self.header_found[line_header] = True
                            # This is the vase for multiple of the same header
                            else:
                                self.header_value[line_header] = self.header_value[line_header] + ' ' + line_value
                    else:
                        pass
                else:
                    pass

    def get_ies_type(self):

        max_vert_angle = (float(self.data_below_headers[0][3])-1) * float(self.data_below_headers[2][1])
        #print self.header_value['file_name'], " Vert. Ang. up to: ", max_vert_angle

        # Begin searching for the max vert. angle on the third line below the header values
        last_angle_index = 1
        found_last_angle = False
        while found_last_angle == False:
            last_angle_index += 1

            for item in self.data_below_headers[last_angle_index]:
                if max_vert_angle == float(item):
                    found_last_angle = True


        print self.header_value['file_name'], " Found the last angle on line: ", last_angle_index


    def write_to_file(self):
        # Take self.header_values, and append it to a csv file
        output_string = ''
        for index in range(len(self.header_names)):

            #Don't want a comma at the end of the last element
            if index == len(self.header_names)-1:
                output_string += self.header_value[self.header_names[index]]
            else:
                output_string += self.header_value[self.header_names[index]] + ','
        #print output_string

        writer = csv.writer(open(self.output_file,'a'), delimiter=',')
        writer.writerow([output_string])

if __name__ == "__main__":

    mypath = "ies_samp"
    output_file = "output.csv"
    list_of_filenames=listdir(mypath)

    for filename in list_of_filenames:
        if filename[-3:].lower() == 'ies':
            parser = ies_parser(mypath+'/'+filename, output_file)
            # Print data after headers for debugging
            #parser.print_below_headers()
            parser.get_ies_type()
        else:
            pass