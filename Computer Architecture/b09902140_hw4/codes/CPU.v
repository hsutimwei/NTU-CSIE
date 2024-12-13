module CPU
(
    clk_i, 
    rst_i,
    start_i
);

// Ports
input               clk_i;
input               rst_i;
input               start_i;
wire [31:0] pc;
wire [31:0] instraddr,instr;

wire [4:0] rd,rs1,rs2;
wire [31:0] data1,data2;
//000000001010_00000_000_00101_0010011  //addi x5,x0,10
assign rs1    = instr[19:15];//00000
assign rs2    = instr[24:20];//no
assign rd     = instr[11:7];//00101
wire  [9:0]  func;
assign func = {instr[31:25],instr[14:12]};//xxxxxxx000

Control Control(
    .Op_i       (instr[6:0]),//0010011
    .ALUOp_o    (ALU_Control.ALUOp_i),
    .ALUSrc_o   (MUX32.select_i),
    .RegWrite_o (Registers.RegWrite_i)
);



Adder Add_PC(
    .data1_in   (instraddr),
    .data2_in   (32'd4),
    .data_o     (pc)
);


PC PC(
    .clk_i      (clk_i),
    .rst_i      (rst_i),
    .start_i    (start_i),
    .pc_i       (pc),
    .pc_o       (instraddr)//4
);

Instruction_Memory Instruction_Memory(
    .addr_i     (instraddr), //4
    .instr_o    (instr)//addi x5,x0,10
); 

Registers Registers(
    .clk_i      (clk_i),
    .RS1addr_i   (rs1),//x0
    .RS2addr_i   (rs2),//no
    .RDaddr_i   (rd),//x5 
    .RDdata_i   (ALU.data_o),//
    .RegWrite_i (Control.RegWrite_o), 
    .RS1data_o   (data1),
    .RS2data_o   (data2) 
);

MUX32 MUX32(
    .data1_i    (data2),
    .data2_i    (Sign_Extend.data_o),
    .select_i   (Control.ALUSrc_o),
    .data_o     (ALU.data2_i)
);//MUX_ALUSrc


 
Sign_Extend Sign_Extend(
    .data_i     (instr[31:20]),
    .data_o     (MUX32.data2_i)
);

  

ALU ALU(
    .data1_i    (data1),
    .data2_i    (MUX32.data_o),
    .ALUCtrl_i  (ALU_Control.ALUCtrl_o),
    .data_o     (Registers.RDdata_i),
    .Zero_o     ()
);



ALU_Control ALU_Control(
    .funct_i    (func), //{func7,func3} 
    .ALUOp_i    (Control.ALUOp_o),//check R type or I type
    .ALUCtrl_o  (ALU.ALUCtrl_i)
);


endmodule

