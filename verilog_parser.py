'''
First: You should initialize a cell using a line from the input .v file
Second: You should check if the given is a valid cell to include in our cell list using --> cell.check_cell()
Third: If the cell is valid, add it to our cell list
Fourth: For Input and output to be ready, you should call cell.find_inputs(), then cell.find_outputs() in order
'''

from liberty.parser import parse_liberty
import math

class cell:
    def __init__(self, line):
        f=open(r"verilog parser\osu035.lib", "r")
        self.library_data=f.read()
        f.close()        
        self.line_arr = line.split(" ")
        self.io_counter = 3                               # We will have inputs or outputs starting from the fourth index of the line_arr
        self.type = self.line_arr[0].replace("\n", "")    # replace to remove any extra endl

        
    def check_cell(self):
        to_find = "cell (" +self.type + ")"
        if(self.library_data.find(to_find) == -1): 
            return False
        else:
            self.name = self.line_arr[1]
            return True   

    def find_inputs(self):
        to_find = "cell (" +self.type + ")"
        starting_idex = self.library_data.find(to_find) 
        if(starting_idex != -1):
            current_cell_info = self.library_data.split(to_find)
            current_cell_info = current_cell_info[1]
            if(current_cell_info.find("cell (") != -1):
                current_cell_info = current_cell_info.split("cell (")
                current_cell_info = current_cell_info[0]
                sp_current_cell_info = current_cell_info.split("direction")
                self.inputs = list()
                for i in range(len(sp_current_cell_info)):
                    if(sp_current_cell_info[i].find("input") != -1):
                         #find the input pin name in the liberty file, then go search in the verilog line
                         port_root_name = sp_current_cell_info[i-1][sp_current_cell_info[i-1].find("pin") + 4: sp_current_cell_info[i-1].rfind(")")]
                         port_con_name =  self.line_arr[self.io_counter][self.line_arr[self.io_counter].find(port_root_name) + 2: self.line_arr[self.io_counter].find(")")]
                         self.io_counter += 1 
                         self.inputs.append([port_root_name, port_con_name])
        self.inputs = list(self.inputs)

                            
    def find_outputs(self):
        to_find = "cell (" +self.type + ")"
        starting_idex = self.library_data.find(to_find) 
        if(starting_idex != -1):
            current_cell_info = self.library_data.split(to_find)
            current_cell_info = current_cell_info[1]
            if(current_cell_info.find("cell (") != -1):
                current_cell_info = current_cell_info.split("cell (")
                current_cell_info = current_cell_info[0]
                sp_current_cell_info = current_cell_info.split("direction")
                self.outputs = list()
                for i in range(len(sp_current_cell_info)):
                    if(sp_current_cell_info[i].find("output") != -1):
                         #find the input pin name in the liberty file, then go search in the verilog line
                         port_root_name = sp_current_cell_info[i-1][sp_current_cell_info[i-1].find("pin") + 4: sp_current_cell_info[i-1].rfind(")")]
                         port_con_name =  self.line_arr[self.io_counter][self.line_arr[self.io_counter].find(port_root_name) + 2: self.line_arr[self.io_counter].find(")")]
                         self.io_counter += 1 
                         self.outputs.append([port_root_name, port_con_name])

    def get_inputs(self):
        return self.inputs

    def set_out_capacitance(self, cap):
        self.out_capacitance = cap

    def set_out_num(self, number_outputs):
        self.out_num = number_outputs

    def calc_delay(self, library):
        library.get_group
        

def create_cell_format(c):
    cell_form = c.type + " " + c.name +" ( ."
    for inp in c.inputs:
        cell_form = cell_form + inp[0] + "(" + inp[1] + "), ."
    for out in c.outputs:
        cell_form = cell_form + out[0] + "(" + out[1] +") );"
    return cell_form

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


with open(r'verilog parser\rca4.rtlnopwr.v') as myFile:
  text = myFile.read()
result = text.split(";")  

cells_list = list()

for i in result:
    cell_i = cell(i)
    if(cell_i.check_cell()):
        cells_list.append(cell_i)
    

for c in cells_list:
    c.find_inputs()
    c.find_outputs()


liberty_file = r"verilog parser\osu035.lib"
library = parse_liberty(open(liberty_file).read())

calc_cells_out_cap(cells_list)
    

#for c in cells_list:
#    c.calc_delay(library)

run_mode = int(input("Please input \n1 for sizing up cells with large fanout \n2 for cloning high fan out cells \n3 for adding buffers for high fanouts\n"))
max_fan_out = int(input("please input max required fanout\n"))

if(run_mode == 1):
    print("sizing up cells")
    counter = 0
    for c in cells_list:
        if (c.out_num > max_fan_out):
            size=c.type.split("X")
            origin=size[0]
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
    for c in cells_list:
        print(create_cell_format(c))



elif(run_mode == 2):
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
                    new_clone.find_inputs()
                    new_clone.find_outputs()
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
    
    for c in cells_list:
        print(create_cell_format(c))

elif(run_mode == 3):
    print("Adding buffers")
    counter_for_while = 1
    while True:
        length_before_change = len(cells_list)
        counterx = 1
        for c in cells_list:
            if (c.out_num > max_fan_out):
                number_of_bufs = math.ceil(c.out_num / max_fan_out)
                size=c.type.split("X")
                size=int(size[1])
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
                    new_buf.find_inputs()
                    new_buf.find_outputs()
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
    for c in cells_list:
            print(create_cell_format(c))
                
else:
    print("Invalid Argument")
