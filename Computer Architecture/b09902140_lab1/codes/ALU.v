module ALU(
    data1_i,
    data2_i,
    ALUCtrl_i,
    data_o,
);
input [31:0] data1_i,data2_i;
input [3:0] ALUCtrl_i;
output [31:0] data_o; 
reg data_o;
wire [4:0] sra;
assign  sra = data2_i[4:0];
 always@(*)begin
        case(ALUCtrl_i)
            4'b0010: begin//add/addi/lw/sw
                data_o=data1_i+data2_i;
            end
            4'b0110: begin//sub
                data_o=data1_i-data2_i;
            end
            4'b1010: begin//mul
                data_o=data1_i*data2_i;
            end
            4'b1000: begin//xor
                data_o=data1_i^data2_i;
            end
            4'b0101: begin//sra-->srai
                data_o=data1_i>>>sra;
            end
            4'b0001: begin//sll
                data_o=data1_i<<data2_i;
            end
            4'b0000: begin//and
                data_o=data1_i&data2_i;
            end
        endcase
 end
endmodule