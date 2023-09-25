def entrenar(dataset_entrenamiento, nombre_columna_clase):
    print('\nEntrenando...')
    columna_clase = dataset_entrenamiento[nombre_columna_clase]
    dataset_entrenamiento = dataset_entrenamiento.drop(columns=nombre_columna_clase)
    valores_clase = columna_clase.unique()

    print('Generando tabla de frecuencias...')
    tabla_frecuencias = {}
    for columna in dataset_entrenamiento.columns:
        tabla_frecuencias[columna] = {}
        valor_clase = tuple(zip(dataset_entrenamiento[columna], columna_clase))
        for valor, clase_esperada in valor_clase:
            if valor not in tabla_frecuencias[columna].keys():
                tabla_frecuencias[columna][valor] = {}
                for clase in valores_clase:
                    tabla_frecuencias[columna][valor][clase] = 0
            tabla_frecuencias[columna][valor][clase_esperada] += 1

    print('Calculando errores de reglas...')
    errores_reglas = {}
    for columna in tabla_frecuencias:
        errores_reglas[columna] = {}
        numerador_total = 0
        denominador = 0
        for fila in tabla_frecuencias[columna]:
            errores_reglas[columna][fila] = {}
            numerador = 0
            errores = 0
            cantidad_clase = 0
            for profundidad in tabla_frecuencias[columna][fila]:
                denominador = denominador + tabla_frecuencias[columna][fila][profundidad]
                if numerador < tabla_frecuencias[columna][fila][profundidad]:
                    numerador = tabla_frecuencias[columna][fila][profundidad]
                cantidad_clase = cantidad_clase + tabla_frecuencias[columna][fila][profundidad]
            errores = cantidad_clase - numerador
            numerador_total = numerador_total + errores
        error_total = numerador_total / denominador
        errores_reglas[columna] = error_total

    atributo_menor_error = ''
    menor_error = 2
    for columna in errores_reglas:
        if errores_reglas[columna] < menor_error:
            menor_error = errores_reglas[columna]
            atributo_menor_error = columna
            
    print('\nPorcentaje de error de las reglas:')
    print(errores_reglas)

    print('\nGenerando regla con menor error...')
    reglas = {}
    for columna in tabla_frecuencias:
        if columna == atributo_menor_error:
            for fila in tabla_frecuencias[columna]:
                reglas[fila] = {}
                clase_dominante = ''
                contador = 0
                for profundidad in tabla_frecuencias[columna][fila]:
                    if contador < tabla_frecuencias[columna][fila][profundidad]:
                        contador = tabla_frecuencias[columna][fila][profundidad]
                        clase_dominante = profundidad
                reglas[fila] = clase_dominante

    print('\nAtributo con menor error: ', atributo_menor_error)
    print('Reglas:')
    for valor in reglas:
        print('If', atributo_menor_error, ' = ', valor, ' -> ', nombre_columna_clase, ' = ', reglas[valor])

    return atributo_menor_error, reglas

def probar(dataset_prueba, nombre_columna_clase, atributo, modelo):
    print('\nProbando...\n')
    columna_atributo = dataset_prueba[atributo]
    columna_clase = dataset_prueba[nombre_columna_clase]
    valor_clase = tuple(zip(columna_atributo, columna_clase))
    
    aciertos = 0
    num_instancias = 0
    for valor, clase in valor_clase:
        for valor_modelo in modelo:
            if valor == valor_modelo:
                num_instancias += 1
                if modelo[valor_modelo] == clase:
                    aciertos += 1
                    print('Valor espereado: ', clase, '| Valor estimado: ', modelo[valor_modelo], ' -> ', 'ACIERTO')
                else:
                    print('Valor espereado: ', clase, '| Valor estimado: ', modelo[valor_modelo], ' -> ', 'ERROR')
    
    exactitud = aciertos / num_instancias
    porcentaje = int(exactitud*100)

    print('\nEl modelo tiene una exactitud de: ', exactitud, ' | ', porcentaje, '%')
