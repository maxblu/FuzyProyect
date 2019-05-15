from func_membre_and_inverse import *
import math

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
    gradoPertenciaRopa_peso_ligera=funcion_membrecia_trapezoidal_pertenencia(pesoRopaLigero_min,pesoRopaLigero_inflexion,
                                                                        pesoRopaLigero_mayor,pesoRopa,0)
    gradoPertenciaRopa_peso_medio=funcion_membrecia_triangular_pertenencia(pesoRopaMitad_mi,pesoRopaMitad_optimo,
                                                                                pesoRopaMitad_mayor,pesoRopa)
    gradoPertenciaRopa_peso_pesado=funcion_membrecia_trapezoidal_pertenencia(pesoRopaPesado_min,pesoRopaPesado_inflexion,
                                                                            pesoRopaPesado_inflexion,pesoRopa,1)

    gradoPertencia_pH_acido=funcion_membrecia_trapezoidal_pertenencia(phAguaAcido_min,phAguaAcido_inflexion,phAguaAcido_mayor,
                                                                                    pH,0)
    gradoPertencia_pH_neutral=funcion_membrecia_triangular_pertenencia(phAguaNeutro_min,phAguaNeutro_optimo,phAguaNeutro_mayor,
                                                                        pH)
    gradoPertencia_pH_basico=funcion_membrecia_trapezoidal_pertenencia(phAguaBasico_min,phAguaBasico_inflexion,phAguaBasico_mayor
                                                    ,pH,1)