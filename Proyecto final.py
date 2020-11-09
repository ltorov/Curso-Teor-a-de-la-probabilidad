#!/usr/bin/env python3
# -- coding: utf-8 --

import numpy as np
import random
import pandas as pd
import matplotlib.pylab as plt
from matplotlib import colors as mcolors


"""Simula la poisson(lambda), un proceso de ramificación para n generaciones
 return = lista de tamaño de poblaciones en cada generación
 param:
    lam = lamba o el número de crías por individuos
    n = número de generaciones
    población inicial = 
"""
def ramificacion(lam, n, poblacionInicial):
	lista = [poblacionInicial]
	for i in range(1,n):
		x = 0
		if lista[i-1] > 0:
			for i in range(lista[i-1]):
				x += np.random.poisson(lam)
		lista.append(x)
	return lista

"""Determina si un grupo se extinguirá
Si el tamaño de la última generación es zero, return=True
 param:
     lista = 
"""
def poblacion_muere(lista):
	poblacion_final = lista[len(lista)-1]
	if poblacion_final == 0:
		return True
	return False

"""Corre un proceso de ramificación para un numero de intentos, con n, el numero de generaciones
 return = promedio de poblaciones extinctas, para aproximar probabilidad de extincion
 param:
    lam = lamba o el número de crías por individuos
    n = número de generaciones
    num_intentos =
"""
def prob_extincion(lam,n,num_intentos):
	results = 0
	for i in range(0,num_intentos):
		poblacion_tiempo = ramificacion(lam,n, poblacionInicial)

		if poblacion_muere(poblacion_tiempo):
			results += 1

	return float(results)/num_intentos

# a genera un numero aleatorio entre 2 y 4 debido a que los osos de anteojos tienen entre 2 y 4 crías.
a= random.randint(2,4)
n = 10
intentos = 300
poblacionInicial = 1


print (prob_extincion(a,n,intentos))
    
"""Trabajo futuro:
    - Ajustar los años de vida de los osos.
    - Ajustar la tasa de muerte de los osos.
    - Separar la población de osos entre fertiles y no fertiles.
    - Cambiar población inicial a la de los osos actualmente.
    - Plottear
    - Mejorar eficiencia
    - Tener en cuenta la probabilidad de tener cada número de hijos.
 """ 