from os import listdir
import csv

DEGREE_CONSTANTS_10 = [0.095,0.283,0.463,0.628,0.774,0.897,
                       0.993,1.058,1.091,1.091,1.058,0.993,
                       0.897,0.774,0.628,0.463,0.283,0.095]

DEGREE_CONSTANTS_5 = [0.0239,0.0715,0.1186,0.1649,0.2097,0.2531,
                      0.2946,0.3337,0.3703,0.4041,0.4349,0.4623,
                      0.4862,0.5064,0.5228,0.5351,0.5434,0.5476,
                      0.5476,0.5434,0.5351,0.5228,0.5064,0.4862,
                      0.4623,0.4349,0.4041,0.3703,0.3337,0.2946,
                      0.2531,0.2097,0.1649,0.1186,0.0715,0.0239]


# Type 1 files are where NUMBER_LAMP, LUMEN_LAMP, etc are on two lines
# Type 2 files are when those values each are on their own line


class ies_parser:
    def __init__(self, filepath, output_file):
        self.header_value = {'file_name':'','IESNA':'','TEST':'','DATE':'','ISSUEDATE':'',
        'MANUFAC':'','LUMCAT':'', 'LAMPCAT':'', 'LUMINAIRE':'','LAMP':'','BALLAST':'',
        'DISTRIBUTION':'','_MOUNTING':'','TILT':'','NUMBER_LAMP':'','LUMEN_LAMP':'',
        'WIDTH':'','LENGTH':'','HEIGHT':'','BALLAST_FACTOR':'','INPUT_WATTS':'','TOTAL_LUMENS':'',
        '_ABSOLUTELUMENS':'','_TOTALLUMINAIRELUMENS':'','OTHER':'','MORE':''}

        self.header_names = ['file_name','IESNA','TEST','DATE','ISSUEDATE',
        'MANUFAC','LUMCAT', 'LAMPCAT', 'LUMINAIRE','LAMP','BALLAST','DISTRIBUTION',
        '_MOUNTING', 'TILT', 'NUMBER_LAMP', 'LUMEN_LAMP', 'WIDTH', 'LENGTH', 'HEIGHT',
        'BALLAST_FACTOR','INPUT_WATTS','TOTAL_LUMENS','_ABSOLUTELUMENS','_TOTALLUMINAIRELUMENS','OTHER','MORE']

        self.header_found = {'file_name':False,'IESNA':False,'TEST':False,'DATE':False,'ISSUEDATE':False,
        'MANUFAC':False,'LUMCAT':False, 'LAMPCAT':False, 'LUMINAIRE':False,'LAMP':False,'BALLAST':False,
        'DISTRIBUTION':False, '_MOUNTING':False, 'TILT':False, 'NUMBER_LAMP':False,'LUMEN_LAMP':False,
        'WIDTH':False, 'LENGTH':False, 'HEIGHT':False, 'BALLAST_FACTOR':False, 'INPUT_WATTS':False,
        'TOTAL_LUMENS':False,'_ABSOLUTELUMENS':False,'_TOTALLUMINAIRELUMENS':False,'OTHER':False,'MORE':False}

        self.filepath = filepath
        self.output_file = output_file
        self.file_contents = self.read_file(self.filepath)
        self.data_below_headers = self.parse_after_headers()
        self.ies_type = self.determine_ies_type()
        self.populate_headers()
        self.populate_non_headers()
        self.max_vert_angle = self.get_max_vert_angle()
        self.line_repeat_count = self.calculate_line_repeat()
        self.data_lists = self.populate_data_lists()
        self.calculate_total_lumens()
        self.write_to_file()

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

        if self.ies_type == 1:
            self.header_value['NUMBER_LAMP'] = self.data_below_headers[0][0]
            self.header_value['LUMEN_LAMP'] = self.data_below_headers[0][1]
            self.header_value['WIDTH'] = self.data_below_headers[0][7]
            self.header_value['LENGTH'] = self.data_below_headers[0][8]
            self.header_value['HEIGHT'] = self.data_below_headers[0][9]
            self.header_value['BALLAST_FACTOR'] = self.data_below_headers[1][0]
            self.header_value['INPUT_WATTS'] = self.data_below_headers[1][2]

        elif self.ies_type == 2:
            self.header_value['NUMBER_LAMP'] = self.data_below_headers[0][0]
            self.header_value['LUMEN_LAMP'] = self.data_below_headers[1][0]
            self.header_value['WIDTH'] = self.data_below_headers[7][0]
            self.header_value['LENGTH'] = self.data_below_headers[8][0]
            self.header_value['HEIGHT'] = self.data_below_headers[9][0]
            self.header_value['BALLAST_FACTOR'] = self.data_below_headers[10][0]
            self.header_value['INPUT_WATTS'] = self.data_below_headers[12][0]

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

                    tilt_line_value = tilt_line_content[1].rstrip('[\r\n').lstrip(' ').replace(',', '')

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
                        line_value = line_content[1].rstrip('[\r\n').strip().replace(',', '')

                        #print line_header + ' ' + line_value

                        # Now we can check if the header is one that we care about
                        # If so, put it into the header_value dictionary, and update the relevant
                        # Header found element
                        if line_header in self.header_names:

                            # We'll include a check here to see if a header value is already present.
                            # Some headers may appear multiple times in a single IES file. We'll combine those
                            # values into a single value
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

    def get_max_vert_angle(self):

        if self.ies_type == 1:
            max_vert_angle = (float(self.data_below_headers[0][3])-1) * float(self.data_below_headers[2][1])
            #print self.header_value['file_name'], " Vert. Ang. up to: ", max_vert_angle
        elif self.ies_type == 2:
            max_vert_angle = (float(self.data_below_headers[3][0])-1) * float(self.data_below_headers[13][1])

        return max_vert_angle

    def calculate_line_repeat(self):
        # Begin searching for the max vert. angle on the third line below the header values

        if self.ies_type == 1:
            last_angle_index = 1
        elif self.ies_type == 2:
            last_angle_index = 12

        found_last_angle = False
        while found_last_angle == False:
            last_angle_index += 1

            for item in self.data_below_headers[last_angle_index]:
                if self.max_vert_angle == float(item):
                    found_last_angle = True

        #Subtract 1 to account for the 2 lines under the headers that are not angles
        # Angles will repeat every line_repeat_count line(s).
        line_repeat_count = last_angle_index-1
        #print line_repeat_count
        return line_repeat_count

    def populate_data_lists(self):

        if self.ies_type == 1:
            number_of_val_lists = (int(self.data_below_headers[0][3])-1)/2

        elif self.ies_type == 2:
            number_of_val_lists = (int(self.data_below_headers[3][0])-1)/2

        data_start_line = self.line_repeat_count + 3

        # Create list of empty lists for values
        candela_vals= []
        for i in range(number_of_val_lists):
            candela_vals.append([])
            
        total_count=0
        for i in range(data_start_line, len(self.data_below_headers)):

            for j in range(0, len(self.data_below_headers[i])):
                # Only care about even values in each line (midpoints)
                if j % 2 != 0:
                    index = total_count%number_of_val_lists
                    candela_vals[index].append(self.data_below_headers[i][j])
                    total_count += 1

        return candela_vals
        #print candela_vals[1]

    def calculate_total_lumens(self):

        lumens_already_calculated = False

        if self.header_found['_ABSOLUTELUMENS']:
            total_lumens = self.header_value['_ABSOLUTELUMENS']
            lumens_already_calculated = True
        elif self.header_found['_TOTALLUMINAIRELUMENS']:
            total_lumens = self.header_value['_TOTALLUMINAIRELUMENS']
            lumens_already_calculated = True

        # Only run if the lumen value is not already in the headers.
        if lumens_already_calculated == False:
            const_array = []
            if self.ies_type == 1:
                if float(self.data_below_headers[2][1]) == 5:
                    const_array = DEGREE_CONSTANTS_10
                else:
                    const_array = DEGREE_CONSTANTS_5
            elif self.ies_type == 2:
                if float(self.data_below_headers[13][1]) == 5:
                    const_array = DEGREE_CONSTANTS_10
                else:
                    const_array = DEGREE_CONSTANTS_5

            total_lumens = 0
            for i in range(len(self.data_lists)):
                self.data_lists[i][:] =[float(x)*const_array[i] for x in self.data_lists[i]]
                #print self.data_lists[i]

                angle_total_lumens = 0
                for j in range(len(self.data_lists[i])):
                    if j == 0 or j == (len(self.data_lists[i])-1):
                        angle_total_lumens += self.data_lists[i][j]
                    else:
                        angle_total_lumens += (self.data_lists[i][j] * 2)
                total_lumens += angle_total_lumens / (len(self.data_lists[i]) * 2 - 2)

            #print total_lumens
            self.header_value['TOTAL_LUMENS'] = str(total_lumens)
            self.header_found['TOTAL_LUMENS'] = True

        return total_lumens


    def mult_by_constant(self, element, const):
        return element * const


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


    def determine_ies_type(self):
        if(len(self.data_below_headers[0]) > 1):
            return 1
        else:
            return 2

if __name__ == "__main__":

    mypath = "ies_samp"
    output_file = "output.csv"
    list_of_filenames=listdir(mypath)
    count = 0
    fail_count = 0
    for filename in list_of_filenames:
        if filename[-3:].lower() == 'ies':

            try:
                parser = ies_parser(mypath+'/'+filename, output_file)
                count += 1
            except:
                print filename
                fail_count += 1

        else:
            pass

    print "Processed ", count, " files."
    print "Failed to process ", fail_count, " files."
