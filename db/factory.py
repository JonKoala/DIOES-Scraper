from db.interface import Interface

##
#CONSTANTS

__DIOES3_PARAMETERS = '[DIOES3]', ('id', 'edicao', 'numero', 'data', 'categoria', 'orgao', 'suborgao', 'tipo', 'materia', 'identificador', 'publicacao')

_PARAMETERS = {
    'dioes3': __DIOES3_PARAMETERS
}

def get_interface(table):

    table = table.lower()

    name, columns = _PARAMETERS[table]
    return Interface(name, columns)
