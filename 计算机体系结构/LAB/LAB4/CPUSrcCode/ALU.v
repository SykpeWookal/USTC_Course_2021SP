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

//功能和接口说明
	//ALU接受两个操作数，根据AluContrl的不同，进行不同的计算操作，将计算结果输出到AluOut
	//AluContrl的类型定义在Parameters.v中
//推荐格式：
    //case()
    //    `ADD:        AluOut<=Operand1 + Operand2; 
    //   	.......
    //    default:    AluOut <= 32'hxxxxxxxx;                          
    //endcase
//实验要求  
    //补全模块

`include "Parameters.v"   
module ALU(
    input wire [31:0] Operand1,
    input wire [31:0] Operand2,
    input wire [3:0] AluContrl,
    input wire [31:0] CSRDATA,
    output reg [31:0] AluOut
    );    
    // 请补全此处代码
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

