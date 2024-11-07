import sqlite3
from db_manager import obtener_preguntas_por_categoria  # Para obtener las preguntas de la base de datos
from registro_usuario import obtener_usuario


# Función para obtener todas las categorías
def obtener_todas_las_categorias():
    return [
        'Pensamiento científico',
        'Comprensión lectora',
        'Redacción indirecta',
        'Pensamiento matemático',
        'Inglés como lengua extranjera'
    ]

# Función para realizar el examen
def realizar_examen():
    correo = input("Ingresa tu correo para comenzar el examen: ")
    usuario = obtener_usuario(correo)
    
    if not usuario:
        print("Usuario no encontrado. Regístrate primero.")
        return
    
    print(f"Bienvenido, {usuario[1]}! Empezaremos tu examen.")
    
    categorias = obtener_todas_las_categorias()
    
    puntaje_total = 0
    puntajes_por_categoria = {}  # Para almacenar los puntajes por categoría
    
    # Recorremos todas las categorías y mostramos sus preguntas
    for categoria in categorias:
        print(f"\n--- {categoria} ---")
        preguntas = obtener_preguntas_por_categoria(categoria)
        
        if not preguntas:
            print(f"No hay preguntas disponibles en la categoría {categoria}.")
            continue
        
        puntaje_categoria = 0  # Puntaje acumulado de la categoría
        
        for pregunta in preguntas:
            print(f"\nPregunta: {pregunta[1]} (Puntos: {pregunta[2]})")
            respuesta_usuario = input("¿Cuál es tu respuesta? ")
            
            if respuesta_usuario.lower() == pregunta[3].lower():
                print("Respuesta correcta!")
                puntaje_categoria += pregunta[2]
            else:
                print(f"Respuesta incorrecta. La correcta era: {pregunta[3]}")
        
        # Guardar el puntaje de la categoría
        if puntaje_categoria > 0:
            puntajes_por_categoria[categoria] = puntaje_categoria
            puntaje_total += puntaje_categoria  # Sumar al puntaje total

    # Actualizar puntaje total del usuario
    conexion = sqlite3.connect('db/usuarios.db')
    cursor = conexion.cursor()
    nuevo_puntaje = usuario[3] + puntaje_total  # Sumar al puntaje total del usuario
    cursor.execute("UPDATE usuarios SET puntaje_total = ? WHERE correo = ?", (nuevo_puntaje, correo))
    
    # Guardar los puntajes por categoría en la tabla puntajes_categorias
    for categoria, puntaje_categoria in puntajes_por_categoria.items():
        cursor.execute('''INSERT OR REPLACE INTO puntajes_categorias (id_usuario, categoria, puntaje)
                          VALUES ((SELECT id FROM usuarios WHERE correo = ?), ?, ?)''', 
                       (correo, categoria, puntaje_categoria))
    
    conexion.commit()
    conexion.close()

    print(f"\nExamen completado. Puntaje total obtenido: {puntaje_total}")
    for categoria, puntaje_categoria in puntajes_por_categoria.items():
        print(f"Puntaje en la categoría '{categoria}': {puntaje_categoria}")
def guardar_examen(correo, categoria, puntaje_obtenido):
    # Obtener el id del usuario
    usuario = obtener_usuario(correo)
    if usuario:
        conexion = sqlite3.connect('db/usuarios.db')
        cursor = conexion.cursor()
        
        # Insertar el examen realizado
        cursor.execute('''INSERT INTO examenes_realizados (id_usuario, categoria, puntaje, fecha) 
                        VALUES (?, ?, ?, CURRENT_TIMESTAMP)''',
                        (usuario[0], categoria, puntaje_obtenido))
        conexion.commit()
        conexion.close()
