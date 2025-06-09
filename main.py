#!/usr/bin/env python
"""
# G code converter
# cod version: v.0.0.1
# ________________________________________
# Modifies g code according to set point
# ________________________________________
# First update: 7.6.2025.
# First programmer: Martin Martinic
# Last update: 7.6.2025.
# Last programmer: Martin Martinic
# ________________________________________
"""

import re


def get_program_names(in_programs_name_string):
    out_programs_name_list = re.split('\n', in_programs_name_string, flags=0)
    return list(filter(None, out_programs_name_list))


def open_g_code(in_program_name):
    try:
        with open(in_program_name) as tmp_program:
            out_program = tmp_program.read()
    except FileNotFoundError:
        print('Provjeri \'PopisPrograma.txt\',\n'
              'Program: \'' + in_program_name + '.CNC\' nije pronaden')
        out_program = None
    return out_program


def change_coordinate(in_program_string, in_axis_list, in_axis_offset):
    if in_program_string is not None:

        out_program_string = in_program_string

        tmp_program_line = re.findall('.*', in_program_string)

        for tmp_count_line in tmp_program_line:

            tmp_new_program_line = tmp_count_line

            for tmp_count_axis in in_axis_list:

                tmp_pattern_str = r'[' + tmp_count_axis + r'|' + tmp_count_axis.lower() + r']\S+'
                tmp_pattern = re.compile(tmp_pattern_str)
                tmp_coordinate = re.findall(tmp_pattern, tmp_count_line)
                try:
                    tmp_new_coordinate = tmp_coordinate[0]
                    # Remove uppercase letters
                    tmp_new_coordinate = tmp_new_coordinate.replace(tmp_count_axis, '')
                    # Remove lowercase letters
                    tmp_new_coordinate = tmp_new_coordinate.replace(tmp_count_axis.lower(), '')
                    # Turn to float
                    try:
                        tmp_new_coordinate = float(tmp_new_coordinate)
                        # Add offset
                        tmp_new_coordinate = tmp_new_coordinate + in_axis_offset[in_axis_list.index(tmp_count_axis)]
                        # Round position to 2 decimals
                        tmp_new_coordinate = round(tmp_new_coordinate, 2)
                        # Turn back to string
                        tmp_new_coordinate = str(tmp_new_coordinate)
                        # Return letter of axis
                        tmp_new_coordinate = tmp_count_axis + tmp_new_coordinate
                        # Generate new program line with offset coordinates
                        tmp_new_program_line = tmp_new_program_line.replace(tmp_coordinate[0], tmp_new_coordinate)
                    except ValueError:
                        pass
                except IndexError:
                    pass

            out_program_string = out_program_string.replace(tmp_count_line, tmp_new_program_line)
    else:
        out_program_string = None

    return out_program_string


if __name__ == '__main__':

    print('╭━━━┳━━━┳━━━┳━━━┳╮\n'
          '┃╭━╮┃╭━╮┃╭━╮┃╭━━┫┃\n'
          '┃╰━╯┃╰━╯┃┃╱┃┃╰━━┫┃\n'
          '┃╭━━┫╭╮╭┫┃╱┃┃╭━━┫┃╱╭╮\n'
          '┃┃╱╱┃┃┃╰┫╰━╯┃╰━━┫╰━╯┃\n'
          '╰╯╱╱╰╯╰━┻━━━┻━━━┻━━━╯\n'
          '╭━━━╮╱╱╭╮╱╱╱╱╱╱╱╱╱╭╮\n'
          '┃╭━╮┃╱╭╯╰╮╱╱╱╱╱╱╱╭╯╰╮╱╱╱╱╱╱╱╱╱╱╱╭╮\n'
          '┃┃╱┃┣╮┣╮╭╋━━┳╮╭┳━┻╮╭╋┳━━━┳━━┳━━┳╋╋━━╮\n'
          '┃╰━╯┃┃┃┃┃┃╭╮┃╰╯┃╭╮┃┃┣╋━━┃┃╭╮┃╭━╋╋┫╭╮┃\n'
          '┃╭━╮┃╰╯┃╰┫╰╯┃┃┃┃╭╮┃╰┫┃┃━━┫╭╮┃╰━┫┃┃╭╮┃\n'
          '╰╯╱╰┻━━┻━┻━━┻┻┻┻╯╰┻━┻┻━━━┻╯╰┻━━┻┫┣╯╰╯\n'
          '╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╭╯┃\n'
          '╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╰━╯')
    print('Skripta za zamicanje tocaka u g kodu.\n')

    try:
        with open('./PopisPrograma.txt') as program_list:
            ProgramList = program_list.read()

        valid_axis = False

        while not valid_axis:
            axis_list = (re.findall(r'([A-Z])', input('Unesi ime svih osi koje se zamicu:\n').upper()))
            axis_offset = [0.0]*len(axis_list)
            if len(axis_list) == 0:
                print('Dozvoljen je iskljucivo unos slova kao ime osi,\n'
                      'svako slovo ce se gledati kao zasebna os neovisno o tome je li uneseno s razmakom ili spojeno')
            else:
                valid_axis = True

        for count_axis in axis_list:
            while axis_offset[axis_list.index(count_axis)] == 0.0:
                try:
                    axis_offset[axis_list.index(count_axis)] = float(input('Unesi za koliko se os: \''
                                                                           + count_axis + '\' zamice:\n'))
                    if axis_offset[axis_list.index(count_axis)] == 0.0:
                        print('Ubuduce nije potrebno unositi ime osi koja se zamice za 0!')
                        axis_offset[axis_list.index(count_axis)] = 0.00000000001

                except ValueError:
                    print('Dozvoljen je samo unos brojeva, a za odvajanje decimalnih mijesta koristite \'.\'')

        for count_program in get_program_names(ProgramList):
            program_name = './' + count_program + '.CNC'
            program = change_coordinate(open_g_code(program_name), axis_list, axis_offset)

            with open(program_name, 'w') as save_program:
                save_program.write(program)
            print('Zamicanje g koda: \'' + count_program + '.CNC\' izvrseno,')
        print('Zamicanje svih g kodova izvrseno.')

    except FileNotFoundError:
        print('Datoteka \'./PopisPrograma.txt\' nije pronadena u mapi skupa s .exe')

    input('Pritisni \'enter\' za kraj.')
