`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: USTC ESLAB 
// Engineer: Wu Yuzhang
// 
// Design Name: RISCV-Pipline CPU
// Module Name: InstructionRamWrapper
// Target Devices: Nexys4
// Tool Versions: Vivado 2017.4.1
// Description: a Verilog-based ram which can be systhesis as BRAM
// 
//////////////////////////////////////////////////////////////////////////////////
//����˵��
    //ͬ����дbram��a��ֻ��������ȡָ��b�ڿɶ�д���������debug_module���ж�д
    //дʹ��Ϊ1bit����֧��byte write
//����
    //clk               ����ʱ��
    //addra             a�ڶ���ַ
    //addrb             b�ڶ�д��ַ
    //dinb              b��д��������
    //web               b��дʹ��
//���
    //douta             a�ڶ�����
    //doutb             b�ڶ�����
//ʵ��Ҫ��  
    //�����޸�

module InstructionRam(
    input  clk,
    input  web,
    input  [31:2] addra, addrb,
    input  [31:0] dinb,
    output reg [31:0] douta, doutb
);
initial begin douta=0; doutb=0; end

wire addra_valid = ( addra[31:14]==18'h0 );
wire addrb_valid = ( addrb[31:14]==18'h0 );
wire [11:0] addral = addra[13:2];
wire [11:0] addrbl = addrb[13:2];

reg [31:0] ram_cell [0:4095];

initial begin    // ���԰Ѳ���ָ���ֶ�����˴�
   /* ram_cell[0] = 32'h00000000;*/
        // ......
    /*ram_cell[1] = 32'h00300093;
    ram_cell[2] = 32'h00700113;
    ram_cell[3] = 32'h00000013;
    ram_cell[4] = 32'h00000013;
    ram_cell[5] = 32'h00000013;
    ram_cell[6] = 32'h00000013;
    
    ram_cell[7] = 32'h00208f33;
    ram_cell[8] = 32'h00a00e93;
    ram_cell[9] = 32'h00400193;
    ram_cell[10] = 32'h00000013;
    ram_cell[11] = 32'h00000013;
    ram_cell[12] = 32'h00000013;
    ram_cell[13] = 32'h00000013;
    ram_cell[14] = 32'h01df0463;
    ram_cell[15] = 32'h2900206f;
    ram_cell[16] = 32'h00300093;
    ram_cell[17] = 32'h00700113;
    ram_cell[18] = 32'h00208f33;
    ram_cell[19] = 32'h00a00e93;
    ram_cell[20] = 32'h00400193;*/
    
end

always @ (posedge clk)
    douta <= addra_valid ? ram_cell[addral] : 0;
    
always @ (posedge clk)
    doutb <= addrb_valid ? ram_cell[addrbl] : 0;

always @ (posedge clk)
    if(web & addrb_valid) 
        ram_cell[addrbl] <= dinb;

endmodule

