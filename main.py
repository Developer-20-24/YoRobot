from examen import realizar_examen # Importamos la función para realizar el examen
from preguntas import gestionar_preguntas  # Importamos la gestión de preguntas
#from registro_usuario import registrar_usuario
import registro_usuario


def main():
    while True:
        print("\n--- Menú Principal ---")
        print("\n1. Registrar nuevo usuario")
        print("2. Realizar Examen")
        print("3. Gestionar Preguntas")
        print("4. ver historial de examenes")
        print("5. Salir")

        opcion = input("Selecciona una opción: ")
        if opcion == '1':
            registrar_usuario()  # type: ignore # Registro de nuevo usuario
        elif opcion == '2':
            realizar_examen()  # Realizar examen
        elif opcion == '3':
            gestionar_preguntas()  # Llamamos al gestor de preguntas
        elif opcion == '4':
            # Ver historial de exámenes de un usuario
            correo = input("Ingresa tu correo para ver el historial de exámenes: ")
            usuario = registro_usuario.obtener_usuario(correo)
            
            if usuario:
                registro_usuario.ver_historial_examenes(usuario[0])  # Mostrar historial de exámenes
            else:
                print("Usuario no encontrado. Por favor regístrate primero.")
        elif opcion == '5':
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    main()
