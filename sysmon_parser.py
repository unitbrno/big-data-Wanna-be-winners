import csv

def remove_quotes(s):
    if s.startswith('"'):
        s = s[1:]
    if s.endswith('"'):
        s = s[:-1]
    return s

def remove_colon(s):
    if s.endswith(":"):
        s = s[:-1]
    return s

def remove_quotes_and_colon(strs):
    return [remove_quotes(remove_colon(s)) for s in strs]

LINES_LIMIT = -1
delim = '\t'

def get_all_columns(filename):
    with open(filename) as input_file:
        csv_reader = csv.reader(input_file, delimiter=';')
        line_count = 0
        message_keys = {}
        for row in csv_reader:
            if line_count == 0:
                column_names = remove_quotes_and_colon(row[0].split(";"))
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                message = row[0]                
                message_parts = message.strip().split('\n')
                for part in message_parts:
                    if (part.strip() == ''):
                        continue

                    del_pos = part.find(': ')
                    key = part.strip()[:del_pos]
                    key = remove_quotes(key)
                    key = remove_colon(key)
                    message_keys[key] = ''
                   
                line_count += 1

            if line_count == LINES_LIMIT:
                print("Exiting after sample lines...")
                break

        message_keys_list = ['Message'] + list(message_keys.keys())
        message_keys_list = sorted(message_keys_list)
        message_columns = delim.join(message_keys_list)
        column_names = delim.join(column_names)
        all_columns = column_names.replace('Message', message_columns)
        return all_columns, message_keys_list
    

input_filename = 'PC6_sysmon.csv'
output_filename = 'processed_' + input_filename



with open(input_filename) as input_file:
    all_columns, message_keys_list = get_all_columns(input_filename)
    all_columns_list = all_columns.split(';')

    with open(output_filename, "w") as output_file:
        output_file.write(all_columns + '\n')

        csv_reader = csv.reader(input_file, delimiter=';')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                line_d = {}
                for key in message_keys_list:
                    key = remove_quotes(key)
                    line_d[key] = ''

                message = row[0]                
                message_parts = message.strip().split('\n')
                index = 0
                for part in message_parts:
                    if (part.strip() == ''):
                        continue

                    del_pos = part.find(': ')
                    if index == 0:
                        key = 'Message'
                    else:
                        key = part.strip()[:del_pos]
                    value = part.strip()[del_pos + 1:].strip()
                    line_d[key] = value
                    index += 1
                
                message_values = []
                for message_key in message_keys_list:
                    message_values.append(line_d[message_key])
                concatenated_message_values = delim.join(message_values)
                #print(concatenated_message_values)
                concatenated_values = concatenated_message_values + delim + delim.join(row[1:])

                """without_quotes = []
                for value in concatenated_values.split(';'):
                    without_quotes.append(remove_quotes(value))
                concatenated_values = ';'.join(without_quotes)"""
                output_file.write(concatenated_values + '\n')

                line_count += 1

            if line_count == LINES_LIMIT:
                print("Exiting after sample lines...")
                break

        #print(column_names)
        print(f'Processed {line_count} lines.')
