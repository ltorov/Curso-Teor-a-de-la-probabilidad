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
def generacion (lam,pobact,edadMuertes):
    pob_siguiente = []
    for i in range (0,len(pobact)):
        if pobact[i] < edadMuertes[i]:
            pob_siguiente.append(pobact[i]+1)
        elif pobact[i]>5: 
            for j in range (0,lam[i]):
                pob_siguiente.append(0)
    return pob_siguiente

""" Simula un proceso de ramificacion de n generaciones en el que cada una se modela con el método generacion.
return = booleano de si muere la población en n generaciones o no
param:
    lam = lamba o el número de crías por individuos
    n = número de generaciones
    pobact = lista de la población de osos en esa generación

"""
def ramificacion(lam,n,pobact):
    pobramificacion = []
    pobmuere = False
    for i in range (0,n):
        if len(pobact) == 0:
            pobmuere = True
            return pobmuere
        pobramificacion = generacion(lam,pobact)
        pobact = pobramificacion
    return pobmuere
        
    
"""Corre un número determinado (número de intentos) de procesos de ramificación con n, el numero de generaciones
 return = promedio de poblaciones extinctas, para aproximar probabilidad de extincion
 param:
    lam = lamba o el número de crías por individuos
    n = número de generaciones
    num_intentos =
"""
def probExtincion (lam,n,num_intentos,pobAct):
    results = 0
    for i in range (0, n):
        pobMuere = ramificacion (lam,n,pobAct)
        if pobMuere:
            results +=1
    return float (results)/num_intentos 
            
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

# lam genera un numero regido por la distribución Normal(2,0.5), la cual siguen los osos de anteojos
n = 10
intentos = 1000
poblacionInicial = 500
numTemporal = 2000

pob_muerte = controlador(positivisador(np.random.normal(22,9,numTemporal)))
pob_act = positivisador(np.random.normal(12,6,numTemporal))

lam =  np.random.normal(2, 0.5, numTemporal)
count, bins, ignored = plt.hist(pob_muerte, 20, normed=True)

# Plot the distribution curve
plt.plot(bins, 1/(7 * np.sqrt(2 * np.pi)) *
    np.exp( - (bins - 25)*2 / (2 * 7*2) ),       linewidth=3, color='y')
plt.show()

count2, bins2, ignored2 = plt.hist(pob_act, 20, normed=True)
plt.plot(bins2, 1/(7 * np.sqrt(2 * np.pi)) *
    np.exp( - (bins2 - 12)*2 / (2 * 7*2) ),       linewidth=3, color='y')
plt.show()


print (pob_muerte)
print (probExtincion(lam,n,intentos,pob_act))
    
"""Trabajo futuro:
    - Ajustar los años de vida de los osos.
    - Ajustar la tasa de muerte de los osos.
    - Separar la población de osos entre fertiles y no fertiles.
    - Cambiar población inicial a la de los osos actualmente.
    - Plottear
    - Mejorar eficiencia
    - Tener en cuenta la probabilidad de tener cada número de hijos.
 """