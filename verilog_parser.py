'''
First: You should initialize a cell using a line from the input .v file
Second: You should check if the given is a valid cell to include in our cell list using --> cell.check_cell()
Third: If the cell is valid, add it to our cell list
Fourth: For Input and output to be ready, you should call cell.find_io().
'''

from liberty.parser import parse_liberty
import math
from cell_class import cell
from liberty.types import select_timing_table
import numpy as np    

#This Function Is responsible for formating an instance of the cell class to a string similar to Verilog
#netlist strings
def create_cell_format(c):      
    cell_form = c.type + " " + c.name +" ( ."
    for inp in c.inputs:
        cell_form = cell_form + inp[0] + "(" + inp[1] + "), ."
    for out in c.outputs:
        cell_form = cell_form + out[0] + "(" + out[1] +") );"
    return cell_form


#This Function takes a list of cells and calculate the number of outputs for each cell and add it as an attribute
#of the cell in the class
def calc_cells_out_number(cells_list):
    for c1 in cells_list:
        counter = 0
        for c2 in cells_list:
            for inp in c2.get_inputs():
                if(c1.outputs[0][1] == inp[1]): 
                    counter += 1
        if(counter == 0):
            c1.set_out_num(counter)
        else:
            c1.set_out_num(counter)

#This Function takes a list of cells and calculate the Capacitance at the output of each cell and save it as an
#attribute of the cell in the class
def calc_cells_out_cap(cells_list):
    for c1 in cells_list:
        cap = 0
        counter = 0
        for c2 in cells_list:
            for inp in c2.get_inputs():
                if(c1.outputs[0][1] == inp[1]): #add the capacitance of the output cell
                    cell_info = library.get_group('cell', str(c2.type))
                    pin_info = cell_info.get_group('pin', str(inp[0]))
                    pin_cap = float(pin_info.get_cap('capacitance'))
                    cap += pin_cap
                    counter += 1
        if(counter == 0): #set cap to -1 to pass an intermediate delay in setting delay step
            c1.set_out_capacitance(-1)
            c1.set_out_num(counter)
        else:
            c1.set_out_capacitance(cap)
            c1.set_out_num(counter)

#This Function calculates The delay of each cell in the given cells list by fetching the corresponding delay value
#to the output capacitance; therefore, it should be called after calculating the capacitance for each cell
def calc_cells_delay(cells_list, library):
    total_delay = 0
    for c in cells_list:
        cell_info = library.get_group("cell", c.type)
        pin_info = cell_info.get_group('pin', c.outputs[0][0])
        max_delay = -1e9
        time_fall = -1e9
        time_rise = -1e9
        if(c.out_capacitance != -1):
            for inp in c.inputs:
                if(str(pin_info).find(inp[0]) != -1):
                    search_for_table_type =  str(pin_info)[str(pin_info).find(inp[0], str(pin_info).find("related_pin")) :]
                    search_for_table_type = search_for_table_type[:search_for_table_type.find("related_pin")]
                    if(search_for_table_type.find("cell_fall") != -1):
                        time_table_fall = select_timing_table(pin_info, inp[0], 'cell_fall')
                        cap_values = time_table_fall.get_array('index_1')[0]
                        time_values_fall = time_table_fall.get_array('values')[:,2]
                        time_fall = np.interp(c.out_capacitance, cap_values, time_values_fall) 
                    
                    if(search_for_table_type.find("cell_fall") != -1):
                        time_table_rise = select_timing_table(pin_info, inp[0], 'cell_rise')
                        cap_values = time_table_rise.get_array('index_1')[0]
                        time_values_rise = time_table_rise.get_array('values')[:,2]
                        time_rise = np.interp(c.out_capacitance, cap_values, time_values_rise)

                    max_delay = max(max_delay, time_rise, time_fall)
        else:
            for inp in c.inputs:
                if(str(pin_info).find(inp[0]) != -1):
                    search_for_table_type =  str(pin_info)[str(pin_info).find(inp[0], str(pin_info).find("related_pin")) :]
                    search_for_table_type = search_for_table_type[:search_for_table_type.find("related_pin")]
                
                    if(search_for_table_type.find("cell_rise") != -1):
                        time_table_rise = select_timing_table(pin_info, inp[0], 'cell_rise')
                        time_rise = time_table_rise.get_array('values')[2][2]
                    if(search_for_table_type.find("cell_fall") != -1):
                        time_table_fall = select_timing_table(pin_info, inp[0], 'cell_fall')
                        time_fall = time_table_fall.get_array('values')[2][2]
                    
                    max_delay = max(time_fall, time_rise, max_delay)

        total_delay += max_delay
    
    return total_delay

#This Function Takes a list of cells and calculates the frequencey of each type and returns A frequency array 
#that includes the frequency of each type of cells
def calc_cell_freq(cells_list):
    cells_freq_list = list()
    for c1 in cells_list:
        flag = True
        for c2 in cells_freq_list:
            if(c1.type == c2[0]):
                flag = False
                c2[1] += 1
        if(flag):
            cells_freq_list.append([c1.type, 1])
    return cells_freq_list
    


f = open("output.v","w+")   #Opens the output .v file for writing

with open(r'verilog parser\rca4.rtlnopwr.v') as myFile: #opens the input .v file that our algorithms would work on
  text = myFile.read()
result = text.split(";")  

cells_list = list()     #Creating a list to hold the cells


for i in result:       #looping on each line in the result array to extract cells info and check if it's a valid cell line
    cell_i = cell(i)
    if(cell_i.check_cell()):
        cells_list.append(cell_i)
    elif(i.find("endmodule") == -1):
        f.write(i)     #Writing non-cell lines to the output to preserve file format
    

for c in cells_list:    #Finding the inputs and outputs of each cell and adding them as internal attribute of each cell
    c.find_io()



liberty_file = r"verilog parser\osu035.lib"         #Opening The liberty file for information extraction
library = parse_liberty(open(liberty_file).read())


#Collecting info about the cells in the give file before processing them for comparison
calc_cells_out_cap(cells_list)                                      #calculate output cap of each cell
delay_before_processing = calc_cells_delay(cells_list, library)     #calculate total cells delay 
cells_freq_before_process = calc_cell_freq(cells_list)              #calculate the frequency of each cell


#Prompting the user For the required algorithm to implement, and the ceil of the fanout
run_mode = int(input("Please input \n1 for sizing up cells with large fanout \n2 for cloning high fan out cells \n3 for adding buffers for high fanouts\n"))
max_fan_out = int(input("please input max required fanout\n"))
if(run_mode == 1):      #Run Mode 1 --> Sizing Up cells with high fanout
    #This mode searches for the cells with fanout more than the ceil of fanout that was taken as input above
    #and upsizes these cells to double its size if this size is available in the library.
    print("sizing up cells")
    counter = 0
    for c in cells_list:
        if (c.out_num > max_fan_out):
            size=c.type.split("X")
            origin=size[0]
            if(len(size)>=2):
                size=int(size[1])
                new_type=origin + "X" + str(size*2)
                # check for new_type in the .lib file !!
                checks = len(library.get_groups("cell", new_type))
                if(checks == 0):
                    #if size*2 of cell doesn't exist, try an even bigger size
                    new_type=origin + "X" + str(size*4)
                    #print(new_type)
                    checks = len(library.get_groups("cell", new_type))
                if(checks != 0):
                    c.type=new_type
                    c.name=new_type+ "__" + str(counter)
                    counter+= 1


elif(run_mode == 2):    #Run Mode 2 --> Cloning Cells With high fanout
    #This mode searches for the cells with fanout more than the ceil of fanout that was taken as input above
    #and clones These cells to a number that accomadtes this fanout, it also rechecks if this change resulted 
    #in other cells to have the same issue wiht fanout and clones these cells till all cells have this at most
    #this ceil fanout number
    print("Cloning cells")
    counter_for_while = 1
    while True:
        length_before_change = len(cells_list)
        for c in cells_list:
            if (c.out_num > max_fan_out):
                number_of_clones = math.ceil(c.out_num / max_fan_out)
                for i in range(number_of_clones-1):
                    cell_form = c.type + " " + c.name +"_" +  str(counter_for_while) +  str(i+1) + " ( ."
                    for inp in c.inputs:
                        cell_form = cell_form + inp[0] + "(" + inp[1] + "), ."
                    for out in c.outputs:
                        cell_form = cell_form + out[0] + "(" + out[1] + "_" + str(counter_for_while) + str(i+1) + ") );"
                    new_clone = cell(cell_form)
                    new_clone.check_cell()
                    new_clone.find_io()
                    new_clone.set_out_num(max_fan_out)
                    counter = 0
                    for c2 in cells_list:
                        if(counter < max_fan_out):
                            for inp in c2.inputs:
                                if (inp[1] == c.outputs[0][1]):
                                    inp[1] = str(c.outputs[0][1]) + "_" + str(counter_for_while)+ str(i+1)
                                    counter += 1

                    cells_list.append(new_clone)
        counter_for_while += 1
        calc_cells_out_number(cells_list)
        length_after_change = len(cells_list)
        if(length_before_change == length_after_change):
            break
    

elif(run_mode == 3):    #Run Mode 3 --> Adding Buffers
    #This mode searches for the cells with fanout more than the ceil of fanout that was taken as input above
    #and adds a tree of buffers to that cell so that to accomodate the needed number of fanouts
    print("Adding buffers")
    counter_for_while = 1
    while True:
        length_before_change = len(cells_list)
        counterx = 1
        for c in cells_list:
            if (c.out_num > max_fan_out):
                number_of_bufs = math.ceil(c.out_num / max_fan_out)
                size=c.type.split("X")
                if(len(size)>=2):
                    size=int(size[1])
                else: size=1
                buf_size = size / number_of_bufs  #getting an approx value for buffer size 
                #validating the buffer size from the library 
                if (0 < buf_size ):
                    temp_buf_size = 2
                    if (len(library.get_groups("cell", "BUFX" + str(temp_buf_size))) != 0):
                        temp_size = temp_buf_size
                if (2 < buf_size ):
                    temp_buf_size = 4
                    if (len(library.get_groups("cell", "BUFX" + str(temp_buf_size))) != 0):
                        temp_size = temp_buf_size
                if (4 < buf_size ):
                    temp_buf_size = 8
                    if (len(library.get_groups("cell", "BUFX" + str(temp_buf_size))) != 0):
                        temp_size = temp_buf_size
                buf_size = temp_size
                buf_form= "BUFX"+ str(buf_size)
                #print(buf_form)
                for i in range(number_of_bufs):
                    cell_form = buf_form + " " + buf_form +"__" + str(counter_for_while) + str(counterx) +  " ( ."
                    cell_form = cell_form + c.inputs[0][0] + "(" + c.outputs[0][1]  + "), ."
                    cell_form = cell_form + c.outputs[0][0] + "(" + c.outputs[0][1]+ "_" + str(counter_for_while) + str(i) +  ") );"
                    new_buf = cell(cell_form)
                    new_buf.check_cell()
                    new_buf.find_io()
                    new_buf.set_out_num(max_fan_out)   
                    counter = 0
                    for c2 in cells_list:
                        if(counter < max_fan_out):
                            for inp in c2.inputs:
                                if (inp[1] == c.outputs[0][1]):
                                    inp[1] = str(c.outputs[0][1]) + "_" +str(counter_for_while) + str(i)  
                                    counter += 1
                    counterx += 1
                    cells_list.append(new_buf)
        counter_for_while += 1         
        length_after_change = len(cells_list)
        calc_cells_out_number(cells_list)
        if(length_before_change == length_after_change): 
            break            

                
else:
    print("Invalid Argument")

#Calculating cells info after Processing
calc_cells_out_cap(cells_list)
cells_freq_after_process = calc_cell_freq(cells_list)


#Displaying the results of the experiment
print("Cells frequency before Processing: ")
for c in cells_freq_before_process:
    print(c[0], " Freq --> ", c[1])

print("Cells frequency after Processing: ")
for c in cells_freq_after_process:
    print(c[0], " Freq --> ", c[1])

for c in cells_list:
    save = create_cell_format(c) + "\n"
    f.write(save)
f.write("endmodule")
f.close()

print ("Total cells delay before Processing: ", delay_before_processing, " ns")   
print ("Total cells delay After Processing: ", calc_cells_delay(cells_list, library), " ns")   '''
First: You should initialize a cell using a line from the input .v file
Second: You should check if the given is a valid cell to include in our cell list using --> cell.check_cell()
Third: If the cell is valid, add it to our cell list
Fourth: For Input and output to be ready, you should call cell.find_inputs(), then cell.find_outputs() in order
'''

from liberty.parser import parse_liberty
import math
from cell_class import cell
from liberty.types import select_timing_table
import numpy as np    

#This Function Is responsible for formating an instance of the cell class to a string similar to Verilog
#netlist strings
def create_cell_format(c):      
    cell_form = c.type + " " + c.name +" ( ."
    for inp in c.inputs:
        cell_form = cell_form + inp[0] + "(" + inp[1] + "), ."
    for out in c.outputs:
        cell_form = cell_form + out[0] + "(" + out[1] +") );"
    return cell_form


#This Function takes a list of cells and calculate the number of outputs for each cell and add it as an attribute
#of the cell in the class
def calc_cells_out_number(cells_list):
    for c1 in cells_list:
        counter = 0
        for c2 in cells_list:
            for inp in c2.get_inputs():
                if(c1.outputs[0][1] == inp[1]): 
                    counter += 1
        if(counter == 0):
            c1.set_out_num(counter)
        else:
            c1.set_out_num(counter)

#This Function takes a list of cells and calculate the Capacitance at the output of each cell and save it as an
#attribute of the cell in the class
def calc_cells_out_cap(cells_list):
    for c1 in cells_list:
        cap = 0
        counter = 0
        for c2 in cells_list:
            for inp in c2.get_inputs():
                if(c1.outputs[0][1] == inp[1]): #add the capacitance of the output cell
                    cell_info = library.get_group('cell', str(c2.type))
                    pin_info = cell_info.get_group('pin', str(inp[0]))
                    pin_cap = float(pin_info.get_cap('capacitance'))
                    cap += pin_cap
                    counter += 1
        if(counter == 0): #set cap to -1 to pass an intermediate delay in setting delay step
            c1.set_out_capacitance(-1)
            c1.set_out_num(counter)
        else:
            c1.set_out_capacitance(cap)
            c1.set_out_num(counter)

#This Function calculates The delay of each cell in the given cells list by fetching the corresponding delay value
#to the output capacitance; therefore, it should be called after calculating the capacitance for each cell
def calc_cells_delay(cells_list, library):
    total_delay = 0
    for c in cells_list:
        cell_info = library.get_group("cell", c.type)
        pin_info = cell_info.get_group('pin', c.outputs[0][0])
        max_delay = -1e9
        time_fall = -1e9
        time_rise = -1e9
        if(c.out_capacitance != -1):
            for inp in c.inputs:
                if(str(pin_info).find(inp[0]) != -1):
                    search_for_table_type =  str(pin_info)[str(pin_info).find(inp[0], str(pin_info).find("related_pin")) :]
                    search_for_table_type = search_for_table_type[:search_for_table_type.find("related_pin")]
                    if(search_for_table_type.find("cell_fall") != -1):
                        time_table_fall = select_timing_table(pin_info, inp[0], 'cell_fall')
                        cap_values = time_table_fall.get_array('index_1')[0]
                        time_values_fall = time_table_fall.get_array('values')[:,2]
                        time_fall = np.interp(c.out_capacitance, cap_values, time_values_fall) 
                    
                    if(search_for_table_type.find("cell_fall") != -1):
                        time_table_rise = select_timing_table(pin_info, inp[0], 'cell_rise')
                        cap_values = time_table_rise.get_array('index_1')[0]
                        time_values_rise = time_table_rise.get_array('values')[:,2]
                        time_rise = np.interp(c.out_capacitance, cap_values, time_values_rise)

                    max_delay = max(max_delay, time_rise, time_fall)
        else:
            for inp in c.inputs:
                if(str(pin_info).find(inp[0]) != -1):
                    search_for_table_type =  str(pin_info)[str(pin_info).find(inp[0], str(pin_info).find("related_pin")) :]
                    search_for_table_type = search_for_table_type[:search_for_table_type.find("related_pin")]
                
                    if(search_for_table_type.find("cell_rise") != -1):
                        time_table_rise = select_timing_table(pin_info, inp[0], 'cell_rise')
                        time_rise = time_table_rise.get_array('values')[2][2]
                    if(search_for_table_type.find("cell_fall") != -1):
                        time_table_fall = select_timing_table(pin_info, inp[0], 'cell_fall')
                        time_fall = time_table_fall.get_array('values')[2][2]
                    
                    max_delay = max(time_fall, time_rise, max_delay)

        total_delay += max_delay
    
    return total_delay

#This Function Takes a list of cells and calculates the frequencey of each type and returns A frequency array 
#that includes the frequency of each type of cells
def calc_cell_freq(cells_list):
    cells_freq_list = list()
    for c1 in cells_list:
        flag = True
        for c2 in cells_freq_list:
            if(c1.type == c2[0]):
                flag = False
                c2[1] += 1
        if(flag):
            cells_freq_list.append([c1.type, 1])
    return cells_freq_list
    


f = open("output.v","w+")   #Opens the output .v file for writing

with open(r'verilog parser\rca4.rtlnopwr.v') as myFile: #opens the input .v file that our algorithms would work on
  text = myFile.read()
result = text.split(";")  

cells_list = list()     #Creating a list to hold the cells


for i in result:       #looping on each line in the result array to extract cells info and check if it's a valid cell line
    cell_i = cell(i)
    if(cell_i.check_cell()):
        cells_list.append(cell_i)
    elif(i.find("endmodule") == -1):
        f.write(i)     #Writing non-cell lines to the output to preserve file format
    

for c in cells_list:    #Finding the inputs and outputs of each cell and adding them as internal attribute of each cell
    c.find_io()



liberty_file = r"verilog parser\osu035.lib"         #Opening The liberty file for information extraction
library = parse_liberty(open(liberty_file).read())


#Collecting info about the cells in the give file before processing them for comparison
calc_cells_out_cap(cells_list)                                      #calculate output cap of each cell
delay_before_processing = calc_cells_delay(cells_list, library)     #calculate total cells delay 
cells_freq_before_process = calc_cell_freq(cells_list)              #calculate the frequency of each cell


#Prompting the user For the required algorithm to implement, and the ceil of the fanout
run_mode = int(input("Please input \n1 for sizing up cells with large fanout \n2 for cloning high fan out cells \n3 for adding buffers for high fanouts\n"))
max_fan_out = int(input("please input max required fanout\n"))
if(run_mode == 1):      #Run Mode 1 --> Sizing Up cells with high fanout
    #This mode searches for the cells with fanout more than the ceil of fanout that was taken as input above
    #and upsizes these cells to double its size if this size is available in the library.
    print("sizing up cells")
    counter = 0
    for c in cells_list:
        if (c.out_num > max_fan_out):
            size=c.type.split("X")
            origin=size[0]
            if(len(size)>=2):
                size=int(size[1])
                new_type=origin + "X" + str(size*2)
                # check for new_type in the .lib file !!
                checks = len(library.get_groups("cell", new_type))
                if(checks == 0):
                    #if size*2 of cell doesn't exist, try an even bigger size
                    new_type=origin + "X" + str(size*4)
                    #print(new_type)
                    checks = len(library.get_groups("cell", new_type))
                if(checks != 0):
                    c.type=new_type
                    c.name=new_type+ "__" + str(counter)
                    counter+= 1


elif(run_mode == 2):    #Run Mode 2 --> Cloning Cells With high fanout
    #This mode searches for the cells with fanout more than the ceil of fanout that was taken as input above
    #and clones These cells to a number that accomadtes this fanout, it also rechecks if this change resulted 
    #in other cells to have the same issue wiht fanout and clones these cells till all cells have this at most
    #this ceil fanout number
    print("Cloning cells")
    counter_for_while = 1
    while True:
        length_before_change = len(cells_list)
        for c in cells_list:
            if (c.out_num > max_fan_out):
                number_of_clones = math.ceil(c.out_num / max_fan_out)
                for i in range(number_of_clones-1):
                    cell_form = c.type + " " + c.name +"_" +  str(counter_for_while) +  str(i+1) + " ( ."
                    for inp in c.inputs:
                        cell_form = cell_form + inp[0] + "(" + inp[1] + "), ."
                    for out in c.outputs:
                        cell_form = cell_form + out[0] + "(" + out[1] + "_" + str(counter_for_while) + str(i+1) + ") );"
                    new_clone = cell(cell_form)
                    new_clone.check_cell()
                    new_clone.find_io()
                    new_clone.set_out_num(max_fan_out)
                    counter = 0
                    for c2 in cells_list:
                        if(counter < max_fan_out):
                            for inp in c2.inputs:
                                if (inp[1] == c.outputs[0][1]):
                                    inp[1] = str(c.outputs[0][1]) + "_" + str(counter_for_while)+ str(i+1)
                                    counter += 1

                    cells_list.append(new_clone)
        counter_for_while += 1
        calc_cells_out_number(cells_list)
        length_after_change = len(cells_list)
        if(length_before_change == length_after_change):
            break
    

elif(run_mode == 3):    #Run Mode 3 --> Adding Buffers
    #This mode searches for the cells with fanout more than the ceil of fanout that was taken as input above
    #and adds a tree of buffers to that cell so that to accomodate the needed number of fanouts
    print("Adding buffers")
    counter_for_while = 1
    while True:
        length_before_change = len(cells_list)
        counterx = 1
        for c in cells_list:
            if (c.out_num > max_fan_out):
                number_of_bufs = math.ceil(c.out_num / max_fan_out)
                size=c.type.split("X")
                if(len(size)>=2):
                    size=int(size[1])
                else: size=1
                buf_size = size / number_of_bufs  #getting an approx value for buffer size 
                #validating the buffer size from the library 
                if (0 < buf_size ):
                    temp_buf_size = 2
                    if (len(library.get_groups("cell", "BUFX" + str(temp_buf_size))) != 0):
                        temp_size = temp_buf_size
                if (2 < buf_size ):
                    temp_buf_size = 4
                    if (len(library.get_groups("cell", "BUFX" + str(temp_buf_size))) != 0):
                        temp_size = temp_buf_size
                if (4 < buf_size ):
                    temp_buf_size = 8
                    if (len(library.get_groups("cell", "BUFX" + str(temp_buf_size))) != 0):
                        temp_size = temp_buf_size
                buf_size = temp_size
                buf_form= "BUFX"+ str(buf_size)
                #print(buf_form)
                for i in range(number_of_bufs):
                    cell_form = buf_form + " " + buf_form +"__" + str(counter_for_while) + str(counterx) +  " ( ."
                    cell_form = cell_form + c.inputs[0][0] + "(" + c.outputs[0][1]  + "), ."
                    cell_form = cell_form + c.outputs[0][0] + "(" + c.outputs[0][1]+ "_" + str(counter_for_while) + str(i) +  ") );"
                    new_buf = cell(cell_form)
                    new_buf.check_cell()
                    new_buf.find_io()
                    new_buf.set_out_num(max_fan_out)   
                    counter = 0
                    for c2 in cells_list:
                        if(counter < max_fan_out):
                            for inp in c2.inputs:
                                if (inp[1] == c.outputs[0][1]):
                                    inp[1] = str(c.outputs[0][1]) + "_" +str(counter_for_while) + str(i)  
                                    counter += 1
                    counterx += 1
                    cells_list.append(new_buf)
        counter_for_while += 1         
        length_after_change = len(cells_list)
        calc_cells_out_number(cells_list)
        if(length_before_change == length_after_change): 
            break            

                
else:
    print("Invalid Argument")

#Calculating cells info after Processing
calc_cells_out_cap(cells_list)
cells_freq_after_process = calc_cell_freq(cells_list)


#Displaying the results of the experiment
print("Cells frequency before Processing: ")
for c in cells_freq_before_process:
    print(c[0], " Freq --> ", c[1])

print("Cells frequency after Processing: ")
for c in cells_freq_after_process:
    print(c[0], " Freq --> ", c[1])

for c in cells_list:
    save = create_cell_format(c) + "\n"
    f.write(save)
f.write("endmodule")
f.close()

print ("Total cells delay before Processing: ", delay_before_processing, " ns")   
print ("Total cells delay After Processing: ", calc_cells_delay(cells_list, library), " ns")   '''
First: You should initialize a cell using a line from the input .v file
Second: You should check if the given is a valid cell to include in our cell list using --> cell.check_cell()
Third: If the cell is valid, add it to our cell list
Fourth: For Input and output to be ready, you should call cell.find_inputs(), then cell.find_outputs() in order
'''

from liberty.parser import parse_liberty
import math
from cell_class import cell
from liberty.types import select_timing_table
import numpy as np    

#This Function Is responsible for formating an instance of the cell class to a string similar to Verilog
#netlist strings
def create_cell_format(c):      
    cell_form = c.type + " " + c.name +" ( ."
    for inp in c.inputs:
        cell_form = cell_form + inp[0] + "(" + inp[1] + "), ."
    for out in c.outputs:
        cell_form = cell_form + out[0] + "(" + out[1] +") );"
    return cell_form


#This Function takes a list of cells and calculate the number of outputs for each cell and add it as an attribute
#of the cell in the class
def calc_cells_out_number(cells_list):
    for c1 in cells_list:
        counter = 0
        for c2 in cells_list:
            for inp in c2.get_inputs():
                if(c1.outputs[0][1] == inp[1]): 
                    counter += 1
        if(counter == 0):
            c1.set_out_num(counter)
        else:
            c1.set_out_num(counter)

#This Function takes a list of cells and calculate the Capacitance at the output of each cell and save it as an
#attribute of the cell in the class
def calc_cells_out_cap(cells_list):
    for c1 in cells_list:
        cap = 0
        counter = 0
        for c2 in cells_list:
            for inp in c2.get_inputs():
                if(c1.outputs[0][1] == inp[1]): #add the capacitance of the output cell
                    cell_info = library.get_group('cell', str(c2.type))
                    pin_info = cell_info.get_group('pin', str(inp[0]))
                    pin_cap = float(pin_info.get_cap('capacitance'))
                    cap += pin_cap
                    counter += 1
        if(counter == 0): #set cap to -1 to pass an intermediate delay in setting delay step
            c1.set_out_capacitance(-1)
            c1.set_out_num(counter)
        else:
            c1.set_out_capacitance(cap)
            c1.set_out_num(counter)

#This Function calculates The delay of each cell in the given cells list by fetching the corresponding delay value
#to the output capacitance; therefore, it should be called after calculating the capacitance for each cell
def calc_cells_delay(cells_list, library):
    total_delay = 0
    for c in cells_list:
        cell_info = library.get_group("cell", c.type)
        pin_info = cell_info.get_group('pin', c.outputs[0][0])
        max_delay = -1e9
        time_fall = -1e9
        time_rise = -1e9
        if(c.out_capacitance != -1):
            for inp in c.inputs:
                if(str(pin_info).find(inp[0]) != -1):
                    search_for_table_type =  str(pin_info)[str(pin_info).find(inp[0], str(pin_info).find("related_pin")) :]
                    search_for_table_type = search_for_table_type[:search_for_table_type.find("related_pin")]
                    if(search_for_table_type.find("cell_fall") != -1):
                        time_table_fall = select_timing_table(pin_info, inp[0], 'cell_fall')
                        cap_values = time_table_fall.get_array('index_1')[0]
                        time_values_fall = time_table_fall.get_array('values')[:,2]
                        time_fall = np.interp(c.out_capacitance, cap_values, time_values_fall) 
                    
                    if(search_for_table_type.find("cell_fall") != -1):
                        time_table_rise = select_timing_table(pin_info, inp[0], 'cell_rise')
                        cap_values = time_table_rise.get_array('index_1')[0]
                        time_values_rise = time_table_rise.get_array('values')[:,2]
                        time_rise = np.interp(c.out_capacitance, cap_values, time_values_rise)

                    max_delay = max(max_delay, time_rise, time_fall)
        else:
            for inp in c.inputs:
                if(str(pin_info).find(inp[0]) != -1):
                    search_for_table_type =  str(pin_info)[str(pin_info).find(inp[0], str(pin_info).find("related_pin")) :]
                    search_for_table_type = search_for_table_type[:search_for_table_type.find("related_pin")]
                
                    if(search_for_table_type.find("cell_rise") != -1):
                        time_table_rise = select_timing_table(pin_info, inp[0], 'cell_rise')
                        time_rise = time_table_rise.get_array('values')[2][2]
                    if(search_for_table_type.find("cell_fall") != -1):
                        time_table_fall = select_timing_table(pin_info, inp[0], 'cell_fall')
                        time_fall = time_table_fall.get_array('values')[2][2]
                    
                    max_delay = max(time_fall, time_rise, max_delay)

        total_delay += max_delay
    
    return total_delay

#This Function Takes a list of cells and calculates the frequencey of each type and returns A frequency array 
#that includes the frequency of each type of cells
def calc_cell_freq(cells_list):
    cells_freq_list = list()
    for c1 in cells_list:
        flag = True
        for c2 in cells_freq_list:
            if(c1.type == c2[0]):
                flag = False
                c2[1] += 1
        if(flag):
            cells_freq_list.append([c1.type, 1])
    return cells_freq_list
    


f = open("output.v","w+")   #Opens the output .v file for writing

with open(r'verilog parser\rca4.rtlnopwr.v') as myFile: #opens the input .v file that our algorithms would work on
  text = myFile.read()
result = text.split(";")  

cells_list = list()     #Creating a list to hold the cells


for i in result:       #looping on each line in the result array to extract cells info and check if it's a valid cell line
    cell_i = cell(i)
    if(cell_i.check_cell()):
        cells_list.append(cell_i)
    elif(i.find("endmodule") == -1):
        f.write(i)     #Writing non-cell lines to the output to preserve file format
    

for c in cells_list:    #Finding the inputs and outputs of each cell and adding them as internal attribute of each cell
    c.find_io()



liberty_file = r"verilog parser\osu035.lib"         #Opening The liberty file for information extraction
library = parse_liberty(open(liberty_file).read())


#Collecting info about the cells in the give file before processing them for comparison
calc_cells_out_cap(cells_list)                                      #calculate output cap of each cell
delay_before_processing = calc_cells_delay(cells_list, library)     #calculate total cells delay 
cells_freq_before_process = calc_cell_freq(cells_list)              #calculate the frequency of each cell


#Prompting the user For the required algorithm to implement, and the ceil of the fanout
run_mode = int(input("Please input \n1 for sizing up cells with large fanout \n2 for cloning high fan out cells \n3 for adding buffers for high fanouts\n"))
max_fan_out = int(input("please input max required fanout\n"))
if(run_mode == 1):      #Run Mode 1 --> Sizing Up cells with high fanout
    #This mode searches for the cells with fanout more than the ceil of fanout that was taken as input above
    #and upsizes these cells to double its size if this size is available in the library.
    print("sizing up cells")
    counter = 0
    for c in cells_list:
        if (c.out_num > max_fan_out):
            size=c.type.split("X")
            origin=size[0]
            if(len(size)>=2):
                size=int(size[1])
                new_type=origin + "X" + str(size*2)
                # check for new_type in the .lib file !!
                checks = len(library.get_groups("cell", new_type))
                if(checks == 0):
                    #if size*2 of cell doesn't exist, try an even bigger size
                    new_type=origin + "X" + str(size*4)
                    #print(new_type)
                    checks = len(library.get_groups("cell", new_type))
                if(checks != 0):
                    c.type=new_type
                    c.name=new_type+ "__" + str(counter)
                    counter+= 1


elif(run_mode == 2):    #Run Mode 2 --> Cloning Cells With high fanout
    #This mode searches for the cells with fanout more than the ceil of fanout that was taken as input above
    #and clones These cells to a number that accomadtes this fanout, it also rechecks if this change resulted 
    #in other cells to have the same issue wiht fanout and clones these cells till all cells have this at most
    #this ceil fanout number
    print("Cloning cells")
    counter_for_while = 1
    while True:
        length_before_change = len(cells_list)
        for c in cells_list:
            if (c.out_num > max_fan_out):
                number_of_clones = math.ceil(c.out_num / max_fan_out)
                for i in range(number_of_clones-1):
                    cell_form = c.type + " " + c.name +"_" +  str(counter_for_while) +  str(i+1) + " ( ."
                    for inp in c.inputs:
                        cell_form = cell_form + inp[0] + "(" + inp[1] + "), ."
                    for out in c.outputs:
                        cell_form = cell_form + out[0] + "(" + out[1] + "_" + str(counter_for_while) + str(i+1) + ") );"
                    new_clone = cell(cell_form)
                    new_clone.check_cell()
                    new_clone.find_io()
                    new_clone.set_out_num(max_fan_out)
                    counter = 0
                    for c2 in cells_list:
                        if(counter < max_fan_out):
                            for inp in c2.inputs:
                                if (inp[1] == c.outputs[0][1]):
                                    inp[1] = str(c.outputs[0][1]) + "_" + str(counter_for_while)+ str(i+1)
                                    counter += 1

                    cells_list.append(new_clone)
        counter_for_while += 1
        calc_cells_out_number(cells_list)
        length_after_change = len(cells_list)
        if(length_before_change == length_after_change):
            break
    

elif(run_mode == 3):    #Run Mode 3 --> Adding Buffers
    #This mode searches for the cells with fanout more than the ceil of fanout that was taken as input above
    #and adds a tree of buffers to that cell so that to accomodate the needed number of fanouts
    print("Adding buffers")
    counter_for_while = 1
    while True:
        length_before_change = len(cells_list)
        counterx = 1
        for c in cells_list:
            if (c.out_num > max_fan_out):
                number_of_bufs = math.ceil(c.out_num / max_fan_out)
                size=c.type.split("X")
                if(len(size)>=2):
                    size=int(size[1])
                else: size=1
                buf_size = size / number_of_bufs  #getting an approx value for buffer size 
                #validating the buffer size from the library 
                if (0 < buf_size ):
                    temp_buf_size = 2
                    if (len(library.get_groups("cell", "BUFX" + str(temp_buf_size))) != 0):
                        temp_size = temp_buf_size
                if (2 < buf_size ):
                    temp_buf_size = 4
                    if (len(library.get_groups("cell", "BUFX" + str(temp_buf_size))) != 0):
                        temp_size = temp_buf_size
                if (4 < buf_size ):
                    temp_buf_size = 8
                    if (len(library.get_groups("cell", "BUFX" + str(temp_buf_size))) != 0):
                        temp_size = temp_buf_size
                buf_size = temp_size
                buf_form= "BUFX"+ str(buf_size)
                #print(buf_form)
                for i in range(number_of_bufs):
                    cell_form = buf_form + " " + buf_form +"__" + str(counter_for_while) + str(counterx) +  " ( ."
                    cell_form = cell_form + c.inputs[0][0] + "(" + c.outputs[0][1]  + "), ."
                    cell_form = cell_form + c.outputs[0][0] + "(" + c.outputs[0][1]+ "_" + str(counter_for_while) + str(i) +  ") );"
                    new_buf = cell(cell_form)
                    new_buf.check_cell()
                    new_buf.find_io()
                    new_buf.set_out_num(max_fan_out)   
                    counter = 0
                    for c2 in cells_list:
                        if(counter < max_fan_out):
                            for inp in c2.inputs:
                                if (inp[1] == c.outputs[0][1]):
                                    inp[1] = str(c.outputs[0][1]) + "_" +str(counter_for_while) + str(i)  
                                    counter += 1
                    counterx += 1
                    cells_list.append(new_buf)
        counter_for_while += 1         
        length_after_change = len(cells_list)
        calc_cells_out_number(cells_list)
        if(length_before_change == length_after_change): 
            break            

                
else:
    print("Invalid Argument")

#Calculating cells info after Processing
calc_cells_out_cap(cells_list)
cells_freq_after_process = calc_cell_freq(cells_list)


#Displaying the results of the experiment
print("Cells frequency before Processing: ")
for c in cells_freq_before_process:
    print(c[0], " Freq --> ", c[1])

print("Cells frequency after Processing: ")
for c in cells_freq_after_process:
    print(c[0], " Freq --> ", c[1])

for c in cells_list:
    save = create_cell_format(c) + "\n"
    f.write(save)
f.write("endmodule")
f.close()

print ("Total cells delay before Processing: ", delay_before_processing, " ns")   
print ("Total cells delay After Processing: ", calc_cells_delay(cells_list, library), " ns")   '''
First: You should initialize a cell using a line from the input .v file
Second: You should check if the given is a valid cell to include in our cell list using --> cell.check_cell()
Third: If the cell is valid, add it to our cell list
Fourth: For Input and output to be ready, you should call cell.find_inputs(), then cell.find_outputs() in order
'''

from liberty.parser import parse_liberty
import math
from cell_class import cell
from liberty.types import select_timing_table
import numpy as np    

#This Function Is responsible for formating an instance of the cell class to a string similar to Verilog
#netlist strings
def create_cell_format(c):      
    cell_form = c.type + " " + c.name +" ( ."
    for inp in c.inputs:
        cell_form = cell_form + inp[0] + "(" + inp[1] + "), ."
    for out in c.outputs:
        cell_form = cell_form + out[0] + "(" + out[1] +") );"
    return cell_form


#This Function takes a list of cells and calculate the number of outputs for each cell and add it as an attribute
#of the cell in the class
def calc_cells_out_number(cells_list):
    for c1 in cells_list:
        counter = 0
        for c2 in cells_list:
            for inp in c2.get_inputs():
                if(c1.outputs[0][1] == inp[1]): 
                    counter += 1
        if(counter == 0):
            c1.set_out_num(counter)
        else:
            c1.set_out_num(counter)

#This Function takes a list of cells and calculate the Capacitance at the output of each cell and save it as an
#attribute of the cell in the class
def calc_cells_out_cap(cells_list):
    for c1 in cells_list:
        cap = 0
        counter = 0
        for c2 in cells_list:
            for inp in c2.get_inputs():
                if(c1.outputs[0][1] == inp[1]): #add the capacitance of the output cell
                    cell_info = library.get_group('cell', str(c2.type))
                    pin_info = cell_info.get_group('pin', str(inp[0]))
                    pin_cap = float(pin_info.get_cap('capacitance'))
                    cap += pin_cap
                    counter += 1
        if(counter == 0): #set cap to -1 to pass an intermediate delay in setting delay step
            c1.set_out_capacitance(-1)
            c1.set_out_num(counter)
        else:
            c1.set_out_capacitance(cap)
            c1.set_out_num(counter)

#This Function calculates The delay of each cell in the given cells list by fetching the corresponding delay value
#to the output capacitance; therefore, it should be called after calculating the capacitance for each cell
def calc_cells_delay(cells_list, library):
    total_delay = 0
    for c in cells_list:
        cell_info = library.get_group("cell", c.type)
        pin_info = cell_info.get_group('pin', c.outputs[0][0])
        max_delay = -1e9
        time_fall = -1e9
        time_rise = -1e9
        if(c.out_capacitance != -1):
            for inp in c.inputs:
                if(str(pin_info).find(inp[0]) != -1):
                    search_for_table_type =  str(pin_info)[str(pin_info).find(inp[0], str(pin_info).find("related_pin")) :]
                    search_for_table_type = search_for_table_type[:search_for_table_type.find("related_pin")]
                    if(search_for_table_type.find("cell_fall") != -1):
                        time_table_fall = select_timing_table(pin_info, inp[0], 'cell_fall')
                        cap_values = time_table_fall.get_array('index_1')[0]
                        time_values_fall = time_table_fall.get_array('values')[:,2]
                        time_fall = np.interp(c.out_capacitance, cap_values, time_values_fall) 
                    
                    if(search_for_table_type.find("cell_fall") != -1):
                        time_table_rise = select_timing_table(pin_info, inp[0], 'cell_rise')
                        cap_values = time_table_rise.get_array('index_1')[0]
                        time_values_rise = time_table_rise.get_array('values')[:,2]
                        time_rise = np.interp(c.out_capacitance, cap_values, time_values_rise)

                    max_delay = max(max_delay, time_rise, time_fall)
        else:
            for inp in c.inputs:
                if(str(pin_info).find(inp[0]) != -1):
                    search_for_table_type =  str(pin_info)[str(pin_info).find(inp[0], str(pin_info).find("related_pin")) :]
                    search_for_table_type = search_for_table_type[:search_for_table_type.find("related_pin")]
                
                    if(search_for_table_type.find("cell_rise") != -1):
                        time_table_rise = select_timing_table(pin_info, inp[0], 'cell_rise')
                        time_rise = time_table_rise.get_array('values')[2][2]
                    if(search_for_table_type.find("cell_fall") != -1):
                        time_table_fall = select_timing_table(pin_info, inp[0], 'cell_fall')
                        time_fall = time_table_fall.get_array('values')[2][2]
                    
                    max_delay = max(time_fall, time_rise, max_delay)

        total_delay += max_delay
    
    return total_delay

#This Function Takes a list of cells and calculates the frequencey of each type and returns A frequency array 
#that includes the frequency of each type of cells
def calc_cell_freq(cells_list):
    cells_freq_list = list()
    for c1 in cells_list:
        flag = True
        for c2 in cells_freq_list:
            if(c1.type == c2[0]):
                flag = False
                c2[1] += 1
        if(flag):
            cells_freq_list.append([c1.type, 1])
    return cells_freq_list
    


f = open("output.v","w+")   #Opens the output .v file for writing

with open(r'verilog parser\rca4.rtlnopwr.v') as myFile: #opens the input .v file that our algorithms would work on
  text = myFile.read()
result = text.split(";")  

cells_list = list()     #Creating a list to hold the cells


for i in result:       #looping on each line in the result array to extract cells info and check if it's a valid cell line
    cell_i = cell(i)
    if(cell_i.check_cell()):
        cells_list.append(cell_i)
    elif(i.find("endmodule") == -1):
        f.write(i)     #Writing non-cell lines to the output to preserve file format
    

for c in cells_list:    #Finding the inputs and outputs of each cell and adding them as internal attribute of each cell
    c.find_io()



liberty_file = r"verilog parser\osu035.lib"         #Opening The liberty file for information extraction
library = parse_liberty(open(liberty_file).read())


#Collecting info about the cells in the give file before processing them for comparison
calc_cells_out_cap(cells_list)                                      #calculate output cap of each cell
delay_before_processing = calc_cells_delay(cells_list, library)     #calculate total cells delay 
cells_freq_before_process = calc_cell_freq(cells_list)              #calculate the frequency of each cell


#Prompting the user For the required algorithm to implement, and the ceil of the fanout
run_mode = int(input("Please input \n1 for sizing up cells with large fanout \n2 for cloning high fan out cells \n3 for adding buffers for high fanouts\n"))
max_fan_out = int(input("please input max required fanout\n"))
if(run_mode == 1):      #Run Mode 1 --> Sizing Up cells with high fanout
    #This mode searches for the cells with fanout more than the ceil of fanout that was taken as input above
    #and upsizes these cells to double its size if this size is available in the library.
    print("sizing up cells")
    counter = 0
    for c in cells_list:
        if (c.out_num > max_fan_out):
            size=c.type.split("X")
            origin=size[0]
            if(len(size)>=2):
                size=int(size[1])
                new_type=origin + "X" + str(size*2)
                # check for new_type in the .lib file !!
                checks = len(library.get_groups("cell", new_type))
                if(checks == 0):
                    #if size*2 of cell doesn't exist, try an even bigger size
                    new_type=origin + "X" + str(size*4)
                    #print(new_type)
                    checks = len(library.get_groups("cell", new_type))
                if(checks != 0):
                    c.type=new_type
                    c.name=new_type+ "__" + str(counter)
                    counter+= 1


elif(run_mode == 2):    #Run Mode 2 --> Cloning Cells With high fanout
    #This mode searches for the cells with fanout more than the ceil of fanout that was taken as input above
    #and clones These cells to a number that accomadtes this fanout, it also rechecks if this change resulted 
    #in other cells to have the same issue wiht fanout and clones these cells till all cells have this at most
    #this ceil fanout number
    print("Cloning cells")
    counter_for_while = 1
    while True:
        length_before_change = len(cells_list)
        for c in cells_list:
            if (c.out_num > max_fan_out):
                number_of_clones = math.ceil(c.out_num / max_fan_out)
                for i in range(number_of_clones-1):
                    cell_form = c.type + " " + c.name +"_" +  str(counter_for_while) +  str(i+1) + " ( ."
                    for inp in c.inputs:
                        cell_form = cell_form + inp[0] + "(" + inp[1] + "), ."
                    for out in c.outputs:
                        cell_form = cell_form + out[0] + "(" + out[1] + "_" + str(counter_for_while) + str(i+1) + ") );"
                    new_clone = cell(cell_form)
                    new_clone.check_cell()
                    new_clone.find_io()
                    new_clone.set_out_num(max_fan_out)
                    counter = 0
                    for c2 in cells_list:
                        if(counter < max_fan_out):
                            for inp in c2.inputs:
                                if (inp[1] == c.outputs[0][1]):
                                    inp[1] = str(c.outputs[0][1]) + "_" + str(counter_for_while)+ str(i+1)
                                    counter += 1

                    cells_list.append(new_clone)
        counter_for_while += 1
        calc_cells_out_number(cells_list)
        length_after_change = len(cells_list)
        if(length_before_change == length_after_change):
            break
    

elif(run_mode == 3):    #Run Mode 3 --> Adding Buffers
    #This mode searches for the cells with fanout more than the ceil of fanout that was taken as input above
    #and adds a tree of buffers to that cell so that to accomodate the needed number of fanouts
    print("Adding buffers")
    counter_for_while = 1
    while True:
        length_before_change = len(cells_list)
        counterx = 1
        for c in cells_list:
            if (c.out_num > max_fan_out):
                number_of_bufs = math.ceil(c.out_num / max_fan_out)
                size=c.type.split("X")
                if(len(size)>=2):
                    size=int(size[1])
                else: size=1
                buf_size = size / number_of_bufs  #getting an approx value for buffer size 
                #validating the buffer size from the library 
                if (0 < buf_size ):
                    temp_buf_size = 2
                    if (len(library.get_groups("cell", "BUFX" + str(temp_buf_size))) != 0):
                        temp_size = temp_buf_size
                if (2 < buf_size ):
                    temp_buf_size = 4
                    if (len(library.get_groups("cell", "BUFX" + str(temp_buf_size))) != 0):
                        temp_size = temp_buf_size
                if (4 < buf_size ):
                    temp_buf_size = 8
                    if (len(library.get_groups("cell", "BUFX" + str(temp_buf_size))) != 0):
                        temp_size = temp_buf_size
                buf_size = temp_size
                buf_form= "BUFX"+ str(buf_size)
                #print(buf_form)
                for i in range(number_of_bufs):
                    cell_form = buf_form + " " + buf_form +"__" + str(counter_for_while) + str(counterx) +  " ( ."
                    cell_form = cell_form + c.inputs[0][0] + "(" + c.outputs[0][1]  + "), ."
                    cell_form = cell_form + c.outputs[0][0] + "(" + c.outputs[0][1]+ "_" + str(counter_for_while) + str(i) +  ") );"
                    new_buf = cell(cell_form)
                    new_buf.check_cell()
                    new_buf.find_io()
                    new_buf.set_out_num(max_fan_out)   
                    counter = 0
                    for c2 in cells_list:
                        if(counter < max_fan_out):
                            for inp in c2.inputs:
                                if (inp[1] == c.outputs[0][1]):
                                    inp[1] = str(c.outputs[0][1]) + "_" +str(counter_for_while) + str(i)  
                                    counter += 1
                    counterx += 1
                    cells_list.append(new_buf)
        counter_for_while += 1         
        length_after_change = len(cells_list)
        calc_cells_out_number(cells_list)
        if(length_before_change == length_after_change): 
            break            

                
else:
    print("Invalid Argument")

#Calculating cells info after Processing
calc_cells_out_cap(cells_list)
cells_freq_after_process = calc_cell_freq(cells_list)


#Displaying the results of the experiment
print("Cells frequency before Processing: ")
for c in cells_freq_before_process:
    print(c[0], " Freq --> ", c[1])

print("Cells frequency after Processing: ")
for c in cells_freq_after_process:
    print(c[0], " Freq --> ", c[1])

for c in cells_list:
    save = create_cell_format(c) + "\n"
    f.write(save)
f.write("endmodule")
f.close()

print ("Total cells delay before Processing: ", delay_before_processing, " ns")   
print ("Total cells delay After Processing: ", calc_cells_delay(cells_list, library), " ns")   
