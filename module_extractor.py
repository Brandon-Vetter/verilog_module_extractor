import os
def main():
    pass

def extract_file(filename):
    system_verilog_file = open(filename, 'r')
    in_instantation = False
    modules_dictonary = {}
    current_name = ''
    for line in system_verilog_file.readlines():
        if 'module' in line.lower():
            in_instantation = True
            parsed_line = parse_line(line.lower())[0]
            current_name = get_value(parsed_line, 'module')
            modules_dictonary[current_name] = {'PARAMTERS' : [],
                                               'COMMENTS' : [],
                                               'VALUES' : []}
        if in_instantation:
            if '//' in line:
                continue
            parsed_line = parsed_line(line.lower()) 
            if 'parameter' in line.lower():
                parameters = parsed_line(line.lower())
                for parameter in parameters:
                    parameter_name = get_value(parameter, 'parameter')
                    modules_dictonary[current_name]['PARAMETERS'][parameter_name] = []
            if ');' in line:
                in_instantation = False

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

def parse_line(line, split_char = ' ', special_chars = []):
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
    

    for char in line:
        if char in escape_table.keys():
            if nested_type == '':
                nested_type = char
                include_spaces = True
                escape_term = escape_table[char]
                nested_count += 1
                if current_term != '':
                    term_list.append(current_term)
                    current_term = char
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
            else:
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
    file = open('example_genome.sv', 'r')
    current_line = 0
    print(os.getcwd())
    while current_line != -1:
        current_line = read_line(file)
        if current_line == -1:
            break
        cleaned_line = current_line.replace('\n', ' ')
        parsed_line = parse_line(cleaned_line)
        if 'module' in parsed_line:
            ind = parsed_line.index('module')
            parsed_line = parsed_line[ind:]

            print(parsed_line)
   # print(parse_line('    input logic [0:0] btn,'))