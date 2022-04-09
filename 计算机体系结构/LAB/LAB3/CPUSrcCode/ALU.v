`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: USTC ESLAB 
// Engineer: Wu Yuzhang
// 
// Design Name: RISCV-Pipline CPU
// Module Name: ALU
// Target Devices: Nexys4
// Tool Versions: Vivado 2017.4.1
// Description: ALU unit of RISCV CPU
//////////////////////////////////////////////////////////////////////////////////

//���ܺͽӿ�˵��
	//ALU��������������������AluContrl�Ĳ�ͬ�����в�ͬ�ļ���������������������AluOut
	//AluContrl�����Ͷ�����Parameters.v��
//�Ƽ���ʽ��
    //case()
    //    `ADD:        AluOut<=Operand1 + Operand2; 
    //   	.......
    //    default:    AluOut <= 32'hxxxxxxxx;                          
    //endcase
//ʵ��Ҫ��  
    //��ȫģ��

`include "Parameters.v"   
module ALU(
    input wire [31:0] Operand1,
    input wire [31:0] Operand2,
    input wire [3:0] AluContrl,
    input wire [31:0] CSRDATA,
    output reg [31:0] AluOut
    );    
    // �벹ȫ�˴�����
    always@(*) begin
        case(AluContrl)
            `SLL: begin
                    AluOut = Operand1 << Operand2[4:0];
                  end
            `SRL: begin
                    AluOut = Operand1 >> Operand2[4:0];
                  end
            `SRA: begin
                    AluOut = ($signed(Operand1)) >>>  Operand2[4:0];
                  end
            `ADD: begin
                    AluOut = Operand1 + Operand2;
                  end
            `SUB: begin
                    AluOut = Operand1 - Operand2;
                  end
            `XOR: begin
                    AluOut = Operand1 ^ Operand2;
                  end
            `OR:  begin
                    AluOut = Operand1 | Operand2;
                  end
            `AND: begin
                    AluOut = Operand1 & Operand2;
                  end
            `SLT: begin
                    AluOut = ($signed(Operand1) < $signed(Operand2))?  32'h1 : 32'h0;
                  end
            `SLTU: begin
                    AluOut = (Operand1 < Operand2)?  32'h1 : 32'h0;
                   end
            `LUI:  begin
                    AluOut = Operand2;
                   end
            `CSR: begin
                    AluOut = CSRDATA;
                   end
            default: AluOut = 0;
        endcase
    end
endmodule

