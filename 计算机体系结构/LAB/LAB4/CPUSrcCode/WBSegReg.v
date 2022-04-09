module WBSegReg(
    input wire clk,
    input wire rst,
    input wire en,
    output wire CacheMiss,
    //Data Memory Access
    input wire [31:0] A,
    input wire [31:0] WD,
    input wire [3:0] WE,
    output wire [31:0] RD,
    output reg [1:0] LoadedBytesSelect,
    // 
    input wire [31:0] ResultM,
    output reg [31:0] ResultW, 
    input wire [4:0] RdM,
    output reg [4:0] RdW,
    // 
    input wire [2:0] RegWriteM,
    output reg [2:0] RegWriteW,
    input wire MemToRegM,
    output reg MemToRegW
    );
    
    // if chip not enable, output instruction ram read result
    // else output last read result
    reg stall_or_clear = 1'b0;
    reg  [31:0] stall_or_clear_data = 0;
    wire [31:0] RD_raw;
    assign RD = stall_or_clear ? stall_or_clear_data : RD_raw;
        always @ (posedge clk or posedge rst) begin
            if(rst) begin
                stall_or_clear <= 1'b0;
                stall_or_clear_data <= 0;
            end else begin
                if(~en) begin
                    stall_or_clear <= 1'b1;
                    stall_or_clear_data <= RD;
                end else begin
                    stall_or_clear <= 1'b0;
                    stall_or_clear_data <= 0;
                end
            end
        end
    
    //
    always@(posedge clk or posedge rst)
        if(rst) begin
            LoadedBytesSelect<=2'b00;
            RegWriteW<=1'b0;
            MemToRegW<=1'b0;
            ResultW=32'b0;
            RdW=5'b0;
        end else if(en) begin
            LoadedBytesSelect<=A[1:0];
            RegWriteW<= RegWriteM;
            MemToRegW<= MemToRegM;
            ResultW=ResultM;
            RdW=RdM;               
        end



reg [31:0] hit_count = 0, miss_count = 0;  // 命中或缺失计数
reg [31:0] last_addr = 0;   // 
wire cache_rd_wr = (|WE) | MemToRegM;

reg cache_rd_wr_reg;
reg cachemiss_reg;
always@(posedge clk)begin
    cachemiss_reg <= CacheMiss;
    cache_rd_wr_reg <= cache_rd_wr;
end

always @ (posedge cache_rd_wr_reg or posedge rst) begin
    if(rst) begin
        hit_count  = 0;
        miss_count = 0;
    end 
    else ;
    if(cachemiss_reg == 1'b1)
       miss_count = miss_count+1;
    else ;
    if(cachemiss_reg == 1'b0)
       hit_count  = hit_count +1;
    else ;
end

cache #(
    .LINE_ADDR_LEN  ( 1             ),
    .SET_ADDR_LEN   ( 1             ),
    .TAG_ADDR_LEN   ( 10            ),
    .WAY_CNT        ( 1             )
) cache_test_instance (
    .clk            ( clk           ),
    .rst            ( rst           ),
    .miss           ( CacheMiss     ),
    .addr           ( A             ),
    .rd_req         ( MemToRegM     ),
    .rd_data        ( RD_raw        ),
    .wr_req         ( |WE           ),
    .wr_data        ( WD            )
);

endmodule