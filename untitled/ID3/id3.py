# Insertar aqui la cabecera


#Miguel Andres Herrero y Viktor Jacynycz Garcia declaramos que esta solucion es fruto exclusivamente
#  de nuestro trabajo personal.No hemos sido ayudados por ninguna otra persona ni hemos obtenido
# la solucion de fuentes externas, y tampoco hemos compartido nuestra solucion con nadie. Declaramos
# ademas que no hemos realizado de manera deshonesta ninguna otra actividad que pueda mejorar nuestros
#  resultados ni perjudicar los resultados de los demas.
import csv
import math
import os.path




class Nodo(object):
    def __init__(self,attribute):

        self.attr = attribute
        self.list = list()
        self.isHoja = False

class Tupla(object):
    def __init__(self, att, clase, rep):
        self.att = att
        self.clase = clase
        self.rep = rep


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
            #valores de clase y numero de veces repetidas
            self.classes = dict()
            self.repeticionesValorAtr = dict()
            i = 0
            #lista de valores de tuplas
            nvaloresAtts = dict()
            self.valoresAtts = dict()
            #tuplas repetidas clave nombre attr valor (att.value, class.value, n_reps)
            self.tuplasRepetidas = dict()
            self.n_instancias = 0
            for row in reader:
                if i == 0:
                    self.attList = row
                    for elem in self.attList:
                        nvaloresAtts[elem] = 0
                        self.valoresAtts[elem] = list()
                        self.repeticionesValorAtr[elem] = dict()

                else:
                    self.instancias.append(row)
                    if self.classes.has_key(row[len(self.attList)-1]):
                        self.classes[row[len(self.attList) - 1]] += 1
                    else:
                        self.classes[row[len(self.attList) - 1]] = 1
                    k = 0
                    while k < len(self.attList)-1:
                        dic = self.repeticionesValorAtr[self.attList[k]]
                        if dic.has_key(row[k]):
                            dic[row[k]] += 1
                        else:
                            dic[row[k]] = 1
                        t = Tupla(row[k],row[len(self.attList)-1],1)
                        auxiliar = list(self.valoresAtts[self.attList[k]])
                        encontrado = False
                        for elem in auxiliar:
                            if (elem.att == row[k]) & (elem.clase == row[len(self.attList)-1]):
                                elem.rep+=1
                                encontrado = True
                        if encontrado is False:
                            self.valoresAtts[self.attList[k]].append(t)
                        k+=1

                i+=1
            self.n_instancias = i-1
            self.arbol = self.id3(self.instancias,self.attList)



    def selecattribute(self,conj, lista):

        eInicial = 0
        eTemporal = 0
        atributo = ''
        for key in self.classes:
            aux = float(self.classes[key])/self.n_instancias
            eInicial += math.fabs(aux*math.log(aux))


        for key in self.valoresAtts:
            if key != 'class':
                auxiliar = float(0)
                if lista.count(key) != 0:
                    for value in self.valoresAtts[key]:
                        aux = dict(self.repeticionesValorAtr[key])
                        n_instancias_attr =aux[value.att]
                        auxiliar += (float(n_instancias_attr)/self.n_instancias)*(float(value.rep)/n_instancias_attr+math.fabs(math.log(float(value.rep)/n_instancias_attr)))
                    if (eTemporal > auxiliar) | (eTemporal == 0):
                        eTemporal = auxiliar
                        atributo = key
        return atributo




    def particion(self,conjunto, atributo, valor):
        lista = list()
        for instancia in conjunto:
            if instancia.count(valor) >0:
                lista.append(instancia)
        return lista




    def id3(self, conjunto, attList):
        previous = 0
        cp = ''
        tabla = dict()
        for elem in conjunto:
            if tabla.has_key(elem[len(self.attList)-1]):
                tabla[elem[len(self.attList)-1]] += 1
            else:
                tabla[elem[len(self.attList) - 1]] = 1
        claseValorMasRepetido = max(tabla.values())
        for key in tabla:
            if tabla[key] == claseValorMasRepetido:
                cp = key

        for instancia in conjunto:
            if (instancia[len(attList)-1] == cp) & (previous == self.n_instancias):
                hoja = Nodo(cp)
                hoja.isHoja = True
                return hoja
            elif len(attList) == 0:
                hoja = Nodo(cp)
                hoja.isHoja = True
                return hoja
            a = self.selecattribute(conjunto,attList)
            nodo = Nodo(a)
            valores = self.repeticionesValorAtr[a].keys()
            for value in valores:
                cj= self.particion(conjunto,a,value)
                if not cj:
                    n = Nodo(cp)
                    n.isHoja = True
                else:
                    nuevosAtributos = list()
                    for atributo in attList:
                        if atributo != "class":
                            if atributo != a:
                                nuevosAtributos.append(atributo)
                    n = self.id3(cj,nuevosAtributos)
                nodo.list.append((n,value))
            return nodo

    def buscarClase(self,arbol, value):
        for elem in arbol.list:
            if elem[1] == value:
                return elem[0]



    def clasifica(self, instancia):
        if self.arbol.isHoja:
            print "Clase predicha: "+self.arbol.attr
        else:
            #keys = instancia.keys()
            auxArbol = self.arbol
            #buscarClase(auxArbol, instancia)
            k = 0
            while k < len(instancia.keys()):
                if auxArbol.isHoja:
                    print "Clase predicha: "+auxArbol.attr
                else:
                    auxArbol = self.buscarClase(auxArbol, instancia[auxArbol.attr])
                k+=1

        print "Clase predicha: "+auxArbol.attr
        return auxArbol.attr


    def test(self, fichero):
        with open(fichero, 'rb') as csvfile:
            dialect = csv.Sniffer().sniff(csvfile.read(), delimiters=",")
            csvfile.seek(0)
            reader = csv.reader(csvfile, dialect)
            attList = list()
            valoresAtts = dict()
            i = 0
            aciertos = 0
            fallos = 0
            for row in reader:
                if i == 0:
                    attList = row
                    auxDict = dict()
                    for elem in attList:
                        valoresAtts[elem] = list()
                        auxDict[elem] = ''
                    i = i + 1
                else:
                    auxDict = dict()
                    j = 0

                    while j < (len(attList)-1):
                        auxDict[attList[j]] = row[j]
                        j = j+1
                    print auxDict
                    print "--"+row[len(attList)-1]
                    clase = self.clasifica(auxDict)
#                    print "Clase predicha: "+clase
                    if clase == row[len(attList)-1]:
                        aciertos+=1
                        print "ACIERTO"
                    else:
                        fallos+=1
                        print "FALLO"
            print "ACIERTOS: "+str(aciertos)
            print "FALLOS: "+str(fallos)
            print "TASA: "+str(float(aciertos)/(fallos+aciertos))

    def buscarHijos(self,auxArbol,csvfile,aristas,atributos, hashtable):

        i = 1
       # if self.attList.count(auxArbol.attr) > 0:  # busco si es un valor de cabecera
        if auxArbol.isHoja:
            csvfile.write('"' +auxArbol.attr + '"' + " [label = " + '"' + auxArbol.attr+ '"' + "];\n")
            atributos[auxArbol.attr] += 1
        else:
            csvfile.write('"' + auxArbol.attr  + '"' + " [label = " + '"' + auxArbol.attr+ '"' + "," + "shape = " + "box" + "];\n")
            atributos[auxArbol.attr] += 1
            for elem in auxArbol.list:
                if not hashtable.has_key('"' + auxArbol.attr + '"' + " -> " +  '"' + elem[0].attr + '"' + " [label= " + '"' + elem[1] + '"' + "];\n"):
                    aristas.append('"' + auxArbol.attr + '"' + " -> " +  '"' + elem[0].attr + '"' + " [label= " + '"' + elem[1] + '"' + "];\n")
                    hashtable['"' + auxArbol.attr + '"' + " -> " +  '"' + elem[0].attr + '"' + " [label= " + '"' + elem[1] + '"' + "];\n"] = 1
                i += 1
            for elem in auxArbol.list:
                self.buscarHijos(elem[0], csvfile, aristas,atributos, hashtable)


    def save_tree(self, fichero):

        with open(fichero, 'w') as csvfile:
            csvfile.seek(0)
            csvfile.write("digraph tree {\n")
            #for nodo in self.arbol:
            auxArbol = self.arbol
            aristas = list()
            atributos = dict()
            hashtable = dict()
            for key in self.attList:
                atributos[key] = 1
            for clase in self.classes:
                atributos[clase] = 1
            self.buscarHijos(auxArbol,csvfile,aristas,atributos, hashtable)
            for arista in aristas:
                csvfile.write(arista)
          #   for nodo in auxArbol:#nodo.list:
            csvfile.write("}")


id3 = ID3("train.data")
#id3.clasifica({'season' : 'winter','wind' : 'high', 'day' : 'weekday', 'rain' : 'heavy'})
id3.test("test.data")
id3.save_tree("arbol.dot")
