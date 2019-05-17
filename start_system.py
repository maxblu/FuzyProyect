from func_membre_and_inverse import *
import math
import plot_membership
import matplotlib.pyplot as plt
from plot_agregations import plot_agregations,plot_results
from defuzzyficationMethods import defuzzify

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
    valores_ropa =np.arange(0,15,0.5)
    valores_pH =np.arange(0,15,0.5)
    valores_detergente =np.arange(0,301,0.5)
    valores_agua =np.arange(0,61,0.5)

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

    print(a2)

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
    #activations no es mas que la funcion concecuente cortado por el valor logico de aplicar las reglas 
    cantDeAguaPoca=max(cantDeAguaPoca2,cantDeAguaPoca3)
    a1_activation=np.fmin(cantDeAguaPoca,a1)
    
    cantDeAguaMedia=max(cantDeAguaMedia1,cantDeAguaMedia5,cantDeAguaMedia6)
    a2_activation=np.fmin(cantDeAguaMedia,a2)


    cantDeAguaMucha=max(cantDeAguaMucha4,cantDeAguaMucha7,cantDeAguaMucha8,cantDeAguaMucha9)
    a3_activation=np.fmin(cantDeAguaMucha,a3)



    cantDetergPoco=max(cantDetergPoco3,cantDetergPoco6,cantDetergPoco9)
    d1_activation=np.fmin(cantDetergPoco,d1)
    
    cantDetergMedia=max(cantDetergMedia2,cantDetergMedia5,cantDeAguaMedia6,cantDetergMedia8)
    d2_activation=np.fmin(cantDetergMedia,d2)

    cantDetergMucha=max(cantDetergMucha1,cantDetergMucha4,cantDetergMucha7)
    d3_activation=np.fmin(cantDetergMucha,d3)

    #Agregaciones Mandami
    plot_agregations(valores_agua,a1,a2,a3,a1_activation,a2_activation,a3_activation,'detergente-mandami')
    plot_agregations(valores_detergente,d1,d2,d3,d1_activation,d2_activation,d3_activation,'agua-mandami')

    #Funcion final de la agregacion para la defusification
    cantDeterg_fun=np.fmax(d1_activation,np.fmax(d2_activation,d3_activation))
    cantDeAgua_fun=np.fmax(a1_activation,np.fmax(a2_activation,a3_activation))

    #Defuzification
    defuzz1=defuzzify(valores_detergente,cantDeterg_fun,'centroide')
    defuzz2=defuzzify(valores_detergente,cantDeterg_fun,'biseccion')
    defuzz3=defuzzify(valores_detergente,cantDeterg_fun,'mai')
    defuzz4=defuzzify(valores_detergente,cantDeterg_fun,'mad')
    defuzz5=defuzzify(valores_detergente,cantDeterg_fun,'mdm')

    defuzz1a=defuzzify(valores_agua,cantDeAgua_fun,'centroide')
    defuzz2a=defuzzify(valores_agua,cantDeAgua_fun,'biseccion')
    defuzz3a=defuzzify(valores_agua,cantDeAgua_fun,'mai')
    defuzz4a=defuzzify(valores_agua,cantDeAgua_fun,'mad')
    defuzz5a=defuzzify(valores_agua,cantDeAgua_fun,'mdm')



    print('Resultados usando centroide')
    print('Cantidad de detergente: ',defuzz1)
    print('Cantidad de agua: ',defuzz1a)

    print('\nResultados usando biseccion')
    print('Cantidad de detergente: ',defuzz2)
    print('Cantidad de agua: ',defuzz2a)
    
    print('\nResultados usando maximo a la izquierda ')
    print('Cantidad de detergente: ',defuzz3)
    print('Cantidad de agua: ',defuzz3a)
    
    print('\nResultados usando maximo a la derecha ')
    print('Cantidad de detergente: ',defuzz4)
    print('Cantidad de agua: ',defuzz4a)
    
    print('\nResultados usando media de los maximos')
    print('Cantidad de detergente: ',defuzz5)
    print('Cantidad de agua: ',defuzz5a)


    grade1 = membership(valores_detergente, cantDeterg_fun, defuzz1)
    grade2 = membership(valores_detergente, cantDeterg_fun, defuzz2)
    grade3= membership(valores_detergente, cantDeterg_fun, defuzz3)
    grade4= membership(valores_detergente, cantDeterg_fun, defuzz4)
    grade5= membership(valores_detergente, cantDeterg_fun, defuzz5)

    
    gradea1 = membership(valores_agua,cantDeAgua_fun, defuzz1a)
    gradea2 = membership(valores_agua,cantDeAgua_fun, defuzz2a)
    gradea3= membership (valores_agua, cantDeAgua_fun, defuzz3a)
    gradea4= membership (valores_agua, cantDeAgua_fun, defuzz4a)
    gradea5= membership (valores_agua, cantDeAgua_fun, defuzz5a)

    #plot results
    plot_results(valores_detergente,cantDeterg_fun,defuzz1,defuzz2,defuzz3,defuzz4,defuzz5,grade1,grade2,grade3,grade4,grade5,'Detergente-Mandami')
    plot_results(valores_agua,cantDeAgua_fun,defuzz1a,defuzz2a,defuzz3a,defuzz4a,defuzz5a,gradea1,gradea2,gradea3,gradea4,gradea5,'Agua-Mandami')
    
    #LARSEN
    #Funciones scaladas
    a1_activation=cantDeAguaPoca * a1     
    a2_activation=cantDeAguaMedia * a2
    a3_activation=cantDeAguaMucha * a3
    d1_activation=cantDetergPoco * d1    
    d2_activation=cantDetergMedia * d2
    d3_activation=cantDetergMucha * d3

    #Agregaciones Larsen
    plot_agregations(valores_agua,a1,a2,a3,a1_activation,a2_activation,a3_activation,'detergente-larsen')
    plot_agregations(valores_detergente,d1,d2,d3,d1_activation,d2_activation,d3_activation,'agua-larsen')

    #Funcion final de la agregacion para la defusification
    cantDeterg_fun=np.fmax(d1_activation,np.fmax(d2_activation,d3_activation))
    cantDeAgua_fun=np.fmax(a1_activation,np.fmax(a2_activation,a3_activation))

    #Defuzification
    defuzz1=defuzzify(valores_detergente,cantDeterg_fun,'centroide')
    defuzz2=defuzzify(valores_detergente,cantDeterg_fun,'biseccion')
    defuzz3=defuzzify(valores_detergente,cantDeterg_fun,'mai')
    defuzz4=defuzzify(valores_detergente,cantDeterg_fun,'mad')
    defuzz5=defuzzify(valores_detergente,cantDeterg_fun,'mdm')

    defuzz1a=defuzzify(valores_agua,cantDeAgua_fun,'centroide')
    defuzz2a=defuzzify(valores_agua,cantDeAgua_fun,'biseccion')
    defuzz3a=defuzzify(valores_agua,cantDeAgua_fun,'mai')
    defuzz4a=defuzzify(valores_agua,cantDeAgua_fun,'mad')
    defuzz5a=defuzzify(valores_agua,cantDeAgua_fun,'mdm')



    print('\nResultados usando centroide')
    print('Cantidad de detergente: ',defuzz1)
    print('Cantidad de agua: ',defuzz1a)

    print('\nResultados usando biseccion')
    print('Cantidad de detergente: ',defuzz2)
    print('Cantidad de agua: ',defuzz2a)
    
    print('\nResultados usando maximo a la izquierda ')
    print('Cantidad de detergente: ',defuzz3)
    print('Cantidad de agua: ',defuzz3a)
    
    print('\nResultados usando maximo a la derecha ')
    print('Cantidad de detergente: ',defuzz4)
    print('Cantidad de agua: ',defuzz4a)
    
    print('\nResultados usando media de los maximos')
    print('Cantidad de detergente: ',defuzz5)
    print('Cantidad de agua: ',defuzz5a)


    grade1 = membership(valores_detergente, cantDeterg_fun, defuzz1)
    grade2 = membership(valores_detergente, cantDeterg_fun, defuzz2)
    grade3= membership(valores_detergente, cantDeterg_fun, defuzz3)
    grade4= membership(valores_detergente, cantDeterg_fun, defuzz4)
    grade5= membership(valores_detergente, cantDeterg_fun, defuzz5)

    
    gradea1 = membership(valores_agua,cantDeAgua_fun, defuzz1a)
    gradea2 = membership(valores_agua,cantDeAgua_fun, defuzz2a)
    gradea3= membership (valores_agua, cantDeAgua_fun, defuzz3a)
    gradea4= membership (valores_agua, cantDeAgua_fun, defuzz4a)
    gradea5= membership (valores_agua, cantDeAgua_fun, defuzz5a)

    #plot results
    plot_results(valores_detergente,cantDeterg_fun,defuzz1,defuzz2,defuzz3,defuzz4,defuzz5,grade1,grade2,grade3,grade4,grade5,'Detergente-Larsen')
    plot_results(valores_agua,cantDeAgua_fun,defuzz1a,defuzz2a,defuzz3a,defuzz4a,defuzz5a,gradea1,gradea2,gradea3,gradea4,gradea5,'Agua-Larsen')







    print('\nAplicando Tsukamoto:')
    print('Cantidad de detergente: ',tsukamoto_methot(tsukamoto_pairs_deter))
    print('Cantidad de agua: ',tsukamoto_methot( tsukamoto_pairs_agua))



if __name__ == "__main__":
        # start_washing_machine(5,7,True)

        start_washing_machine(4.5,6.5,True)

