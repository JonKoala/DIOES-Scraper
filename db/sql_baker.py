
##
#PUBLIC

def insert(table, dictionary):
    if not table or len(dictionary) < 1:
        return ''

    keys = ['[{}]'.format(k) for k in dictionary]
    keys = ', '.join(keys)

    values = ['\'{}\''.format(_format_string(dictionary[k])) for k in dictionary]
    values = ', '.join(values)

    return 'INSERT INTO {0} ({1}) VALUES ({2})'.format(table, keys, values)

def select(table, tuples, operator):
    if not table:
        return '';

    parameters = []
    for k, v in tuples:
        parameter = '[{0}] LIKE \'%{1}%\''.format(k, _format_string(v))
        parameters.append(parameter)

    parameters = ' {} '.format(operator).join(parameters)
    where = 'WHERE ' + parameters if parameters else ''
    
    return 'SELECT * FROM {0} {1}'.format(table, where)


##
#UTILS

def _format_string(string):
    string = str(string)
    return string.replace('\'', '\'\'')
