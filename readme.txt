System Verilog Module Extractor

Author: Brandon Vetter

How to run:
You will need python version 3.8 to run.  basic command:
python3 module_extractor.py <filename> [flags]

Description: 
takes verilog files, finds the modules and extracts information
from them.  It will output the modules in a component format, or
can returns the names of the modules.
Paramters:
filename - the file to extract module information from

-f, --output_file_location - location to output file to.  If left with
just the flag, output will go to the file where the module was extracted
from.  If file exists will append to file.

-q, --quiet_output - stops output from being printed from stdout.

-n, --print_names - prints only the names of the modules

-s, --specify_modules - only get the data from the specific modules listed

-na, --not_append - will overwrite a file instead of appending to it

examples:
lets say the verlog file is called test.sv

python3 module_extractor.py test.sv
This would print componets of the modules to stdout or the terminal

python3 module_extractor.py test.sv -f 
This would append the output to test.sv

python3 module_extractor.py -f output_file.sv -q
This would append output to output_file.sv, if it does not exist, will
append it.  The -q will not print the output to stdout.

python3 module_extractor.py -s modulea moduleb
Only the data of modulea and moduleb will be printed

python3 module_extractor.py -n
get all the names of the modules in the file

python3 module_extractor.py -f output_file.sv -na
Will overwite output_file.sv, will not append it.