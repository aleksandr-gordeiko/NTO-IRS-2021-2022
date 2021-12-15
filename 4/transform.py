with open('3', 'r') as file:
    lines = file.readlines()
    new_lines = []
    for line in lines:
        line_list: list = line[:-1].split(' ')
        hex_color = int('0x' + line_list[3], base=16)
        line_list.pop()
        line_list.append(str(hex_color >> 16))
        line_list.append(str((hex_color >> 8) % 256))
        line_list.append(str(hex_color % 256))
        new_line = ' '.join(line_list) + '\n'
        new_lines.append(new_line)
    with open('3new', 'a') as new:
        new.writelines(new_lines)
