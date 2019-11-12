module rca4 (a, b, ci, s, co);

input ci;
output co;
input [3:0] a;
input [3:0] b;
output [3:0] s;
wire c1;
OR2X1 OR2X1_2 ( .A(_4_), .B(_1_), .Y(c1) );
OR2X2 OR2X2_1 ( .A(c1_10), .B(a[1]), .Y(_12_) );
NAND2X1 NAND2X1_1 ( .A(c1_10), .B(a[1]), .Y(_13_) );
NOR2X1 NOR2X1_1 ( .A(c1_10), .B(a[1]), .Y(_8_) );
AND2X2 AND2X2_1 ( .A(c1_11), .B(a[1]), .Y(_9_) );
AND2X2 AND2X2_2 ( .A(c1_11), .B(a[1]), .Y(_9_) );
BUFX2 BUFX2__11 ( .A(c1_11), .Y(c1_10) );
BUFX2 BUFX2__12 ( .A(c1), .Y(c1_11) );
endmodule