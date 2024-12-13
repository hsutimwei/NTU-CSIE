module MuxforMEM (
    MemtoReg_i,
    MEMdata_i,
    ALUoutbyMEMWB_i,
    WBdata_o
);

input	[31:0]		ALUoutbyMEMWB_i, MEMdata_i;
input				MemtoReg_i;
output	[31:0]		WBdata_o;

assign	WBdata_o = (MemtoReg_i == 1'b0)?  ALUoutbyMEMWB_i : MEMdata_i;
   

endmodule