# Insertar aqui la cabecera

import Arbol
import csv


class Tupla(object):
    def __init__(self, clase, rep):

        self.rep = rep
        self.clase = clase

class Entropia(object):
    def __init__(self, att, clase, prob):
        self.att = att
        self.clase = clase
        self.entropia = prob


class Instancia(object):

    def __init__(self, lista):
        self.lista = lista


class ID3(object):
    def __init__(self, fichero):
        with open(fichero, 'rb') as csvfile:
            dialect = csv.Sniffer().sniff(csvfile.read(), delimiters=",")
            csvfile.seek(0)
            reader = csv.reader(csvfile, dialect)
            #lista de atributos
            self.attList = list()
            #lista de instancias
            self.instancias = list()
            #valores de clase
            self.classes = dict()
            i = 0
            #lista de valores de tuplas
            nvaloresAtts = dict()
            self.valoresAtts = dict()
            #tuplas repetidas
            tuplasRepetidas = dict()
            for row in reader:
                if i == 0:
                    self.attList = row
                    for elem in self.attList:
                        nvaloresAtts[elem] = 0
                        self.valoresAtts[elem] = list()
                    if self.classes.has_key(row[len(self.attList)-1]):
                        self.classes[row[len(self.attList) - 1]]+=1
                    else:
                        self.classes[row[len(self.attList) - 1]] =0
                 else:
                    self.instancias.append(row)

                i+=1


    def id3(self, conjunto, attList):

        pass


    def clasifica(self, instancia):
        pass

    def test(self, fichero):
        pass

    def save_tree(self, fichero):
        pass

id3 = ID3("train.data")