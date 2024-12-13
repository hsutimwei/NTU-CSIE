module Forward_unit(
    MEM_RegWrite_i,
    MEM_Rd_i,
    WB_RegWrite_i,
    WB_Rd_i,
    Ex_rs1_i,
    Ex_rs2_i,
    ForwardingA_o,
    ForwardingB_o
);

input   MEM_RegWrite_i, WB_RegWrite_i;
input   [4:0]  MEM_Rd_i, WB_Rd_i;
input   [4:0]  Ex_rs1_i , Ex_rs2_i ;
output   [1:0]  ForwardingA_o;
output   [1:0]  ForwardingB_o;
reg  [1:0]  ForwardingA_o;
reg  [1:0]  ForwardingB_o;
always @(*) begin

    if (MEM_RegWrite_i == 1'b1 && MEM_Rd_i != 5'b0 && MEM_Rd_i == Ex_rs1_i ) begin
        ForwardingA_o <= 2'b10;
    end
    else if (WB_RegWrite_i == 1'b1 && WB_Rd_i != 5'b0 && WB_Rd_i == Ex_rs1_i )  begin
        ForwardingA_o <= 2'b01;
    end
    else begin
        ForwardingA_o <= 2'b00;
    end

    if (MEM_RegWrite_i == 1'b1 && MEM_Rd_i != 5'b0 && MEM_Rd_i == Ex_rs2_i ) begin
        ForwardingB_o <= 2'b10;
    end
    else if (WB_RegWrite_i == 1'b1 && WB_Rd_i != 5'b0 && WB_Rd_i == Ex_rs2_i )  begin
        ForwardingB_o <= 2'b01;
    end
    else begin
        ForwardingB_o <= 2'b00;
    end
end

endmodule