bubble_sort #(
// PARAMETERS
	.size(4) // parameter  
	.arr_size(3) // parameter  
) bubble_sort_inst (
// INPUTS
	.clk(clk) // logic 1 bit 
	.rst(rst) // logic 1 bit 
	.en(en) // logic 1 bit 
	.din(din) // logic [size - 1:0] 
// OUTPUTS
	.dout(dout) // logic [size - 1:0] 
	.raddr(raddr) // logic [arr_size - 1:0] 
	.waddr(waddr) // logic [arr_size - 1:0] 
	.we(we) // logic 1 bit 
	.done(done) // logic 1 bit 
);
