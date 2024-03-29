
module mem #(                   // 
    parameter  ADDR_LEN  = 11   // 
) (
    input  clk, rst,
    input  [ADDR_LEN-1:0] addr, // memory address
    output reg [31:0] rd_data,  // data read out
    input  wr_req,
    input  [31:0] wr_data       // data write in
);
localparam MEM_SIZE = 1<<ADDR_LEN;
reg [31:0] ram_cell [MEM_SIZE];

always @ (posedge clk or posedge rst)
    if(rst)
        rd_data <= 0;
    else
        rd_data <= ram_cell[addr];

always @ (posedge clk)
    if(wr_req) 
        ram_cell[addr] <= wr_data;

initial begin
    ram_cell[       0] = 32'h00000001;
    ram_cell[       1] = 32'h00000007;
    ram_cell[       2] = 32'h00000005;
    ram_cell[       3] = 32'h00000004;
    ram_cell[       4] = 32'h00000003;
    ram_cell[       5] = 32'h00000000;
    ram_cell[       6] = 32'h00000002;
    ram_cell[       7] = 32'h00000006;
end

endmodule

