# DD2_Verilog_netList_enhancer
Acknowledgments: <br/>
    1. This Project was done for Digital Design 2 course under supervision of Dr Mohamed Shalan <br/>
    2. This Project was done under the umberlla of the csce department at The American University in Cairo <br/> <br/>
Assumptions: <br/>
    1. fixed input transition (intermediate transition). <br/>
    2. we are dealing with single output cells. <br/>
    3. the delays are calculated for each cell with the related pin that has the highest delay. <br/>
    4. the delay calculated is the sum of the delays of all the cell individually, no partiqular path is traced. <br/> <br/>
How to use: <br/>
    change the .v file name in the code and the .lib if needed <br/>
        the .lib file name should be changed in two loactions, inside the class and inside the main code <br/>
        the .v file name should only be changed inside the main code <br/>
    run the code <br/>
    choose the optimizing methodology <br/>
    specify the maximum fan out <br/>
    the program will run and display at the end the frequency of each cell before and after alterations <br/>
    the total delay before and after alterations will also be displayed automatically. The Final Netlist <br/>
    will be saved in a file named output.v that will be present in the running path. <br/> <br/>
Limitations: <br/>
    - depending on the provided liberity file, sizing up may not be possible as large sizes of the cells aren't <br/>
        available in the liberity <br/>
    - the total cell delay may actually increase after modifications since we aim to improve individual cell <br/>
        delays and signals, so added cells or buffers my increase the accumilative cell delay <br/>
    - the program can't handle verilog netlists that contain cells with more than one output, it handles them as <br/>
        single-output cells and neglects all additional outputs <br/>
        
