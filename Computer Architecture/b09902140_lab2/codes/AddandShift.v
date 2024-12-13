module AddandShift (
    pc_i,
    shift_i,
    addr_o
);

input [31:0]  pc_i, shift_i;
output [31:0] addr_o;

assign  addr_o = pc_i + (shift_i << 1);

   

endmodule