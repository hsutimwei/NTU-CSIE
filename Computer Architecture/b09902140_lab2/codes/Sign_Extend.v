module Sign_Extend(
    data_i,//instr
    data_o
);

input[31:0] data_i;
output[31:0] data_o;
wire [6:0] opcode;
reg [31:0] data_o;
assign  opcode = data_i[6:0];
always@(*)begin
        case(opcode)
            7'b0110011: begin//R type
                data_o = {{20{data_i[31]}}, data_i[31:20]};
            end
            7'b0010011: begin//I type
                data_o = {{20{data_i[31]}}, data_i[31:20]};
            end
            7'b0000011: begin//lw
                data_o = {{20{data_i[31]}}, data_i[31:20]};
            end
            7'b0100011: begin//sw
                data_o = {{20{data_i[31]}}, data_i[31:25],data_i[11:7]};
            end
            7'b1100011: begin//beq
                data_o = {{21{data_i[31]}}, data_i[7], data_i[30:25],data_i[11:8]};
            end
         endcase  
end 

endmodule