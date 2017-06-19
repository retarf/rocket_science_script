import os


# make list with all hash positions
def find_hash_places(line):

    positions_list = []
    actual_position = 0

    while True:
        actual_position = line.find('#', actual_position)
        if actual_position == -1:
            break
        positions_list.append(actual_position)
        actual_position += 1

    return positions_list


# get specific hash position
def get_hash_position(hash_line, hash_number):

    hash_number -= 1
    hash_position = find_hash_places(hash_line)[hash_number]

    return hash_position


def get_column_name(heading_line, hash_line, column_number):

    column_start = get_hash_position(hash_line, column_number)
    column_lenght = get_column_lenght(hash_line, column_number)
    column_end = column_start + column_lenght

    name = heading_line[column_start:column_end]

    # delete unnecessary charts
    name = name.lstrip("#")
    name = name.lstrip()
    name = name.rstrip()

    return name


def get_column_lenght(data, column_number):

    if column_number == 11:
        return 30

    column_pos = get_hash_position(data, column_number)
    next_column_pos = get_hash_position(data, column_number + 1)

    lenght = next_column_pos - 1 - column_pos

    return lenght


def get_column_data(heading_line, hash_line, number):

    hash_positions = 0
    column_start = get_hash_position(hash_line, number)
    column_end = column_start + get_column_lenght(hash_line, number)

    data = {}
    data['start'] = column_start
    data['end'] = column_end

    return data


def get_year_end(date_start):
    year_end = date_start + 4

    return year_end


def get_month_start(date_start):
    month_start = date_start + 5

    return month_start


def get_month_end(date_start):
    month_end = date_start + 8

    return month_end


def prepare_data_table(stream_list):

    heading_line = stream_list[0]
    hash_line = stream_list[1]

    columns_data = {}
    for i in range(1, 12):
        column_name = get_column_name(heading_line, hash_line, i)
        columns_data[column_name] = get_column_data(heading_line, hash_line, i)

    table = []

    date_column_start = columns_data['Launch Date (UTC)']['start']

    year_start = date_column_start
    year_end = get_year_end(date_column_start)

    month_start = get_month_start(date_column_start)
    month_end = get_month_end(date_column_start)

    suc_start = columns_data['Suc']['start']
    suc_end = columns_data['Suc']['end']

    # get data and put it in dictionary

    for line in stream_list:
        if line[0] != "#":
            year = line[year_start:year_end]
            month = line[month_start:month_end]
            suc = line[suc_start:suc_end]
            # clear right spaces
            suc = suc.rstrip()
            if year[0] == " ":
                table_last = len(table) - 1
                year = table[table_last]['year']
                month = table[table_last]['month']
                suc = table[table_last]['suc']

            dictionary = {}
            dictionary['year'] = year
            dictionary['month'] = month
            dictionary['suc'] = suc

            # append dictionary to table
            table.append(dictionary)

    return table


def group_by(stream, field, success=None):

    # convert stream to list
    stream_as_list = list(stream)

    # prepare data and put it in list "table"
    data_list = prepare_data_table(stream_as_list)

    # filter output
    output = {}

    if success == True:

        for index in data_list:
            data = index[field]
            suc = index['suc']
            if suc == 'S':
                if data in output:
                    output[data] += 1
                else:
                    output[data] = 1

    elif success == False:

        for index in data_list:
            data = index[field]
            suc = index['suc']
            if suc == 'F':
                if data in output:
                    output[data] += 1
                else:
                    output[data] = 1

    else:

        for index in data_list:
            data = index[field]
            if data in output:
                output[data] += 1
            else:
                output[data] = 1

    return output
