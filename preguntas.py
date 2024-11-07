# preguntas.py
from db_manager import agregar_pregunta, editar_pregunta, eliminar_pregunta, ver_preguntas, obtener_id_categoria

# Función para seleccionar categoría
def seleccionar_categoria():
    print("\nSelecciona la categoría de la pregunta:")
    print("1. Pensamiento científico")
    print("2. Comprensión lectora")
    print("3. Redacción indirecta")
    print("4. Pensamiento matemático")
    print("5. Inglés como lengua extranjera")
    categoria_opcion = input("Selecciona la opción: ")

    categorias = {
        '1': 'Pensamiento científico',
        '2': 'Comprensión lectora',
        '3': 'Redacción indirecta',
        '4': 'Pensamiento matemático',
        '5': 'Inglés como lengua extranjera'
    }

    return categorias.get(categoria_opcion, None)

# Función para gestionar preguntas a través de un menú
def gestionar_preguntas():
    while True:
        print("\n--- Sistema de Gestión de Preguntas ---")
        print("1. Agregar nueva pregunta")
        print("2. Editar pregunta existente")
        print("3. Eliminar pregunta")
        print("4. Ver todas las preguntas")
        print("5. Salir")
        
        opcion = input("Selecciona una opción: ")
        
        if opcion == '1':
            # Seleccionar la categoría para agregar una nueva pregunta
            categoria = seleccionar_categoria()
            if categoria is None:
                print("Opción de categoría no válida.")
                continue

            pregunta = input("Ingresa la pregunta: ")
            while True:
                try:
                    puntos = float(input("Ingresa los puntos (1 a 10): "))
                    if 1 <= puntos <= 10:
                        break
                    else:
                        print("Por favor, ingresa un valor de puntos entre 1 y 10.")
                except ValueError:
                    print("Entrada inválida. Por favor ingresa un número.")
            respuesta_correcta = input("Ingresa la respuesta correcta: ")
            respuestas_incorrectas = []
            for i in range(6):
                respuesta = input(f"Ingrese respuesta incorrecta {i+1} (o presiona Enter para omitir): ")
                if respuesta:
                    respuestas_incorrectas.append(respuesta)
                else:
                    break
            
            # Obtener el siguiente ID para la categoría seleccionada
            nuevo_id = obtener_id_categoria(categoria)
            print(f"ID de la nueva pregunta: {nuevo_id}")
            
            # Agregar la pregunta a la base de datos
            agregar_pregunta(nuevo_id, pregunta, puntos, respuesta_correcta, respuestas_incorrectas, categoria)

        elif opcion == '2':
            # Seleccionar la categoría para editar preguntas
            categoria = seleccionar_categoria()
            if categoria is None:
                print("Opción de categoría no válida.")
                continue

            ver_preguntas(categoria)  # Ver preguntas de la categoría seleccionada para poder elegir
            id_pregunta = input("Ingresa el ID de la pregunta a editar: ")
            nueva_pregunta = input("Ingresa la nueva pregunta: ")
            while True:
                try:
                    nuevos_puntos = float(input("Ingresa los nuevos_puntos (1 a 10): "))
                    if 1 <= nuevos_puntos <= 10:
                        break
                    else:
                        print("Por favor, ingresa un valor de puntos entre 1 y 10.")
                except ValueError:
                    print("Entrada inválida. Por favor ingresa un número.")
            nueva_respuesta_correcta = input("Ingresa la nueva respuesta correcta: ")
            nuevas_respuestas_incorrectas = []
            for i in range(6):
                respuesta = input(f"Ingrese nueva respuesta incorrecta {i+1} (o presiona Enter para omitir): ")
                if respuesta:
                    nuevas_respuestas_incorrectas.append(respuesta)
                else:
                    break
            
            editar_pregunta(id_pregunta, nueva_pregunta, nuevos_puntos, nueva_respuesta_correcta, nuevas_respuestas_incorrectas, categoria)

        elif opcion == '3':
            # Seleccionar la categoría para eliminar preguntas
            categoria = seleccionar_categoria()
            if categoria is None:
                print("Opción de categoría no válida.")
                continue

            ver_preguntas(categoria)  # Ver preguntas de la categoría seleccionada para poder elegir
            id_pregunta = input("Ingresa el ID de la pregunta a eliminar: ")
            eliminar_pregunta(id_pregunta)
        
        elif opcion == '4':
            # Seleccionar la categoría para ver preguntas
            categoria = seleccionar_categoria()
            if categoria is None:
                print("Opción de categoría no válida.")
                continue
            
            ver_preguntas(categoria)  # Ver preguntas solo de la categoría seleccionada

        elif opcion == '5':
            print("¡Hasta luego!")
            break
        
        else:
            print("Opción no válida, intenta de nuevo.")