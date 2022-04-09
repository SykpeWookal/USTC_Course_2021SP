`timescale 1ns / 1ps

module BrPrediction(
    input wire clk, 
    input wire [31:0] PCF,  //当前PC
    input wire [31:0] PCE,  //EX段PC
    input wire [31:0] BrNPC,//从EX段传出的分支目标地址
    input wire BranchE,     //EX段送回的是否跳转信号
    
    input wire Branch_P_EX, //EX段送回的预测值
    output reg Branch_P_IF,   //送给下一段的预测值
    
    input wire BTBhit_EX,//EX回传的是否BTB命中
    output reg BTBhit_IF,//命中信号
    
    output reg Branch_Real,//送给NPC生成模块，跳转标志
    output reg [31:0] BranchTarget_Real,//送给NPC生成模块
    
    output reg error_flush,
    input wire StallE,
    output reg [31:0] brancherror_count
);

`define BTB
//`define BHT

    localparam BTBSIZE = 12;//PC[13：2] 12位直接映射到BTB表项上

`ifdef BTB
    reg [31:0] brnpc_reg;
    always@(*) begin
        brnpc_reg = BrNPC;    
    end
    

    reg [ 32 + BTBSIZE : 0 ] Branch_Target_Buffer[ (1<<BTBSIZE) -  1 : 0 ];//PC的低12位直接映射到BTB   [0]是否跳转 [1-32]target，[33-44] PC
    
    always@(*) begin  //IF段使用BTB表
        if( PCF[ BTBSIZE + 1 : 2 ] == Branch_Target_Buffer[ PCF[BTBSIZE + 1 : 2] ][ 32 + BTBSIZE : 33 ] ) begin//BTB命中，说明它是分支指令，根据[0]的值选择NPC
            BTBhit_IF = 1'b1;
            if(Branch_Target_Buffer[ PCF[BTBSIZE + 1 : 2] ][0] == 1) begin  //预测跳转，直接将这些信号传给NPC生成模块将分支地址作为下一个PC
                Branch_Real = 1;
                BranchTarget_Real = Branch_Target_Buffer[ PCF[BTBSIZE + 1 : 2] ][ 32 : 1 ];
                Branch_P_IF = 1;
            end
            else begin //预测不跳转
                Branch_Real = 0;
                Branch_P_IF = 1'b0;
            end
        end
        else begin//BTB未命中
            Branch_Real = 0;
            Branch_P_IF = 1'b0;
            BTBhit_IF = 1'b0;
        end
        
        
        error_flush = 0;
        if((BranchE == 1'b1) && (BTBhit_EX == 1'b0)) begin  //增加新的BTB表项,BTB未命中且BranchE==1
            error_flush = 1;          //预测错误，清除前两段段间流水寄存器
            Branch_Real = 1;          //实际跳转
            BranchTarget_Real = brnpc_reg;//实际跳转地址
        end
        if(BTBhit_EX == 1'b1) begin //当前EX段是一条分支指令且早在BTB命中，根据当前BranchE更新BTB表
            if((Branch_P_EX == 1'b0) && (BranchE == 1'b1)) begin
                error_flush = 1;//预测错误，清除前两段段间流水寄存器
                Branch_Real = 1;
                BranchTarget_Real = brnpc_reg;
            end
            if((Branch_P_EX == 1'b1) && (BranchE == 1'b0)) begin
                error_flush = 1;//预测错误，清除前两段段间流水寄存器
                Branch_Real = 1;
                BranchTarget_Real = PCE + 32'h4;
            end
        end

    end


    always@(posedge clk) begin //维护BTB表
        if(BranchE && (BTBhit_EX == 1'b0)) begin  //增加新的BTB表项,BTB未命中且BranchE==1
            Branch_Target_Buffer[ PCE[BTBSIZE + 1 : 2] ][ 32 + BTBSIZE : 33 ] = PCE[ BTBSIZE + 1 : 2 ];
            Branch_Target_Buffer[ PCE[BTBSIZE + 1 : 2] ][ 32  : 1 ] = brnpc_reg;
            Branch_Target_Buffer[ PCE[BTBSIZE + 1 : 2] ][0] = 1;
        end
     end

     always@(posedge clk) begin
        if(BTBhit_EX == 1'b1) begin //当前EX段是一条分支指令且早在BTB命中，根据当前BranchE更新BTB表
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
    

    reg [ 33 + BTBSIZE : 0 ] Branch_Target_Buffer[ (1<<BTBSIZE) -  1 : 0 ];//PC的低12位直接映射  [1:0]是否跳转 [2-33]target，[34-45] PC
    
    always@(*) begin  //IF段使用BTB表
        if( PCF[ BTBSIZE + 1 : 2 ] == Branch_Target_Buffer[ PCF[BTBSIZE + 1 : 2] ][ 33 + BTBSIZE : 34 ] ) begin
            //BTB命中，说明它是分支指令，根据[0]的值选择NPC
            BTBhit_IF = 1'b1;
            if(Branch_Target_Buffer[ PCF[BTBSIZE + 1 : 2] ][1:0] == 2'b11 || Branch_Target_Buffer[ PCF[BTBSIZE + 1 : 2] ][1:0] == 2'b10) begin  
                //预测跳转，直接将这些信号传给NPC生成模块将分支地址作为下一个PC
                Branch_Real = 1;
                BranchTarget_Real = Branch_Target_Buffer[ PCF[BTBSIZE + 1 : 2] ][ 33 : 2 ];
                Branch_P_IF = 1;
            end
            else begin //预测不跳转
                Branch_Real = 0;
                Branch_P_IF = 1'b0;
            end
        end
        else begin//BTB未命中
            Branch_Real = 0;
            Branch_P_IF = 1'b0;
            BTBhit_IF = 1'b0;
        end
        
        error_flush = 0;
        if((BranchE == 1'b1) && (BTBhit_EX == 1'b0)) begin  //增加新的BTB表项,BTB未命中且BranchE==1
            error_flush = 1;          //预测错误，清除前两段段间流水寄存器
            Branch_Real = 1;          //实际跳转
            BranchTarget_Real = brnpc_reg;//实际跳转地址
        end
        if(BTBhit_EX == 1'b1) begin //当前EX段是一条分支指令且早在BTB命中，根据当前BranchE更新BTB表
            if((Branch_P_EX == 1'b0) && (BranchE == 1'b1)) begin
                error_flush = 1;//预测错误，清除前两段段间流水寄存器
                Branch_Real = 1;
                BranchTarget_Real = brnpc_reg;
            end
            if((Branch_P_EX == 1'b1) && (BranchE == 1'b0)) begin
                error_flush = 1;//预测错误，清除前两段段间流水寄存器
                Branch_Real = 1;
                BranchTarget_Real = PCE + 32'h4;
            end
        end
    end


    always@(posedge clk) begin //维护BHT表
        if(BranchE && (BTBhit_EX == 1'b0)) begin  //增加新的BTB表项,BTB未命中且BranchE==1
            Branch_Target_Buffer[ PCE[BTBSIZE + 1 : 2] ][ 33 + BTBSIZE : 34 ] = PCE[ BTBSIZE + 1 : 2 ];
            Branch_Target_Buffer[ PCE[BTBSIZE + 1 : 2] ][ 33  : 2 ] = brnpc_reg;
            Branch_Target_Buffer[ PCE[BTBSIZE + 1 : 2] ][1:0] = 2'b11;
        end
     end

     always@(posedge clk) begin
        if(BTBhit_EX == 1'b1) begin //当前EX段是一条分支指令且早在BTB命中，根据当前BranchE更新BTB表
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
    //维护预测错误次数
    always@(posedge clk) begin
        if(StallE) begin
            brancherror_count <= brancherror_count;
        end
        else begin
            if(BranchE && (BTBhit_EX == 1'b0))begin//增加新表项时预测错误
                brancherror_count <= brancherror_count + 1;
            end
            if(BTBhit_EX == 1'b1)begin
                if((Branch_P_EX == 1'b0) && (BranchE == 1'b1)) begin  //预测错误
                    brancherror_count <= brancherror_count + 1;
                end
                if((Branch_P_EX == 1'b1) && (BranchE == 1'b0)) begin
                    brancherror_count <= brancherror_count + 1;
                end
            end
        end
    end


endmodule