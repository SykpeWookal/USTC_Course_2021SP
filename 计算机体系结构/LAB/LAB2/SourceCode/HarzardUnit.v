`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: USTC ESLAB 
// Engineer: Wu Yuzhang
// 
// Design Name: RISCV-Pipline CPU
// Module Name: HarzardUnit
// Target Devices: Nexys4
// Tool Versions: Vivado 2017.4.1
// Description: Deal with harzards in pipline
//////////////////////////////////////////////////////////////////////////////////
//����˵��
    //HarzardUnit����������ˮ�߳�ͻ��ͨ���������ݣ�forward�Լ���ˢ��ˮ�ν��������غͿ�����أ�����߼���·
    //�������ʵ�֡�ǰ�ڲ���CPU��ȷ��ʱ��������ÿ����ָ������������ָ�Ȼ��ֱ�Ӱѱ�ģ�������Ϊ����forward����stall����flush 
//����
    //CpuRst                                    �ⲿ�źţ�������ʼ��CPU����CpuRst==1ʱCPUȫ�ָ�λ���㣨���жμĴ���flush����Cpu_Rst==0ʱcpu��ʼִ��ָ��
    //ICacheMiss, DCacheMiss                    Ϊ����ʵ��Ԥ���źţ���ʱ�������ӣ���������cache miss
    //BranchE, JalrE, JalD                      ��������������
    //Rs1D, Rs2D, Rs1E, Rs2E, RdE, RdM, RdW     ��������������أ��ֱ��ʾԴ�Ĵ���1���룬Դ�Ĵ���2���룬Ŀ��Ĵ�������
    //RegReadE RegReadD[1]==1                   ��ʾA1��Ӧ�ļĴ���ֵ��ʹ�õ��ˣ�RegReadD[0]==1��ʾA2��Ӧ�ļĴ���ֵ��ʹ�õ��ˣ�����forward�Ĵ���
    //RegWriteM, RegWriteW                      ��������������أ�RegWrite!=3'b0˵����Ŀ��Ĵ�����д�����
    //MemToRegE                                 ��ʾEx�ε�ǰָ�� ��Data Memory�м������ݵ��Ĵ�����
//���
    //StallF, FlushF, StallD, FlushD, StallE, FlushE, StallM, FlushM, StallW, FlushW    ��������μĴ�������stall��ά��״̬���䣩��flush�����㣩
    //Forward1E, Forward2E                                                              ����forward
//ʵ��Ҫ��  
    //��ȫģ��  
    
    
module HarzardUnit(
    input wire CpuRst, ICacheMiss, DCacheMiss, 
    input wire BranchE, JalrE, JalD, 
    input wire [4:0] Rs1D, Rs2D, Rs1E, Rs2E, RdE, RdM, RdW,
    input wire [1:0] RegReadE,
    input wire MemToRegE,
    input wire [2:0] RegWriteM, RegWriteW,
    output reg StallF, FlushF, StallD, FlushD, StallE, FlushE, StallM, FlushM, StallW, FlushW,
    output reg [1:0] Forward1E, Forward2E
    );
    // �벹ȫ�˴�����
      initial StallF = 1'b0;
      initial   FlushF = 1'b0;
      initial   StallD = 1'b0;
      initial   FlushD = 1'b0;
      initial   StallE = 1'b0;
      initial   FlushE = 1'b0;
      initial   StallM = 1'b0;
      initial   FlushM = 1'b0;
      initial   StallW = 1'b0;
      initial   FlushW = 1'b0;
      initial   Forward1E = 2'b00;
      initial   Forward2E = 2'b00;

    always@(*) begin
        StallF = 1'b0;
        FlushF = 1'b0;
        StallD = 1'b0;
        FlushD = 1'b0;
        StallE = 1'b0;
        FlushE = 1'b0;
        StallM = 1'b0;
        FlushM = 1'b0;
        StallW = 1'b0;
        FlushW = 1'b0;
     end
    
    always@(*) begin
        StallF = 1'b0; FlushF = 1'b0; StallD = 1'b0; FlushD = 1'b0; StallE = 1'b0;
        FlushE = 1'b0; StallM = 1'b0; FlushM = 1'b0; StallW = 1'b0; FlushW = 1'b0;
        if(CpuRst) begin
            FlushF = 1'b1; FlushD = 1'b1; FlushE = 1'b1; FlushM = 1'b1;  FlushW = 1'b1;
        end
        else if(BranchE) begin /*��֧��EXE��ִ�з�֧�����ID,EX�Ĵ�����IFȡͬһ��ָ��*/
            FlushD = 1'b1;  FlushE = 1'b1; FlushM = 1'b1;
        end
        else if(JalrE) begin 
            FlushD = 1'b1;  FlushE = 1'b1; 
        end
        else if(JalD) begin
            FlushD = 1'b1;
        end
        else if(MemToRegE & ((RdE == Rs1D) || (RdE == Rs2D))) begin
            StallF = 1'b1;
            StallD = 1'b1;
            FlushE = 1'b1;
        end
    end
    
    //Forward�ź�
    always@(*) begin
      /*Forward1E*/
        if((RegWriteM != `NOREGWRITE) && (RdM == Rs1E) && (RdM != 5'b0))
            Forward1E = 2'b10;
        else if((RegWriteW != `NOREGWRITE) && (RdW == Rs1E) && (RdW != 5'b0))
            Forward1E = 2'b01;
        else
            Forward1E = 2'b00;
      /*Forward2E*/
        if((RegWriteM != `NOREGWRITE) && (RdM == Rs2E) && (RdM != 5'b0))
            Forward2E = 2'b10;
        else if((RegWriteW != `NOREGWRITE) && (RdW == Rs2E) && (RdW != 5'b0))
            Forward2E = 2'b01;
        else
            Forward2E = 2'b00;
    end  

endmodule