`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company:
// Engineer:
//
// Create Date: 03/22/2024 08:24:13 PM
// Design Name:
// Module Name: top
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


module top #(
    parameter int ELEMENT_SIZE = 4,
    localparam CODON_MAX_LENGTH = 5,
    parameter ELEMENT_COUNT = 32,
    parameter SEGMENT_SIZE = ELEMENT_COUNT + (CODON_MAX_LENGTH - 1),
    parameter MAX_CODONS = 6,
    parameter MAX_COUNT = 16,
    parameter GENE_MEM_DEPTH = 256,
    parameter GENE_MEM_DEPTH_PADDED = GENE_MEM_DEPTH + (CODON_MAX_LENGTH - 1),
    parameter PROC_UNIT_COUNT = GENE_MEM_DEPTH / ELEMENT_COUNT,
    parameter GENE_MEM_COUNT = 2,
    parameter CODON_MEM_DEPTH = 32,
    parameter CODON_MEM_COUNT = 2
    )(
    input logic CLK,
    input logic [3:0] BTN,
    input logic [2:0] SW,
    output logic [3:0] LED
    );
