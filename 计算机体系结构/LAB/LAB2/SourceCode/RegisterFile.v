`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: USTC ESLAB 
// Engineer: Wu Yuzhang
// 
// Design Name: RISCV-Pipline CPU
// Module Name: RegisterFile
// Target Devices: Nexys4
// Tool Versions: Vivado 2017.4.1
// Description: 
//////////////////////////////////////////////////////////////////////////////////
//����˵��
    //������д�룬�첽���ļĴ����ѣ�0�żĴ���ֵʼ��Ϊ32'b0
    //�ڽ���RV32Coreʱ������Ϊ~clk����˱�ģ��ʱ���������������ʼ���෴
    //�ȼ���������ģ��ʱ��������ʱ��clk��ͬʱ�޸Ĵ���Ϊalways@(negedge clk or negedge rst) 
//ʵ��Ҫ��  
    //�����޸�

module RegisterFile(
    input wire clk,
    input wire rst,
    input wire WE3,//дʹ��
    input wire [4:0] A1,
    input wire [4:0] A2,
    input wire [4:0] A3,//д��ַ
    input wire [31:0] WD3,//д����
    output wire [31:0] RD1,
    output wire [31:0] RD2
    );

    reg [31:0] RegFile[31:1];
     initial begin //����Ϊ������ԣ�ʵ��Ӧ��ֻ�轫0�żĴ�����0���ɣ����಻Ӱ��
      RegFile[1]=0;RegFile[2]=0;RegFile[3]=0;RegFile[4]=0;RegFile[5]=0;RegFile[6]=0;RegFile[7]=0;
      RegFile[8]=0;RegFile[9]=0;RegFile[10]=0;RegFile[11]=0;RegFile[12]=0;RegFile[13]=0;RegFile[14]=0;RegFile[15]=0;
      RegFile[16]=0;RegFile[17]=0;RegFile[18]=0;RegFile[19]=0;RegFile[20]=0;RegFile[21]=0;RegFile[22]=0;RegFile[23]=0;
      RegFile[24]=0;RegFile[25]=0;RegFile[26]=0;RegFile[27]=0;RegFile[28]=0;RegFile[29]=0;RegFile[30]=0;RegFile[31]=0;
    end
    integer i;
    //
    always@(posedge clk or posedge rst) 
    begin 
        if(rst)                                 for(i=1;i<32;i=i+1) RegFile[i][31:0]<=32'b0;
        else if( (WE3==1'b1) && (A3!=5'b0) )    RegFile[A3]<=WD3;   
    end
    //    
    reg [31:0]rd1_reg,rd2_reg;
    always@(*) begin
        if(A1 == 5'b0) rd1_reg = 32'b0;
        else if( WE3 == 1'b1 && A3 == A1) rd1_reg = WD3;
        else rd1_reg = RegFile[A1];
        if(A2 == 5'b0) rd2_reg = 32'b0;
        else if( WE3 == 1'b1 && A3 == A2) rd2_reg = WD3;
        else rd2_reg = RegFile[A2];
    end
    assign RD1 = rd1_reg;
    assign RD2 = rd2_reg;
    
endmodule
