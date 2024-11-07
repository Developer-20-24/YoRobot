import sqlite3
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Obtener los datos históricos de los exámenes
def obtener_datos_examenes():
    conexion = sqlite3.connect('db/usuarios.db')
    cursor = conexion.cursor()

    cursor.execute('''
        SELECT u.id, e.categoria, e.puntaje
        FROM usuarios u
        JOIN examenes_realizados e ON u.id = e.id_usuario
    ''')
    datos = cursor.fetchall()
    conexion.close()
    
    return datos

# Preparar los datos para el modelo de IA
def preparar_datos(datos):
    df = pd.DataFrame(datos, columns=["id_usuario", "categoria", "puntaje"])
    
    # Convertir puntajes en categorías de "fortaleza" o "debilidad"
    df['resultado'] = df['puntaje'].apply(lambda x: 1 if x >= 7 else 0)  # 1: Fortaleza, 0: Debilidad

    # Para el modelo, necesitamos convertir las categorías a variables numéricas
    df['categoria'] = pd.Categorical(df['categoria']).codes

    return df

# Entrenar un modelo de IA
def entrenar_modelo(df):
    X = df[['categoria', 'puntaje']]  # Características (categoría y puntaje)
    y = df['resultado']  # Etiqueta (fortaleza o debilidad)

    # Dividir los datos en entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Entrenar un modelo de Random Forest
    modelo = RandomForestClassifier(n_estimators=100, random_state=42)
    modelo.fit(X_train, y_train)

    # Evaluar el modelo
    y_pred = modelo.predict(X_test)
    print(f"Accuracy: {accuracy_score(y_test, y_pred) * 100:.2f}%")

    return modelo

# Predecir las fortalezas y debilidades para un usuario
def predecir_fortalezas_debilidades(id_usuario, modelo):
    conexion = sqlite3.connect('db/usuarios.db')
    cursor = conexion.cursor()

    cursor.execute('''
        SELECT categoria, puntaje FROM examenes_realizados WHERE id_usuario = ?
    ''', (id_usuario,))
    examenes = cursor.fetchall()
    
    conexion.close()

    # Predecir para cada categoría del usuario
    for categoria, puntaje in examenes:
        categoria_code = pd.Categorical([categoria]).codes[0]
        prediccion = modelo.predict([[categoria_code, puntaje]])

        resultado = "Fortaleza" if prediccion == 1 else "Debilidad"
        print(f"Categoría: {categoria} - Puntaje: {puntaje} - Resultado: {resultado}")

# Función principal para entrenar y predecir
def main():
    # Obtener los datos históricos
    datos = obtener_datos_examenes()
    
    # Preparar los datos para el modelo de IA
    df = preparar_datos(datos)
    
    # Entrenar el modelo
    modelo = entrenar_modelo(df)
    
    # Obtener el usuario y predecir sus fortalezas/debilidades
    correo = input("Ingresa tu correo para analizar tus fortalezas y debilidades: ")
    usuario = obtener_usuario(correo)
    
    if usuario:
        print(f"\nAnálisis de fortalezas y debilidades para {usuario[1]}:")
        predecir_fortalezas_debilidades(usuario[0], modelo)  # Predecir con el ID del usuario
    else:
        print("Usuario no encontrado. Por favor regístrate primero.")

if __name__ == "__main__":
    main()
