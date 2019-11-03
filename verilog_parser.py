
class cell:
    def __init__(self, line):
        f=open(r"verilog parser\osu035.lib", "r")
        self.library_data=f.read()
        f.close()        
        self.line_arr = line.split(" ")
        self.type = self.line_arr[0]
        self.name = self.line_arr[1]

    def check_cell(self):
        to_find = "cell (" +self.type + ")"
        if(self.library_data.find(to_find) == -1): 
            return False
        else:
            return True   

    def find_inputs(self):
        to_find = "cell (" +self.type + ")"
        if(self.library_data.find(to_find) != -1):
            print (self.library_data[self.library_data.index(to_find), len(to_find)])


    def find_outputs(self, line):



with open(r'verilog parser\rca4.rtlnopwr.v') as myFile:
  text = myFile.read()
result = text.split(";")  

cell_1 = cell("BUFX2 BUFX2_1 ( .A(fa0_s), .Y(s[0]) );")

cell_1.find_inputs()

