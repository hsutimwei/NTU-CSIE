module Muxforreg2forwardingcheck (
    ForwardingB_i,
    data2_i,
    MEM_ALUresult_i,
    WB_WriteData_i,
    WRdata_o
);


input	[31:0]  	data2_i,MEM_ALUresult_i,WB_WriteData_i;
input	[1:0]		ForwardingB_i;
output	[31:0]		WRdata_o;

assign	WRdata_o =  (ForwardingB_i == 2'b00)? data2_i :
                    (ForwardingB_i == 2'b01)? WB_WriteData_i :
                    (ForwardingB_i == 2'b10)? MEM_ALUresult_i :
                    32'bx;
   

   

endmodule