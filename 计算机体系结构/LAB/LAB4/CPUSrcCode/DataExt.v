`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: USTC ESLAB
// Engineer: Wu Yuzhang
//
// Design Name: RISCV-Pipline CPU
// Module Name: DataExt
// Target Devices: Nexys4
// Tool Versions: Vivado 2017.4.1
// Description: Data Extension module
//////////////////////////////////////////////////////////////////////////////////
//����˵��
    //DataExt������������ֶ���load�����Σ�ͬʱ����load�Ĳ�ͬģʽ��Data Mem��load�������з��Ż����޷�����չ������߼���·
//����
    //IN                    �Ǵ�Data Memory��load��32bit��
    //LoadedBytesSelect     �ȼ���AluOutM[1:0]���Ƕ�Data Memory��ַ�ĵ���λ��
                            //��ΪDataMemory�ǰ��֣�32bit�����з��ʵģ�������Ҫ���ֽڵ�ַת��Ϊ�ֵ�ַ����DataMem
                            //DataMemһ�η���һ���֣�����λ��ַ������32bit������ѡ��������Ҫ���ֽ�
    //RegWriteW             ��ʾ��ͬ�� �Ĵ���д��ģʽ ������ģʽ������Parameters.v��
//���
    //OUT��ʾҪд��Ĵ���������ֵ
//ʵ��Ҫ��
    //��ȫģ��

`include "Parameters.v"
module DataExt(
    input wire [31:0] IN,
    input wire [1:0] LoadedBytesSelect,
    input wire [2:0] RegWriteW, //�����RFģ��ʱ��λ���Ϊдʹ���ź�,ֻҪ��Ϊ���д��Ч
    output reg [31:0] OUT
    ); 
    // �벹ȫ�˴�����
    always@(*) begin
        case(RegWriteW)
            `NOREGWRITE: begin
                OUT = IN;
                end
            `LB: begin  //��ȡ8bit��������չΪ32λ
                if(LoadedBytesSelect == 2'b00) OUT = { {24{IN[7]}}, IN[7:0] };
                else if(LoadedBytesSelect == 2'b01) OUT = { {24{IN[15]}}, IN[15:8] };
                else if(LoadedBytesSelect == 2'b10) OUT = { {24{IN[23]}}, IN[23:16] };
                else if(LoadedBytesSelect == 2'b11) OUT = { {24{IN[31]}}, IN[31:24] };
                else ;
                end
            `LH: begin
                if(LoadedBytesSelect == 2'b00) OUT = { {16{IN[15]}}, IN[15:0] };
                else if(LoadedBytesSelect == 2'b01) OUT = { {24{IN[24]}}, IN[24:8] };
                else if(LoadedBytesSelect == 2'b10) OUT = { {24{IN[31]}}, IN[31:16] };
                else ;
                end
            `LW: begin
                OUT = IN;
                end
            `LBU: begin
                if(LoadedBytesSelect == 2'b00) OUT = { 24'b0, IN[7:0] };
                else if(LoadedBytesSelect == 2'b01) OUT = { 24'b0, IN[15:8] };
                else if(LoadedBytesSelect == 2'b10) OUT = { 24'b0, IN[23:16] };
                else if(LoadedBytesSelect == 2'b11) OUT = { 24'b0, IN[31:24] };
                else ;
                end
            `LHU: begin
                if(LoadedBytesSelect == 2'b00) OUT = { 16'b0, IN[15:0] };
                else if(LoadedBytesSelect == 2'b01) OUT = { 16'b0, IN[24:8] };
                else if(LoadedBytesSelect == 2'b10) OUT = { 16'b0, IN[31:16] };
                else ;
                end
            default: ;
        endcase
    end
endmodule

