gene_comparitor gene_comparitor_inst (
// INPUTS
	.sw(sw) // logic [2:0] 
	.btn(btn) // logic [0:0] 
	.clk(clk) // logic 1 bit 
// OUTPUTS
	.led(led) // logic [3:0] 
);

fsm_main_phase fsm_main_phase_inst (
// INPUTS
	.sw(sw) // logic [2:0] 
	.btn(btn) // logic [0:0] 
	.clk(clk) // logic 1 bit 
	.rst(rst) // logic 1 bit 
	.clk(clk) // logic 1 bit 
	.eofg(eofg) // logic 1 bit 
	.done_pre(done_pre) // logic 1 bit 
	.eql(eql) // logic [5:0] 
// OUTPUTS
	.led(led) // logic [3:0] 
	.inc(inc) // logic [5:0] 
	.done(done) // logic 1 bit 
	.sft_g(sft_g) // logic 1 bit 
	.inc_g_addr(inc_g_addr) // logic 1 bit 
	.inc_c_addr(inc_c_addr) // logic 1 bit 
	.cls_c_addr(cls_c_addr) // logic 1 bit 
);

fsm_pre fsm_pre_inst (
// INPUTS
	.sw(sw) // logic [2:0] 
	.btn(btn) // logic [0:0] 
	.clk(clk) // logic 1 bit 
	.rst(rst) // logic 1 bit 
	.clk(clk) // logic 1 bit 
	.eofg(eofg) // logic 1 bit 
	.done_pre(done_pre) // logic 1 bit 
	.eql(eql) // logic [5:0] 
	.clk(clk) // logic 1 bit 
	.rst(rst) // logic 1 bit 
	.start(start) // logic 1 bit 
	.eolc(eolc) // logic [5:0] 
	.eofc(eofc) // logic [5:0] 
// OUTPUTS
	.led(led) // logic [3:0] 
	.inc(inc) // logic [5:0] 
	.done(done) // logic 1 bit 
	.sft_g(sft_g) // logic 1 bit 
	.inc_g_addr(inc_g_addr) // logic 1 bit 
	.inc_c_addr(inc_c_addr) // logic 1 bit 
	.cls_c_addr(cls_c_addr) // logic 1 bit 
	.done_pre(done_pre) // logic 1 bit 
	.inc_codon_addr(inc_codon_addr) // logic 1 bit 
	.sft(sft) // logic [5:0] 
);

bubble_sort #(
// PARAMETERS
	.size(4) // parameter  
	.arr_size(3) // parameter  
) bubble_sort_inst (
// INPUTS
	.sw(sw) // logic [2:0] 
	.btn(btn) // logic [0:0] 
	.clk(clk) // logic 1 bit 
	.rst(rst) // logic 1 bit 
	.clk(clk) // logic 1 bit 
	.eofg(eofg) // logic 1 bit 
	.done_pre(done_pre) // logic 1 bit 
	.eql(eql) // logic [5:0] 
	.clk(clk) // logic 1 bit 
	.rst(rst) // logic 1 bit 
	.start(start) // logic 1 bit 
	.eolc(eolc) // logic [5:0] 
	.eofc(eofc) // logic [5:0] 
	.clk(clk) // logic 1 bit 
	.rst(rst) // logic 1 bit 
	.en(en) // logic 1 bit 
	.din(din) // logic [size - 1:0] 
// OUTPUTS
	.led(led) // logic [3:0] 
	.inc(inc) // logic [5:0] 
	.done(done) // logic 1 bit 
	.sft_g(sft_g) // logic 1 bit 
	.inc_g_addr(inc_g_addr) // logic 1 bit 
	.inc_c_addr(inc_c_addr) // logic 1 bit 
	.cls_c_addr(cls_c_addr) // logic 1 bit 
	.done_pre(done_pre) // logic 1 bit 
	.inc_codon_addr(inc_codon_addr) // logic 1 bit 
	.sft(sft) // logic [5:0] 
	.dout(dout) // logic [size - 1:0] 
	.raddr(raddr) // logic [arr_size - 1:0] 
	.waddr(waddr) // logic [arr_size - 1:0] 
	.we(we) // logic 1 bit 
	.done(done) // logic 1 bit 
);

