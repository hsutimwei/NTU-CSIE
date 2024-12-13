module dcache_sram
(
    clk_i,
    rst_i,
    addr_i,
    tag_i,
    data_i,
    enable_i,
    write_i,
    tag_o,
    data_o,
    hit_o
);

// I/O Interface from/to controller
input              clk_i;
input              rst_i;
input    [3:0]     addr_i;
input    [24:0]    tag_i;
input    [255:0]   data_i;
input              enable_i;
input              write_i;

output reg   [24:0]    tag_o;
output reg   [255:0]   data_o;
output                 hit_o;

wire               cache1;

// Memory
reg      [24:0]    tag [0:15][0:1];    
reg      [255:0]   data[0:15][0:1];
reg                replace[0:15];
integer            i, j;


// Write Data      
// 1. Write hit
// 2. Read miss: Read from memory
always@(posedge clk_i or posedge rst_i) begin
    if (rst_i) begin
        for (i=0;i<16;i=i+1) begin
            for (j=0;j<2;j=j+1) begin
                tag[i][j] <= 25'b0;
                data[i][j] <= 256'b0;
                replace[i] <= 1'b0;
            end
        end
    end
    if (enable_i && write_i) begin
        // TODO: Handle your write of 2-way associative cache + LRU here
        if(enable_i && (tag_i[22:0] == tag[addr_i][0][22:0]) && tag[addr_i][0][24]) begin
            data[addr_i][0] <= data_i;
            tag[addr_i][0][23] <= 1'b1;
            replace[addr_i] <= 1'b1;
        end
        else if (enable_i && (tag_i[22:0] == tag[addr_i][1][22:0]) && tag[addr_i][1][24]) begin
            data[addr_i][1] <= data_i;
            tag[addr_i][1][23] <= 1'b1;
            replace[addr_i] <= 1'b0;
        end
        else if(replace[addr_i]) begin
            tag[addr_i][1] <= tag_i;
            data[addr_i][1] <= data_i;
            replace[addr_i] <= 1'b0;
        end
        else begin
            tag[addr_i][0] <= tag_i;
            data[addr_i][0] <= data_i;
            replace[addr_i] <= 1'b1;
        end
    end
end

// Read Data      
// TODO: tag_o=? data_o=? hit_o=?
assign	hit_o =  (enable_i && (tag_i[22:0] == tag[addr_i][0][22:0]) && tag[addr_i][0][24])? 1'b1 :
                 (enable_i && (tag_i[22:0] == tag[addr_i][1][22:0]) && tag[addr_i][1][24])? 1'b1 :
                  1'b0;
always@(*) begin
    if ((tag_i[22:0] == tag[addr_i][0][22:0]) && enable_i && tag[addr_i][0][24]) begin
       tag_o <= tag[addr_i][0];
       data_o <= data[addr_i][0];
       replace[addr_i] <= 1'b1;
    end
    else if((tag_i == tag[addr_i][1]) && enable_i && tag[addr_i][1][24]) begin
       tag_o <= tag[addr_i][1];
       data_o <= data[addr_i][1];
       replace[addr_i] <= 1'b0;
    end
    else begin
       tag_o <= 25'b0;
       data_o <= 256'b0;
    end
end
endmodule
