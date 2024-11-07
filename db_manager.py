# db_manager.py
import sqlite3
import os

# Crear la carpeta "db" si no existe
def crear_carpetas():
    if not os.path.exists('db'):
        os.makedirs('db')

# Función para crear la base de datos
def crear_base_datos():
    crear_carpetas()
    conexion = sqlite3.connect('db/usuarios.db')
    cursor = conexion.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        correo TEXT NOT NULL UNIQUE,
        puntaje_total REAL DEFAULT 0
    )''')

    # Crear tabla para puntajes por categoría
    cursor.execute('''CREATE TABLE IF NOT EXISTS puntajes_categorias (
        id_usuario INTEGER,
        categoria TEXT,
        puntaje REAL,
        FOREIGN KEY (id_usuario) REFERENCES usuarios(id),
        PRIMARY KEY (id_usuario, categoria)
    )''')
    
    conexion.commit()
    conexion.close()

# Función para obtener el siguiente ID secuencial por categoría
def obtener_id_categoria(categoria):
    conexion = sqlite3.connect('db/sistema_admision.db')
    cursor = conexion.cursor()
    
    cursor.execute('SELECT MAX(id) FROM preguntas WHERE categoria = ?', (categoria,))
    max_id = cursor.fetchone()[0]
    
    if max_id:
        numero_actual = int(max_id.split(' ')[1])
    else:
        numero_actual = 0
    
    conexion.close()
    
    prefijos = {
        'Pensamiento científico': '1',
        'Comprensión lectora': '2',
        'Redacción indirecta': '3',
        'Pensamiento matemático': '4',
        'Inglés como lengua extranjera': '5'
    }
    
    prefijo = prefijos.get(categoria, '1')
    nuevo_id = f"{prefijo} {numero_actual + 1}"
    
    return nuevo_id

# Función para agregar una pregunta
def agregar_pregunta(id, pregunta, puntos, respuesta_correcta, respuestas_incorrectas, categoria):
    if not (1 <= puntos <= 10):
        raise ValueError("Los puntos deben estar entre 1 y 10.")
    
    conexion = sqlite3.connect('db/sistema_admision.db')
    cursor = conexion.cursor()
    
    # Convertir la lista de respuestas incorrectas en un solo string
    respuestas_incorrectas_str = "; ".join(respuestas_incorrectas)
    
    cursor.execute('''
    INSERT INTO preguntas (id, pregunta, puntos, respuesta_correcta, respuestas_incorrectas, categoria)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (id, pregunta, puntos, respuesta_correcta, respuestas_incorrectas_str, categoria))
    
    conexion.commit()
    conexion.close()

# Función para editar una pregunta
def editar_pregunta(id, nueva_pregunta, nuevos_puntos, nueva_respuesta_correcta, nuevas_respuestas_incorrectas, nueva_categoria):
    if not (1 <= nuevos_puntos <= 10):
        raise ValueError("Los puntos deben estar entre 1 y 10.")
    conexion = sqlite3.connect('db/sistema_admision.db')
    cursor = conexion.cursor()
    
    nuevas_respuestas_incorrectas_str = "; ".join(nuevas_respuestas_incorrectas)
    
    cursor.execute('''
    UPDATE preguntas
    SET pregunta = ?, puntos = ?, respuesta_correcta = ?, respuestas_incorrectas = ?, categoria = ?
    WHERE id = ?
    ''', (nueva_pregunta, nuevos_puntos, nueva_respuesta_correcta, nuevas_respuestas_incorrectas_str, nueva_categoria, id))
    
    conexion.commit()
    conexion.close()

# Función para eliminar una pregunta
def eliminar_pregunta(id):
    conexion = sqlite3.connect('db/sistema_admision.db')
    cursor = conexion.cursor()
    
    cursor.execute('DELETE FROM preguntas WHERE id = ?', (id,))
    
    conexion.commit()
    conexion.close()

# Función para ver todas las preguntas
def ver_preguntas(categoria=None):
    conexion = sqlite3.connect('db/sistema_admision.db')
    cursor = conexion.cursor()
    
    if categoria:
        cursor.execute('SELECT * FROM preguntas WHERE categoria = ?', (categoria,))
    else:
        cursor.execute('SELECT * FROM preguntas')
    
    preguntas = cursor.fetchall()
    
    for pregunta in preguntas:
        print(f"ID: {pregunta[0]}, Pregunta: {pregunta[1]}, Puntos: {pregunta[2]}, Correcta: {pregunta[3]}, Incorrectas: {pregunta[4]}, Categoría: {pregunta[5]}")
    
    conexion.close()
# Conectar a la base de datos y obtener preguntas de una categoría específica
def obtener_preguntas_por_categoria(categoria):
    conexion = sqlite3.connect('db/sistema_admision.db')
    cursor = conexion.cursor()
    
    # Consulta para obtener todas las preguntas de la categoría
    cursor.execute('SELECT id, pregunta, puntos, respuesta_correcta, respuestas_incorrectas, categoria FROM preguntas WHERE categoria = ?', (categoria,))
    preguntas = cursor.fetchall()
    
    conexion.close()
    return preguntas

# Llamar a la función de creación de base de datos al importar el módulo
crear_base_datos()
