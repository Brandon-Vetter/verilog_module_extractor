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
def parse_line(line, comment = False):
    term_list = []
    current_term = ''
    include_spaces = comment
    last_char = ''
    line = line.strip()
    
    for char in line:
        if include_spaces:
            current_term += char
            if char == ']' or char == '}':
                include_spaces = False
        elif char != ' ':
            if char == '(' or char == ')' or char == ',':
                term_list.append(char)
                current_term = ''
                continue
            current_term += char
            if char == '[' or char == '{':
                include_spaces = True
            elif last_char + char == '//':
                include_spaces = True
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
    print(parse_line('    input logic [0:0] btn,'))