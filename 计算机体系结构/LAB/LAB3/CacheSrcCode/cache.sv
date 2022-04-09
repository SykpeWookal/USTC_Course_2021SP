module cache #(
    parameter  LINE_ADDR_LEN = 3, // line内地址长度，决定了每个line具有2^3个word
    parameter  SET_ADDR_LEN  = 1, // 组地址长度，决定了一共有2^3=8组
    parameter  TAG_ADDR_LEN  = 8, // tag长度
    parameter  WAY_CNT       = 4  // 组相连度，决定了每组中有多少路line，这里是直接映射型cache，因此该参数没用到
)(
    input  clk, rst,
    output miss,               // 对CPU发出的miss信号
    input  [31:0] addr,        // 读写请求地址
    input  rd_req,             // 读请求信号
    output reg [31:0] rd_data, // 读出的数据，一次读一个word
    input  wr_req,             // 写请求信号
    input  [31:0] wr_data      // 要写入的数据，一次写一个word
);

localparam MEM_ADDR_LEN    = TAG_ADDR_LEN + SET_ADDR_LEN ; // 计算主存地址长度 MEM_ADDR_LEN，主存大小=2^MEM_ADDR_LEN个line
localparam UNUSED_ADDR_LEN = 32 - TAG_ADDR_LEN - SET_ADDR_LEN - LINE_ADDR_LEN - 2 ;       // 计算未使用的地址的长度

localparam LINE_SIZE       = 1 << LINE_ADDR_LEN  ;         // 计算 line 中 word 的数量，即 2^LINE_ADDR_LEN 个word 每 line
localparam SET_SIZE        = 1 << SET_ADDR_LEN   ;         // 计算一共有多少组，即 2^SET_ADDR_LEN 个组
localparam WAY_SIZE        = 1 << WAY_CNT   ; 

reg [            31:0] cache_mem    [SET_SIZE][WAY_SIZE][LINE_SIZE]; // SET_SIZE个line，每个line有LINE_SIZE个word
reg [TAG_ADDR_LEN-1:0] cache_tags   [SET_SIZE][WAY_SIZE];            // SET_SIZE个TAG
reg                    valid        [SET_SIZE][WAY_SIZE];            // SET_SIZE个valid(有效位)
reg                    dirty        [SET_SIZE][WAY_SIZE];            // SET_SIZE个dirty(脏位)

wire [              2-1:0]   word_addr;                   // 将输入地址addr拆分成这5个部分
wire [  LINE_ADDR_LEN-1:0]   line_addr;
wire [   SET_ADDR_LEN-1:0]    set_addr;
wire [   TAG_ADDR_LEN-1:0]    tag_addr;
wire [UNUSED_ADDR_LEN-1:0] unused_addr;

enum  {IDLE, SWAP_OUT, SWAP_IN, SWAP_IN_OK} cache_stat;    // cache 状态机的状态定义
                                                           // IDLE代表就绪，SWAP_OUT代表正在换出，SWAP_IN代表正在换入，SWAP_IN_OK代表换入后进行一周期的写入cache操作。

reg  [   SET_ADDR_LEN-1:0] mem_rd_set_addr = 0;
reg  [   TAG_ADDR_LEN-1:0] mem_rd_tag_addr = 0;
wire [   MEM_ADDR_LEN-1:0] mem_rd_addr = {mem_rd_tag_addr, mem_rd_set_addr};
reg  [   MEM_ADDR_LEN-1:0] mem_wr_addr = 0;

reg  [31:0] mem_wr_line [LINE_SIZE];
wire [31:0] mem_rd_line [LINE_SIZE];

wire mem_gnt;      // 主存响应读写的握手信号

assign {unused_addr, tag_addr, set_addr, line_addr, word_addr} = addr;  // 拆分 32bit ADDR

reg cache_hit = 1'b0; 
integer way_hit = 0;
always @ (*) begin              // 判断 输入的address 是否在 cache 中命中
    cache_hit = 1'b0;
    for(integer i=0; i<WAY_SIZE; i++) begin
        if( valid[set_addr][i] && cache_tags[set_addr][i] == tag_addr ) begin
            cache_hit = 1'b1;
            way_hit = i;
        end
    end
end


//`define FIFO
`define LRU

reg[WAY_CNT-1:0] wayout_choice;//换出way选择
/*置换算法实现*/
`ifdef FIFO         
reg [31:0] FIFO_Choice [SET_SIZE]; //只需要对于每一个set，分别用一个变量记录该set应该换出的way号即可
always@(*) begin
    if (rst) begin
        wayout_choice = 0;
        for(integer i = 0; i < SET_SIZE; i++) begin
            FIFO_Choice[i] = 0;
        end
    end 
    else begin
        ;
    end
    if(cache_stat == IDLE)begin
        wayout_choice = FIFO_Choice[set_addr]; //选路时只需要在需要换出时，根据不同的set编号，选择相应的way即可 
    end
    if(cache_stat == SWAP_IN_OK)
        FIFO_Choice[set_addr] = (FIFO_Choice[set_addr] + 1) % WAY_SIZE;  //选路完成后，需要对每一组的换出变量进行更新
                                  //这样实现的原因是，FIFO策略是先进先出，实际上就是一个循环队列，按照顺序进行更新即可。
    else ;
end
`endif


`ifdef LRU  //LRU策略换出最长时间未被使用的块
reg [WAY_CNT - 1 : 0] set_way_select[SET_SIZE][WAY_SIZE];
    //对每一个set，例如set_way_select[1][1~4] = {4 2 3 1}代表4号way刚被使用过，1号way最久未使用
reg [WAY_CNT - 1 : 0] set_way_select_temp;     //循环右移后最后插入[SET_SIZE][0]号的交换temp寄存器
integer exchange_flag;//用于记录开始每一元素右移一位的标志信号
always@(*) begin
    if (rst) begin
        for (integer i=0; i < SET_SIZE; i++) begin
            for (integer k=0; k < WAY_SIZE; k++) begin
                set_way_select[i][k] = k;
            end
        end
    end
    else ;
    if(cache_stat == IDLE && ~cache_hit)begin
        wayout_choice = set_way_select[set_addr][WAY_SIZE - 1];//换出选择
    end
    else begin
        ;
    end
    
   if(cache_stat == IDLE && cache_hit && (wr_req || rd_req))begin
        exchange_flag = 0;
        for(integer i = WAY_SIZE; i >= 1; i--)begin
            if(exchange_flag)begin //不变部分
                set_way_select[set_addr][i] = set_way_select[set_addr][i-1];        
            end
            else if(set_way_select[set_addr][i-1] == way_hit)begin//开始每一位右移一次
                exchange_flag = 1;
            end
        end
        set_way_select[set_addr][0] = way_hit;
    end
    
    if(cache_stat == SWAP_IN_OK) begin
        set_way_select_temp = set_way_select[set_addr][WAY_SIZE-1];
        for (integer i = WAY_SIZE; i > 0; i--) begin
            set_way_select[set_addr][i] = set_way_select[set_addr][i-1];
        end
        set_way_select[set_addr][0] = set_way_select_temp;
    end
end
`endif




always @ (posedge clk or posedge rst) begin     // ?? cache ???
    if(rst) begin
        cache_stat <= IDLE;
        for(integer i = 0; i < SET_SIZE; i++) begin
            for (integer j=0; j<WAY_CNT; j++) begin
                dirty[i][j] = 1'b0;
                valid[i][j] = 1'b0; 
            end
        end
        for(integer k = 0; k < LINE_SIZE; k++)
            mem_wr_line[k] <= 0;
        mem_wr_addr <= 0;
        {mem_rd_tag_addr, mem_rd_set_addr} <= 0;
        rd_data <= 0;
    end else begin
        case(cache_stat)
        IDLE:       begin
                        if(cache_hit) begin
                            if(rd_req) begin    // 如果cache命中，并且是读请求，
                                rd_data <= cache_mem[set_addr][way_hit][line_addr];   //则直接从cache中取出要读的数据
                            end else if(wr_req) begin // 如果cache命中，并且是写请求，
                                cache_mem[set_addr][way_hit][line_addr] <= wr_data;   // 则直接向cache中写入数据
                                dirty[set_addr][way_hit] <= 1'b1;                     // 写数据的同时置脏位
                            end 
                        end else begin
                            if(wr_req | rd_req) begin   // 如果 cache 未命中，并且有读写请求，则需要进行换入
                                if(valid[set_addr][wayout_choice] & dirty[set_addr][wayout_choice]) begin    // 如果 要换入的cache line 本来有效，且脏，则需要先将它换出
                                    cache_stat  <= SWAP_OUT;
                                    mem_wr_addr <= {cache_tags[set_addr][wayout_choice], set_addr};
                                    mem_wr_line <= cache_mem[set_addr][wayout_choice];
                                end else begin                                   // 反之，不需要换出，直接换入
                                    cache_stat  <= SWAP_IN;
                                end
                                {mem_rd_tag_addr, mem_rd_set_addr} <= {tag_addr, set_addr};
                            end
                        end
                    end
        SWAP_OUT:   begin
                        if(mem_gnt) begin           // 如果主存握手信号有效，说明换出成功，跳到下一状态
                            cache_stat <= SWAP_IN;
                        end
                    end
        SWAP_IN:    begin
                        if(mem_gnt) begin           // 如果主存握手信号有效，说明换入成功，跳到下一状态
                            cache_stat <= SWAP_IN_OK;
                        end
                    end
        SWAP_IN_OK: begin           // 上一个周期换入成功，这周期将主存读出的line写入cache，并更新tag，置高valid，置低dirty
                        for(integer i=0; i<LINE_SIZE; i++)  
                            cache_mem[mem_rd_set_addr][wayout_choice][i] <= mem_rd_line[i];
                        cache_tags[mem_rd_set_addr][wayout_choice] <= mem_rd_tag_addr;
                        valid     [mem_rd_set_addr][wayout_choice] <= 1'b1;
                        dirty     [mem_rd_set_addr][wayout_choice] <= 1'b0;
                        cache_stat <= IDLE;        // 回到就绪状态
                    end
        endcase
    end
end

wire mem_rd_req = (cache_stat == SWAP_IN );
wire mem_wr_req = (cache_stat == SWAP_OUT);
wire [   MEM_ADDR_LEN-1 :0] mem_addr = mem_rd_req ? mem_rd_addr : ( mem_wr_req ? mem_wr_addr : 0);

assign miss = (rd_req | wr_req) & ~(cache_hit && cache_stat==IDLE) ;     // 当 有读写请求时，如果cache不处于就绪(IDLE)状态，或者未命中，则miss=1

main_mem #(     // 主存，每次读写以line 为单位
    .LINE_ADDR_LEN  ( LINE_ADDR_LEN          ),
    .ADDR_LEN       ( MEM_ADDR_LEN           )
) main_mem_instance (
    .clk            ( clk                    ),
    .rst            ( rst                    ),
    .gnt            ( mem_gnt                ),
    .addr           ( mem_addr               ),
    .rd_req         ( mem_rd_req             ),
    .rd_line        ( mem_rd_line            ),
    .wr_req         ( mem_wr_req             ),
    .wr_line        ( mem_wr_line            )
);


endmodule