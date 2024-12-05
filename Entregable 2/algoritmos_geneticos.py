
import random

# Inicializar la población con soluciones aleatorias
def inicializar_poblacion(tamano, num_zonas, max_trabajadores, max_energia):
    return [
        [random.randint(1, max_trabajadores) for _ in range(num_zonas)]
        + [random.randint(1, max_energia) for _ in range(num_zonas)]
        for _ in range(tamano)
    ]

# Evaluar el fitness de una solución
def evaluar_fitness(solucion, especia_por_trabajador, especia_por_energia):
    trabajadores = solucion[:len(solucion)//2]
    energia = solucion[len(solucion)//2:]
    especia_recolectada = sum(t * especia_por_trabajador + e * especia_por_energia
                              for t, e in zip(trabajadores, energia))
    return especia_recolectada

# Selección de las mejores soluciones
def seleccion(poblacion, fitness, num_seleccionados):
    poblacion_ordenada = sorted(zip(poblacion, fitness), key=lambda x: x[1], reverse=True)
    return [individuo[0] for individuo in poblacion_ordenada[:num_seleccionados]]

# Cruce de dos soluciones
def cruce(solucion1, solucion2):
    punto_cruce = random.randint(1, len(solucion1) - 1)
    hijo = solucion1[:punto_cruce] + solucion2[punto_cruce:]
    return hijo

# Mutación de una solución
def mutacion(solucion, max_trabajadores, max_energia):
    index = random.randint(0, len(solucion) - 1)
    if index < len(solucion) // 2:
        solucion[index] = random.randint(1, max_trabajadores)
    else:
        solucion[index] = random.randint(1, max_energia)
    return solucion

# Algoritmo genético con opción de elitismo
def algoritmo_genetico_general(num_generaciones, tamano_poblacion, num_zonas, max_trabajadores, max_energia,
                               especia_por_trabajador, especia_por_energia, probabilidad_mutacion, usar_elitismo=False, num_elitismo=0):
    poblacion = inicializar_poblacion(tamano_poblacion, num_zonas, max_trabajadores, max_energia)
    for _ in range(num_generaciones):
        fitness = [evaluar_fitness(sol, especia_por_trabajador, especia_por_energia) for sol in poblacion]
        seleccionados = seleccion(poblacion, fitness, tamano_poblacion // 2)
        
        # Elitismo opcional
        elite = seleccion(poblacion, fitness, num_elitismo) if usar_elitismo else []
        
        nueva_poblacion = elite  # Agregar las soluciones de élite si el elitismo está habilitado
        while len(nueva_poblacion) < tamano_poblacion:
            padre1, padre2 = random.sample(seleccionados, 2)
            hijo = cruce(padre1, padre2)
            if random.random() < probabilidad_mutacion:
                hijo = mutacion(hijo, max_trabajadores, max_energia)
            nueva_poblacion.append(hijo)
        poblacion = nueva_poblacion
    
    fitness_final = [evaluar_fitness(sol, especia_por_trabajador, especia_por_energia) for sol in poblacion]
    mejor_solucion = poblacion[fitness_final.index(max(fitness_final))]
    return mejor_solucion, max(fitness_final)

# Mostrar resultados del algoritmo genético
def mostrar_resultados():
    # Parámetros del problema
    num_generaciones = 50
    tamano_poblacion = 20
    num_zonas = 5
    max_trabajadores = 10
    max_energia = 10
    especia_por_trabajador = 2
    especia_por_energia = 1
    probabilidad_mutacion = 0.1

    # Ejecutar el algoritmo genético sin elitismo
    mejor_solucion_sin_elitismo, mejor_fitness_sin_elitismo = algoritmo_genetico_general(
        num_generaciones, tamano_poblacion, num_zonas, max_trabajadores, max_energia,
        especia_por_trabajador, especia_por_energia, probabilidad_mutacion, usar_elitismo=False
    )

    # Ejecutar el algoritmo genético con elitismo
    mejor_solucion_con_elitismo, mejor_fitness_con_elitismo = algoritmo_genetico_general(
        num_generaciones, tamano_poblacion, num_zonas, max_trabajadores, max_energia,
        especia_por_trabajador, especia_por_energia, probabilidad_mutacion, usar_elitismo=True, num_elitismo=2
    )

    # Mostrar resultados
    print("Resultados del Algoritmo Genético:")
    print("\nSin elitismo:")
    print(f"- Mejor solución: {mejor_solucion_sin_elitismo}")
    print(f"- Fitness: {mejor_fitness_sin_elitismo}")

    print("\nCon elitismo:")
    print(f"- Mejor solución: {mejor_solucion_con_elitismo}")
    print(f"- Fitness: {mejor_fitness_con_elitismo}")

# Ejecutar el programa
mostrar_resultados()

"""
 Posibles mejoras adicionales:
-Diversidad genética inicial: asegurar que la población inicial tenga una amplia variedad de 
combinaciones para explorar mejor el espacio de búsqueda.
Mutación adaptativa: reducir la probabilidad de mutación a medida que aumenta el número de 
generaciones para centrarse en la explotación de soluciones prometedoras.
"""