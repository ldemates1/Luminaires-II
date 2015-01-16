'''
print "Hello World"
f = open('IES_Test1', 'r')
'''

things_cared_about = ["Item1", "Item2", "Other"]
my_list = ["Hello", "There", "Other", "Things"]

if(len(my_list) > len(things_cared_about)):
    new_list = []
    list_index = 0
    for item in my_list:
        if list_index < len(things_cared_about):
            new_list.append(item)
        else:
            new_list[len(things_cared_about)-1] = new_list[len(things_cared_about)-1] + ' ' + item
        list_index += 1


    myString = ",".join(new_list)
    print myString

    #turn this list into CSV
