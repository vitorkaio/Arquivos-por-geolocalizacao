# coding: utf-8

import math


''' Este arquivo implementa varias funções que serão de utilidade para o servidor'''


def verifica_posicao(sua_posicao, arquivo_posicao):
    ''' Esta função define se a posição do usuário está dentro do raio da posição do arquivo

        Parâmetros:
                 sua_posicao: Define a posição do usuário(pego pelo gps)
                 arquivo_posicao: Define a posicão do arquivo cadastrado em nosso banco.
    '''

    #distancia_max = 10 -> km
    distancia_max = 0.0001
    distancia = distancia_entre_dois_pontos(sua_posicao, arquivo_posicao)

    print '\n\nDistancia: ' + str(distancia) + '\n\n'

    if distancia <= distancia_max:
        print 'Dentro do raio'
        return True
    else:
        print 'Fora do raio'
        return False

def distancia_entre_dois_pontos(sua_posicao, arquivo_posicao):

    sua_lat = float(sua_posicao['lat'])
    sua_lon = float(sua_posicao['lon'])

    arquivo_lat = float(arquivo_posicao['lat'])
    arquivo_lon = float(arquivo_posicao['lon'])

    R = 6371

    d_lat = grau_radianos(arquivo_lat - sua_lat)
    d_lon = grau_radianos(arquivo_lon - sua_lon)

    a = math.sin(d_lat / 2) * math.sin(d_lat / 2) + math.cos(grau_radianos(sua_lat)) * math.cos(grau_radianos(arquivo_lat)) * math.sin(d_lon / 2) * math.sin(d_lon / 2)

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    d = R * c

    return d

def grau_radianos(graus):
    return graus * (math.pi / 180)



# pos_inicial = {'lat':-21.4315571, 'lon':-43.9690796}
# pos_final = {'lat':-21.432536, 'lon':-43.966172}

# verifica_posicao(pos_inicial, pos_final)
