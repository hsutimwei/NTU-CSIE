module IFID
(
    clk_i,
    rst_i,
    instr_i,
    pcaddress_i,
    stall_i,
    flush_i,
    instr_o,
    pcaddress_o
);


input               clk_i;
input               rst_i;
input   [31:0]      instr_i;
input   [31:0]      pcaddress_i;
input               stall_i;
input               flush_i;
output  [31:0]      instr_o;
output  [31:0]      pcaddress_o;

reg [31:0] instr_o;
reg [31:0] pcaddress_o;

always@(posedge clk_i or posedge rst_i) begin
	if(flush_i==1'b1) begin
		pcaddress_o <= 32'b0;
		instr_o <= 32'b0;
	end
	else if(stall_i==1'b0) begin
		pcaddress_o <= pcaddress_i;
		instr_o <= instr_i;
	end
end

endmodule
