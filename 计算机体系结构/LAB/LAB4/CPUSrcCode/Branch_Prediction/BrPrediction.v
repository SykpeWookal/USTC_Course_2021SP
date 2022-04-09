`timescale 1ns / 1ps

module BrPrediction(
    input wire clk, 
    input wire [31:0] PCF,  //��ǰPC
    input wire [31:0] PCE,  //EX��PC
    input wire [31:0] BrNPC,//��EX�δ����ķ�֧Ŀ���ַ
    input wire BranchE,     //EX���ͻص��Ƿ���ת�ź�
    
    input wire Branch_P_EX, //EX���ͻص�Ԥ��ֵ
    output reg Branch_P_IF,   //�͸���һ�ε�Ԥ��ֵ
    
    input wire BTBhit_EX,//EX�ش����Ƿ�BTB����
    output reg BTBhit_IF,//�����ź�
    
    output reg Branch_Real,//�͸�NPC����ģ�飬��ת��־
    output reg [31:0] BranchTarget_Real,//�͸�NPC����ģ��
    
    output reg error_flush,
    input wire StallE,
    output reg [31:0] brancherror_count
);

`define BTB
//`define BHT

    localparam BTBSIZE = 12;//PC[13��2] 12λֱ��ӳ�䵽BTB������

`ifdef BTB
    reg [31:0] brnpc_reg;
    always@(*) begin
        brnpc_reg = BrNPC;    
    end
    

    reg [ 32 + BTBSIZE : 0 ] Branch_Target_Buffer[ (1<<BTBSIZE) -  1 : 0 ];//PC�ĵ�12λֱ��ӳ�䵽BTB   [0]�Ƿ���ת [1-32]target��[33-44] PC
    
    always@(*) begin  //IF��ʹ��BTB��
        if( PCF[ BTBSIZE + 1 : 2 ] == Branch_Target_Buffer[ PCF[BTBSIZE + 1 : 2] ][ 32 + BTBSIZE : 33 ] ) begin//BTB���У�˵�����Ƿ�ָ֧�����[0]��ֵѡ��NPC
            BTBhit_IF = 1'b1;
            if(Branch_Target_Buffer[ PCF[BTBSIZE + 1 : 2] ][0] == 1) begin  //Ԥ����ת��ֱ�ӽ���Щ�źŴ���NPC����ģ�齫��֧��ַ��Ϊ��һ��PC
                Branch_Real = 1;
                BranchTarget_Real = Branch_Target_Buffer[ PCF[BTBSIZE + 1 : 2] ][ 32 : 1 ];
                Branch_P_IF = 1;
            end
            else begin //Ԥ�ⲻ��ת
                Branch_Real = 0;
                Branch_P_IF = 1'b0;
            end
        end
        else begin//BTBδ����
            Branch_Real = 0;
            Branch_P_IF = 1'b0;
            BTBhit_IF = 1'b0;
        end
        
        
        error_flush = 0;
        if((BranchE == 1'b1) && (BTBhit_EX == 1'b0)) begin  //�����µ�BTB����,BTBδ������BranchE==1
            error_flush = 1;          //Ԥ��������ǰ���ζμ���ˮ�Ĵ���
            Branch_Real = 1;          //ʵ����ת
            BranchTarget_Real = brnpc_reg;//ʵ����ת��ַ
        end
        if(BTBhit_EX == 1'b1) begin //��ǰEX����һ����ָ֧��������BTB���У����ݵ�ǰBranchE����BTB��
            if((Branch_P_EX == 1'b0) && (BranchE == 1'b1)) begin
                error_flush = 1;//Ԥ��������ǰ���ζμ���ˮ�Ĵ���
                Branch_Real = 1;
                BranchTarget_Real = brnpc_reg;
            end
            if((Branch_P_EX == 1'b1) && (BranchE == 1'b0)) begin
                error_flush = 1;//Ԥ��������ǰ���ζμ���ˮ�Ĵ���
                Branch_Real = 1;
                BranchTarget_Real = PCE + 32'h4;
            end
        end

    end


    always@(posedge clk) begin //ά��BTB��
        if(BranchE && (BTBhit_EX == 1'b0)) begin  //�����µ�BTB����,BTBδ������BranchE==1
            Branch_Target_Buffer[ PCE[BTBSIZE + 1 : 2] ][ 32 + BTBSIZE : 33 ] = PCE[ BTBSIZE + 1 : 2 ];
            Branch_Target_Buffer[ PCE[BTBSIZE + 1 : 2] ][ 32  : 1 ] = brnpc_reg;
            Branch_Target_Buffer[ PCE[BTBSIZE + 1 : 2] ][0] = 1;
        end
     end

     always@(posedge clk) begin
        if(BTBhit_EX == 1'b1) begin //��ǰEX����һ����ָ֧��������BTB���У����ݵ�ǰBranchE����BTB��
            if((Branch_P_EX == 1'b0) && (BranchE == 1'b1)) begin
                Branch_Target_Buffer[ PCE[BTBSIZE + 1 : 2] ][0] = 1;
            end
            if((Branch_P_EX == 1'b1) && (BranchE == 1'b0)) begin
                Branch_Target_Buffer[ PCE[BTBSIZE + 1 : 2] ][0] = 0;
            end
        end
    end
`endif





`ifdef BHT
    reg [31:0] brnpc_reg;
    always@(*) begin
        brnpc_reg = BrNPC;    
    end
    

    reg [ 33 + BTBSIZE : 0 ] Branch_Target_Buffer[ (1<<BTBSIZE) -  1 : 0 ];//PC�ĵ�12λֱ��ӳ��  [1:0]�Ƿ���ת [2-33]target��[34-45] PC
    
    always@(*) begin  //IF��ʹ��BTB��
        if( PCF[ BTBSIZE + 1 : 2 ] == Branch_Target_Buffer[ PCF[BTBSIZE + 1 : 2] ][ 33 + BTBSIZE : 34 ] ) begin
            //BTB���У�˵�����Ƿ�ָ֧�����[0]��ֵѡ��NPC
            BTBhit_IF = 1'b1;
            if(Branch_Target_Buffer[ PCF[BTBSIZE + 1 : 2] ][1:0] == 2'b11 || Branch_Target_Buffer[ PCF[BTBSIZE + 1 : 2] ][1:0] == 2'b10) begin  
                //Ԥ����ת��ֱ�ӽ���Щ�źŴ���NPC����ģ�齫��֧��ַ��Ϊ��һ��PC
                Branch_Real = 1;
                BranchTarget_Real = Branch_Target_Buffer[ PCF[BTBSIZE + 1 : 2] ][ 33 : 2 ];
                Branch_P_IF = 1;
            end
            else begin //Ԥ�ⲻ��ת
                Branch_Real = 0;
                Branch_P_IF = 1'b0;
            end
        end
        else begin//BTBδ����
            Branch_Real = 0;
            Branch_P_IF = 1'b0;
            BTBhit_IF = 1'b0;
        end
        
        error_flush = 0;
        if((BranchE == 1'b1) && (BTBhit_EX == 1'b0)) begin  //�����µ�BTB����,BTBδ������BranchE==1
            error_flush = 1;          //Ԥ��������ǰ���ζμ���ˮ�Ĵ���
            Branch_Real = 1;          //ʵ����ת
            BranchTarget_Real = brnpc_reg;//ʵ����ת��ַ
        end
        if(BTBhit_EX == 1'b1) begin //��ǰEX����һ����ָ֧��������BTB���У����ݵ�ǰBranchE����BTB��
            if((Branch_P_EX == 1'b0) && (BranchE == 1'b1)) begin
                error_flush = 1;//Ԥ��������ǰ���ζμ���ˮ�Ĵ���
                Branch_Real = 1;
                BranchTarget_Real = brnpc_reg;
            end
            if((Branch_P_EX == 1'b1) && (BranchE == 1'b0)) begin
                error_flush = 1;//Ԥ��������ǰ���ζμ���ˮ�Ĵ���
                Branch_Real = 1;
                BranchTarget_Real = PCE + 32'h4;
            end
        end
    end


    always@(posedge clk) begin //ά��BHT��
        if(BranchE && (BTBhit_EX == 1'b0)) begin  //�����µ�BTB����,BTBδ������BranchE==1
            Branch_Target_Buffer[ PCE[BTBSIZE + 1 : 2] ][ 33 + BTBSIZE : 34 ] = PCE[ BTBSIZE + 1 : 2 ];
            Branch_Target_Buffer[ PCE[BTBSIZE + 1 : 2] ][ 33  : 2 ] = brnpc_reg;
            Branch_Target_Buffer[ PCE[BTBSIZE + 1 : 2] ][1:0] = 2'b11;
        end
     end

     always@(posedge clk) begin
        if(BTBhit_EX == 1'b1) begin //��ǰEX����һ����ָ֧��������BTB���У����ݵ�ǰBranchE����BTB��
            if((Branch_P_EX == 1'b0) && (BranchE == 1'b1)) begin
                if(Branch_Target_Buffer[ PCE[BTBSIZE + 1 : 2] ][1:0] == 2'b00) begin
                    Branch_Target_Buffer[ PCE[BTBSIZE + 1 : 2] ][1:0] = 2'b01;
                end
                else if(Branch_Target_Buffer[ PCE[BTBSIZE + 1 : 2] ][1:0] == 2'b01)begin
                    Branch_Target_Buffer[ PCE[BTBSIZE + 1 : 2] ][1:0] = 2'b10;
                end
            end
            if((Branch_P_EX == 1'b1) && (BranchE == 1'b0)) begin
                if(Branch_Target_Buffer[ PCE[BTBSIZE + 1 : 2] ][1:0] == 2'b10) begin
                    Branch_Target_Buffer[ PCE[BTBSIZE + 1 : 2] ][1:0] = 2'b01;
                end
                else if(Branch_Target_Buffer[ PCE[BTBSIZE + 1 : 2] ][1:0] == 2'b11)begin
                    Branch_Target_Buffer[ PCE[BTBSIZE + 1 : 2] ][1:0] = 2'b10;
                end
            end
            if((Branch_P_EX == 1'b1) && (BranchE == 1'b1)) begin
                if(Branch_Target_Buffer[ PCE[BTBSIZE + 1 : 2] ][1:0] == 2'b10) begin
                    Branch_Target_Buffer[ PCE[BTBSIZE + 1 : 2] ][1:0] = 2'b11;
                end
            end
            if((Branch_P_EX == 1'b0) && (BranchE == 1'b0)) begin
                if(Branch_Target_Buffer[ PCE[BTBSIZE + 1 : 2] ][1:0] == 2'b01) begin
                    Branch_Target_Buffer[ PCE[BTBSIZE + 1 : 2] ][1:0] = 2'b00;
                end
            end
        end
     end
`endif
    


    initial brancherror_count = 0;
    //ά��Ԥ��������
    always@(posedge clk) begin
        if(StallE) begin
            brancherror_count <= brancherror_count;
        end
        else begin
            if(BranchE && (BTBhit_EX == 1'b0))begin//�����±���ʱԤ�����
                brancherror_count <= brancherror_count + 1;
            end
            if(BTBhit_EX == 1'b1)begin
                if((Branch_P_EX == 1'b0) && (BranchE == 1'b1)) begin  //Ԥ�����
                    brancherror_count <= brancherror_count + 1;
                end
                if((Branch_P_EX == 1'b1) && (BranchE == 1'b0)) begin
                    brancherror_count <= brancherror_count + 1;
                end
            end
        end
    end


endmodule