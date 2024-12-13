module ALU_Control(
    funct_i,
    ALUOp_i,
    ALUCtrl_o
);
input [9:0] funct_i;
input [1:0] ALUOp_i;
output [3:0] ALUCtrl_o;
reg [3:0] ALUCtrl_o;
wire [2:0] func3;
assign func3 = funct_i[2:0];
 always@(*)begin
        case(ALUOp_i)
            2'b10: begin
                ALUCtrl_o = (funct_i == 10'b0000000000)? 4'b0010 ://add
                            (funct_i == 10'b0100000000)? 4'b0110 ://sub
                            (funct_i == 10'b0000000111)? 4'b0000 ://and
                            (funct_i == 10'b0000000100)? 4'b1000 ://xor
                            (funct_i == 10'b0000000001)? 4'b0001 ://sll
                            (funct_i == 10'b0000001000)? 4'b1010 ://mul
                            4'bx;
            end
            2'b00: begin
                ALUCtrl_o = (func3 == 3'b000)? 4'b0010 ://addi
                            (func3 == 3'b101)? 4'b0101 ://srai
                            4'bx;
            end
        endcase
 end

endmodule