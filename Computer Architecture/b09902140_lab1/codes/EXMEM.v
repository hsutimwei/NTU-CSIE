module EXMEM
(
    clk_i,
    rst_i,
    RegWrite_i,
    MemtoReg_i,
    MemRead_i,
    MemWrite_i,
    ALUout_i,
    MEMWRdata_i,
    WRRD_i,
    RegWrite_o,
    MemtoReg_o,
    MemRead_o,
    MemWrite_o,
    ALUout_o,
    MEMWRdata_o,
    WRRD_o
);

input               clk_i,rst_i,RegWrite_i,MemtoReg_i,MemRead_i,MemWrite_i;
input   [4:0]       WRRD_i;
input   [31:0]      ALUout_i,MEMWRdata_i;
output              RegWrite_o,MemtoReg_o,MemRead_o,MemWrite_o;
output   [4:0]      WRRD_o;
output   [31:0]     ALUout_o,MEMWRdata_o;

reg              RegWrite_o,MemtoReg_o,MemRead_o,MemWrite_o;
reg   [4:0]      WRRD_o;
reg   [31:0]     ALUout_o,MEMWRdata_o;

always@(posedge clk_i or posedge rst_i) begin
         RegWrite_o<=RegWrite_i;
         MemtoReg_o<=MemtoReg_i;
         MemRead_o<=MemRead_i;
         MemWrite_o<=MemWrite_i;
         WRRD_o<=WRRD_i;
         ALUout_o<=ALUout_i;
         MEMWRdata_o<=MEMWRdata_i;
end

endmodule
