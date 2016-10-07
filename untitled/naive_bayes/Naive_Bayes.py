# Insertar aqui la cabecera

import  csv
import math



class Tupla(object):
    def __init__(self, clase, rep):

        self.rep = rep
        self.clase = clase

class Probabilidad(object):
    def __init__(self, att, clase, prob):
        self.att = att
        self.clase = clase
        self.prob = prob

class NaiveBayes(object):


    def __init__(self, fichero, smooth=1):


        with open(fichero, 'rb') as csvfile:
            dialect = csv.Sniffer().sniff(csvfile.read(), delimiters=",")
            csvfile.seek(0)
            reader = csv.reader(csvfile, dialect)
            #lista de atributos
            attList = list()
            #lista de probabilidades
            self.prob = list()
            #valores de clase
            self.classes = list()
            i = 0
            #lista de valores de tuplas
            nvaloresAtts = dict()
            valoresAtts = dict()
            #tuplas repetidas
            tuplasRepetidas = dict()
            for row in reader:
                if i == 0:
                    attList = row
                    repeticiones = {}
                    j = 0
                    while j < len(attList):
                        repeticiones[j] = 0
                        j= j+1
                    for elem in attList:
                        nvaloresAtts[elem] = 0
                        valoresAtts[elem] = list()

                else:
                    k = 0
                    if self.classes.count(row[len(attList)-1]) == 0:
                        self.classes.append(row[len(attList)-1])
                    while k < len(attList):
                        if tuplasRepetidas.has_key(row[k]+" "+attList[k]):
                            auxList = list(tuplasRepetidas[row[k]+" "+attList[k]])
                            encontrado = False
                            for elem in auxList:
                                aux = elem
                                if aux.clase == row[len(attList)-1]:
                                    aux.rep = aux.rep+1
                                    auxList.remove(elem)
                                    auxList.append(aux)
                                    encontrado = True
                                    break
                                    #tuplasRepetidas[row[k] + " " + attList[k]] = auxList

                            if encontrado == False:
                                t = Tupla(row[len(attList) - 1], 1)
                                auxList.append(t)
                                #tuplasRepetidas[row[k] + " " + attList[k]] = auxList
                            tuplasRepetidas[row[k] + " " + attList[k]] = auxList
                        else:
                            t = Tupla(row[len(attList)-1],1)
                            listaAuxiliar = list()
                            listaAuxiliar.append(t)
                            tuplasRepetidas[row[k]+" "+attList[k]] = listaAuxiliar
                            nvaloresAtts[attList[k]] = nvaloresAtts[attList[k]]+1
                            valores = list(valoresAtts[attList[k]])
                            valores.append(row[k])
                            valoresAtts[attList[k]] = valores
                        k = k+1



                i = i+1


            print "Numero total de instancias leidas: "+str(i-1)+"\n"
            for key in attList:
                if key == "class":
                    print "Instancias clase "+key+": "+str(valoresAtts[key])
                    for value in valoresAtts[key]:
                        if tuplasRepetidas.has_key(value+ " class"):
                            del tuplasRepetidas[value+" class"]
                else:
                    print "Atributo: "+key+": { " + str(valoresAtts[key]) + " }\n"


            n_tuplas = (len(attList)-1)*(i-1)


            for elem in tuplasRepetidas:
                aux = str(elem).split(" ")
                for valor in tuplasRepetidas[elem]:
                    probabilidad = Probabilidad(aux[0], valor.clase, float(valor.rep+smooth)/(n_tuplas+smooth*nvaloresAtts[aux[1]]))
                    self.prob.append(probabilidad)


    def clasifica(self, instancia):
        acumulador = float(0)
        max = float(0)
        clase = ''
        lista = list()
        for key in instancia:
            for value in self.classes:
                for elem in self.prob:
                    probabilidad = elem
                    if probabilidad.clase == value:
                        if probabilidad.att == instancia[key]:
                            acumulador = acumulador +  math.fabs(math.log(probabilidad.prob))
                if max < acumulador:
                    max = acumulador
                    clase = value
        return clase

    def test(self, fichero):

        with open(fichero, 'rb') as csvfile:
            dialect = csv.Sniffer().sniff(csvfile.read(), delimiters=",")
            csvfile.seek(0)
            reader = csv.reader(csvfile,dialect)
            attList = list()
            valoresAtts = dict()
            i = 0
            aciertos = 0
            fallos = 0
            for row in reader:
                if i == 0:
                    attList = row
                    for elem in attList:
                        valoresAtts[elem] = list()
                    i=i+1
                else:
                    auxDict = dict()
                    j = 0
                    while j < (len(attList)-1):
                        auxDict[attList[j]] = row[j]
                        j = j+1
                    print auxDict
                    print "--"+row[len(attList)-1]
                    clase = self.clasifica(auxDict)
                    print "Clase predicha: "+clase
                    if clase == row[len(attList)-1]:
                        aciertos+=1
                        print "ACIERTO"
                    else:
                        fallos+=1
                        print  "FALLO"

            return (aciertos, fallos+aciertos, float(aciertos)/fallos+aciertos)






naive = NaiveBayes("train.data",1)

naive.clasifica({'season' : 'winter','wind' : 'high', 'day' : 'weekday', 'rain' : 'heavy'})
naive.test("test.data")