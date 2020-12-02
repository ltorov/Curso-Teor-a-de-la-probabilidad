#!/usr/bin/env python3
# -- coding: utf-8 --

import numpy as np
import random
import pandas as pd
import matplotlib.pylab as plt
from matplotlib import colors as mcolors


""" Simula una generación de osos, teniendo en cuenta la muerte por causas naturales a los 25 años.
También simula para cada generación cierto número de crías por oso, modelada por una distribución normal.
return = lista de tamaño del número de osos con cada posición correspondiente a la edad de ese oso.
param:
    lam = lamba o el número de crías por individuos
    pobact = lista de la población de osos en esa generación

"""
def generacion (pobact,edadMuertes):
    pob_siguiente = []
    muertesHumanos = int(len(pobact)/7)
    media, desviacion = aproxLamba(pobact)
    lam = lamba (media,desviacion ,len(pobact))
    
    for i in range (0,len(pobact)):
        a = random.randint(0,len(edadMuertes))
        if pobact[i] < edadMuertes[a-1]:
            pob_siguiente.append(pobact[i]+1)
        elif pobact[i]>5: 
            if len(lam) == 0:
                continue
            b = random.randint(0,len(lam)-1)
            for j in range (0,int(lam[b])):
                pob_siguiente.append(0)
    pob_final = [0]*(len(pob_siguiente)-muertesHumanos)
    for i in range(0,len(pob_siguiente)-muertesHumanos):
        pob_final[i] = pob_siguiente[i+muertesHumanos]
    return pob_final

""" Simula un proceso de ramificacion de n generaciones en el que cada una se modela con el método generacion.
return = booleano de si muere la población en n generaciones o no
param:
    lam = lamba o el número de crías por individuos
    n = número de generaciones
    pobact = lista de la población de osos en esa generación

"""
def ramificacion(n,pobact, edadMuertes):
    pobramificacion = []
    pob_historica = [0] * n
    pobmuere = False
    for i in range (0,n):
        if len(pobact) <= 40:
            pobmuere = True
            return pobmuere
        pobramificacion = generacion(pobact,edadMuertes)
        pobact = pobramificacion
        pob_historica[i] = len(pobact)
    return pobmuere
        
    
"""Corre un número determinado (número de intentos) de procesos de ramificación con n, el numero de generaciones
 return = promedio de poblaciones extinctas, para aproximar probabilidad de extincion
 param:
    lam = lamba o el número de crías por individuos
    n = número de generaciones
    num_intentos =
"""
def probExtincion (n,num_intentos,pobAct,edadMuertes):
    results = 0
    for i in range (0, num_intentos):
        pobMuere =ramificacion (n,pobAct,edadMuertes)
        if pobMuere:
            results +=1
        
    return float (results)/num_intentos 

def aproxLamba (pobact):
   media = 2
   desviacion = 0.5
   pob = len(pobact)
   if pob <10:
       media =0
       desviacion = 0
   elif pob< 50:
       media = 0.3
       desviacion  = 0.1
   elif pob< 100:
       media = 0.8
       desviacion  = 0.3
   elif pob< 300:
       media = 1.3
       desviacion  = 0.4
   elif pob < 500:
       media = 1.6
       desviacion  = 0.6
   return media, desviacion 
        
    
            
""" Un método auxiliar para que el número de crías o de muertes por oso (lam) siempre sea positivo para que corresponda con la realidad.
return = lista de distribución normal de crías sin números negativos
param: 
    array = lista para quitarle los números negativos.
"""
def positivisador(array):
    cont = 0
    for i in range (0,len(array)):
        if array[i] >= 0:
            cont += 1
    array_new = [0]*cont
    cont2=0
    for i in range (0, len(array)):
        if array[i] >= 0:
            array_new[cont2] = array[i]
            cont2 +=1           
    return array_new

""" Un método auxiliar para que el número de muertes por oso (lam) siempre sea menor que 33 para que corresponda con la realidad.
return = lista de distribución normal de crías sin números mayores a 33
param: 
    array = lista para quitarle los números mayores a 33.
"""
def controlador(array):
    cont = 0
    for i in range (0,len(array)):
        if array[i] <= 33:
            cont += 1
    array_new = [0]*cont
    cont2=0
    for i in range (0, len(array)):
        if array[i] <= 33:
            array_new[cont2] = array[i]
            cont2 +=1           
    return array_new



""" Un método auxiliar que genera tres variables aleatorias.
return:
    pob_muerte = lista con número de la distribución Normal (22, 9 , numTemporal) que muestra las edades en las que mueren
    pob_act = lista con número de la distribución Normal (12, 6 , poblacionInicial) que muestra las edades de los osos en cada generación
    lam = lista con número de la distribución Normal (2, 0.5, numTemporal) que muestra las crías por oso.
"""
def variablesAleatorias ():
    pob_muerte = controlador(positivisador(np.random.normal(22,9,numTemporal)))
    pob_act = positivisador(np.random.normal(12,6,poblacionInicial))
    return pob_muerte, pob_act

def lamba (media, desviacion, intentos):
    lam = positivisador(np.random.normal(media, desviacion, intentos))
    return lam

""" Un método auxiliar que grafica las diferentes distribuciones usadas.
"""
def graficas ():
    count, bins, ignored = plt.hist(pob_muerte, 20, normed=True)
    # Plot the distribution curve
    plt.plot(bins, 1/(7 * np.sqrt(2 * np.pi)) *
    np.exp( - (bins - 25)*2 / (2 * 7*2) ),       linewidth=3, color='y')
    plt.show()
    

    count2, bins2, ignored2 = plt.hist(pob_act, 12, normed=True)
    plt.plot(bins2, 1/(7 * np.sqrt(2 * np.pi)) *
    np.exp( - (bins2 - 12)*2 / (2 * 7*2) ),       linewidth=2, color='y')
    plt.title('Edad población actual')
    plt.xlabel('Edad')
    plt.ylabel('Número de osos')
    plt.show()
    
    
    count3, bins3, ignored3 = plt.hist(lam, 100, normed=False)
    plt.plot(bins3, 1/(7* np.sqrt(3 * np.pi)) *
    np.exp( - (bins2 - 12)*2 / (2 * 7*2) ),       linewidth=2, color='y')
    plt.show()
    
    

n = 40
intentos = 300
poblacionInicial = 11000
numTemporal = 2000
pob_muerte,pob_act = variablesAleatorias()


print (probExtincion(n,intentos,pob_act,pob_muerte))




"""Trabajo futuro:
    - Ajustar los años de vida de los osos.
    - Ajustar la tasa de muerte de los osos.
    - Separar la población de osos entre fertiles y no fertiles.
    - Cambiar población inicial a la de los osos actualmente.
    - Plottear
    - Mejorar eficiencia
    - Tener en cuenta la probabilidad de tener cada número de hijos.
 """