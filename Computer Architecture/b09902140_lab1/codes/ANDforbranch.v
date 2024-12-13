module ANDforbranch (
    branch_i,
    isequal_i,
    branchcheck_o
);

input  branch_i, isequal_i;
output	branchcheck_o;

assign	branchcheck_o=branch_i & isequal_i;
   

endmodule