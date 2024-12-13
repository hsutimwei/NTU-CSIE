module Muxforreg1forwardingcheck (
    ForwardingA_i,
    data1_i,
    MEM_ALUresult_i,
    WB_WriteData_i,
    WRdata_o
);

input	[31:0]  	data1_i, MEM_ALUresult_i,WB_WriteData_i;
input	[1:0]		ForwardingA_i;
output	[31:0]		WRdata_o;

assign	WRdata_o =  (ForwardingA_i == 2'b00)? data1_i :
                    (ForwardingA_i == 2'b01)? WB_WriteData_i :
                    (ForwardingA_i == 2'b10)? MEM_ALUresult_i :
                    32'bx;
   

endmodule