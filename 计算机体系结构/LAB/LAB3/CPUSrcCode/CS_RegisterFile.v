`timescale 1ns / 1ps

`include "Parameters.v"

module CS_RegisterFile(
    input wire clk,
    input wire rst,
    input wire [11:0] CSR_Addr,
    input wire [31:0] RegFileData,
    input wire [31:0] rsdata,
    input wire [2:0] CSRType,
    
    output wire [31:0] CSRout
);

    reg [31:0] CSReg[4095:0];
    integer i;
    reg [31:0] CSRout_reg;
    initial CSRout_reg = 0;
    
    always@(negedge clk or posedge rst) begin
        if(rst) begin
            for(i=0;i<4095;i=i+1) begin
                CSReg[i][31:0]<=32'b0;
            end
        end
        else begin
            case(CSRType)
              `CSRRW_Type: begin
                    CSRout_reg = CSReg[CSR_Addr];
                    CSReg[CSR_Addr] = RegFileData; /*非阻塞式赋值，CSRData_reg得到的是CSR更新前的数据*/
                  end
              `CSRRS_Type: begin
                    CSRout_reg = CSReg[CSR_Addr];
                    CSReg[CSR_Addr] = CSReg[CSR_Addr] | RegFileData;
                  end
              `CSRRC_Type: begin
                    CSRout_reg = CSReg[CSR_Addr];
                    CSReg[CSR_Addr] = CSReg[CSR_Addr] & (~RegFileData);
                  end
               `CSRRWI_Type: begin
                    CSRout_reg = CSReg[CSR_Addr];
                    CSReg[CSR_Addr] = rsdata;
                  end
               `CSRRSI_Type: begin
                    CSRout_reg = CSReg[CSR_Addr];
                    CSReg[CSR_Addr] = CSReg[CSR_Addr] | rsdata;
                  end
               `CSRRCI_Type: begin
                    CSRout_reg = CSReg[CSR_Addr];
                    CSReg[CSR_Addr] = CSReg[CSR_Addr] & (~rsdata);
                  end
               `NOTCSR_Type:  begin
                    CSRout_reg = 32'b0;
                  end
               default: CSRout_reg = 32'b0;
             endcase
        end
    end

    assign CSRout = CSRout_reg;
    
endmodule