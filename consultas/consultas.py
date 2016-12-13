# 
# CABECERA AQUI
#
import pymongo


# 1. Fecha y titulo de las primeras 'n' peliculas vistas por el usuario 'user_id'.
# >>> usuario_peliculas( 'fernandonoguera', 3 )
def usuario_peliculas(user_id, n):

    for post in db.usuarios.find({'_id': user_id}):
        i = 0
        for peli in post['visualizaciones']:
            if i < n:
                print peli['titulo']+' '+peli['fecha']
                i += 1
            else:
                break


# 2. _id, nombre y apellidos de los primeros 'n' usuarios a los que les gusten
# varios tipos de pelicula ('gustos') a la vez.
# >>> usuarios_gustos(  ['terror', 'comedia'], 5  )
def usuarios_gustos(gustos, n):

    for post in db.usuarios.find({'gustos' : {'$all': gustos}}).limit(n):
        print post['_id']+' '+post['nombre']+' '+post['apellido1']+' '+post['apellido2']


# 3. Numero de peliculas producidas (aunque sea parcialmente) en un pais
# >>> num_peliculas( 'Espanya' )
def num_peliculas(pais):
    print db.peliculas.find({'pais' : {'$in': [pais]}}).count()


# 4. _id de los usuarios que viven en tipo de via y en un piso concreto.
# >>> usuarios_via_num('Plaza', 1)
def usuarios_via_num(tipo_via, numero):
    for post in db.usuarios.find({'direccion.tipo_via': tipo_via}, {'direccion.piso': numero}):
        print post['direccion']['piso']


# 5. _id de usuario de un determinado sexo y edad en un rango
# >>> usuario_sexo_edad('M', 50, 80)
def usuario_sexo_edad(sexo, edad_min, edad_max):
    for post in db.usuarios.find({'sexo': sexo}, {'edad': {'$lt' :edad_max, 'gt' : edad_min}}):
        print post['direccion']['piso']


# 6. Nombre, apellido1 y apellido2 de los usuarios cuyos apellidos coinciden,
# ordenado por edad ascendente
# >>> usuarios_apellidos()
def usuarios_apellidos():
    pass

# 7.- Titulo de las peliculas cuyo director tienen un nombre que empieza por
# un prefijo
# >>> pelicula_prefijo( 'Yol' )
def pelicula_prefijo(prefijo):
    pass


# 8.- _id de usuarios con exactamente 'n' gustos cinematograficos, ordenados por
# edad descendente
# >>> usuarios_gustos_numero( 6 )
def usuarios_gustos_numero(n):
    pass


# 9.- usuarios que vieron una determinada pelicula en un periodo concreto
# >>> usuarios_vieron_pelicula( '583ef650323e9572e2812680', '2015-01-01', '2016-12-31' )
def usuarios_vieron_pelicula(id_pelicula, inicio, fin):
    pass


# Connection to Mongo DB
try:
    client = pymongo.MongoClient('localhost', 27017)
    print "Connected successfully!!!"
except pymongo.errors.ConnectionFailure, e:
    print "Could not connect to MongoDB: %s" % e
db = client.sgdi_pr3

usuario_peliculas('fernandonoguera', 3)
usuarios_gustos(['terror','comedia'],3)
num_peliculas('Eslovaquia')
usuarios_via_num('Calle',9)
usuario_sexo_edad('M',20,80)