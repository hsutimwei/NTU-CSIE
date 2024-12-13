module MuxforPC (
   add4_i,        //pc+4
   branch_i,   //branch的address
   branchcheck_i, //確認是哪個
   pc_o      //最終pc address
);

input	[31:0]  	add4_i, branch_i;
input				branchcheck_i;
output	[31:0]		pc_o;

assign	pc_o = (branchcheck_i == 1'b0)?  add4_i : branch_i;
   

endmodule