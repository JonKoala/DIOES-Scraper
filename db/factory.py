from db.interface import Interface

##
#CONSTANTS

__DIOES3_PARAMETERS = '[DIOES3]', ('id', 'edicao', 'numero', 'data', 'categoria', 'orgao', 'suborgao', 'tipo', 'materia', 'identificador', 'publicacao')
__Latest_Update_PARAMETERS = '[Latest_Update_DIOES3]', ('data', )

_PARAMETERS = {
    'publicacao': __DIOES3_PARAMETERS,
    'latest_publicacao': __Latest_Update_PARAMETERS
}

def get_interface(table):

    table = table.lower()

    name, columns = _PARAMETERS[table]
    return Interface(name, columns)
