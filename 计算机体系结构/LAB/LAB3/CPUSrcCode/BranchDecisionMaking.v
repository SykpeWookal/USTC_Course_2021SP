`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: USTC ESLAB 
// Engineer: Wu Yuzhang
// 
// Design Name: RISCV-Pipline CPU
// Module Name: BranchDecisionMaking
// Target Devices: Nexys4
// Tool Versions: Vivado 2017.4.1
// Description: Decide whether to branch 
//////////////////////////////////////////////////////////////////////////////////
//���ܺͽӿ�˵��
    //BranchDecisionMaking��������������������BranchTypeE�Ĳ�ͬ�����в�ͬ���жϣ�����֧Ӧ��takenʱ����BranchE=1'b1
    //BranchTypeE�����Ͷ�����Parameters.v��
//�Ƽ���ʽ��
    //case()
    //    `BEQ: ???
    //      .......
    //    default:                            BranchE<=1'b0;  //NOBRANCH
    //endcase
//ʵ��Ҫ��  
    //��ȫģ��
 
`include "Parameters.v"   
module BranchDecisionMaking(
    input wire [2:0] BranchTypeE,
    input wire [31:0] Operand1,Operand2,
    output reg BranchE
    );
    // �벹ȫ�˴�����
    always@(*) begin
        case(BranchTypeE)
            `NOBRANCH: BranchE = 1'b0;
            `BEQ: begin
                BranchE = (Operand1 == Operand2)?  1'b1 : 1'b0;
                end
            `BNE: begin
                BranchE = (Operand1 != Operand2)?  1'b1 : 1'b0;
                end
            `BLT: begin
                BranchE = ($signed(Operand1) < $signed(Operand2))?  1'b1 : 1'b0;
                end
            `BLTU: begin
                BranchE = (Operand1 < Operand2)?  1'b1 : 1'b0;
                end
            `BGE: begin
                BranchE = ($signed(Operand1) >= $signed(Operand2))?  1'b1 : 1'b0;
                end
            `BGEU: begin
                BranchE = (Operand1 >= Operand2)?  1'b1 : 1'b0;
                end
            default: BranchE = 1'b0;
        endcase
    end
endmodule

