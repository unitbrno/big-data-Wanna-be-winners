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

delim = '\t'

input_filename = 'PC1_security.csv'
output_filename = 'processed_' + input_filename
with open(input_filename) as input_file:
    with open(output_filename, "w") as output_file:
        csv_reader = csv.reader(input_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                column_names = row[0]
                print(f'Column names are {", ".join(row)}')
                column_names = column_names.replace('Message',
        '"Message";"Process ID";"Application Name";"Network Information";"Direction";"Source Address";"Source Port";"Destination Address";"Destination Port";"Protocol";"Filter Information";"Filter Run-Time ID";"Layer Name";"Layer Run-Time ID"')
                without_quotes = []
                for col_name in column_names.split(';'):
                    without_quotes.append(remove_quotes(col_name))
                column_names = delim.join(without_quotes)
                output_file.write(column_names + '\n')
                line_count += 1
            else:
                line_d = {}
                message_keys = '"Message";"Process ID";"Application Name";"Network Information";"Direction";"Source Address";"Source Port";"Destination Address";"Destination Port";"Protocol";"Filter Information";"Filter Run-Time ID";"Layer Name";"Layer Run-Time ID"'.split(';')
                message_keys_list = []
                for key in message_keys:
                    key = remove_quotes(key)
                    message_keys_list.append(key)
                    line_d[key] = ''
                #print(row)
                r = row[0]
                #print(len(r.split(';')))
                #print(r.split(';'))
                
                message = r.split(';')[0]
                #print(message)
                message_values = []
                index = 0
                for pair in message.strip().split('\n'):
                    pair_objects = pair.strip().split('\t')
                    pair_objects = [obj for obj in pair_objects if obj != '']
                    if len(pair_objects) == 0:
                        continue
                    #print('pair_objects_len=', len(pair_objects), pair_objects)

                    value = ''
                    if len(pair_objects) == 2:
                        key = remove_quotes(pair_objects[0])
                        key = remove_colon(key)
                        line_d[key] = pair_objects[1]
                    elif len(pair_objects) == 1 and (not pair_objects[0].lower().endswith('information:') or index == 0):
                        line_d["Message"] = pair_objects[0]
                    index += 1
                
                message_values = []
                for message_key in message_keys_list:
                    message_values.append(line_d[message_key])
                concatenated_message_values = ';'.join(message_values)
                #print(concatenated_message_values)
                concatenated_values = concatenated_message_values + ';' + ';'.join(r.split(';')[1:])

                without_quotes = []
                for value in concatenated_values.split(';'):
                    without_quotes.append(remove_quotes(value))
                concatenated_values = delim.join(without_quotes)
                output_file.write(concatenated_values + '\n')


                line_count += 1

            #if line_count == 100:
            #    print("Exiting after sample lines...")
            #    break

        #print(column_names)
        print(f'Processed {line_count} lines.')
