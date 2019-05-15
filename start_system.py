from func_membre_and_inverse import *
import math
import matplotlib.pyplot as plt

#Variables por ahora fija que definen los intervalos para 
#La fusificacion de las variables de entrada
pesoRopaLigero_min=0
pesoRopaLigero_inflexion=4
pesoRopaLigero_mayor=5

pesoRopaMitad_mi=4
pesoRopaMitad_optimo=7
pesoRopaMitad_mayor=10

pesoRopaPesado_min=8
pesoRopaPesado_inflexion=12
pesoRopaPesado_mayor=14

phAguaAcido_min=0
phAguaAcido_inflexion=5
phAguaAcido_mayor=7

phAguaNeutro_min=5
phAguaNeutro_optimo=7
phAguaNeutro_mayor=9

phAguaBasico_min =7
phAguaBasico_inflexion=10
phAguaBasico_mayor=14

cantDetergPoco_min  =0
cantDetergPoco_inflexion=50
cantDetergPoco_mayor=100

cantDetergMedia_min=90
cantDetergMedia_optimo=180
cantDetergMedia_mayor=220

cantDetergMucho_min=200
cantDetergMucho_inflexion=260
cantDetergMucho_mucho=300

cantDeAguaPoca_min=0
cantDeAguaPoca_inflexion=12
cantDeAguaPoca_mayor=22

cantDeAguaMedia_min=20
cantDeAguaMedia_optimo=31
cantDeAguaMedia_mayor=42

cantDeAguaMucha_min = 40
cantDeAguaMucha_inflexion=52
cantDeAguaMucha_mayor=60


def tsukamoto_methot (wzis):

    products=[]
    wis=[]
    for i,j in wzis:
        products.append(i*j)
        wis.append(i)
    
    return sum(products )/sum(wis)


def start_washing_machine(pesoRopa,pH,tsukamoto):
    """
    Este es el metodo principal para iniciar el sistema de inferencia
    dadas los paramentros de entrada.
    Para la fusificacion los parametros que marcan los intervalos para generar las variables 
    lenguisticas estan fijas con las variables arriba.
    """
    #Fusification proccess
    valores_ropa =np.arange(0,15,1)
    valores_pH =np.arange(0,15,1)
    valores_detergente =np.arange(0,301,1)
    valores_agua =np.arange(0,61,1)

    p1=funcion_membrecia_trapezoidal(valores_ropa,[pesoRopaLigero_min,pesoRopaLigero_inflexion,pesoRopaLigero_inflexion,
                                                                        pesoRopaLigero_mayor])
    p2=funcion_membrecia_triangular(valores_ropa,[pesoRopaMitad_mi,pesoRopaMitad_optimo,pesoRopaMitad_mayor])

    p3=funcion_membrecia_trapezoidal(valores_ropa,[pesoRopaPesado_min,pesoRopaPesado_inflexion,
                                                                            pesoRopaPesado_inflexion,pesoRopaPesado_mayor])

    ph1=funcion_membrecia_trapezoidal(valores_pH,[phAguaAcido_min,phAguaAcido_inflexion,phAguaAcido_inflexion,phAguaAcido_mayor])
    ph2=funcion_membrecia_triangular(valores_pH,[phAguaNeutro_min,phAguaNeutro_optimo,phAguaNeutro_mayor])
    ph3=funcion_membrecia_trapezoidal(valores_pH,[phAguaBasico_min,phAguaBasico_inflexion,phAguaBasico_inflexion,phAguaBasico_mayor])

    d1=funcion_membrecia_trapezoidal(valores_detergente,[cantDetergPoco_min,cantDetergPoco_inflexion,cantDetergPoco_inflexion,cantDetergPoco_mayor])
    d2=funcion_membrecia_triangular(valores_detergente,[cantDetergMedia_min,cantDetergMedia_optimo,cantDetergMedia_mayor])
    d3=funcion_membrecia_trapezoidal(valores_detergente,[cantDetergMucho_min,cantDetergMucho_inflexion,cantDetergMucho_inflexion,cantDetergMucho_mucho])

    a1=funcion_membrecia_trapezoidal(valores_agua,[cantDeAguaPoca_min,cantDeAguaPoca_inflexion,cantDeAguaPoca_inflexion,cantDeAguaPoca_mayor])
    a2=funcion_membrecia_triangular(valores_agua,[cantDeAguaMedia_min,cantDeAguaMedia_optimo,cantDeAguaMedia_mayor])
    a3=funcion_membrecia_trapezoidal(valores_agua,[cantDeAguaMucha_min,cantDeAguaMucha_inflexion,cantDeAguaMucha_inflexion,cantDeAguaMucha_mayor])


    #Grado de memebrecia de los valores de la entrada (Fuzification)
    gradoPertenciaRopa_peso_ligera=membership(valores_ropa,p1,pesoRopa)
    gradoPertenciaRopa_peso_medio=membership(valores_ropa,p2,pesoRopa)
    gradoPertenciaRopa_peso_pesado=membership(valores_ropa,p3,pesoRopa)


    gradoPertencia_pH_acido=membership(valores_pH,ph1,pH)
    gradoPertencia_pH_neutral=membership(valores_pH,ph2,pH)
    gradoPertencia_pH_basico=membership(valores_pH,ph2,pH)

    #Ploteo de las funciones de membrecia
    