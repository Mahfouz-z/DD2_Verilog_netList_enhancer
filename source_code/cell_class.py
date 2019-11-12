
#This class is a simple parser class for verilog files. It needs the liberty file that will parse the verilog
#file for in order to validate the existence of the cells in the verilog netlist. The main Functions will be
#described in comments above each line


class cell:
    # The init function opens the liberty file for reading, initializes variables needed later on, and
    # Assigns the type attribute of the cell
    def __init__(self, line):
        f=open(r"source_code\osu035.lib", "r")
        self.library_data=f.read()
        f.close()        
        self.line_arr = line.split(" ")
        self.io_counter = 3                               # We will have inputs or outputs starting from the fourth index of the line_arr
        self.type = self.line_arr[0].replace("\n", "")    # replace to remove any extra endl

    # The check_cell function checks if the type assigned in the intializer is a valid type that exists in
    # the liberty file, which, if true, extracts the name from the line read from the netlist    
    def check_cell(self):
        to_find = "cell (" +self.type + ")"
        if(self.library_data.find(to_find) == -1): 
            return False
        else:
            self.name = self.line_arr[1]
            return True   

    # After checking the cells, this function is called to collect information about the inputs and outputs of
    # each cell and save them in lists as attributes of each cell in the class
    def find_io(self):
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
                self.outputs = list()
                for i in range(len(sp_current_cell_info)):
                    if(sp_current_cell_info[i].find("input") != -1):
                         #find the input pin name in the liberty file, then go search in the verilog line
                         
                         port_root_name = sp_current_cell_info[i-1][sp_current_cell_info[i-1].find("pin(") + 4: sp_current_cell_info[i-1].rfind(")")]
                         
                         port_con_name =  self.line_arr[self.io_counter][self.line_arr[self.io_counter].find(port_root_name) + 1 + len(port_root_name): self.line_arr[self.io_counter].find(")")]
                         
                         self.io_counter += 1 
                         self.inputs.append([port_root_name, port_con_name])

                    elif(sp_current_cell_info[i].find("output") != -1):
                         port_root_name = sp_current_cell_info[i-1][sp_current_cell_info[i-1].find("pin(") + 4: sp_current_cell_info[i-1].rfind(")")]
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
        
