`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: USTC ESLAB 
// Engineer: Wu Yuzhang
// 
// Design Name: RISCV-Pipline CPU
// Module Name: 
// Target Devices: Nexys4
// Tool Versions: Vivado 2017.4.1
// Description: Define some constant values
//////////////////////////////////////////////////////////////////////////////////
//功能说明
    //为了代码可读性，定义了常量值
//实验要求  
    //无需修改

`ifndef CONST_VALUES
`define CONST_VALUES
//ALUContrl[3:0]
    `define SLL  4'd0
    `define SRL  4'd1
    `define SRA  4'd2
    `define ADD  4'd3
    `define SUB  4'd4
    `define XOR  4'd5
    `define OR  4'd6
    `define AND  4'd7
    `define SLT  4'd8
    `define SLTU  4'd9
    `define LUI  4'd10
    `define CSR  4'd11
//BranchType[2:0]
    `define NOBRANCH  3'd0
    `define BEQ  3'd1
    `define BNE  3'd2
    `define BLT  3'd3
    `define BLTU  3'd4
    `define BGE  3'd5
    `define BGEU  3'd6
//ImmType[2:0]
    `define RTYPE  3'd0
    `define ITYPE  3'd1
    `define STYPE  3'd2
    `define SBTYPE  3'd3
    `define UTYPE  3'd4
    `define UJTYPE  3'd5  
    `define NOIMM   3'd6
    /*CSR*/
    `define CSRITYPE   3'd7
//RegWrite[2:0]  six kind of ways to save values to Register
    `define NOREGWRITE  3'b0	//	Do not write Register
    `define LB  3'b001			//	load 8bit from Mem then signed extended to 32bit
    `define LH  3'b010			//	load 16bit from Mem then signed extended to 32bit
    `define LW  3'b011			//	write 32bit to Register
    `define LBU  3'b100			//	load 8bit from Mem then unsigned extended to 32bit
    `define LHU  3'b101			//	load 16bit from Mem then unsigned extended to 32bit
    `define YES  3'b111        //其他指令需要写寄存器堆
//MEMWrite[3:0]
    `define NOSTORE 4'b0000
    `define SB 4'b0001
    `define SH 4'b0011
    `define SW 4'b1111


//op定义 阶段一
    `define SLLI_OP   7'b0010011
    `define SRLI_OP   7'b0010011
    `define SRAI_OP   7'b0010011
    `define ADD_OP    7'b0110011
    `define SUB_OP    7'b0110011
    `define SLL_OP    7'b0110011
    `define SLT_OP    7'b0110011
    `define SLTU_OP   7'b0110011
    `define XOR_OP    7'b0110011
    `define SRL_OP    7'b0110011
    `define SRA_OP    7'b0110011
    `define OR_OP     7'b0110011
    `define AND_OP    7'b0110011
    `define ADDI_OP   7'b0010011
    `define SLTI_OP   7'b0010011
    `define SLTIU_OP  7'b0010011
    `define XORI_OP   7'b0010011
    `define ORI_OP    7'b0010011
    `define ANDI_OP   7'b0010011
    `define LUI_OP    7'b0110111
    `define AUIPC_OP  7'b0010111
//阶段二
    `define JALR_OP   7'b1100111
    `define LB_OP     7'b0000011
    `define LH_OP     7'b0000011
    `define LW_OP     7'b0000011
    `define LBU_OP    7'b0000011
    `define LHU_OP    7'b0000011
    `define SB_OP     7'b0100011
    `define SH_OP     7'b0100011
    `define SW_OP     7'b0100011
    `define BEQ_OP    7'b1100011
    `define BNE_OP    7'b1100011
    `define BLT_OP    7'b1100011
    `define BLTU_OP   7'b1100011
    `define BGE_OP    7'b1100011
    `define BGEU_OP   7'b1100011
    `define JAL_OP    7'b1101111
//阶段三
    `define CSRRW_OP  7'b1110011
    `define CSRRS_OP  7'b1110011
    `define CSRRC_OP  7'b1110011
    `define CSRRWI_OP 7'b1110011
    `define CSRRSI_OP 7'b1110011
    `define CSRRCI_OP 7'b1110011
    

//Fn3定义 阶段一
    `define SLLI_FN3   3'b001
    `define SRLI_FN3   3'b101
    `define SRAI_FN3   3'b101
    `define ADD_FN3    3'b000
    `define SUB_FN3    3'b000
    `define SLL_FN3    3'b001
    `define SLT_FN3    3'b010
    `define SLTU_FN3   3'b011
    `define XOR_FN3    3'b100
    `define SRL_FN3    3'b101
    `define SRA_FN3    3'b101
    `define OR_FN3     3'b110
    `define AND_FN3    3'b111
    `define ADDI_FN3   3'b000
    `define SLTI_FN3   3'b010
    `define SLTIU_FN3  3'b011
    `define XORI_FN3   3'b100
    `define ORI_FN3    3'b110
    `define ANDI_FN3   3'b111
//阶段二
    `define JALR_FN3   3'b000
    `define LB_FN3     3'b000
    `define LH_FN3     3'b001
    `define LW_FN3     3'b010
    `define LBU_FN3    3'b100
    `define LHU_FN3    3'b101
    `define SB_FN3     3'b000
    `define SH_FN3     3'b001
    `define SW_FN3     3'b010
    `define BEQ_FN3    3'b000
    `define BNE_FN3    3'b001
    `define BLT_FN3    3'b100
    `define BLTU_FN3   3'b110
    `define BGE_FN3    3'b101
    `define BGEU_FN3   3'b111
//阶段三
    `define CSRRW_FN3  3'b001
    `define CSRRS_FN3  3'b010
    `define CSRRC_FN3  3'b011
    `define CSRRWI_FN3 3'b101
    `define CSRRSI_FN3 3'b110
    `define CSRRCI_FN3 3'b111

//Fn7定义
    `define SRLI_FN7   7'b0000000
    `define SRAI_FN7   7'b0100000
    `define ADD_FN7    7'b0000000
    `define SUB_FN7    7'b0100000
    `define SRL_FN7    7'b0000000
    `define SRA_FN7    7'b0100000
    
  //CSRType
    `define CSRRW_Type  3'b000
    `define CSRRS_Type  3'b001
    `define CSRRC_Type  3'b010
    `define CSRRWI_Type 3'b011
    `define CSRRSI_Type 3'b100
    `define CSRRCI_Type 3'b101
    `define NOTCSR_Type 3'b111
    
`endif
