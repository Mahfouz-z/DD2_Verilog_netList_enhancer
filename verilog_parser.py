'''
First: You should initialize a cell using a line from the input .v file
Second: You should check if the given is a valid cell to include in our cell list using --> cell.check_cell()
Third: If the cell is valid, add it to our cell list
Fourth: For Input and output to be ready, you should call cell.find_inputs(), then cell.find_outputs() in order
'''

from liberty.parser import parse_liberty

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
                         self.inputs.append((port_root_name, port_con_name))

                            
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
                         self.outputs.append((port_root_name, port_con_name))

    def get_inputs(self):
        return self.inputs

    def set_out_capacitance(self, cap):
        self.out_capacitance = cap

    def set_delay(self, delay):
        self.delay = delay



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
    else:
        c1.set_out_capacitance(cap)
    


for c in cells_list:
    print(c.out_capacitance)
