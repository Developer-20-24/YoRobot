import sqlite3
import os

# Crear la carpeta "db" si no existe
def crear_carpetas():
    if not os.path.exists('db'):
        os.makedirs('db')

# Crear la base de datos de usuarios
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
    
    conexion.commit()
    conexion.close()

# Crear la tabla para los exámenes realizados
def crear_tabla_examenes():
    conexion = sqlite3.connect('db/usuarios.db')
    cursor = conexion.cursor()
    
    # Crear la tabla de exámenes realizados si no existe
    cursor.execute('''CREATE TABLE IF NOT EXISTS examenes_realizados (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_usuario INTEGER,
        categoria TEXT,
        puntaje REAL,
        fecha TEXT,
        FOREIGN KEY(id_usuario) REFERENCES usuarios(id)
    )''')
    
    conexion.commit()
    conexion.close()


# Función para registrar un nuevo usuario
def registrar_usuario():
    nombre = input("Ingresa tu nombre: ")
    correo = input("Ingresa tu correo electrónico: ")
    
    # Verificar si el correo ya está registrado
    conexion = sqlite3.connect('db/usuarios.db')
    cursor = conexion.cursor()
    
    cursor.execute("SELECT * FROM usuarios WHERE correo = ?", (correo,))
    if cursor.fetchone():
        print("Este correo ya está registrado.")
        conexion.close()
        return None
    
    # Registrar usuario
    cursor.execute("INSERT INTO usuarios (nombre, correo) VALUES (?, ?)", (nombre, correo))
    conexion.commit()
    print(f"Usuario {nombre} registrado correctamente.")
    conexion.close()
    
# Función para obtener un usuario por su correo
def obtener_usuario(correo):
    conexion = sqlite3.connect('db/usuarios.db')
    cursor = conexion.cursor()
    
    cursor.execute("SELECT * FROM usuarios WHERE correo = ?", (correo,))
    usuario = cursor.fetchone()
    
    conexion.close()
    return usuario

# Función para guardar los resultados de un examen en el historial del usuario
def guardar_resultados_examen(usuario_id, categoria, puntaje):
    conexion = sqlite3.connect('db/usuarios.db')
    cursor = conexion.cursor()
    
    cursor.execute('''INSERT INTO examenes_realizados (usuario_id, categoria, puntaje)
                      VALUES (?, ?, ?)''', (usuario_id, categoria, puntaje))
    conexion.commit()
    conexion.close()

# Función para ver el historial de exámenes de un usuario
def ver_historial_examenes(id_usuario):
    conexion = sqlite3.connect('db/usuarios.db')
    cursor = conexion.cursor()
    
    # Obtener el historial de exámenes
    cursor.execute('''SELECT categoria, puntaje, fecha FROM examenes_realizados 
                      WHERE id_usuario = ?''', (id_usuario,))
    examenes = cursor.fetchall()
    
    if examenes:
        print("\nHistorial de exámenes:")
        for examen in examenes:
            print(f"Categoría: {examen[0]}, Puntaje: {examen[1]}, Fecha: {examen[2]}")
    else:
        print("No se han encontrado exámenes realizados.")
    
    conexion.close()
