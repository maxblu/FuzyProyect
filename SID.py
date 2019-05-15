from funciones_de_membrecia import *
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
    
    # max_pH_class=min(gradoPertencia_pH_acido,gradoPertencia_pH_neutral,gradoPertencia_pH_basico)
    # max_RopaPeso_class=min(gradoPertenciaRopa_peso_ligera,gradoPertenciaRopa_peso_medio,gradoPertenciaRopa_peso_pesado)

    #Determinar dado 
    # class_ph

    #Inicializacion para variables a inferir
    cantDetergPoco=-math.inf
    cantDetergMedia=-math.inf
    cantDetergMucha=-math.inf

    cantDeAguaPoca=-math.inf
    cantDeAguaMedia=-math.inf
    cantDeAguaMucha=-math.inf

    tsukamoto_pairs_deter=[]
    tsukamoto_pairs_agua=[]
    
    #Reglas para la inferencia
    #1
    antecedente1=min(gradoPertencia_pH_acido, gradoPertenciaRopa_peso_ligera )
    cantDetergMucha1=antecedente1
    zi=funcion_membrecia_trapezoidal_inversa(cantDetergMucho_min,cantDetergMucho_inflexion,cantDetergMucho_mucho,cantDetergMucha1,tipo=0)
    tsukamoto_pairs_deter.append((antecedente1,zi))

    cantDeAguaMedia1=antecedente1
    zi=funcion_membrecia_triangular_inversa(cantDeAguaMedia_min,cantDeAguaMedia_optimo,cantDeAguaMedia_mayor,antecedente1,0)
    tsukamoto_pairs_agua.append((antecedente1,zi))
    

    #2
    antecedente2=min( gradoPertencia_pH_neutral,gradoPertenciaRopa_peso_ligera  )
    cantDetergMedia2=cantDeAguaPoca2=antecedente2

    zi =funcion_membrecia_triangular_inversa(cantDetergMedia_min,cantDetergMedia_optimo,cantDetergMedia_mayor,antecedente2,0)
    tsukamoto_pairs_deter.append((antecedente2,zi))

    zi=funcion_membrecia_trapezoidal_inversa(cantDeAguaPoca_min,cantDeAguaPoca_inflexion,cantDeAguaPoca_mayor,antecedente2,0)
    tsukamoto_pairs_agua.append((antecedente2,zi))


    #3
    antecedente3=min(gradoPertencia_pH_basico,gradoPertenciaRopa_peso_ligera )
    cantDeAguaPoca3=cantDetergPoco3=antecedente3

    zi=funcion_membrecia_trapezoidal_inversa(cantDetergPoco_min,cantDetergPoco_inflexion,cantDetergMucho_mucho,antecedente3,0)
    tsukamoto_pairs_deter.append((antecedente3,zi))

    zi=funcion_membrecia_trapezoidal_inversa(cantDeAguaPoca_min,cantDeAguaPoca_inflexion,cantDeAguaPoca_mayor,antecedente3,0)
    tsukamoto_pairs_agua.append((antecedente3,zi))


    #4
    antecedente4=min( gradoPertencia_pH_acido,gradoPertenciaRopa_peso_medio)
    cantDeAguaMucha4=cantDetergMucha4=antecedente4

    zi=funcion_membrecia_trapezoidal_inversa(cantDetergMucho_min,cantDetergMucho_inflexion,cantDetergMucho_mucho,antecedente4,tipo=0)
    tsukamoto_pairs_deter.append((antecedente4,zi))

    zi=funcion_membrecia_trapezoidal_inversa(cantDeAguaMucha_min,cantDeAguaMucha_inflexion,cantDeAguaMucha_mayor,antecedente4,0)
    tsukamoto_pairs_agua.append((antecedente4,zi))




    #5
    antecedente5=min( gradoPertencia_pH_neutral,gradoPertenciaRopa_peso_medio)
    cantDetergMedia5=cantDeAguaMedia5=antecedente5

    zi =funcion_membrecia_triangular_inversa(cantDetergMedia_min,cantDetergMedia_optimo,cantDetergMedia_mayor,antecedente5,0)
    tsukamoto_pairs_deter.append((antecedente5,zi))

    zi=funcion_membrecia_triangular_inversa(cantDeAguaMedia_min,cantDeAguaMedia_optimo,cantDeAguaMedia_mayor,antecedente5,0)
    tsukamoto_pairs_agua.append((antecedente5,zi))



    #6
    antecedente6=min(gradoPertencia_pH_basico,gradoPertenciaRopa_peso_medio)
    cantDetergPoco6=cantDeAguaMedia6=antecedente6

    zi=funcion_membrecia_trapezoidal_inversa(cantDetergPoco_min,cantDetergPoco_inflexion,cantDetergMucho_mucho,antecedente6,0)
    tsukamoto_pairs_deter.append((antecedente6,zi))


    zi=funcion_membrecia_triangular_inversa(cantDeAguaMedia_min,cantDeAguaMedia_optimo,cantDeAguaMedia_mayor,antecedente6,0)
    tsukamoto_pairs_agua.append((antecedente6,zi))

    #7
    antecedente7 =min (gradoPertencia_pH_acido,gradoPertenciaRopa_peso_pesado )
    cantDetergMucha7=cantDeAguaMucha7=antecedente7

    zi=funcion_membrecia_trapezoidal_inversa(cantDetergMucho_min,cantDetergMucho_inflexion,cantDetergMucho_mucho,antecedente7,0)
    tsukamoto_pairs_deter.append((antecedente7,zi))

    zi=funcion_membrecia_trapezoidal_inversa(cantDeAguaMucha_min,cantDeAguaMucha_inflexion,cantDeAguaMucha_mayor,antecedente7,0)
    tsukamoto_pairs_agua.append((antecedente7,zi))



    #8
    antecedente8= min (gradoPertencia_pH_neutral,gradoPertenciaRopa_peso_pesado)
    cantDetergMedia8=cantDeAguaMucha8=antecedente8

    zi =funcion_membrecia_triangular_inversa(cantDetergMedia_min,cantDetergMedia_optimo,cantDetergMedia_mayor,antecedente8,0)
    tsukamoto_pairs_deter.append((antecedente8,zi))


    zi=funcion_membrecia_trapezoidal_inversa(cantDeAguaMucha_min,cantDeAguaMucha_inflexion,cantDeAguaMucha_mayor,antecedente8,0)
    tsukamoto_pairs_agua.append((antecedente8,zi))


    #9
    antecedente9=min(gradoPertencia_pH_basico,gradoPertenciaRopa_peso_pesado) 
    cantDetergPoco9=cantDeAguaMucha9=antecedente9

    zi=funcion_membrecia_trapezoidal_inversa(cantDetergPoco_min,cantDetergPoco_inflexion,cantDetergMucho_mucho,antecedente9,0)
    tsukamoto_pairs_deter.append((antecedente9,zi))

    zi=funcion_membrecia_trapezoidal_inversa(cantDeAguaMucha_min,cantDeAguaMucha_inflexion,cantDeAguaMucha_mayor,antecedente9,0)
    tsukamoto_pairs_agua.append((antecedente9,zi))

    #Aplicando el valor al consecuente(Revisar aqui si me quedo con el min o el max)
    cantDeAguaPoca=max(cantDeAguaPoca2,cantDeAguaPoca3)
    cantDeAguaMedia=max(cantDeAguaMedia1,cantDeAguaMedia5,cantDeAguaMedia6)
    cantDeAguaMucha=max(cantDeAguaMucha4,cantDeAguaMucha7,cantDeAguaMucha8,cantDeAguaMucha9)

    cantDetergPoco=max(cantDetergPoco3,cantDetergPoco6,cantDetergPoco9)
    cantDetergMedia=max(cantDetergMedia2,cantDetergMedia5,cantDeAguaMedia6,cantDetergMedia8)
    cantDetergMucha=max(cantDetergMucha1,cantDetergMucha4,cantDetergMucha7)

    if tsukamoto:
        print(tsukamoto_pairs_deter)

        print(tsukamoto_pairs_agua)
        
        detergent_prdiction=tsukamoto_methot(tsukamoto_pairs_deter)
        agua_prediction= tsukamoto_methot(tsukamoto_pairs_agua)

        print('Cantidad de detergente '+ str(detergent_prdiction)+' gramos')
        print('Cantidad de agua '+ str(agua_prediction)+" litros")

if __name__ == "__main__":
    start_washing_machine(10,5,True)
