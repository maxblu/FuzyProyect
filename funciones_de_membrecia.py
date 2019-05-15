
import skfuzzy as fuzz
import numpy as np
import matplotlib.pyplot as plt

def funcion_membrecia_trapezoidal_pertenencia_skfuzzy_inverse(minimo , inflexion1,inflexion2, mayor,valor,tipo):
    

    if tipo==0:
        x=np.arange(minimo,mayor,1)

        trapecio= fuzz.membership.trapmf(x,[minimo,inflexion1,inflexion1,mayor])
        posibles=fuzz.interp_universe(x,trapecio,valor)
        plt.plot(trapecio)
        plt.show()
        

        return posibles
    else:
        
        x=np.arange(minimo,mayor,1)

        trapecio= fuzz.membership.trapmf(x,[minimo,inflexion1,inflexion2,mayor])
        plt.plot(trapecio)
        plt.show()

        posibles=fuzz.interp_universe(x,trapecio,valor)
        return posibles

def funcion_membrecia_triangular_pertenencia_skfuzzy_inverse(minimo , inflexion, mayor,valor):
    

    x=np.arange(minimo,mayor,1)

    trin= fuzz.membership.trimf(x,[minimo,inflexion,mayor])
    posibles=fuzz.interp_universe(x,trin,valor)
    plt.plot(trin)
    plt.show()
    

    return posibles

def funcion_membrecia_triangular_pertenencia(minimo,optimo,mayor,valor):
    """minimo del intervalo 
       optimo pico del triangulo 
       mayor extremo del intervalo por la derecha
       valor x a evaluar para saber el grado de pertenecia"""
    pendiente1=1/(optimo-minimo)
    pendiente2=-1/(mayor-optimo)

    if minimo>valor or  valor > optimo :
        return 0 
    elif minimo==optimo and valor == minimo :
        return 1
    elif mayor==optimo and valor==mayor :
        return 1
    elif valor <= optimo:
        return 1 - pendiente1*(optimo - valor)
    return -pendiente2(optimo-valor)


def funcion_membrecia_trapezoidal_pertenencia(minimo , inflexion, mayor,valor,direccion):
    """minimo del intervalo 
       inflexion donde el trapecio inicia una subida o bajada  
       mayor extremo del intervalo por la derecha
       valor x a evaluar para saber el grado de pertenecia
       direccion indica si el trapecio tine un recta hacia abajo (0) o hacia arriba(1) """
    #recta descendiente
    if direccion==0:
        pendiente=-1/(mayor-inflexion)
        if valor > mayor :
            return 0
        elif valor >= inflexion and valor < mayor:
            return -pendiente*(inflexion-valor)
        else:
            return 1    

    #recta ascendiente
    else:
        pendiente=1/(inflexion-minimo)

        if valor <= minimo:
            return 0 
        elif valor > minimo and valor <= inflexion:
            return 1 - pendiente*(inflexion - valor)
        else:
            return 1

def funcion_membrecia_triangular_inversa(minimo,optimo,mayor,valor,side):
    """minimo del intervalo 
       optimo pico del triangulo 
       mayor extremo del intervalo por la derecha
       valor y a evaluar para saber el valor para la desdefuzificacion"""
    pendiente1=1/(optimo-minimo)
    pendiente2=-1/(mayor-optimo)

    x1 = optimo - (1 - valor)/pendiente1
    x2 = mayor - (-valor)/pendiente2

    if (minimo == optimo):
            return x2
    if (optimo == mayor):
            return x1

    #minimo a la izquierda
    if side==0:
        return x1
    else :
        return x2

def funcion_membrecia_trapezoidal_inversa(minimo , inflexion, mayor,valor,tipo,inflexion2=-1):
    """minimo del intervalo 
       inflexion donde el trapecio inicia una subida o bajada  
       mayor extremo del intervalo por la derecha
       valor y a evaluar para saber el valor para la desdefuzificacion
       direccion indica si el trapecio tine un recta hacia abajo (0) o hacia arriba(1) """
    if tipo==0:
        pendiente=-1/(mayor-inflexion)
        

        if valor > mayor :
            return 0
        elif valor >= inflexion and valor < mayor:
            return mayor - (-valor)/pendiente
        else:
            #por ahora minimo a la izquierda
            return minimo

    #recta ascendiente
    if tipo ==1:
        pendiente=1/(inflexion-minimo)

        if valor <= minimo:
            return 0 
        elif valor > minimo and valor <= inflexion:
            return 1 - pendiente*(inflexion - valor)
        else:
            return 1