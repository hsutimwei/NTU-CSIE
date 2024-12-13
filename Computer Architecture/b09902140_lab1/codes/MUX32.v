module MUX32 (
    data1_i,//data1
    data2_i,//data2
    select_i,//MUX_ALUSrc
    data_o//output
);//MUX_ALUSrc

input	[31:0]		data1_i, data2_i;
input				select_i;
output	[31:0]		data_o;

assign	data_o = (select_i == 1'b0)?  data1_i : data2_i;
   

endmodule