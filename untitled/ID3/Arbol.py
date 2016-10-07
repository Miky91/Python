


class Nodo(object):
    def __init__(self, data):
        self.atributos = dict()
        #self.listanodos = list()
        #self.data = data
    #el diccionario tiene como clave el valor del atributo y como valor una lista de tipo Entropia
        # (atributo, clase, entropia)

class Arbol(object):

    def __init__(self, lista):
        self.atributos = dict()#diccionario clave nombre att valor lista de entropias (att, clase, entropia
        for elem in lista:
            self.atributos[elem] = list()

    def insert(self, nodo, att):
        self.atributos[att].append(nodo)
