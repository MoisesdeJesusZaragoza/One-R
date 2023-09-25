import one_r
import pandas

def main():
    dataset = pandas.read_csv('golf-dataset-categorical.csv')
    nombre_columna_clase = 'Play'

    dataset_entrenamiento = dataset.sample(frac=.7)
    dataset_prueba = dataset.drop(dataset_entrenamiento.index)
    
    print('\nDatos de entrenamiento (70%)')
    print(dataset_entrenamiento)

    atributo, modelo = one_r.entrenar(dataset_entrenamiento, nombre_columna_clase)
        
    print('\nDatos de prueba (30%)')
    print(dataset_prueba)
    
    one_r.probar(dataset_prueba, nombre_columna_clase, atributo, modelo)
    

if __name__ == '__main__':
    main()