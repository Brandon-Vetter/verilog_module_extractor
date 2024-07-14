#!/usr/lib/python3

import os
import argparse

"""
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
"""
class ModuleDataValues:
    """
    Is a basic class to store data of the parameters.
    Is basicly just a struct with the added feature of
    being able to print its data as a string.
    """

    def __init__(self, data_type, data_width='1 bit', bus_width=''):
        self.data_type=data_type
        self.data_width=data_width
        self.bus_width=bus_width
        self.values = []
        self.name_overides = {}
    
    def output_data_string(self):
        output_str = ""
        bus_width_str = ""
        if self.bus_width != '':
            bus_width_str = f"bus {self.bus_width}"
        for value in self.values:
            try:
                value_input = self.name_overides[value]
            except KeyError:
                value_input = value
            output_str += f"\t.{value}({value_input}) // {self.data_type} {self.data_width} {bus_width_str}\n"
        return output_str

def main():
    """
    Is the main function ran.
    Runs the parser and runs the specified files.
    """

    parser = argparse.ArgumentParser(
        prog='Verilog module extractor',
        description="Searches for modules in a .sv file and outputs a copiable version of the components to use elsewhere in the project.",
        epilog='Made in request for Holonium.'
    )
    
    parser.add_argument('filename', 
                        help="file to parse")
    parser.add_argument('-f', '--output_file_location',
                        nargs='?',
                        const='',
                        default=None,
                        help="what file to save the output to.  If file exists will append to file. If no parameter is given will append file read from.")
    parser.add_argument('-q', '--quiet_stdout',
                        action='store_true',
                        help="hides output to stdout")
    parser.add_argument('-n', '--print_names',
                        action='store_true',
                        help="Prints out only the names of every module")
    parser.add_argument('-s', '--specify_modules',
                        nargs='*',
                        default=[],
                        help="Print out only these modules. Default is all.")
    parser.add_argument('-na', '--not_append',
                        action='store_true',
                        help="do not append a file being written to.")
    
    args = parser.parse_args()
    filename = args.filename
    get_data = None

    if args.print_names:
        get_data = get_module_names(filename)
    else:
        get_data = extract_modules(filename, args.specify_modules)

    if not args.quiet_stdout:
        for data in get_data:
            print(data)
    
    if args.output_file_location != None:
        output_file = args.output_file_location
        if output_file == '':
            output_file = args.filename
        
        IO_file = None
        if os.path.isfile(output_file) and not args.not_append:
            IO_file = open(output_file, 'a')
            IO_file.write("\n\n")
        else:
            IO_file = open(output_file, 'w')
        
        for data in get_data:
            IO_file.write(data)
        IO_file.close()



def parse_modules(file_name):
    """
    Parses out the modules of the file
    """
    file = open(file_name, 'r')
    current_line = 0
    modules = []
    while current_line != -1:
        current_line = read_line(file)
        if current_line == -1:
            break
        cleaned_line = current_line.replace('\n', ' ')
        parsed_line = parse_line(cleaned_line)
        if 'module' in parsed_line:
            ind = parsed_line.index('module')
            parsed_line = parsed_line[ind:]
            modules.append(parsed_line)

    file.close()
    return modules

def extract_modules(file_name, modules_to_extract = []):
    """
    Extracts out the paramters of the modules and returns the data
    in an array of strings consisting of a module that can be used.
    """
    modules = parse_modules(file_name)
    inputs = []
    outputs = []
    static_data = []
    return_data = []
    for module in modules:
        name = module[1]
        if name not in modules_to_extract and modules_to_extract != []:
            continue

        wire_inputs = 2

        # checks for if parameters exist and parse their data
        if "#" in module[2]:
            wire_inputs = 4
            static_parameters = module[3].replace('(', '').replace(')', '')
            static_input = parse_line(static_parameters, split_char=',', ignore_escape=True)
            data_value = False
            last_var_name = ''
            for var in static_input:
                local_paramter = parse_line(var, special_chars=['='])
                for param in local_paramter:
                    if 'parameter' in param.lower():
                        static_data.append(ModuleDataValues(param, data_width=''))
                    elif '=' in param:
                        data_value = True
                        continue
                    elif data_value:
                        data_value = False
                        static_data[-1].name_overides[last_var_name] = param
                    else:
                        last_var_name = param
                        static_data[-1].values.append(param)

        parameters = module[wire_inputs].replace('(', '').replace(')', '')
        parsed_parameters = parse_line(parameters, split_char=',', ignore_escape=True)
        ip = False
        op = False
        
        #parse module wire parameters
        for parameter in parsed_parameters:
            if 'input' in parameter or 'output' in parameter:
                data_value = parse_line(parameter)
                data_type = data_value[1]
                value = ModuleDataValues(data_type)
                if '[' in data_value[2]:
                    value.data_width = data_value[2]
                    value.values.append(data_value[3])
                else:
                    value.values.append(data_value[2])
                if 'input' in data_value[0]:
                    inputs.append(value)
                    ip = True
                    op = False
                if 'output' in data_value[0]:
                    outputs.append(value)
                    ip = False
                    op = True
                try:
                    value.bus_width = data_value[4]
                except IndexError:
                    pass
            else:
                if ip:
                    inputs[-1].values.append(parameter.strip())
                elif op:
                    outputs[-1].values.append(parameter.strip())
        
        # add the names for the sections
        print_str = name
        if static_data != []:
            print_str += " #(\n"
            print_str += "// PARAMETERS\n"
            for data in static_data:
                print_str += data.output_data_string()
            print_str += ")"
        print_str += f" {name}_inst "
        print_str += "(\n"
        
        print_str += "// INPUTS\n"
        for input in inputs:
            print_str += input.output_data_string()
        print_str += "// OUTPUTS\n"
        for output in outputs:
            print_str += output.output_data_string()
        
        # add to list
        return_data.append(print_str + ");\n")
    
    return return_data
                
            

# need to write parser

def read_line(file):
    """
    Reads the lines of the file and removes the comments.
    splits the lines by ";".
    """
    line = ''
    single_line_comment = False
    multi_line_comment = True
    last_char = ''
    while True:
        char = file.read(1)
        if not char:
            return -1
        if char == ';':
            break
        if last_char + char == '//':
            single_line_comment = True
            line = line[:-1]
        if single_line_comment and last_char + char == '\n':
            single_line_comment = False
        if last_char + char == '/*':
            line = line[:-1]
            multi_line_comment = True
        if multi_line_comment and last_char + char == '*/':
            multi_line_comment = False
        if not (single_line_comment and multi_line_comment):
            line += char
            last_char = char
    return line.strip()

def get_module_names(file_name):
    """
    Returns the names of the modules of the file
    """
    modules = parse_modules(file_name)
    names = []
    for module in modules:
        names.append(module[1])
    
    return names

def parse_line(line, split_char = ' ', special_chars = [], ignore_escape=False):
    """
    Returns a parsed array from a line.
    Used to parse the module lines."""
    term_list = []
    current_term = ''
    escape_term = ''
    nested_type = ''
    special_chars_str = ''
    nested_count = 0
    include_spaces = False
    escape_table = {
        '[' : ']',
        '{' : '}',
        '(' : ')'
    }
    if ignore_escape:
        escape_table = {}
    

    for char in line:
        # if (), [], {} found, include spaces
        if char in escape_table.keys() and not ignore_escape:
            if nested_type == '':
                nested_type = char
                include_spaces = True
                escape_term = escape_table[char]
                if current_term != '':
                    term_list.append(current_term)
                    current_term = char
                    continue
            elif nested_type == char:
                nested_count += 1

        # include spaces, unless end of (), [], {}
        if include_spaces:
            current_term += char
            if char == escape_term and nested_count == 0:
                include_spaces = False
                escape_term = ''
                nested_type = ''
                if current_term != '':
                    term_list.append(current_term)
                    current_term = ''
            elif char == escape_term:
                nested_count -= 1
            continue
        if char != split_char:
            current_term += char
            if special_chars != []:
                for spe_char in special_chars:
                    if current_term[-len(spe_char):0] == spe_char:
                        
                        term_list.append(current_term[-len(spe_char):0]) 
                        term_list.append(spe_char)
                        current_term = ''

        elif current_term != '':
            term_list.append(current_term)
            current_term = ''
        last_char = char

    if current_term != '':
        term_list.append(current_term)
    return term_list

def get_value(line, value, offset = 1):
    index = line.index(value)
    return line[value + offset]

if __name__ == '__main__':
    main()