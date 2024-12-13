module beqcheckequal (
    data1_i,
    data2_i,
    isequal_o
);

input [31:0]  data1_i, data2_i;
output	isequal_o;

assign	isequal_o= (data1_i==data2_i)? 1'b1: 1'b0;
   

endmodule