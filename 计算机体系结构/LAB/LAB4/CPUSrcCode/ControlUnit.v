`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: USTC ESLAB 
// Engineer: Wu Yuzhang
// 
// Design Name: RISCV-Pipline CPU
// Module Name: ControlUnit
// Target Devices: Nexys4
// Tool Versions: Vivado 2017.4.1
// Description: RISC-V Instruction Decoder
//////////////////////////////////////////////////////////////////////////////////
//功能和接口说明
    //ControlUnit       是本CPU的指令译码器，组合逻辑电路
//输入
    // Op               是指令的操作码部分
    // Fn3              是指令的func3部分
    // Fn7              是指令的func7部分
//输出
    // JalD==1          表示Jal指令到达ID译码阶段
    // JalrD==1         表示Jalr指令到达ID译码阶段
    // RegWriteD        表示ID阶段的指令对应的寄存器写入模式
    // MemToRegD==1     表示ID阶段的指令需要将data memory读取的值写入寄存器,
    // MemWriteD        共4bit，为1的部分表示有效，对于data memory的32bit字按byte进行写入,MemWriteD=0001表示只写入最低1个byte，和xilinx bram的接口类似
    // LoadNpcD==1      表示将NextPC输出到ResultM
    // RegReadD         表示A1和A2对应的寄存器值是否被使用到了，用于forward的处理
    // BranchTypeD      表示不同的分支类型，所有类型定义在Parameters.v中
    // AluContrlD       表示不同的ALU计算功能，所有类型定义在Parameters.v中
    // AluSrc2D         表示Alu输入源2的选择
    // AluSrc1D         表示Alu输入源1的选择
    // ImmType          表示指令的立即数格式
//实验要求  
    //补全模块  

`include "Parameters.v"   
module ControlUnit(
    input wire [6:0] Op,
    input wire [2:0] Fn3,
    input wire [6:0] Fn7,
    output wire JalD,
    output wire JalrD,
    output reg [2:0] RegWriteD,
    output wire MemToRegD,
    output reg [3:0] MemWriteD,
    output wire LoadNpcD,
    output reg [1:0] RegReadD,
    output reg [2:0] BranchTypeD,
    output reg [3:0] AluContrlD,
    output wire [1:0] AluSrc2D,
    output wire AluSrc1D,
    output reg [2:0] ImmType,
    
    output reg [2:0] CSRType  //CSR类型
    ); 
    // 请补全此处代码
    
    localparam LOAD_TYPE_OP = 7'b0000011, STORE_TYPE_OP = 7'b0100011, CSR_TYPE_OP = 7'b1110011; 
    
    assign LoadNpcD = JalD | JalrD;
    assign JalD = ( Op == `JAL_OP )?   1'b1 : 1'b0;
    assign JalrD = ( Op == `JALR_OP )? 1'b1 : 1'b0;
    assign MemToRegD = (Op == LOAD_TYPE_OP)?  1'b1 : 1'b0;
    assign AluSrc1D = (Op == `AUIPC_OP)? 1'b1:1'b0;
    assign AluSrc2D = ( (Op==7'b0010011)&&(Fn3[1:0]==2'b01) )?(2'b01):(((Op==7'b0110011)||(Op==7'b1100011))? 2'b00:2'b10);
    
    always@(*) begin
        if(Op==`SLLI_OP && Fn3==`SLLI_FN3) begin
            RegWriteD = `YES;  MemWriteD = `NOSTORE;  RegReadD = 2'bxx;
            BranchTypeD = `NOBRANCH;  AluContrlD = `SLL; ImmType = `ITYPE; CSRType = `NOTCSR_Type;
        end
        else if(Op==`SRLI_OP && Fn3==`SRLI_FN3 && Fn7==`SRLI_FN7) begin
            RegWriteD = `YES;  MemWriteD = `NOSTORE;  RegReadD = 2'bxx;
            BranchTypeD = `NOBRANCH;  AluContrlD = `SRL; ImmType = `ITYPE; CSRType = `NOTCSR_Type;
        end
        else if(Op==`SRAI_OP && Fn3==`SRAI_FN3 && Fn7==`SRAI_FN7) begin
            RegWriteD = `YES;  MemWriteD = `NOSTORE;  RegReadD = 2'bxx;
            BranchTypeD = `NOBRANCH;  AluContrlD = `SRA; ImmType = `ITYPE; CSRType = `NOTCSR_Type;
        end
        else if(Op==`ADD_OP && Fn3==`ADD_FN3 && Fn7==`ADD_FN7) begin
            RegWriteD = `YES;  MemWriteD = `NOSTORE;  RegReadD = 2'bxx;
            BranchTypeD = `NOBRANCH;  AluContrlD = `ADD; ImmType = `NOIMM; CSRType = `NOTCSR_Type;
        end
        else if(Op==`SUB_OP && Fn3==`SUB_FN3 && Fn7==`SUB_FN7) begin
            RegWriteD = `YES;  MemWriteD = `NOSTORE;  RegReadD = 2'bxx;
            BranchTypeD = `NOBRANCH;  AluContrlD = `SUB; ImmType = `NOIMM; CSRType = `NOTCSR_Type;
        end
        else if(Op==`SLL_OP && Fn3==`SLL_FN3) begin
            RegWriteD = `YES;  MemWriteD = `NOSTORE;  RegReadD = 2'bxx;
            BranchTypeD = `NOBRANCH;  AluContrlD = `SLL; ImmType = `NOIMM; CSRType = `NOTCSR_Type;
        end
        else if(Op==`SLT_OP && Fn3==`SLT_FN3) begin
            RegWriteD = `YES;  MemWriteD = `NOSTORE;  RegReadD = 2'bxx;
            BranchTypeD = `NOBRANCH;  AluContrlD = `SLT; ImmType = `ITYPE; CSRType = `NOTCSR_Type;
        end
        else if(Op==`SLTU_OP && Fn3==`SLTU_FN3) begin
            RegWriteD = `YES;  MemWriteD = `NOSTORE;  RegReadD = 2'bxx;
            BranchTypeD = `NOBRANCH;  AluContrlD = `SLTU; ImmType = `ITYPE; CSRType = `NOTCSR_Type;
        end
        else if(Op==`XOR_OP && Fn3==`XOR_FN3) begin
            RegWriteD = `YES;  MemWriteD = `NOSTORE;  RegReadD = 2'bxx;
            BranchTypeD = `NOBRANCH;  AluContrlD = `XOR; ImmType = `NOIMM; CSRType = `NOTCSR_Type;
        end
        else if(Op==`SRL_OP && Fn3==`SRL_FN3 && Fn7==`SRL_FN7) begin
            RegWriteD = `YES;  MemWriteD = `NOSTORE;  RegReadD = 2'bxx;
            BranchTypeD = `NOBRANCH;  AluContrlD = `SRL; ImmType = `NOIMM; CSRType = `NOTCSR_Type;
        end
        else if(Op==`SRA_OP && Fn3==`SRA_FN3 && Fn7==`SRA_FN7) begin
            RegWriteD = `YES;  MemWriteD = `NOSTORE;  RegReadD = 2'bxx;
            BranchTypeD = `NOBRANCH;  AluContrlD = `SRA; ImmType = `NOIMM; CSRType = `NOTCSR_Type;
        end
        else if(Op==`OR_OP && Fn3==`OR_FN3) begin
            RegWriteD = `YES;  MemWriteD = `NOSTORE;  RegReadD = 2'bxx;
            BranchTypeD = `NOBRANCH;  AluContrlD = `OR; ImmType = `NOIMM; CSRType = `NOTCSR_Type;
        end
        else if(Op==`AND_OP && Fn3==`AND_FN3) begin
            RegWriteD = `YES;  MemWriteD = `NOSTORE;  RegReadD = 2'bxx;
            BranchTypeD = `NOBRANCH;  AluContrlD = `AND; ImmType = `NOIMM; CSRType = `NOTCSR_Type;
        end
        else if(Op==`ADDI_OP && Fn3==`ADDI_FN3) begin
            RegWriteD = `YES;  MemWriteD = `NOSTORE;  RegReadD = 2'bxx;
            BranchTypeD = `NOBRANCH;  AluContrlD = `ADD; ImmType = `ITYPE; CSRType = `NOTCSR_Type;
        end
        else if(Op==`SLTI_OP && Fn3==`SLTI_FN3) begin
            RegWriteD = `YES;  MemWriteD = `NOSTORE;  RegReadD = 2'bxx;
            BranchTypeD = `NOBRANCH;  AluContrlD = `SLT; ImmType = `ITYPE; CSRType = `NOTCSR_Type;
        end
        else if(Op==`SLTIU_OP && Fn3==`SLTIU_FN3) begin
            RegWriteD = `YES;  MemWriteD = `NOSTORE;  RegReadD = 2'bxx;
            BranchTypeD = `NOBRANCH;  AluContrlD = `SLTU; ImmType = `ITYPE; CSRType = `NOTCSR_Type;
        end
        else if(Op==`XORI_OP && Fn3==`XORI_FN3) begin
            RegWriteD = `YES;  MemWriteD = `NOSTORE;  RegReadD = 2'bxx;
            BranchTypeD = `NOBRANCH;  AluContrlD = `XOR; ImmType = `ITYPE; CSRType = `NOTCSR_Type;
        end
        else if(Op==`ORI_OP && Fn3==`ORI_FN3) begin
            RegWriteD = `YES;  MemWriteD = `NOSTORE;  RegReadD = 2'bxx;
            BranchTypeD = `NOBRANCH;  AluContrlD = `OR; ImmType = `ITYPE; CSRType = `NOTCSR_Type;
        end
        else if(Op==`ANDI_OP && Fn3==`ANDI_FN3) begin
            RegWriteD = `YES;  MemWriteD = `NOSTORE;  RegReadD = 2'bxx;
            BranchTypeD = `NOBRANCH;  AluContrlD = `AND; ImmType = `ITYPE; CSRType = `NOTCSR_Type;
        end
        else if(Op==`LUI_OP) begin
            RegWriteD = `YES;  MemWriteD = `NOSTORE;  RegReadD = 2'bxx;
            BranchTypeD = `NOBRANCH;  AluContrlD = `LUI; /*任意*/ImmType = `UTYPE; CSRType = `NOTCSR_Type;
        end
        else if(Op==`AUIPC_OP) begin
            RegWriteD = `YES;  MemWriteD = `NOSTORE;  RegReadD = 2'bxx;
            BranchTypeD = `NOBRANCH;  AluContrlD = `ADD; ImmType = `UTYPE; CSRType = `NOTCSR_Type;
        end
/*阶段二*/
        else if(Op==`JALR_OP && Fn3==`JALR_FN3) begin
            RegWriteD = `YES;  MemWriteD = `NOSTORE;  RegReadD = 2'bxx;
            BranchTypeD = `NOBRANCH;  AluContrlD = `ADD; ImmType = `ITYPE; CSRType = `NOTCSR_Type;
        end
        else if(Op==`LB_OP && Fn3==`LB_FN3) begin
            RegWriteD = `LB;  MemWriteD = `NOSTORE;  RegReadD = 2'bxx;
            BranchTypeD = `NOBRANCH;  AluContrlD = `ADD; ImmType = `ITYPE; CSRType = `NOTCSR_Type;
        end
        else if(Op==`LH_OP && Fn3==`LH_FN3) begin
            RegWriteD = `LH;  MemWriteD = `NOSTORE;  RegReadD = 2'bxx;
            BranchTypeD = `NOBRANCH;  AluContrlD = `ADD; ImmType = `ITYPE; CSRType = `NOTCSR_Type;
        end
        else if(Op==`LW_OP && Fn3==`LW_FN3) begin
            RegWriteD = `LW;  MemWriteD = `NOSTORE;  RegReadD = 2'bxx;
            BranchTypeD = `NOBRANCH;  AluContrlD = `ADD; ImmType = `ITYPE; CSRType = `NOTCSR_Type;
        end
        else if(Op==`LBU_OP && Fn3==`LBU_FN3) begin
            RegWriteD = `LBU;  MemWriteD = `NOSTORE;  RegReadD = 2'bxx;
            BranchTypeD = `NOBRANCH;  AluContrlD = `ADD; ImmType = `ITYPE; CSRType = `NOTCSR_Type;
        end
        else if(Op==`LHU_OP && Fn3==`LHU_FN3) begin
            RegWriteD = `LHU;  MemWriteD = `NOSTORE;  RegReadD = 2'bxx;
            BranchTypeD = `NOBRANCH;  AluContrlD = `ADD; ImmType = `ITYPE; CSRType = `NOTCSR_Type;
        end
        else if(Op==`SB_OP && Fn3==`SB_FN3) begin
            RegWriteD = `NOREGWRITE;  MemWriteD = `SB;  RegReadD = 2'bxx;
            BranchTypeD = `NOBRANCH;  AluContrlD = `ADD; ImmType = `STYPE; CSRType = `NOTCSR_Type;
        end
        else if(Op==`SH_OP && Fn3==`SH_FN3) begin
            RegWriteD = `NOREGWRITE;  MemWriteD = `SH;  RegReadD = 2'bxx;
            BranchTypeD = `NOBRANCH;  AluContrlD = `ADD; ImmType = `STYPE; CSRType = `NOTCSR_Type;
        end
        else if(Op==`SW_OP && Fn3==`SW_FN3) begin
            RegWriteD = `NOREGWRITE;  MemWriteD = `SW;  RegReadD = 2'bxx;
            BranchTypeD = `NOBRANCH;  AluContrlD = `ADD; ImmType = `STYPE; CSRType = `NOTCSR_Type;
        end
        else if(Op==`BEQ_OP && Fn3==`BEQ_FN3) begin
            RegWriteD = `NOREGWRITE;  MemWriteD = `NOSTORE;  RegReadD = 2'bxx;
            BranchTypeD = `BEQ;  AluContrlD = `AND;/*任意*/ ImmType = `SBTYPE; CSRType = `NOTCSR_Type;
        end
        else if(Op==`BNE_OP && Fn3==`BNE_FN3) begin
            RegWriteD = `NOREGWRITE;  MemWriteD = `NOSTORE;  RegReadD = 2'bxx;
            BranchTypeD = `BNE;  AluContrlD = `AND;/*任意*/ ImmType = `SBTYPE; CSRType = `NOTCSR_Type;
        end
        else if(Op==`BLT_OP && Fn3==`BLT_FN3) begin
            RegWriteD = `NOREGWRITE;  MemWriteD = `NOSTORE;  RegReadD = 2'bxx;
            BranchTypeD = `BLT;  AluContrlD = `AND;/*任意*/ ImmType = `SBTYPE; CSRType = `NOTCSR_Type;
        end
        else if(Op==`BLTU_OP && Fn3==`BLTU_FN3) begin
            RegWriteD = `NOREGWRITE;  MemWriteD = `NOSTORE;  RegReadD = 2'bxx;
            BranchTypeD = `BLTU;  AluContrlD = `AND;/*任意*/ ImmType = `SBTYPE; CSRType = `NOTCSR_Type;
        end
        else if(Op==`BGE_OP && Fn3==`BGE_FN3) begin
            RegWriteD = `NOREGWRITE;  MemWriteD = `NOSTORE;  RegReadD = 2'bxx;
            BranchTypeD = `BGE;  AluContrlD = `AND;/*任意*/ ImmType = `SBTYPE; CSRType = `NOTCSR_Type;
        end
        else if(Op==`BGEU_OP && Fn3==`BGEU_FN3) begin
            RegWriteD = `NOREGWRITE;  MemWriteD = `NOSTORE;  RegReadD = 2'bxx;
            BranchTypeD = `BGEU;  AluContrlD = `AND;/*任意*/ ImmType = `SBTYPE; CSRType = `NOTCSR_Type;
        end
        else if(Op==`JAL_OP) begin
            RegWriteD = `YES;  MemWriteD = `NOSTORE;  RegReadD = 2'bxx;
            BranchTypeD = `NOBRANCH;  AluContrlD = `ADD; ImmType = `UJTYPE; CSRType = `NOTCSR_Type;
        end
        
        /*阶段三*/
        else if(Op==`CSRRW_OP && Fn3==`CSRRW_FN3) begin
            RegWriteD = `YES;  MemWriteD = `NOSTORE;  CSRType = `CSRRW_Type;
            BranchTypeD = `NOBRANCH;  AluContrlD = `CSR; ImmType = `NOIMM;
        end
        else if(Op==`CSRRS_OP && Fn3==`CSRRS_FN3) begin
            RegWriteD = `YES;  MemWriteD = `NOSTORE; CSRType = `CSRRS_Type;
            BranchTypeD = `NOBRANCH;  AluContrlD = `CSR; ImmType = `NOIMM;
        end
        else if(Op==`CSRRC_OP && Fn3==`CSRRC_FN3) begin
            RegWriteD = `YES;  MemWriteD = `NOSTORE; CSRType = `CSRRC_Type;
            BranchTypeD = `NOBRANCH;  AluContrlD = `CSR; ImmType = `NOIMM; 
        end
        else if(Op==`CSRRWI_OP && Fn3==`CSRRWI_FN3) begin
            RegWriteD = `YES;  MemWriteD = `NOSTORE; CSRType = `CSRRWI_Type;
            BranchTypeD = `NOBRANCH;  AluContrlD = `CSR; ImmType = `CSRITYPE; 
        end
        else if(Op==`CSRRSI_OP && Fn3==`CSRRSI_FN3) begin
            RegWriteD = `YES;  MemWriteD = `NOSTORE;  CSRType = `CSRRSI_Type;
            BranchTypeD = `NOBRANCH;  AluContrlD = `CSR; ImmType = `CSRITYPE; 
        end
        else if(Op==`CSRRCI_OP && Fn3==`CSRRCI_FN3) begin
            RegWriteD = `YES;  MemWriteD = `NOSTORE;  CSRType = `CSRRCI_Type;
            BranchTypeD = `NOBRANCH;  AluContrlD = `CSR; ImmType = `CSRITYPE; 
        end
        
        else begin
            RegWriteD = `NOREGWRITE;  MemWriteD = `NOSTORE; CSRType = `NOTCSR_Type;
            BranchTypeD = `NOBRANCH;  AluContrlD = `ADD; ImmType = `NOIMM; 
        end
    end
endmodule

