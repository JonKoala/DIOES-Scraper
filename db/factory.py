from db.interface import Interface

##
#CONSTANTS

__Publicacao_Original_PARAMETERS = '[Publicacao_Original]', ('id', 'edicao', 'numero', 'data', 'categoria', 'orgao', 'suborgao', 'tipo', 'materia', 'identificador', 'corpo')
__Latest_Update_PARAMETERS = '[Latest_Update]', ('data', )

_PARAMETERS = {
    'publicacao': __Publicacao_Original_PARAMETERS,
    'latest_publicacao': __Latest_Update_PARAMETERS
}

def get_interface(table):

    table = table.lower()

    name, columns = _PARAMETERS[table]
    return Interface(name, columns)
