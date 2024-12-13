module Hazard_Detection(
	Ex_Memread_i,
    Ex_WRRD_i,
    rs1addr_i,
    rs2addr_i,
    isstall_o,
    PCWrite_o,
    NoOp_o
);

input	Ex_Memread_i;
input	[4:0]  Ex_WRRD_i;
input	[4:0]  rs1addr_i,rs2addr_i;

output reg 	isstall_o;
output reg 	NoOp_o;
output reg  PCWrite_o;

always @( * ) begin
    //load-use hazard
	if (Ex_Memread_i && ((Ex_WRRD_i == rs1addr_i) || (Ex_WRRD_i == rs2addr_i))) begin 
		isstall_o <= 1'b1;
		PCWrite_o <= 1'b0;
		NoOp_o    <= 1'b1;
	end
	else begin
		isstall_o <= 1'b0;
		PCWrite_o <= 1'b1;
		NoOp_o    <= 1'b0;
	end
end

endmodule