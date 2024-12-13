module IDEX
(
    clk_i,
    rst_i,
    stall_i,
    RegWrite_i,
    MemtoReg_i,
    MemRead_i,
    MemWrite_i,
    ALUOp_i,
    ALUSrc_i,
    data1_i,
    data2_i,
    signextend_i,
    func_i,
    Ex_rs1_i,
    Ex_rs2_i,
    WRRD_i,
    RegWrite_o,
    MemtoReg_o,
    MemRead_o,
    MemWrite_o,
    ALUOp_o,
    ALUSrc_o,
    data1_o,
    data2_o,
    signextend_o,
    func_o,
    Ex_rs1_o,
    Ex_rs2_o,
    WRRD_o
);

input               clk_i,rst_i,RegWrite_i,MemtoReg_i,MemRead_i,MemWrite_i,ALUSrc_i,stall_i;
input   [1:0]       ALUOp_i;
input   [4:0]       Ex_rs1_i,Ex_rs2_i,WRRD_i;
input   [9:0]       func_i;
input   [31:0]      data1_i,data2_i,signextend_i;
output              RegWrite_o,MemtoReg_o,MemRead_o,MemWrite_o,ALUSrc_o;
output  [1:0]       ALUOp_o;
output  [4:0]       Ex_rs1_o,Ex_rs2_o,WRRD_o;
output  [9:0]       func_o;
output  [31:0]      data1_o,data2_o,signextend_o;

reg              RegWrite_o,MemtoReg_o,MemRead_o,MemWrite_o,ALUSrc_o;
reg  [1:0]       ALUOp_o;
reg  [4:0]       Ex_rs1_o,Ex_rs2_o,WRRD_o;
reg  [9:0]       func_o;
reg  [31:0]      data1_o,data2_o,signextend_o;

always@(posedge clk_i or posedge rst_i) begin
    if(stall_i==1'b0) begin
         RegWrite_o<=RegWrite_i;
         MemtoReg_o<=MemtoReg_i;
         MemRead_o<=MemRead_i;
         MemWrite_o<=MemWrite_i;
         ALUOp_o<=ALUOp_i;
         ALUSrc_o<=ALUSrc_i;
         data1_o<=data1_i;
         data2_o<=data2_i;
         signextend_o<=signextend_i;
         func_o<=func_i;
         Ex_rs1_o<=Ex_rs1_i;
         Ex_rs2_o<=Ex_rs2_i;
         WRRD_o<=WRRD_i;
    end
end

endmodule
