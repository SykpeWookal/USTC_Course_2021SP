`timescale 1ns / 1ps

`include "Parameters.v"

module CS_EXE(
    input wire [31:0] CSRData,
    input wire [31:0] rsdata,
    input wire [2:0] CSRType,
    output wire [31:0] CSRResult
);

    reg [31:0] out;
    initial out = 0;
    
    always@(*) begin
        if(CSRType == `CSRRW_Type) begin
            out = CSRData;        
        end
        else if(CSRType == `CSRRS_Type) begin
            out = CSRData | rsdata;
        end
        else if(CSRType == `CSRRC_Type) begin
            out = CSRData & (~rsdata);
        end
        else if(CSRType == `CSRRWI_Type) begin
            out = CSRData;        
        end
        else if(CSRType == `CSRRSI_Type) begin
            out = CSRData | rsdata;
        end
        else if(CSRType == `CSRRCI_Type) begin
            out = CSRData & (~rsdata);
        end
    end
    
    assign CSRResult = out ;
    
endmodule