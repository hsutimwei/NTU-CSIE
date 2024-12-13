module MEMWB
(
    clk_i,
    rst_i,
    RegWrite_i,
    MemtoReg_i,
    ALUoutbyEXMEM_i,
    MEMdata_i,
    WRRD_i,
    RegWrite_o,
    MemtoReg_o,
    ALUout_o,
    MEMdata_o,
    WRRD_o
);

input               clk_i,rst_i,RegWrite_i,MemtoReg_i;
input   [4:0]       WRRD_i;
input   [31:0]      ALUoutbyEXMEM_i,MEMdata_i;
output              RegWrite_o,MemtoReg_o;
output   [4:0]      WRRD_o;
output   [31:0]     ALUout_o,MEMdata_o;

reg              RegWrite_o,MemtoReg_o;
reg   [4:0]      WRRD_o;
reg   [31:0]     ALUout_o,MEMdata_o;

always@(posedge clk_i or posedge rst_i) begin
         RegWrite_o<=RegWrite_i;
         MemtoReg_o<=MemtoReg_i;
         WRRD_o<=WRRD_i;
         ALUout_o<=ALUoutbyEXMEM_i;
         MEMdata_o<=MEMdata_i;
end

endmodule
