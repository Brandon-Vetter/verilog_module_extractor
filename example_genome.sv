module gene_comparitor (
    input logic [2:0] sw,
    input logic [0:0] btn,
    output logic [3:0] led,
    input logic clk
);
    logic rst, eofg, start, sft_g, done;
    logic [5:0] eql, eolc, eofc;
    logic [7:0] g_addr;
    logic [4:0] c_addr;
    logic [3:0] count_regs [5:0];
    logic [5:0] sft;
    syncronizer_1_bit syn1 (
    .clk(clk),
    .din(btn),
    .dout(rst)
    );
    assign start = ~rst;
    fsm_main fsm (.*);
    datapath_main datapath (.*);
    always_comb
    begin
        led = 4'b0000;
        case(sw)
            3'h1 : led = count_regs[0];
            3'h2 : led = count_regs[1];
            3'h3 : led = count_regs[2];
            3'h4 : led = count_regs[3];
            3'h5 : led = count_regs[4];
            3'h6 : led = count_regs[5];
            default : led = {3'h0, done};
        endcase
    end
endmodule
\end{lstlisting}
\subsection{fsm\_main}
\begin{lstlisting}[language = Verilog]
`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 03/23/2024 03:09:35 AM
// Design Name: 
// Module Name: fsm_main
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////


module fsm_main(
    input logic rst, clk, eofg, start,
    input logic [5:0] eql, eolc, eofc,
    output logic [7:0] g_addr,
    output logic [4:0] c_addr,
    output logic [3:0] count_regs [5:0],
    output logic [5:0] sft,
    output logic done, sft_g
    );
    logic inc_g_addr, inc_c_addra, inc_c_addrb, inc_c_addr, cls_c_addr, done_pre;
    logic [5:0] inc;
    logic [3:0] cregs [5:0]; 
    logic [7:0] gene_address = 7'b0000000;
    logic [4:0] codon_address = 5'b0000;
    fsm_pre fsm_pre_state (
    .start(start),
    .eolc(eolc),
    .eofc(eofc),
    .clk(clk),
    .rst(rst),
    .inc_codon_addr(inc_c_addra),
    .sft(sft),
    .done_pre(done_pre)
    );
    fsm_main_phase main_phase(
    .rst(rst),
    .clk(clk),
    .eofg(eofg),
    .eql(eql),
    .inc(inc),
    .sft_g(sft_g),
    .done_pre(done_pre),
    .inc_g_addr(inc_g_addr),
    .inc_c_addr(inc_c_addrb),
    .cls_c_addr(cls_c_addr),
    .done(done)
    );
    always_ff @(posedge clk)
    begin
        if(rst)
        begin
            integer i;
            for(i = 0; i < 6; i = i+1)
            begin
                cregs[i] <= 4'b0000;
            end
            gene_address <= 7'b0000000;
            codon_address <= 5'b00000;
        end
        if(inc[0]) cregs[0] <= cregs[0] + 1;
        if(inc[1]) cregs[1] <= cregs[1] + 1;
        if(inc[2]) cregs[2] <= cregs[2] + 1;
        if(inc[3]) cregs[3] <= cregs[3] + 1;
        if(inc[4]) cregs[4] <= cregs[4] + 1;
        if(inc[5]) cregs[5] <= cregs[5] + 1;
        if(inc_g_addr) gene_address <= gene_address + 1;
        if(inc_c_addr) codon_address <= codon_address + 1;
        if(cls_c_addr) codon_address <= 5'b0000;
    end
    assign inc_c_addr = done_pre ? inc_c_addrb : inc_c_addra;
    assign c_addr = codon_address;
    assign g_addr = gene_address;
    assign count_regs = cregs;
endmodule
module fsm_main_phase(
    input logic rst, clk, eofg, done_pre,
    input logic [5:0] eql,
    output logic [5:0] inc,
    output logic done, sft_g, inc_g_addr, inc_c_addr, cls_c_addr
    );
    typedef enum logic [1:0] {idle, sft_gene, done_st} statetype;
    statetype state = idle;
    always_ff  @(posedge clk)
    begin
        if(rst) state <= idle;
        else
        begin
            case(state)
                idle : if(done_pre) state <= sft_gene;
                sft_gene : if(eofg) state <= done_st;
            endcase
        end
    end
    always_comb
    begin
        inc = 5'b00000;
        done = 0; sft_g = 0; inc_g_addr = 0; inc_c_addr = 0; cls_c_addr = 0;
        case(state)
            idle : begin
                if(done_pre) 
                begin
                    cls_c_addr = 1;
                    inc_g_addr = 1;
                    sft_g = 1;
                end
                end
            sft_gene: begin
                inc_g_addr = 1;
                sft_g = 1;
                if(eql[0]) inc[0] = 1;
                if(eql[1]) inc[1] = 1;
                if(eql[2]) inc[2] = 1;
                if(eql[3]) inc[3] = 1;
                if(eql[4]) inc[4] = 1;
                if(eql[5]) inc[5] = 1;
                end
            done_st : done = 1;
        endcase
    end
endmodule

module fsm_pre
(
    input logic clk, rst, start,
    input logic [5:0] eolc, eofc,
    output logic done_pre,
    output logic inc_codon_addr,
    output logic [5:0] sft
);
typedef enum logic [3:0] {idle, load_c_0, load_c_1, load_c_2, load_c_3, load_c_4, load_c_5, done} statetype;
statetype state = idle;

always_ff @(posedge clk)
begin
    if (rst)
        state <= idle;
    else
    begin
    case(state)
        idle : if(start) state <= load_c_0;
        load_c_0 : begin 
            if(eolc[0]) state <= load_c_1;
            else if (eofc[0]) state <= done;
            end
        load_c_1 : begin 
            if(eolc[1]) state <= load_c_2;
            else if (eofc[1]) state <= done;
            end
        load_c_2 : begin 
            if(eolc[2]) state <= load_c_3;
            else if (eofc[2]) state <= done;
            end
        load_c_3 : begin 
            if(eolc[3]) state <= load_c_4;
            else if (eofc[3]) state <= done;
            end
        load_c_4 : begin 
            if(eolc[4]) state <= load_c_5;
            else if (eofc[4]) state <= done;
            end
        load_c_5 : begin 
            if(eolc[5] | eofc[5]) state <= done;
            end
    endcase
    end
end
    always_comb
    begin
        inc_codon_addr = 0;
        sft = 5'b00000;
        done_pre = 0;
        case(state)
            idle : if(start) begin
                sft[0] = 1;
                inc_codon_addr = 1;
                end
            load_c_0: begin
                inc_codon_addr = 1;
                if(eolc[0]) sft[1] = 1;
                else sft[0] = 1;
                end
            load_c_1: begin
                inc_codon_addr = 1;
                if(eolc[1]) sft[2] = 1;
                else sft[1] = 1;
                end
            load_c_2: begin
                inc_codon_addr = 1;
                if(eolc[2]) sft[3] = 1;
                else sft[2] = 1;
                end
            load_c_3: begin
                inc_codon_addr = 1;
                if(eolc[3]) sft[4] = 1;
                else sft[3] = 1;
                end
            load_c_4: begin
                inc_codon_addr = 1;
                if(eolc[4]) sft[5] = 1;
                else sft[4] = 1;
                end
            load_c_5: begin
                inc_codon_addr = 1;
                if(~eolc[5]) sft[5] = 1;
                end
            done : done_pre = 1;
        endcase
    end
endmodule