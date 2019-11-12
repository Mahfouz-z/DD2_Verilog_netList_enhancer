
from "source_code\liberty-parser\liberty\parser.py" import select_timing_table
from liberty.parser import parse_liberty
library = parse_liberty(open(r"test_data\gscl45nm.lib").read())
play = library.get_group('cell', 'AND2X2')
assert play is not None


pin = play.get_group('pin', 'Y')

#timings_y = pin.get_groups('timing')
#timing_y_a = [g for g in timings_y if g['related_pin'] == 'A'][0]
#assert timing_y_a['related_pin'] == 'A'
#array = timing_y_a.get_group('cell_rise').get_array('values')
#assert array.shape == (6, 6) 
##the size of this array should be set similar to the number of elements in the index_1
# and index_2 

time=select_timing_table(pin,"A",'cell_rise')
ind1=time.get_array("index_1")

print(ind1)

#ind1 = timing_y_a.get_group('cell_rise').get_array('index_1')
#ind2 =timing_y_a.get_group('cell_rise').get_array('index_2')
##print(str(play))
##print(str(pin))
##print(array)
##print(array[0][0])
#print(ind1[0])
#print(ind1[0][1])
#print(ind2[0][2])

