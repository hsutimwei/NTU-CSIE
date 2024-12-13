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
wire [31:0] pc_i,pcadd;
wire [31:0] pc_branch;
wire [31:0] branchaddress;
wire [31:0] pcaddr,instr,IFID_instr;
wire branchcheck;
wire [4:0] rd,rs1,rs2,IDEX_rd,EXMEM_rd,MEMWB_rd,IDEX_rs1,IDEX_rs2;
wire [31:0] data1,data2,IDEX_data1,IDEX_data2,Mux_data2,EXMEM_MEMWRdata;
assign rs1    = IFID_instr[19:15];
assign rs2    = IFID_instr[24:20];
assign rd     = IFID_instr[11:7];
wire  [9:0]  func,IDEX_func;
assign func = {IFID_instr[31:25],IFID_instr[14:12]};
wire [1:0] ALUOp;
wire [1:0] IDEX_ALUOp;
wire [6:0] opcode;
assign opcode  = IFID_instr[6:0];
wire RegWrite;
wire IDEX_RegWrite;
wire EXMEM_RegWrite;
wire MEMWB_RegWrite;
reg  MEMWB_RegWritetoreg;
always@(*) begin
      if(MEMWB_RegWrite==1 || MEMWB_RegWrite==0) begin
        MEMWB_RegWritetoreg <=MEMWB_RegWrite;
      end
      else begin
        MEMWB_RegWritetoreg=0;
      end
end
wire [31:0] WBresult;
wire MemtoReg;
wire IDEX_MemtoReg;
wire EXMEM_MemtoReg;
wire MEMWB_MemtoReg;
wire MemRead;
wire IDEX_MemRead;
wire EXMEM_MemRead;
wire MemWrite;
wire IDEX_MemWrite;
wire EXMEM_MemWrite;
wire [31:0] ALUout;
wire [31:0] EXMEM_ALUout;
wire [31:0] MEMWB_ALUout;
wire stall;
wire [31:0] MEMdata,MEMWB_MEMdata;
wire isequal;
wire branch;
wire [31:0] IFID_pcaddr;
wire [31:0] signextend_data,IDEX_signextend_data,ALUdata1,ALUdata2;
wire [1:0] forwardingA;
wire [1:0] forwardingB;
wire ALUSrc;
wire IDEX_ALUSrc;
wire Pcwrite;
wire NoOp;
Control Control(
    .Op_i       (opcode),
    .NoOp_i     (NoOp),
    .ALUOp_o    (ALUOp),
    .ALUSrc_o   (ALUSrc),  //to Mux32.select_i
    .RegWrite_o (RegWrite), //to Registers.RegWrite_i
    .MemtoReg_o (MemtoReg),
    .MemRead_o  (MemRead),
    .MemWrite_o (MemWrite),
    .Branch_o   (branch)
);

Data_Memory Data_Memory
(
    .clk_i      (clk_i), 
    .addr_i     (EXMEM_ALUout),
    .MemRead_i  (EXMEM_MemRead),
    .MemWrite_i (EXMEM_MemWrite),
    .data_i     (EXMEM_MEMWRdata),
    .data_o     (MEMdata)
);

MuxforPC MuxforPC(
   .add4_i        (pcadd),        //pc+4
   .branch_i      (pc_branch),   //branch的address
   .branchcheck_i (branchcheck), //確認是哪個
   .pc_o          (pc)          //最終pc address
);

AddandShift AddandShift(
   .pc_i    (IFID_pcaddr),
   .shift_i (signextend_data),
   .addr_o  (pc_branch)
);

beqcheckequal beqcheckequal(
    .data1_i     (data1),
    .data2_i     (data2),
    .isequal_o   (isequal)
);

ANDforbranch ANDforbranch(
    .branch_i       (branch),
    .isequal_i      (isequal),
    .branchcheck_o  (branchcheck)
);

Hazard_Detection Hazard_Detection(
    .Ex_Memread_i   (IDEX_MemRead),
    .Ex_WRRD_i      (IDEX_rd),
    .rs1addr_i      (rs1),
    .rs2addr_i      (rs2),
    .isstall_o      (stall),
    .PCWrite_o      (Pcwrite),
    .NoOp_o         (NoOp)
);

Forward_unit Forward_unit(
    .MEM_RegWrite_i    (EXMEM_RegWrite),
    .MEM_Rd_i          (EXMEM_rd),
    .WB_RegWrite_i     (MEMWB_RegWrite),
    .WB_Rd_i           (MEMWB_rd),
    .Ex_rs1_i          (IDEX_rs1),
    .Ex_rs2_i          (IDEX_rs2),
    .ForwardingA_o     (forwardingA),
    .ForwardingB_o     (forwardingB)
);

Muxforreg1forwardingcheck Muxforreg1forwardingcheck(
    .ForwardingA_i     (forwardingA),
    .data1_i             (IDEX_data1),
    .MEM_ALUresult_i   (EXMEM_ALUout),
    .WB_WriteData_i    (WBresult),
    .WRdata_o          (ALUdata1)
);

Muxforreg2forwardingcheck Muxforreg2forwardingcheck(
    .ForwardingB_i     (forwardingB),
    .data2_i             (IDEX_data2),
    .MEM_ALUresult_i   (EXMEM_ALUout),
    .WB_WriteData_i    (WBresult),
    .WRdata_o          (Mux_data2)
);

MuxforMEM MuxforMEM(
    .MemtoReg_i        (MEMWB_MemtoReg),
    .MEMdata_i         (MEMWB_MEMdata),
    .ALUoutbyMEMWB_i   (MEMWB_ALUout),
    .WBdata_o          (WBresult)
);

Adder Add_PC(
    .data1_in   (pcaddr),
    .data2_in   (32'd4),
    .data_o     (pcadd)
);

PC PC(
    .clk_i      (clk_i),
    .rst_i      (rst_i),
    .start_i    (start_i),
    .PCWrite_i  (Pcwrite),
    .pc_i       (pc),
    .pc_o       (pcaddr)
);

Instruction_Memory Instruction_Memory(
    .addr_i     (pcaddr),
    .instr_o    (instr)
); 

Registers Registers(
    .clk_i       (clk_i),
    .RS1addr_i   (rs1),
    .RS2addr_i   (rs2),
    .RDaddr_i    (MEMWB_rd),
    .RDdata_i    (WBresult),
    .RegWrite_i  (MEMWB_RegWritetoreg), 
    .RS1data_o   (data1),
    .RS2data_o   (data2) 
);

MUX32 MUX32(
    .data1_i    (Mux_data2),
    .data2_i    (IDEX_signextend_data),
    .select_i   (IDEX_ALUSrc),
    .data_o     (ALUdata2)
);

 
Sign_Extend Sign_Extend(
    .data_i     (IFID_instr),
    .data_o     (signextend_data)
);

  

ALU ALU(
    .data1_i    (ALUdata1),
    .data2_i    (MUX32.data_o),
    .ALUCtrl_i  (ALU_Control.ALUCtrl_o),
    .data_o     (ALUout)
);



ALU_Control ALU_Control(
    .funct_i    (IDEX_func), //{func7,func3} 
    .ALUOp_i    (IDEX_ALUOp),//check R type or I type // form IDEX from Control
    .ALUCtrl_o  (ALU.ALUCtrl_i)
);

IFID IFID(
    .clk_i        (clk_i),
    .rst_i        (rst_i),
    .instr_i      (instr),
    .pcaddress_i  (pcaddr),
    .stall_i      (stall),
    .flush_i      (branchcheck),
    .instr_o      (IFID_instr),
    .pcaddress_o  (IFID_pcaddr)
);

IDEX IDEX(
    .clk_i        (clk_i),
    .rst_i        (rst_i),
    .RegWrite_i   (RegWrite),
    .MemtoReg_i   (MemtoReg),
    .MemRead_i    (MemRead),
    .MemWrite_i   (MemWrite),
    .ALUOp_i      (ALUOp),
    .ALUSrc_i     (ALUSrc),
    .data1_i      (data1),
    .data2_i      (data2),
    .signextend_i (signextend_data),
    .func_i       (func),
    .Ex_rs1_i     (rs1),   //for forwarding
    .Ex_rs2_i     (rs2),   //for forwarding
    .WRRD_i       (rd),   //recording write back address
    .RegWrite_o   (IDEX_RegWrite),
    .MemtoReg_o   (IDEX_MemtoReg),
    .MemRead_o    (IDEX_MemRead),
    .MemWrite_o   (IDEX_MemWrite),
    .ALUOp_o      (IDEX_ALUOp),
    .ALUSrc_o     (IDEX_ALUSrc),
    .data1_o      (IDEX_data1),
    .data2_o      (IDEX_data2),
    .signextend_o (IDEX_signextend_data),
    .func_o       (IDEX_func),
    .Ex_rs1_o     (IDEX_rs1),   //for forwarding
    .Ex_rs2_o     (IDEX_rs2),   //for forwarding
    .WRRD_o       (IDEX_rd)   //recording write back address
    
);

EXMEM EXMEM(
    .clk_i        (clk_i),
    .rst_i        (rst_i),
    .RegWrite_i   (IDEX_RegWrite),
    .MemtoReg_i   (IDEX_MemtoReg),
    .MemRead_i    (IDEX_MemRead),
    .MemWrite_i   (IDEX_MemWrite),
    .ALUout_i     (ALUout),
    .MEMWRdata_i  (Mux_data2),  //sw 時寫回data用
    .WRRD_i       (IDEX_rd),   //recording write back address
    .RegWrite_o   (EXMEM_RegWrite),
    .MemtoReg_o   (EXMEM_MemtoReg),
    .MemRead_o    (EXMEM_MemRead),
    .MemWrite_o   (EXMEM_MemWrite),
    .ALUout_o     (EXMEM_ALUout),
    .MEMWRdata_o  (EXMEM_MEMWRdata),  //sw 時寫回data用
    .WRRD_o       (EXMEM_rd)   //recording write back address
);

MEMWB MEMWB(
    .clk_i             (clk_i),
    .rst_i             (rst_i),
    .RegWrite_i        (EXMEM_RegWrite),
    .MemtoReg_i        (EXMEM_MemtoReg),
    .ALUoutbyEXMEM_i   (EXMEM_ALUout),
    .MEMdata_i         (MEMdata),
    .WRRD_i            (EXMEM_rd),   //recording write back address
    .RegWrite_o        (MEMWB_RegWrite),
    .MemtoReg_o        (MEMWB_MemtoReg),
    .ALUout_o          (MEMWB_ALUout),
    .MEMdata_o         (MEMWB_MEMdata),
    .WRRD_o            (MEMWB_rd)   //recording write back address
);
endmodule

