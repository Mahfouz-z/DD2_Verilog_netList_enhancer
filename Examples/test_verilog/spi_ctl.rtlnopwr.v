module spi_ctl (clk, reset_n, cfg_op_req, cfg_op_type, cfg_transfer_size, cfg_sck_period, cfg_sck_cs_period, cfg_cs_byte, cfg_datain, byte_in, sck_int, cfg_dataout, op_done, cs_int_n, sck_pe, sck_ne, shift_out, shift_in, byte_out, load_byte);

input clk;
input reset_n;
input cfg_op_req;
output sck_int;
output op_done;
output cs_int_n;
output sck_pe;
output sck_ne;
output shift_out;
output shift_in;
output load_byte;
input [1:0] cfg_op_type;
input [1:0] cfg_transfer_size;
input [5:0] cfg_sck_period;
input [4:0] cfg_sck_cs_period;
input [7:0] cfg_cs_byte;
input [31:0] cfg_datain;
input [7:0] byte_in;
output [31:0] cfg_dataout;
output [7:0] byte_out;

wire vdd = 1'b1;
wire gnd = 1'b0;

BUFX4 BUFX4_1 ( .A(clk), .Y(clk_bF_buf6) );
BUFX4 BUFX4_2 ( .A(clk), .Y(clk_bF_buf5) );
BUFX4 BUFX4_3 ( .A(clk), .Y(clk_bF_buf4) );
BUFX4 BUFX4_4 ( .A(clk), .Y(clk_bF_buf3) );
BUFX4 BUFX4_5 ( .A(clk), .Y(clk_bF_buf2) );
BUFX4 BUFX4_6 ( .A(clk), .Y(clk_bF_buf1) );
BUFX4 BUFX4_7 ( .A(clk), .Y(clk_bF_buf0) );
BUFX4 BUFX4_8 ( .A(_179_), .Y(_179__bF_buf3) );
BUFX4 BUFX4_9 ( .A(_179_), .Y(_179__bF_buf2) );
BUFX4 BUFX4_10 ( .A(_179_), .Y(_179__bF_buf1) );
BUFX4 BUFX4_11 ( .A(_179_), .Y(_179__bF_buf0) );
BUFX4 BUFX4_12 ( .A(spiif_cs_1_), .Y(spiif_cs_1_bF_buf5) );
BUFX4 BUFX4_13 ( .A(spiif_cs_1_), .Y(spiif_cs_1_bF_buf4) );
BUFX4 BUFX4_14 ( .A(spiif_cs_1_), .Y(spiif_cs_1_bF_buf3) );
BUFX4 BUFX4_15 ( .A(spiif_cs_1_), .Y(spiif_cs_1_bF_buf2) );
BUFX4 BUFX4_16 ( .A(spiif_cs_1_), .Y(spiif_cs_1_bF_buf1) );
BUFX4 BUFX4_17 ( .A(spiif_cs_1_), .Y(spiif_cs_1_bF_buf0) );
BUFX4 BUFX4_18 ( .A(reset_n), .Y(reset_n_bF_buf6) );
BUFX4 BUFX4_19 ( .A(reset_n), .Y(reset_n_bF_buf5) );
BUFX4 BUFX4_20 ( .A(reset_n), .Y(reset_n_bF_buf4) );
BUFX4 BUFX4_21 ( .A(reset_n), .Y(reset_n_bF_buf3) );
BUFX4 BUFX4_22 ( .A(reset_n), .Y(reset_n_bF_buf2) );
BUFX4 BUFX4_23 ( .A(reset_n), .Y(reset_n_bF_buf1) );
BUFX4 BUFX4_24 ( .A(reset_n), .Y(reset_n_bF_buf0) );
INVX1 INVX1_1 ( .A(spiif_cs_2_), .Y(_14_) );
INVX1 INVX1_2 ( .A(spiif_cs_5_), .Y(_15_) );
NAND2X1 NAND2X1_1 ( .A(_14_), .B(_15_), .Y(_16_) );
INVX1 INVX1_3 ( .A(_16_), .Y(_17_) );
NAND3X1 NAND3X1_1 ( .A(sck_cnt_1_), .B(sck_cnt_2_), .C(sck_cnt_0_), .Y(_18_) );
INVX1 INVX1_4 ( .A(sck_cnt_5_), .Y(_19_) );
NOR2X1 NOR2X1_1 ( .A(sck_cnt_4_), .B(sck_cnt_3_), .Y(_20_) );
NAND3X1 NAND3X1_2 ( .A(_19_), .B(_329_), .C(_20_), .Y(_21_) );
NOR2X1 NOR2X1_2 ( .A(_18_), .B(_21_), .Y(_22_) );
INVX1 INVX1_5 ( .A(_22_), .Y(_23_) );
INVX4 INVX4_1 ( .A(_329_), .Y(_24_) );
INVX1 INVX1_6 ( .A(sck_cnt_3_), .Y(_25_) );
INVX1 INVX1_7 ( .A(cfg_sck_cs_period[2]), .Y(_26_) );
AOI22X1 AOI22X1_1 ( .A(_25_), .B(cfg_sck_cs_period[3]), .C(_26_), .D(sck_cnt_2_), .Y(_27_) );
INVX1 INVX1_8 ( .A(sck_cnt_2_), .Y(_28_) );
INVX1 INVX1_9 ( .A(cfg_sck_cs_period[1]), .Y(_29_) );
AOI22X1 AOI22X1_2 ( .A(_28_), .B(cfg_sck_cs_period[2]), .C(sck_cnt_1_), .D(_29_), .Y(_30_) );
NAND2X1 NAND2X1_2 ( .A(sck_cnt_0_), .B(cfg_sck_cs_period[0]), .Y(_31_) );
OR2X2 OR2X2_1 ( .A(sck_cnt_0_), .B(cfg_sck_cs_period[0]), .Y(_32_) );
NAND2X1 NAND2X1_3 ( .A(_31_), .B(_32_), .Y(_33_) );
NAND3X1 NAND3X1_3 ( .A(_27_), .B(_30_), .C(_33_), .Y(_34_) );
INVX1 INVX1_10 ( .A(cfg_sck_cs_period[4]), .Y(_35_) );
NAND2X1 NAND2X1_4 ( .A(sck_cnt_4_), .B(_35_), .Y(_36_) );
INVX2 INVX2_1 ( .A(sck_cnt_4_), .Y(_37_) );
INVX1 INVX1_11 ( .A(cfg_sck_cs_period[3]), .Y(_38_) );
AOI22X1 AOI22X1_3 ( .A(_37_), .B(cfg_sck_cs_period[4]), .C(_38_), .D(sck_cnt_3_), .Y(_39_) );
INVX1 INVX1_12 ( .A(sck_cnt_1_), .Y(_40_) );
AOI21X1 AOI21X1_1 ( .A(_40_), .B(cfg_sck_cs_period[1]), .C(sck_cnt_5_), .Y(_41_) );
NAND3X1 NAND3X1_4 ( .A(_36_), .B(_41_), .C(_39_), .Y(_42_) );
NOR2X1 NOR2X1_3 ( .A(_42_), .B(_34_), .Y(_43_) );
INVX1 INVX1_13 ( .A(_43_), .Y(_44_) );
OAI21X1 OAI21X1_1 ( .A(_24_), .B(_44_), .C(spiif_cs_1_bF_buf4), .Y(_45_) );
OAI21X1 OAI21X1_2 ( .A(_17_), .B(_23_), .C(_45_), .Y(_322__1_) );
OAI21X1 OAI21X1_3 ( .A(_18_), .B(_21_), .C(spiif_cs_2_), .Y(_46_) );
NOR2X1 NOR2X1_4 ( .A(cfg_op_type[0]), .B(cfg_op_type[1]), .Y(_47_) );
INVX1 INVX1_14 ( .A(_47_), .Y(_48_) );
NAND3X1 NAND3X1_5 ( .A(_329_), .B(spiif_cs_3_), .C(_43_), .Y(_49_) );
OAI21X1 OAI21X1_4 ( .A(_48_), .B(_49_), .C(_46_), .Y(_322__2_) );
INVX1 INVX1_15 ( .A(spiif_cs_4_), .Y(_50_) );
INVX4 INVX4_2 ( .A(cfg_op_req), .Y(_51_) );
INVX2 INVX2_2 ( .A(byte_cnt_1_), .Y(_52_) );
INVX1 INVX1_16 ( .A(cfg_transfer_size[0]), .Y(_53_) );
AOI22X1 AOI22X1_4 ( .A(_53_), .B(byte_cnt_0_), .C(cfg_transfer_size[1]), .D(_52_), .Y(_54_) );
OAI21X1 OAI21X1_5 ( .A(cfg_transfer_size[1]), .B(_52_), .C(_54_), .Y(_55_) );
INVX2 INVX2_3 ( .A(byte_cnt_2_), .Y(_56_) );
OAI21X1 OAI21X1_6 ( .A(byte_cnt_0_), .B(_53_), .C(_56_), .Y(_57_) );
NOR2X1 NOR2X1_5 ( .A(_57_), .B(_55_), .Y(_58_) );
INVX1 INVX1_17 ( .A(_58_), .Y(_59_) );
NAND2X1 NAND2X1_5 ( .A(spiif_cs_1_bF_buf4), .B(_329_), .Y(_60_) );
NOR3X1 NOR3X1_1 ( .A(_60_), .B(_42_), .C(_34_), .Y(_61_) );
INVX1 INVX1_18 ( .A(_61_), .Y(_62_) );
OAI22X1 OAI22X1_1 ( .A(_50_), .B(_51_), .C(_59_), .D(_62_), .Y(_322__4_) );
OAI21X1 OAI21X1_7 ( .A(_55_), .B(_57_), .C(_61_), .Y(_63_) );
NAND2X1 NAND2X1_6 ( .A(cfg_op_req), .B(spiif_cs_0_), .Y(_64_) );
OAI21X1 OAI21X1_8 ( .A(_24_), .B(_44_), .C(spiif_cs_3_), .Y(_65_) );
NAND3X1 NAND3X1_6 ( .A(_64_), .B(_63_), .C(_65_), .Y(_322__3_) );
OAI22X1 OAI22X1_2 ( .A(_15_), .B(_22_), .C(_47_), .D(_49_), .Y(_322__5_) );
AND2X2 AND2X2_1 ( .A(_329_), .B(shift_enb), .Y(_332_) );
INVX1 INVX1_19 ( .A(sck_cnt_0_), .Y(_66_) );
NOR2X1 NOR2X1_6 ( .A(_66_), .B(_24_), .Y(_67_) );
NOR2X1 NOR2X1_7 ( .A(clr_sck_cnt), .B(_24_), .Y(_68_) );
INVX1 INVX1_20 ( .A(_68_), .Y(_69_) );
AOI21X1 AOI21X1_2 ( .A(_69_), .B(_66_), .C(_67_), .Y(_7__0_) );
INVX1 INVX1_21 ( .A(clr_sck_cnt), .Y(_70_) );
OAI22X1 OAI22X1_3 ( .A(_24_), .B(_70_), .C(sck_cnt_1_), .D(_67_), .Y(_71_) );
AOI21X1 AOI21X1_3 ( .A(sck_cnt_1_), .B(_67_), .C(_71_), .Y(_7__1_) );
OAI21X1 OAI21X1_9 ( .A(_40_), .B(_66_), .C(_28_), .Y(_72_) );
NAND3X1 NAND3X1_7 ( .A(_18_), .B(_68_), .C(_72_), .Y(_73_) );
OAI21X1 OAI21X1_10 ( .A(_28_), .B(_329_), .C(_73_), .Y(_7__2_) );
NOR2X1 NOR2X1_8 ( .A(_25_), .B(_18_), .Y(_74_) );
INVX1 INVX1_22 ( .A(_74_), .Y(_75_) );
AOI22X1 AOI22X1_5 ( .A(sck_cnt_3_), .B(_24_), .C(_68_), .D(_75_), .Y(_76_) );
AOI21X1 AOI21X1_4 ( .A(_25_), .B(_18_), .C(_76_), .Y(_7__3_) );
NAND3X1 NAND3X1_8 ( .A(_37_), .B(_68_), .C(_74_), .Y(_77_) );
AOI21X1 AOI21X1_5 ( .A(_75_), .B(_70_), .C(_24_), .Y(_78_) );
OAI21X1 OAI21X1_11 ( .A(_37_), .B(_78_), .C(_77_), .Y(_7__4_) );
OAI21X1 OAI21X1_12 ( .A(_37_), .B(_75_), .C(_19_), .Y(_79_) );
NAND3X1 NAND3X1_9 ( .A(sck_cnt_4_), .B(sck_cnt_5_), .C(_74_), .Y(_80_) );
NAND3X1 NAND3X1_10 ( .A(_68_), .B(_80_), .C(_79_), .Y(_81_) );
OAI21X1 OAI21X1_13 ( .A(_19_), .B(_329_), .C(_81_), .Y(_7__5_) );
OAI21X1 OAI21X1_14 ( .A(_60_), .B(_44_), .C(byte_cnt_0_), .Y(_82_) );
OAI21X1 OAI21X1_15 ( .A(byte_cnt_0_), .B(_63_), .C(_82_), .Y(_0__0_) );
NOR2X1 NOR2X1_9 ( .A(byte_cnt_0_), .B(_52_), .Y(_83_) );
INVX1 INVX1_23 ( .A(byte_cnt_0_), .Y(_84_) );
NOR2X1 NOR2X1_10 ( .A(byte_cnt_1_), .B(_84_), .Y(_85_) );
NOR2X1 NOR2X1_11 ( .A(_83_), .B(_85_), .Y(_86_) );
OAI22X1 OAI22X1_4 ( .A(_52_), .B(_61_), .C(_86_), .D(_63_), .Y(_0__1_) );
INVX1 INVX1_24 ( .A(_60_), .Y(_87_) );
NAND3X1 NAND3X1_11 ( .A(byte_cnt_0_), .B(byte_cnt_1_), .C(_61_), .Y(_88_) );
NAND3X1 NAND3X1_12 ( .A(byte_cnt_0_), .B(byte_cnt_1_), .C(_43_), .Y(_89_) );
NAND2X1 NAND2X1_7 ( .A(_58_), .B(_43_), .Y(_90_) );
OAI21X1 OAI21X1_16 ( .A(_56_), .B(_89_), .C(_90_), .Y(_91_) );
AOI22X1 AOI22X1_6 ( .A(_56_), .B(_88_), .C(_87_), .D(_91_), .Y(_0__2_) );
INVX1 INVX1_25 ( .A(_328_), .Y(_92_) );
AND2X2 AND2X2_2 ( .A(cfg_op_req), .B(sck_out_en), .Y(_93_) );
NAND2X1 NAND2X1_8 ( .A(cfg_sck_period[5]), .B(clk_cnt_5_), .Y(_94_) );
OR2X2 OR2X2_2 ( .A(cfg_sck_period[5]), .B(clk_cnt_5_), .Y(_95_) );
XOR2X1 XOR2X1_1 ( .A(clk_cnt_4_), .B(cfg_sck_period[4]), .Y(_96_) );
AOI21X1 AOI21X1_6 ( .A(_94_), .B(_95_), .C(_96_), .Y(_97_) );
INVX2 INVX2_4 ( .A(clk_cnt_1_), .Y(_98_) );
INVX1 INVX1_26 ( .A(cfg_sck_period[1]), .Y(_99_) );
NOR2X1 NOR2X1_12 ( .A(_98_), .B(_99_), .Y(_100_) );
NOR2X1 NOR2X1_13 ( .A(clk_cnt_1_), .B(cfg_sck_period[1]), .Y(_101_) );
XNOR2X1 XNOR2X1_1 ( .A(clk_cnt_0_), .B(cfg_sck_period[0]), .Y(_102_) );
OAI21X1 OAI21X1_17 ( .A(_100_), .B(_101_), .C(_102_), .Y(_103_) );
XNOR2X1 XNOR2X1_2 ( .A(clk_cnt_3_), .B(cfg_sck_period[3]), .Y(_104_) );
AND2X2 AND2X2_3 ( .A(clk_cnt_2_), .B(cfg_sck_period[2]), .Y(_105_) );
NOR2X1 NOR2X1_14 ( .A(clk_cnt_2_), .B(cfg_sck_period[2]), .Y(_106_) );
OAI21X1 OAI21X1_18 ( .A(_105_), .B(_106_), .C(_104_), .Y(_107_) );
NOR2X1 NOR2X1_15 ( .A(_103_), .B(_107_), .Y(_108_) );
AND2X2 AND2X2_4 ( .A(_108_), .B(_97_), .Y(_109_) );
NAND2X1 NAND2X1_9 ( .A(_93_), .B(_109_), .Y(_110_) );
INVX1 INVX1_27 ( .A(clk_cnt_2_), .Y(_111_) );
INVX1 INVX1_28 ( .A(clk_cnt_3_), .Y(_112_) );
NAND2X1 NAND2X1_10 ( .A(cfg_sck_period[4]), .B(_112_), .Y(_113_) );
OAI21X1 OAI21X1_19 ( .A(_111_), .B(cfg_sck_period[3]), .C(_113_), .Y(_114_) );
NAND2X1 NAND2X1_11 ( .A(cfg_sck_period[3]), .B(_111_), .Y(_115_) );
OAI21X1 OAI21X1_20 ( .A(cfg_sck_period[2]), .B(_98_), .C(_115_), .Y(_116_) );
NOR2X1 NOR2X1_16 ( .A(_114_), .B(_116_), .Y(_117_) );
INVX1 INVX1_29 ( .A(cfg_sck_period[5]), .Y(_118_) );
OAI22X1 OAI22X1_5 ( .A(clk_cnt_4_), .B(_118_), .C(_112_), .D(cfg_sck_period[4]), .Y(_119_) );
AOI21X1 AOI21X1_7 ( .A(_118_), .B(clk_cnt_4_), .C(_119_), .Y(_120_) );
AOI22X1 AOI22X1_7 ( .A(_98_), .B(cfg_sck_period[2]), .C(_99_), .D(clk_cnt_0_), .Y(_121_) );
INVX1 INVX1_30 ( .A(clk_cnt_0_), .Y(_122_) );
AOI21X1 AOI21X1_8 ( .A(_122_), .B(cfg_sck_period[1]), .C(clk_cnt_5_), .Y(_123_) );
AND2X2 AND2X2_5 ( .A(_121_), .B(_123_), .Y(_124_) );
AND2X2 AND2X2_6 ( .A(_124_), .B(_120_), .Y(_125_) );
NAND2X1 NAND2X1_12 ( .A(_117_), .B(_125_), .Y(_126_) );
INVX1 INVX1_31 ( .A(_126_), .Y(_127_) );
AOI22X1 AOI22X1_8 ( .A(_93_), .B(_127_), .C(_92_), .D(_110_), .Y(_8_) );
NAND2X1 NAND2X1_13 ( .A(_126_), .B(_109_), .Y(_128_) );
NAND3X1 NAND3X1_13 ( .A(cfg_op_req), .B(clk_cnt_0_), .C(_128_), .Y(_2__0_) );
NAND2X1 NAND2X1_14 ( .A(_97_), .B(_108_), .Y(_129_) );
AOI21X1 AOI21X1_9 ( .A(_117_), .B(_125_), .C(_129_), .Y(_130_) );
XNOR2X1 XNOR2X1_3 ( .A(clk_cnt_1_), .B(clk_cnt_0_), .Y(_131_) );
NOR3X1 NOR3X1_2 ( .A(_51_), .B(_131_), .C(_130_), .Y(_2__1_) );
OAI21X1 OAI21X1_21 ( .A(_98_), .B(_122_), .C(_111_), .Y(_132_) );
NAND3X1 NAND3X1_14 ( .A(clk_cnt_2_), .B(clk_cnt_1_), .C(clk_cnt_0_), .Y(_133_) );
NAND2X1 NAND2X1_15 ( .A(_133_), .B(_132_), .Y(_134_) );
NOR3X1 NOR3X1_3 ( .A(_51_), .B(_134_), .C(_130_), .Y(_2__2_) );
NAND2X1 NAND2X1_16 ( .A(_112_), .B(_133_), .Y(_135_) );
NOR2X1 NOR2X1_17 ( .A(_112_), .B(_133_), .Y(_136_) );
INVX1 INVX1_32 ( .A(_136_), .Y(_137_) );
NAND2X1 NAND2X1_17 ( .A(_135_), .B(_137_), .Y(_138_) );
NOR3X1 NOR3X1_4 ( .A(_51_), .B(_138_), .C(_130_), .Y(_2__3_) );
XNOR2X1 XNOR2X1_4 ( .A(_136_), .B(clk_cnt_4_), .Y(_139_) );
NOR3X1 NOR3X1_5 ( .A(_51_), .B(_139_), .C(_130_), .Y(_2__4_) );
NAND2X1 NAND2X1_18 ( .A(clk_cnt_4_), .B(_136_), .Y(_140_) );
XOR2X1 XOR2X1_2 ( .A(_140_), .B(clk_cnt_5_), .Y(_141_) );
NOR3X1 NOR3X1_6 ( .A(_51_), .B(_141_), .C(_130_), .Y(_2__5_) );
INVX1 INVX1_33 ( .A(_324__0_), .Y(_142_) );
INVX2 INVX2_5 ( .A(spiif_cs_0_), .Y(_143_) );
NAND2X1 NAND2X1_19 ( .A(spiif_cs_1_bF_buf3), .B(_143_), .Y(_144_) );
NAND2X1 NAND2X1_20 ( .A(byte_cnt_0_), .B(byte_cnt_1_), .Y(_145_) );
INVX1 INVX1_34 ( .A(_145_), .Y(_146_) );
INVX1 INVX1_35 ( .A(cfg_op_type[1]), .Y(_147_) );
NAND2X1 NAND2X1_21 ( .A(cfg_op_type[0]), .B(_147_), .Y(_148_) );
NOR2X1 NOR2X1_18 ( .A(_24_), .B(_148_), .Y(_149_) );
NAND3X1 NAND3X1_15 ( .A(_146_), .B(_149_), .C(_43_), .Y(_150_) );
AOI22X1 AOI22X1_9 ( .A(_64_), .B(_144_), .C(spiif_cs_1_bF_buf3), .D(_150_), .Y(_151_) );
NAND2X1 NAND2X1_22 ( .A(spiif_cs_1_bF_buf1), .B(byte_in[0]), .Y(_152_) );
OR2X2 OR2X2_3 ( .A(_150_), .B(_152_), .Y(_153_) );
OAI21X1 OAI21X1_22 ( .A(_142_), .B(_151_), .C(_153_), .Y(_1__0_) );
INVX1 INVX1_36 ( .A(_324__1_), .Y(_154_) );
NAND2X1 NAND2X1_23 ( .A(spiif_cs_1_bF_buf3), .B(byte_in[1]), .Y(_155_) );
OR2X2 OR2X2_4 ( .A(_150_), .B(_155_), .Y(_156_) );
OAI21X1 OAI21X1_23 ( .A(_154_), .B(_151_), .C(_156_), .Y(_1__1_) );
INVX1 INVX1_37 ( .A(_324__2_), .Y(_157_) );
NAND2X1 NAND2X1_24 ( .A(spiif_cs_1_bF_buf0), .B(byte_in[2]), .Y(_158_) );
OR2X2 OR2X2_5 ( .A(_150_), .B(_158_), .Y(_159_) );
OAI21X1 OAI21X1_24 ( .A(_157_), .B(_151_), .C(_159_), .Y(_1__2_) );
INVX1 INVX1_38 ( .A(_324__3_), .Y(_160_) );
NAND2X1 NAND2X1_25 ( .A(spiif_cs_1_bF_buf0), .B(byte_in[3]), .Y(_161_) );
OR2X2 OR2X2_6 ( .A(_150_), .B(_161_), .Y(_162_) );
OAI21X1 OAI21X1_25 ( .A(_160_), .B(_151_), .C(_162_), .Y(_1__3_) );
INVX1 INVX1_39 ( .A(_324__4_), .Y(_163_) );
NAND2X1 NAND2X1_26 ( .A(spiif_cs_1_bF_buf3), .B(byte_in[4]), .Y(_164_) );
OR2X2 OR2X2_7 ( .A(_150_), .B(_164_), .Y(_165_) );
OAI21X1 OAI21X1_26 ( .A(_163_), .B(_151_), .C(_165_), .Y(_1__4_) );
INVX1 INVX1_40 ( .A(_324__5_), .Y(_166_) );
NAND2X1 NAND2X1_27 ( .A(spiif_cs_1_bF_buf0), .B(byte_in[5]), .Y(_167_) );
OR2X2 OR2X2_8 ( .A(_150_), .B(_167_), .Y(_168_) );
OAI21X1 OAI21X1_27 ( .A(_166_), .B(_151_), .C(_168_), .Y(_1__5_) );
INVX1 INVX1_41 ( .A(_324__6_), .Y(_169_) );
NAND2X1 NAND2X1_28 ( .A(spiif_cs_1_bF_buf3), .B(byte_in[6]), .Y(_170_) );
OR2X2 OR2X2_9 ( .A(_150_), .B(_170_), .Y(_171_) );
OAI21X1 OAI21X1_28 ( .A(_169_), .B(_151_), .C(_171_), .Y(_1__6_) );
INVX1 INVX1_42 ( .A(_324__7_), .Y(_172_) );
NAND2X1 NAND2X1_29 ( .A(spiif_cs_1_bF_buf1), .B(byte_in[7]), .Y(_173_) );
OR2X2 OR2X2_10 ( .A(_150_), .B(_173_), .Y(_174_) );
OAI21X1 OAI21X1_29 ( .A(_172_), .B(_151_), .C(_174_), .Y(_1__7_) );
INVX1 INVX1_43 ( .A(_324__8_), .Y(_175_) );
AND2X2 AND2X2_7 ( .A(_149_), .B(_83_), .Y(_176_) );
NAND2X1 NAND2X1_30 ( .A(_176_), .B(_43_), .Y(_177_) );
OAI21X1 OAI21X1_30 ( .A(byte_in[0]), .B(_177_), .C(spiif_cs_1_bF_buf1), .Y(_178_) );
AND2X2 AND2X2_8 ( .A(_144_), .B(_64_), .Y(_179_) );
NAND2X1 NAND2X1_31 ( .A(_324__8_), .B(_179__bF_buf3), .Y(_180_) );
AOI22X1 AOI22X1_10 ( .A(_175_), .B(_177_), .C(_180_), .D(_178_), .Y(_1__8_) );
INVX1 INVX1_44 ( .A(_324__9_), .Y(_181_) );
OAI21X1 OAI21X1_31 ( .A(byte_in[1]), .B(_177_), .C(spiif_cs_1_bF_buf1), .Y(_182_) );
NAND2X1 NAND2X1_32 ( .A(_324__9_), .B(_179__bF_buf3), .Y(_183_) );
AOI22X1 AOI22X1_11 ( .A(_181_), .B(_177_), .C(_183_), .D(_182_), .Y(_1__9_) );
INVX1 INVX1_45 ( .A(_324__10_), .Y(_184_) );
OAI21X1 OAI21X1_32 ( .A(byte_in[2]), .B(_177_), .C(spiif_cs_1_bF_buf2), .Y(_185_) );
NAND2X1 NAND2X1_33 ( .A(_324__10_), .B(_179__bF_buf1), .Y(_186_) );
AOI22X1 AOI22X1_12 ( .A(_184_), .B(_177_), .C(_186_), .D(_185_), .Y(_1__10_) );
INVX1 INVX1_46 ( .A(_324__11_), .Y(_187_) );
OAI21X1 OAI21X1_33 ( .A(byte_in[3]), .B(_177_), .C(spiif_cs_1_bF_buf3), .Y(_188_) );
NAND2X1 NAND2X1_34 ( .A(_324__11_), .B(_179__bF_buf0), .Y(_189_) );
AOI22X1 AOI22X1_13 ( .A(_187_), .B(_177_), .C(_189_), .D(_188_), .Y(_1__11_) );
INVX1 INVX1_47 ( .A(_324__12_), .Y(_190_) );
OAI21X1 OAI21X1_34 ( .A(byte_in[4]), .B(_177_), .C(spiif_cs_1_bF_buf4), .Y(_191_) );
NAND2X1 NAND2X1_35 ( .A(_324__12_), .B(_179__bF_buf0), .Y(_192_) );
AOI22X1 AOI22X1_14 ( .A(_190_), .B(_177_), .C(_192_), .D(_191_), .Y(_1__12_) );
INVX1 INVX1_48 ( .A(_324__13_), .Y(_193_) );
OAI21X1 OAI21X1_35 ( .A(byte_in[5]), .B(_177_), .C(spiif_cs_1_bF_buf2), .Y(_194_) );
NAND2X1 NAND2X1_36 ( .A(_324__13_), .B(_179__bF_buf1), .Y(_195_) );
AOI22X1 AOI22X1_15 ( .A(_193_), .B(_177_), .C(_195_), .D(_194_), .Y(_1__13_) );
INVX1 INVX1_49 ( .A(_324__14_), .Y(_196_) );
OAI21X1 OAI21X1_36 ( .A(byte_in[6]), .B(_177_), .C(spiif_cs_1_bF_buf5), .Y(_197_) );
NAND2X1 NAND2X1_37 ( .A(_324__14_), .B(_179__bF_buf1), .Y(_198_) );
AOI22X1 AOI22X1_16 ( .A(_196_), .B(_177_), .C(_198_), .D(_197_), .Y(_1__14_) );
INVX1 INVX1_50 ( .A(_324__15_), .Y(_199_) );
OAI21X1 OAI21X1_37 ( .A(byte_in[7]), .B(_177_), .C(spiif_cs_1_bF_buf2), .Y(_200_) );
NAND2X1 NAND2X1_38 ( .A(_324__15_), .B(_179__bF_buf0), .Y(_201_) );
AOI22X1 AOI22X1_17 ( .A(_199_), .B(_177_), .C(_201_), .D(_200_), .Y(_1__15_) );
INVX1 INVX1_51 ( .A(_324__16_), .Y(_202_) );
INVX4 INVX4_3 ( .A(_85_), .Y(_203_) );
INVX1 INVX1_52 ( .A(_149_), .Y(_204_) );
NOR2X1 NOR2X1_19 ( .A(_203_), .B(_204_), .Y(_205_) );
NAND2X1 NAND2X1_39 ( .A(_43_), .B(_205_), .Y(_206_) );
OAI21X1 OAI21X1_38 ( .A(byte_in[0]), .B(_206_), .C(spiif_cs_1_bF_buf5), .Y(_207_) );
NAND2X1 NAND2X1_40 ( .A(_324__16_), .B(_179__bF_buf2), .Y(_208_) );
AOI22X1 AOI22X1_18 ( .A(_202_), .B(_206_), .C(_208_), .D(_207_), .Y(_1__16_) );
INVX1 INVX1_53 ( .A(_324__17_), .Y(_209_) );
OAI21X1 OAI21X1_39 ( .A(byte_in[1]), .B(_206_), .C(spiif_cs_1_bF_buf5), .Y(_210_) );
NAND2X1 NAND2X1_41 ( .A(_324__17_), .B(_179__bF_buf0), .Y(_211_) );
AOI22X1 AOI22X1_19 ( .A(_209_), .B(_206_), .C(_211_), .D(_210_), .Y(_1__17_) );
INVX1 INVX1_54 ( .A(_324__18_), .Y(_212_) );
OAI21X1 OAI21X1_40 ( .A(byte_in[2]), .B(_206_), .C(spiif_cs_1_bF_buf4), .Y(_213_) );
NAND2X1 NAND2X1_42 ( .A(_324__18_), .B(_179__bF_buf1), .Y(_214_) );
AOI22X1 AOI22X1_20 ( .A(_212_), .B(_206_), .C(_214_), .D(_213_), .Y(_1__18_) );
INVX1 INVX1_55 ( .A(_324__19_), .Y(_215_) );
OAI21X1 OAI21X1_41 ( .A(byte_in[3]), .B(_206_), .C(spiif_cs_1_bF_buf3), .Y(_216_) );
NAND2X1 NAND2X1_43 ( .A(_324__19_), .B(_179__bF_buf2), .Y(_217_) );
AOI22X1 AOI22X1_21 ( .A(_215_), .B(_206_), .C(_217_), .D(_216_), .Y(_1__19_) );
INVX1 INVX1_56 ( .A(_324__20_), .Y(_218_) );
OAI21X1 OAI21X1_42 ( .A(byte_in[4]), .B(_206_), .C(spiif_cs_1_bF_buf2), .Y(_219_) );
NAND2X1 NAND2X1_44 ( .A(_324__20_), .B(_179__bF_buf0), .Y(_220_) );
AOI22X1 AOI22X1_22 ( .A(_218_), .B(_206_), .C(_220_), .D(_219_), .Y(_1__20_) );
INVX1 INVX1_57 ( .A(_324__21_), .Y(_221_) );
OAI21X1 OAI21X1_43 ( .A(byte_in[5]), .B(_206_), .C(spiif_cs_1_bF_buf0), .Y(_222_) );
NAND2X1 NAND2X1_45 ( .A(_324__21_), .B(_179__bF_buf2), .Y(_223_) );
AOI22X1 AOI22X1_23 ( .A(_221_), .B(_206_), .C(_223_), .D(_222_), .Y(_1__21_) );
INVX1 INVX1_58 ( .A(_324__22_), .Y(_224_) );
OAI21X1 OAI21X1_44 ( .A(byte_in[6]), .B(_206_), .C(spiif_cs_1_bF_buf5), .Y(_225_) );
NAND2X1 NAND2X1_46 ( .A(_324__22_), .B(_179__bF_buf2), .Y(_226_) );
AOI22X1 AOI22X1_24 ( .A(_224_), .B(_206_), .C(_226_), .D(_225_), .Y(_1__22_) );
INVX1 INVX1_59 ( .A(_324__23_), .Y(_227_) );
OAI21X1 OAI21X1_45 ( .A(byte_in[7]), .B(_206_), .C(spiif_cs_1_bF_buf2), .Y(_228_) );
NAND2X1 NAND2X1_47 ( .A(_324__23_), .B(_179__bF_buf1), .Y(_229_) );
AOI22X1 AOI22X1_25 ( .A(_227_), .B(_206_), .C(_229_), .D(_228_), .Y(_1__23_) );
INVX1 INVX1_60 ( .A(_324__24_), .Y(_230_) );
NAND2X1 NAND2X1_48 ( .A(_84_), .B(_52_), .Y(_231_) );
NOR2X1 NOR2X1_20 ( .A(_231_), .B(_204_), .Y(_232_) );
NAND2X1 NAND2X1_49 ( .A(_43_), .B(_232_), .Y(_233_) );
OAI21X1 OAI21X1_46 ( .A(byte_in[0]), .B(_233_), .C(spiif_cs_1_bF_buf0), .Y(_234_) );
NAND2X1 NAND2X1_50 ( .A(_324__24_), .B(_179__bF_buf2), .Y(_235_) );
AOI22X1 AOI22X1_26 ( .A(_230_), .B(_233_), .C(_235_), .D(_234_), .Y(_1__24_) );
INVX1 INVX1_61 ( .A(_324__25_), .Y(_236_) );
OAI21X1 OAI21X1_47 ( .A(byte_in[1]), .B(_233_), .C(spiif_cs_1_bF_buf1), .Y(_237_) );
NAND2X1 NAND2X1_51 ( .A(_324__25_), .B(_179__bF_buf3), .Y(_238_) );
AOI22X1 AOI22X1_27 ( .A(_236_), .B(_233_), .C(_238_), .D(_237_), .Y(_1__25_) );
INVX1 INVX1_62 ( .A(_324__26_), .Y(_239_) );
OAI21X1 OAI21X1_48 ( .A(byte_in[2]), .B(_233_), .C(spiif_cs_1_bF_buf0), .Y(_240_) );
NAND2X1 NAND2X1_52 ( .A(_324__26_), .B(_179__bF_buf3), .Y(_241_) );
AOI22X1 AOI22X1_28 ( .A(_239_), .B(_233_), .C(_241_), .D(_240_), .Y(_1__26_) );
INVX1 INVX1_63 ( .A(_324__27_), .Y(_242_) );
OAI21X1 OAI21X1_49 ( .A(byte_in[3]), .B(_233_), .C(spiif_cs_1_bF_buf0), .Y(_243_) );
NAND2X1 NAND2X1_53 ( .A(_324__27_), .B(_179__bF_buf2), .Y(_244_) );
AOI22X1 AOI22X1_29 ( .A(_242_), .B(_233_), .C(_244_), .D(_243_), .Y(_1__27_) );
INVX1 INVX1_64 ( .A(_324__28_), .Y(_245_) );
OAI21X1 OAI21X1_50 ( .A(byte_in[4]), .B(_233_), .C(spiif_cs_1_bF_buf2), .Y(_246_) );
NAND2X1 NAND2X1_54 ( .A(_324__28_), .B(_179__bF_buf1), .Y(_247_) );
AOI22X1 AOI22X1_30 ( .A(_245_), .B(_233_), .C(_247_), .D(_246_), .Y(_1__28_) );
INVX1 INVX1_65 ( .A(_324__29_), .Y(_248_) );
OAI21X1 OAI21X1_51 ( .A(byte_in[5]), .B(_233_), .C(spiif_cs_1_bF_buf1), .Y(_249_) );
NAND2X1 NAND2X1_55 ( .A(_324__29_), .B(_179__bF_buf3), .Y(_250_) );
AOI22X1 AOI22X1_31 ( .A(_248_), .B(_233_), .C(_250_), .D(_249_), .Y(_1__29_) );
INVX1 INVX1_66 ( .A(_324__30_), .Y(_251_) );
OAI21X1 OAI21X1_52 ( .A(byte_in[6]), .B(_233_), .C(spiif_cs_1_bF_buf4), .Y(_252_) );
NAND2X1 NAND2X1_56 ( .A(_324__30_), .B(_179__bF_buf0), .Y(_253_) );
AOI22X1 AOI22X1_32 ( .A(_251_), .B(_233_), .C(_253_), .D(_252_), .Y(_1__30_) );
INVX1 INVX1_67 ( .A(_324__31_), .Y(_254_) );
OAI21X1 OAI21X1_53 ( .A(byte_in[7]), .B(_233_), .C(spiif_cs_1_bF_buf1), .Y(_255_) );
NAND2X1 NAND2X1_57 ( .A(_324__31_), .B(_179__bF_buf3), .Y(_256_) );
AOI22X1 AOI22X1_33 ( .A(_254_), .B(_233_), .C(_256_), .D(_255_), .Y(_1__31_) );
NOR2X1 NOR2X1_21 ( .A(spiif_cs_1_bF_buf4), .B(spiif_cs_3_), .Y(_257_) );
OAI21X1 OAI21X1_54 ( .A(_24_), .B(_257_), .C(_325_), .Y(_258_) );
NAND2X1 NAND2X1_58 ( .A(_56_), .B(_85_), .Y(_259_) );
NAND2X1 NAND2X1_59 ( .A(_56_), .B(_83_), .Y(_260_) );
AOI22X1 AOI22X1_34 ( .A(spiif_cs_1_bF_buf5), .B(cfg_cs_byte[2]), .C(spiif_cs_3_), .D(cfg_cs_byte[3]), .Y(_261_) );
AOI22X1 AOI22X1_35 ( .A(spiif_cs_1_bF_buf5), .B(cfg_cs_byte[0]), .C(spiif_cs_3_), .D(cfg_cs_byte[1]), .Y(_262_) );
MUX2X1 MUX2X1_1 ( .A(_262_), .B(_261_), .S(_260_), .Y(_263_) );
OR2X2 OR2X2_11 ( .A(_231_), .B(byte_cnt_2_), .Y(_264_) );
AOI22X1 AOI22X1_36 ( .A(spiif_cs_1_bF_buf5), .B(cfg_cs_byte[4]), .C(spiif_cs_3_), .D(cfg_cs_byte[5]), .Y(_265_) );
OAI21X1 OAI21X1_55 ( .A(_265_), .B(_259_), .C(_264_), .Y(_266_) );
AOI21X1 AOI21X1_10 ( .A(_263_), .B(_259_), .C(_266_), .Y(_267_) );
INVX1 INVX1_68 ( .A(spiif_cs_3_), .Y(_268_) );
INVX1 INVX1_69 ( .A(cfg_cs_byte[7]), .Y(_269_) );
NAND2X1 NAND2X1_60 ( .A(spiif_cs_1_bF_buf2), .B(cfg_cs_byte[6]), .Y(_270_) );
OAI21X1 OAI21X1_56 ( .A(_268_), .B(_269_), .C(_270_), .Y(_271_) );
OAI21X1 OAI21X1_57 ( .A(_271_), .B(_264_), .C(_329_), .Y(_272_) );
OAI21X1 OAI21X1_58 ( .A(_272_), .B(_267_), .C(_258_), .Y(_4_) );
NAND2X1 NAND2X1_61 ( .A(spiif_cs_5_), .B(_268_), .Y(_273_) );
OAI21X1 OAI21X1_59 ( .A(_273_), .B(_23_), .C(_331_), .Y(_274_) );
OAI21X1 OAI21X1_60 ( .A(_47_), .B(_49_), .C(_274_), .Y(_13_) );
OAI21X1 OAI21X1_61 ( .A(spiif_cs_3_), .B(_14_), .C(_326_), .Y(_275_) );
OAI21X1 OAI21X1_62 ( .A(_48_), .B(_49_), .C(_275_), .Y(_5_) );
OAI21X1 OAI21X1_63 ( .A(spiif_cs_1_bF_buf4), .B(_143_), .C(_327_), .Y(_276_) );
OAI21X1 OAI21X1_64 ( .A(_60_), .B(_90_), .C(_276_), .Y(_6_) );
NOR2X1 NOR2X1_22 ( .A(_48_), .B(_49_), .Y(_277_) );
NOR2X1 NOR2X1_23 ( .A(spiif_cs_2_), .B(spiif_cs_0_), .Y(_278_) );
OAI21X1 OAI21X1_65 ( .A(spiif_cs_3_), .B(_278_), .C(shift_enb), .Y(_279_) );
OAI21X1 OAI21X1_66 ( .A(_279_), .B(_277_), .C(_46_), .Y(_12_) );
NAND2X1 NAND2X1_62 ( .A(_329_), .B(_43_), .Y(_280_) );
NOR2X1 NOR2X1_24 ( .A(spiif_cs_0_), .B(_16_), .Y(_281_) );
NAND2X1 NAND2X1_63 ( .A(_257_), .B(_281_), .Y(_282_) );
NAND2X1 NAND2X1_64 ( .A(_329_), .B(_282_), .Y(_283_) );
OAI21X1 OAI21X1_67 ( .A(_17_), .B(_23_), .C(_143_), .Y(_284_) );
AOI21X1 AOI21X1_11 ( .A(clr_sck_cnt), .B(_283_), .C(_284_), .Y(_285_) );
OAI21X1 OAI21X1_68 ( .A(_280_), .B(_257_), .C(_285_), .Y(_3_) );
NAND2X1 NAND2X1_65 ( .A(sck_out_en), .B(_281_), .Y(_286_) );
OAI21X1 OAI21X1_69 ( .A(_329_), .B(sck_out_en), .C(_16_), .Y(_287_) );
OAI21X1 OAI21X1_70 ( .A(_287_), .B(_22_), .C(_286_), .Y(_10_) );
INVX4 INVX4_4 ( .A(_264_), .Y(_288_) );
MUX2X1 MUX2X1_2 ( .A(cfg_datain[0]), .B(cfg_datain[8]), .S(_260_), .Y(_289_) );
OAI21X1 OAI21X1_71 ( .A(byte_cnt_2_), .B(_203_), .C(_289_), .Y(_290_) );
OAI21X1 OAI21X1_72 ( .A(cfg_datain[16]), .B(_259_), .C(_290_), .Y(_291_) );
NAND2X1 NAND2X1_66 ( .A(cfg_datain[24]), .B(_288_), .Y(_292_) );
OAI21X1 OAI21X1_73 ( .A(_288_), .B(_291_), .C(_292_), .Y(_323__0_) );
OAI21X1 OAI21X1_74 ( .A(cfg_datain[17]), .B(_259_), .C(_264_), .Y(_293_) );
MUX2X1 MUX2X1_3 ( .A(cfg_datain[1]), .B(cfg_datain[9]), .S(_260_), .Y(_294_) );
AND2X2 AND2X2_9 ( .A(_294_), .B(_259_), .Y(_295_) );
NAND2X1 NAND2X1_67 ( .A(cfg_datain[25]), .B(_288_), .Y(_296_) );
OAI21X1 OAI21X1_75 ( .A(_293_), .B(_295_), .C(_296_), .Y(_323__1_) );
MUX2X1 MUX2X1_4 ( .A(cfg_datain[2]), .B(cfg_datain[10]), .S(_260_), .Y(_297_) );
OAI21X1 OAI21X1_76 ( .A(byte_cnt_2_), .B(_203_), .C(_297_), .Y(_298_) );
OAI21X1 OAI21X1_77 ( .A(cfg_datain[18]), .B(_259_), .C(_298_), .Y(_299_) );
NAND2X1 NAND2X1_68 ( .A(cfg_datain[26]), .B(_288_), .Y(_300_) );
OAI21X1 OAI21X1_78 ( .A(_288_), .B(_299_), .C(_300_), .Y(_323__2_) );
MUX2X1 MUX2X1_5 ( .A(cfg_datain[3]), .B(cfg_datain[11]), .S(_260_), .Y(_301_) );
OAI21X1 OAI21X1_79 ( .A(byte_cnt_2_), .B(_203_), .C(_301_), .Y(_302_) );
OAI21X1 OAI21X1_80 ( .A(cfg_datain[19]), .B(_259_), .C(_302_), .Y(_303_) );
NAND2X1 NAND2X1_69 ( .A(cfg_datain[27]), .B(_288_), .Y(_304_) );
OAI21X1 OAI21X1_81 ( .A(_288_), .B(_303_), .C(_304_), .Y(_323__3_) );
MUX2X1 MUX2X1_6 ( .A(cfg_datain[4]), .B(cfg_datain[12]), .S(_260_), .Y(_305_) );
OAI21X1 OAI21X1_82 ( .A(byte_cnt_2_), .B(_203_), .C(_305_), .Y(_306_) );
OAI21X1 OAI21X1_83 ( .A(cfg_datain[20]), .B(_259_), .C(_306_), .Y(_307_) );
NAND2X1 NAND2X1_70 ( .A(cfg_datain[28]), .B(_288_), .Y(_308_) );
OAI21X1 OAI21X1_84 ( .A(_288_), .B(_307_), .C(_308_), .Y(_323__4_) );
MUX2X1 MUX2X1_7 ( .A(cfg_datain[5]), .B(cfg_datain[13]), .S(_260_), .Y(_309_) );
OAI21X1 OAI21X1_85 ( .A(byte_cnt_2_), .B(_203_), .C(_309_), .Y(_310_) );
OAI21X1 OAI21X1_86 ( .A(cfg_datain[21]), .B(_259_), .C(_310_), .Y(_311_) );
NAND2X1 NAND2X1_71 ( .A(cfg_datain[29]), .B(_288_), .Y(_312_) );
OAI21X1 OAI21X1_87 ( .A(_288_), .B(_311_), .C(_312_), .Y(_323__5_) );
MUX2X1 MUX2X1_8 ( .A(cfg_datain[6]), .B(cfg_datain[14]), .S(_260_), .Y(_313_) );
OAI21X1 OAI21X1_88 ( .A(byte_cnt_2_), .B(_203_), .C(_313_), .Y(_314_) );
OAI21X1 OAI21X1_89 ( .A(cfg_datain[22]), .B(_259_), .C(_314_), .Y(_315_) );
NAND2X1 NAND2X1_72 ( .A(cfg_datain[30]), .B(_288_), .Y(_316_) );
OAI21X1 OAI21X1_90 ( .A(_288_), .B(_315_), .C(_316_), .Y(_323__6_) );
MUX2X1 MUX2X1_9 ( .A(cfg_datain[7]), .B(cfg_datain[15]), .S(_260_), .Y(_317_) );
OAI21X1 OAI21X1_91 ( .A(byte_cnt_2_), .B(_203_), .C(_317_), .Y(_318_) );
OAI21X1 OAI21X1_92 ( .A(cfg_datain[23]), .B(_259_), .C(_318_), .Y(_319_) );
NAND2X1 NAND2X1_73 ( .A(cfg_datain[31]), .B(_288_), .Y(_320_) );
OAI21X1 OAI21X1_93 ( .A(_288_), .B(_319_), .C(_320_), .Y(_323__7_) );
AOI21X1 AOI21X1_12 ( .A(_50_), .B(_143_), .C(cfg_op_req), .Y(_321_) );
NOR2X1 NOR2X1_25 ( .A(_51_), .B(_128_), .Y(_11_) );
NOR2X1 NOR2X1_26 ( .A(_51_), .B(_126_), .Y(_9_) );
BUFX2 BUFX2_1 ( .A(_323__0_), .Y(byte_out[0]) );
BUFX2 BUFX2_2 ( .A(_323__1_), .Y(byte_out[1]) );
BUFX2 BUFX2_3 ( .A(_323__2_), .Y(byte_out[2]) );
BUFX2 BUFX2_4 ( .A(_323__3_), .Y(byte_out[3]) );
BUFX2 BUFX2_5 ( .A(_323__4_), .Y(byte_out[4]) );
BUFX2 BUFX2_6 ( .A(_323__5_), .Y(byte_out[5]) );
BUFX2 BUFX2_7 ( .A(_323__6_), .Y(byte_out[6]) );
BUFX2 BUFX2_8 ( .A(_323__7_), .Y(byte_out[7]) );
BUFX2 BUFX2_9 ( .A(_324__0_), .Y(cfg_dataout[0]) );
BUFX2 BUFX2_10 ( .A(_324__1_), .Y(cfg_dataout[1]) );
BUFX2 BUFX2_11 ( .A(_324__2_), .Y(cfg_dataout[2]) );
BUFX2 BUFX2_12 ( .A(_324__3_), .Y(cfg_dataout[3]) );
BUFX2 BUFX2_13 ( .A(_324__4_), .Y(cfg_dataout[4]) );
BUFX2 BUFX2_14 ( .A(_324__5_), .Y(cfg_dataout[5]) );
BUFX2 BUFX2_15 ( .A(_324__6_), .Y(cfg_dataout[6]) );
BUFX2 BUFX2_16 ( .A(_324__7_), .Y(cfg_dataout[7]) );
BUFX2 BUFX2_17 ( .A(_324__8_), .Y(cfg_dataout[8]) );
BUFX2 BUFX2_18 ( .A(_324__9_), .Y(cfg_dataout[9]) );
BUFX2 BUFX2_19 ( .A(_324__10_), .Y(cfg_dataout[10]) );
BUFX2 BUFX2_20 ( .A(_324__11_), .Y(cfg_dataout[11]) );
BUFX2 BUFX2_21 ( .A(_324__12_), .Y(cfg_dataout[12]) );
BUFX2 BUFX2_22 ( .A(_324__13_), .Y(cfg_dataout[13]) );
BUFX2 BUFX2_23 ( .A(_324__14_), .Y(cfg_dataout[14]) );
BUFX2 BUFX2_24 ( .A(_324__15_), .Y(cfg_dataout[15]) );
BUFX2 BUFX2_25 ( .A(_324__16_), .Y(cfg_dataout[16]) );
BUFX2 BUFX2_26 ( .A(_324__17_), .Y(cfg_dataout[17]) );
BUFX2 BUFX2_27 ( .A(_324__18_), .Y(cfg_dataout[18]) );
BUFX2 BUFX2_28 ( .A(_324__19_), .Y(cfg_dataout[19]) );
BUFX2 BUFX2_29 ( .A(_324__20_), .Y(cfg_dataout[20]) );
BUFX2 BUFX2_30 ( .A(_324__21_), .Y(cfg_dataout[21]) );
BUFX2 BUFX2_31 ( .A(_324__22_), .Y(cfg_dataout[22]) );
BUFX2 BUFX2_32 ( .A(_324__23_), .Y(cfg_dataout[23]) );
BUFX2 BUFX2_33 ( .A(_324__24_), .Y(cfg_dataout[24]) );
BUFX2 BUFX2_34 ( .A(_324__25_), .Y(cfg_dataout[25]) );
BUFX2 BUFX2_35 ( .A(_324__26_), .Y(cfg_dataout[26]) );
BUFX2 BUFX2_36 ( .A(_324__27_), .Y(cfg_dataout[27]) );
BUFX2 BUFX2_37 ( .A(_324__28_), .Y(cfg_dataout[28]) );
BUFX2 BUFX2_38 ( .A(_324__29_), .Y(cfg_dataout[29]) );
BUFX2 BUFX2_39 ( .A(_324__30_), .Y(cfg_dataout[30]) );
BUFX2 BUFX2_40 ( .A(_324__31_), .Y(cfg_dataout[31]) );
BUFX2 BUFX2_41 ( .A(_325_), .Y(cs_int_n) );
BUFX2 BUFX2_42 ( .A(_326_), .Y(load_byte) );
BUFX2 BUFX2_43 ( .A(_327_), .Y(op_done) );
BUFX2 BUFX2_44 ( .A(_328_), .Y(sck_int) );
BUFX2 BUFX2_45 ( .A(_329_), .Y(sck_ne) );
BUFX2 BUFX2_46 ( .A(_330_), .Y(sck_pe) );
BUFX2 BUFX2_47 ( .A(_331_), .Y(shift_in) );
BUFX2 BUFX2_48 ( .A(_332_), .Y(shift_out) );
DFFPOSX1 DFFPOSX1_1 ( .CLK(clk_bF_buf3), .D(_6_), .Q(_327_) );
DFFSR DFFSR_1 ( .CLK(clk_bF_buf0), .D(_321_), .Q(spiif_cs_0_), .R(vdd), .S(reset_n_bF_buf1) );
DFFSR DFFSR_2 ( .CLK(clk_bF_buf4), .D(_322__1_), .Q(spiif_cs_1_), .R(reset_n_bF_buf4), .S(vdd) );
DFFSR DFFSR_3 ( .CLK(clk_bF_buf2), .D(_322__2_), .Q(spiif_cs_2_), .R(reset_n_bF_buf4), .S(vdd) );
DFFSR DFFSR_4 ( .CLK(clk_bF_buf2), .D(_322__3_), .Q(spiif_cs_3_), .R(reset_n_bF_buf4), .S(vdd) );
DFFSR DFFSR_5 ( .CLK(clk_bF_buf6), .D(_322__4_), .Q(spiif_cs_4_), .R(reset_n_bF_buf6), .S(vdd) );
DFFSR DFFSR_6 ( .CLK(clk_bF_buf2), .D(_322__5_), .Q(spiif_cs_5_), .R(reset_n_bF_buf4), .S(vdd) );
DFFSR DFFSR_7 ( .CLK(clk_bF_buf0), .D(_1__0_), .Q(_324__0_), .R(reset_n_bF_buf1), .S(vdd) );
DFFSR DFFSR_8 ( .CLK(clk_bF_buf4), .D(_1__1_), .Q(_324__1_), .R(reset_n_bF_buf0), .S(vdd) );
DFFSR DFFSR_9 ( .CLK(clk_bF_buf5), .D(_1__2_), .Q(_324__2_), .R(reset_n_bF_buf3), .S(vdd) );
DFFSR DFFSR_10 ( .CLK(clk_bF_buf5), .D(_1__3_), .Q(_324__3_), .R(reset_n_bF_buf3), .S(vdd) );
DFFSR DFFSR_11 ( .CLK(clk_bF_buf4), .D(_1__4_), .Q(_324__4_), .R(reset_n_bF_buf0), .S(vdd) );
DFFSR DFFSR_12 ( .CLK(clk_bF_buf4), .D(_1__5_), .Q(_324__5_), .R(reset_n_bF_buf0), .S(vdd) );
DFFSR DFFSR_13 ( .CLK(clk_bF_buf4), .D(_1__6_), .Q(_324__6_), .R(reset_n_bF_buf0), .S(vdd) );
DFFSR DFFSR_14 ( .CLK(clk_bF_buf5), .D(_1__7_), .Q(_324__7_), .R(reset_n_bF_buf3), .S(vdd) );
DFFSR DFFSR_15 ( .CLK(clk_bF_buf0), .D(_1__8_), .Q(_324__8_), .R(reset_n_bF_buf1), .S(vdd) );
DFFSR DFFSR_16 ( .CLK(clk_bF_buf0), .D(_1__9_), .Q(_324__9_), .R(reset_n_bF_buf1), .S(vdd) );
DFFSR DFFSR_17 ( .CLK(clk_bF_buf1), .D(_1__10_), .Q(_324__10_), .R(reset_n_bF_buf5), .S(vdd) );
DFFSR DFFSR_18 ( .CLK(clk_bF_buf2), .D(_1__11_), .Q(_324__11_), .R(reset_n_bF_buf4), .S(vdd) );
DFFSR DFFSR_19 ( .CLK(clk_bF_buf1), .D(_1__12_), .Q(_324__12_), .R(reset_n_bF_buf5), .S(vdd) );
DFFSR DFFSR_20 ( .CLK(clk_bF_buf1), .D(_1__13_), .Q(_324__13_), .R(reset_n_bF_buf5), .S(vdd) );
DFFSR DFFSR_21 ( .CLK(clk_bF_buf1), .D(_1__14_), .Q(_324__14_), .R(reset_n_bF_buf5), .S(vdd) );
DFFSR DFFSR_22 ( .CLK(clk_bF_buf1), .D(_1__15_), .Q(_324__15_), .R(reset_n_bF_buf5), .S(vdd) );
DFFSR DFFSR_23 ( .CLK(clk_bF_buf4), .D(_1__16_), .Q(_324__16_), .R(reset_n_bF_buf0), .S(vdd) );
DFFSR DFFSR_24 ( .CLK(clk_bF_buf1), .D(_1__17_), .Q(_324__17_), .R(reset_n_bF_buf0), .S(vdd) );
DFFSR DFFSR_25 ( .CLK(clk_bF_buf1), .D(_1__18_), .Q(_324__18_), .R(reset_n_bF_buf5), .S(vdd) );
DFFSR DFFSR_26 ( .CLK(clk_bF_buf4), .D(_1__19_), .Q(_324__19_), .R(reset_n_bF_buf0), .S(vdd) );
DFFSR DFFSR_27 ( .CLK(clk_bF_buf2), .D(_1__20_), .Q(_324__20_), .R(reset_n_bF_buf5), .S(vdd) );
DFFSR DFFSR_28 ( .CLK(clk_bF_buf5), .D(_1__21_), .Q(_324__21_), .R(reset_n_bF_buf3), .S(vdd) );
DFFSR DFFSR_29 ( .CLK(clk_bF_buf4), .D(_1__22_), .Q(_324__22_), .R(reset_n_bF_buf4), .S(vdd) );
DFFSR DFFSR_30 ( .CLK(clk_bF_buf1), .D(_1__23_), .Q(_324__23_), .R(reset_n_bF_buf5), .S(vdd) );
DFFSR DFFSR_31 ( .CLK(clk_bF_buf0), .D(_1__24_), .Q(_324__24_), .R(reset_n_bF_buf1), .S(vdd) );
DFFSR DFFSR_32 ( .CLK(clk_bF_buf5), .D(_1__25_), .Q(_324__25_), .R(reset_n_bF_buf3), .S(vdd) );
DFFSR DFFSR_33 ( .CLK(clk_bF_buf0), .D(_1__26_), .Q(_324__26_), .R(reset_n_bF_buf1), .S(vdd) );
DFFSR DFFSR_34 ( .CLK(clk_bF_buf5), .D(_1__27_), .Q(_324__27_), .R(reset_n_bF_buf3), .S(vdd) );
DFFSR DFFSR_35 ( .CLK(clk_bF_buf1), .D(_1__28_), .Q(_324__28_), .R(reset_n_bF_buf5), .S(vdd) );
DFFSR DFFSR_36 ( .CLK(clk_bF_buf5), .D(_1__29_), .Q(_324__29_), .R(reset_n_bF_buf3), .S(vdd) );
DFFSR DFFSR_37 ( .CLK(clk_bF_buf2), .D(_1__30_), .Q(_324__30_), .R(reset_n_bF_buf4), .S(vdd) );
DFFSR DFFSR_38 ( .CLK(clk_bF_buf4), .D(_1__31_), .Q(_324__31_), .R(reset_n_bF_buf0), .S(vdd) );
DFFSR DFFSR_39 ( .CLK(clk_bF_buf2), .D(_4_), .Q(_325_), .R(vdd), .S(reset_n_bF_buf4) );
DFFSR DFFSR_40 ( .CLK(clk_bF_buf2), .D(_13_), .Q(_331_), .R(reset_n_bF_buf4), .S(vdd) );
DFFSR DFFSR_41 ( .CLK(clk_bF_buf2), .D(_5_), .Q(_326_), .R(reset_n_bF_buf2), .S(vdd) );
DFFSR DFFSR_42 ( .CLK(clk_bF_buf3), .D(_7__0_), .Q(sck_cnt_0_), .R(reset_n_bF_buf2), .S(vdd) );
DFFSR DFFSR_43 ( .CLK(clk_bF_buf3), .D(_7__1_), .Q(sck_cnt_1_), .R(reset_n_bF_buf2), .S(vdd) );
DFFSR DFFSR_44 ( .CLK(clk_bF_buf3), .D(_7__2_), .Q(sck_cnt_2_), .R(reset_n_bF_buf2), .S(vdd) );
DFFSR DFFSR_45 ( .CLK(clk_bF_buf3), .D(_7__3_), .Q(sck_cnt_3_), .R(reset_n_bF_buf2), .S(vdd) );
DFFSR DFFSR_46 ( .CLK(clk_bF_buf6), .D(_7__4_), .Q(sck_cnt_4_), .R(reset_n_bF_buf6), .S(vdd) );
DFFSR DFFSR_47 ( .CLK(clk_bF_buf3), .D(_7__5_), .Q(sck_cnt_5_), .R(reset_n_bF_buf2), .S(vdd) );
DFFSR DFFSR_48 ( .CLK(clk_bF_buf3), .D(_12_), .Q(shift_enb), .R(reset_n_bF_buf2), .S(vdd) );
DFFSR DFFSR_49 ( .CLK(clk_bF_buf3), .D(_3_), .Q(clr_sck_cnt), .R(vdd), .S(reset_n_bF_buf2) );
DFFSR DFFSR_50 ( .CLK(clk_bF_buf3), .D(_10_), .Q(sck_out_en), .R(reset_n_bF_buf2), .S(vdd) );
DFFSR DFFSR_51 ( .CLK(clk_bF_buf6), .D(_0__0_), .Q(byte_cnt_0_), .R(reset_n_bF_buf6), .S(vdd) );
DFFSR DFFSR_52 ( .CLK(clk_bF_buf6), .D(_0__1_), .Q(byte_cnt_1_), .R(reset_n_bF_buf6), .S(vdd) );
DFFSR DFFSR_53 ( .CLK(clk_bF_buf0), .D(_0__2_), .Q(byte_cnt_2_), .R(reset_n_bF_buf1), .S(vdd) );
DFFSR DFFSR_54 ( .CLK(clk_bF_buf6), .D(_8_), .Q(_328_), .R(reset_n_bF_buf6), .S(vdd) );
DFFSR DFFSR_55 ( .CLK(clk_bF_buf6), .D(_11_), .Q(_330_), .R(reset_n_bF_buf6), .S(vdd) );
DFFSR DFFSR_56 ( .CLK(clk_bF_buf6), .D(_9_), .Q(_329_), .R(reset_n_bF_buf6), .S(vdd) );
DFFSR DFFSR_57 ( .CLK(clk_bF_buf0), .D(_2__0_), .Q(clk_cnt_0_), .R(vdd), .S(reset_n_bF_buf1) );
DFFSR DFFSR_58 ( .CLK(clk_bF_buf0), .D(_2__1_), .Q(clk_cnt_1_), .R(reset_n_bF_buf3), .S(vdd) );
DFFSR DFFSR_59 ( .CLK(clk_bF_buf5), .D(_2__2_), .Q(clk_cnt_2_), .R(reset_n_bF_buf3), .S(vdd) );
DFFSR DFFSR_60 ( .CLK(clk_bF_buf6), .D(_2__3_), .Q(clk_cnt_3_), .R(reset_n_bF_buf6), .S(vdd) );
DFFSR DFFSR_61 ( .CLK(clk_bF_buf5), .D(_2__4_), .Q(clk_cnt_4_), .R(reset_n_bF_buf1), .S(vdd) );
DFFSR DFFSR_62 ( .CLK(clk_bF_buf6), .D(_2__5_), .Q(clk_cnt_5_), .R(reset_n_bF_buf6), .S(vdd) );
endmodule
