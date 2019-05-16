from func_membre_and_inverse import *
import math
import plot_membership
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
                                                                        pesoRopaLigero_mayor],1)
    p2=funcion_membrecia_triangular(valores_ropa,[pesoRopaMitad_mi,pesoRopaMitad_optimo,pesoRopaMitad_mayor])

    p3=funcion_membrecia_trapezoidal(valores_ropa,[pesoRopaPesado_min,pesoRopaPesado_inflexion,
                                                                            pesoRopaPesado_inflexion,pesoRopaPesado_mayor],0)

    ph1=funcion_membrecia_trapezoidal(valores_pH,[phAguaAcido_min,phAguaAcido_inflexion,phAguaAcido_inflexion,phAguaAcido_mayor],1)
    ph2=funcion_membrecia_triangular(valores_pH,[phAguaNeutro_min,phAguaNeutro_optimo,phAguaNeutro_mayor])
    ph3=funcion_membrecia_trapezoidal(valores_pH,[phAguaBasico_min,phAguaBasico_inflexion,phAguaBasico_inflexion,phAguaBasico_mayor],0)

    d1=funcion_membrecia_trapezoidal(valores_detergente,[cantDetergPoco_min,cantDetergPoco_inflexion,cantDetergPoco_inflexion,cantDetergPoco_mayor],1)
    d2=funcion_membrecia_triangular(valores_detergente,[cantDetergMedia_min,cantDetergMedia_optimo,cantDetergMedia_mayor])
    d3=funcion_membrecia_trapezoidal(valores_detergente,[cantDetergMucho_min,cantDetergMucho_inflexion,cantDetergMucho_inflexion,cantDetergMucho_mucho],0)

    a1=funcion_membrecia_trapezoidal(valores_agua,[cantDeAguaPoca_min,cantDeAguaPoca_inflexion,cantDeAguaPoca_inflexion,cantDeAguaPoca_mayor],1)
    a2=funcion_membrecia_triangular(valores_agua,[cantDeAguaMedia_min,cantDeAguaMedia_optimo,cantDeAguaMedia_mayor])
    a3=funcion_membrecia_trapezoidal(valores_agua,[cantDeAguaMucha_min,cantDeAguaMucha_inflexion,cantDeAguaMucha_inflexion,cantDeAguaMucha_mayor],0)


    #Grado de memebrecia de los valores de la entrada (Fuzification)
    gradoPertenciaRopa_peso_ligera=membership(valores_ropa,p1,pesoRopa)
    gradoPertenciaRopa_peso_medio=membership(valores_ropa,p2,pesoRopa)
    gradoPertenciaRopa_peso_pesado=membership(valores_ropa,p3,pesoRopa)

    print('Grado de pernencia para peso de ropa:')
    print(gradoPertenciaRopa_peso_ligera)
    print(gradoPertenciaRopa_peso_medio)
    print(gradoPertenciaRopa_peso_pesado)

    gradoPertencia_pH_acido=membership(valores_pH,ph1,pH)
    gradoPertencia_pH_neutral=membership(valores_pH,ph2,pH)
    gradoPertencia_pH_basico=membership(valores_pH,ph3,pH)

    print('\nGrado de pernencia para pH: ')
    print(gradoPertencia_pH_acido)
    print(gradoPertencia_pH_neutral)
    print(gradoPertencia_pH_basico)

    #Ploteo de las funciones de membrecia
    plot_membership.plot_funtions(valores_ropa,p1,p2,p3,valores_pH,ph1,ph2,ph3,valores_detergente,d1,d2,d3,valores_agua,a1,a2,a3)
    

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
    zi=inverse_membership(valores_detergente,d3,antecedente1)[0]
    tsukamoto_pairs_deter.append((antecedente1,zi))

    cantDeAguaMedia1=antecedente1
    zi=inverse_membership(valores_agua,a2,antecedente1)[0]
    tsukamoto_pairs_agua.append((antecedente1,zi))
    

    #2
    antecedente2=min( gradoPertencia_pH_neutral,gradoPertenciaRopa_peso_ligera  )
    cantDetergMedia2=cantDeAguaPoca2=antecedente2

    zi =inverse_membership(valores_detergente,d2,antecedente2)[0]
    tsukamoto_pairs_deter.append((antecedente2,zi))

    zi=inverse_membership(valores_agua,a1,antecedente2)[0]
    tsukamoto_pairs_agua.append((antecedente2,zi))


    #3
    antecedente3=min(gradoPertencia_pH_basico,gradoPertenciaRopa_peso_ligera )
    cantDeAguaPoca3=cantDetergPoco3=antecedente3

    zi=inverse_membership(valores_detergente,d1,antecedente3)[0]
    tsukamoto_pairs_deter.append((antecedente3,zi))

    zi=inverse_membership(valores_agua,a1,antecedente3)[0]
    tsukamoto_pairs_agua.append((antecedente3,zi))


    #4
    antecedente4=min( gradoPertencia_pH_acido,gradoPertenciaRopa_peso_medio)
    cantDeAguaMucha4=cantDetergMucha4=antecedente4

    zi=inverse_membership(valores_detergente,d3,antecedente4)[0]
    tsukamoto_pairs_deter.append((antecedente4,zi))

    zi=inverse_membership(valores_agua,a3,antecedente4)[0]
    tsukamoto_pairs_agua.append((antecedente4,zi))




    #5
    antecedente5=min( gradoPertencia_pH_neutral,gradoPertenciaRopa_peso_medio)
    cantDetergMedia5=cantDeAguaMedia5=antecedente5

    zi =inverse_membership(valores_detergente,d2,antecedente5)[0]
    tsukamoto_pairs_deter.append((antecedente5,zi))

    zi=inverse_membership(valores_agua,a2,antecedente5)[0]
    tsukamoto_pairs_agua.append((antecedente5,zi))



    #6
    antecedente6=min(gradoPertencia_pH_basico,gradoPertenciaRopa_peso_medio)
    cantDetergPoco6=cantDeAguaMedia6=antecedente6

    zi=inverse_membership(valores_detergente,d1,antecedente6)[0]
    tsukamoto_pairs_deter.append((antecedente6,zi))


    zi=inverse_membership(valores_agua,a2,antecedente6)[0]
    tsukamoto_pairs_agua.append((antecedente6,zi))

    #7
    antecedente7 =min (gradoPertencia_pH_acido,gradoPertenciaRopa_peso_pesado )
    cantDetergMucha7=cantDeAguaMucha7=antecedente7

    zi=inverse_membership(valores_detergente,d3,antecedente7)[0]
    tsukamoto_pairs_deter.append((antecedente7,zi))

    zi=inverse_membership(valores_agua,a3,antecedente7)[0]
    tsukamoto_pairs_agua.append((antecedente7,zi))



    #8
    antecedente8= min (gradoPertencia_pH_neutral,gradoPertenciaRopa_peso_pesado)
    cantDetergMedia8=cantDeAguaMucha8=antecedente8

    zi =inverse_membership(valores_detergente,d2,antecedente8)[0]
    tsukamoto_pairs_deter.append((antecedente8,zi))


    zi=inverse_membership(valores_agua,a3,antecedente8)[0]
    tsukamoto_pairs_agua.append((antecedente8,zi))


    #9
    antecedente9=min(gradoPertencia_pH_basico,gradoPertenciaRopa_peso_pesado) 
    cantDetergPoco9=cantDeAguaMucha9=antecedente9

    zi=inverse_membership(valores_detergente,d1,antecedente9)[0]
    tsukamoto_pairs_deter.append((antecedente9,zi))

    zi=inverse_membership(valores_agua,a3,antecedente9)[0]
    tsukamoto_pairs_agua.append((antecedente9,zi))

    #Aplicando el valor al consecuente(Revisar aqui si me quedo con el min o el max)
    cantDeAguaPoca=max(cantDeAguaPoca2,cantDeAguaPoca3)
    cantDeAguaMedia=max(cantDeAguaMedia1,cantDeAguaMedia5,cantDeAguaMedia6)
    cantDeAguaMucha=max(cantDeAguaMucha4,cantDeAguaMucha7,cantDeAguaMucha8,cantDeAguaMucha9)

    cantDetergPoco=max(cantDetergPoco3,cantDetergPoco6,cantDetergPoco9)
    cantDetergMedia=max(cantDetergMedia2,cantDetergMedia5,cantDeAguaMedia6,cantDetergMedia8)
    cantDetergMucha=max(cantDetergMucha1,cantDetergMucha4,cantDetergMucha7)

    print(tsukamoto_pairs_deter)

    print(tsukamoto_pairs_deter)
    if tsukamoto:
        print('Cantidad de detergente: ',tsukamoto_methot(tsukamoto_pairs_deter))
        print('Cantidad de agua: ',tsukamoto_methot( tsukamoto_pairs_agua))



if __name__ == "__main__":
        # start_washing_machine(5,7,True)

        start_washing_machine(10,1,True)

