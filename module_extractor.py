import os

class ModuleDataValues:
    def __init__(self, data_type, data_width='1 bit', bus_width=''):
        self.data_type=data_type
        self.data_width=data_width
        self.bus_width=bus_width
        self.values = []
    
    def output_data_string(self):
        output_str = ""
        for value in self.values:
            output_str += f"\t.{value.upper()}({value.upper()}) // {self.data_width} \n"
        return output_str

def main():
    file = open('example_genome.sv', 'r')
    current_line = 0
    print(os.getcwd())
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
    inputs = []
    outputs = []
    for module in modules:
        name = module[1]
        parameters = module[2].replace('(', '').replace(')', '')
        parsed_parameters = parse_line(parameters, split_char=',', ignore_escape=True)
        ip = False
        op = False
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
            else:
                if ip:
                    inputs[-1].values.append(parameter.strip())
                elif op:
                    outputs[-1].values.append(parameter.strip())
        
        print_str = name
        print_str += f" {name}_inst (\n"
        print_str += "// INPUTS\n"
        for input in inputs:
            print_str += input.output_data_string()
        print_str += "// OUTPUTS\n"
        for output in outputs:
            print_str += output.output_data_string()
        print(print_str + ');')
        
                
            

# need to write parser

def read_line(file):
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

def parse_line(line, split_char = ' ', special_chars = [], ignore_escape=False):
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


        if include_spaces:
            current_term += char
            if char == escape_term and nested_count == 0:
                include_spaces = False
                escape_term = ''
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
   # print(parse_line('    input logic [0:0] btn,'))