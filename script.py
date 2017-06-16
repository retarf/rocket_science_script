import os

def group_by(stream, field, success=None):

    # prapare data and put it in table

    table = []
    for line in stream:
        if line[0] != " " and line[0] != "#":
            year = line[13:17]
            month = line[18:21]
            suc = line[193:194]
            dictionary = {}
            dictionary['year'] = year
            dictionary['month'] = month
            dictionary['suc'] = suc
            table.append(dictionary)

    # filter output

    output = {}

    if success == True:

        for index in table:
            data = index[field]
            suc = index['suc']
            if suc == 'S':
                if data in output:
                    output[data] += 1
                else:
                    output[data] = 1

    elif success == False:

        for index in table:
            data = index[field]
            suc = index['suc']
            if suc == 'F':
                if data in output:
                    output[data] += 1
                else:
                    output[data] = 1

    else:

        for index in table:
            data = index[field]
            if data in output:
                output[data] += 1
            else:
                output[data] = 1

    return output

print( group_by(open('launchlog.txt'), 'year'))
