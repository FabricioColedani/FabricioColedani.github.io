import random

# Definición de las preguntas y respuestas
preguntas = {
    "¿Cuál es la unidad de medida de la longitud en el Sistema Internacional?": ["a) Metro", "b) Kilogramo", "c) Segundo"],
    "¿Cuál es la unidad de medida de la masa en el Sistema Internacional?": ["a) Kilogramo", "b) Metro", "c) Segundo"],
    "¿Cuál es la unidad de medida del tiempo en el Sistema Internacional?": ["a) Segundo", "b) Metro", "c) Kilogramo"]
}

# Función para seleccionar una pregunta aleatoria
def obtener_pregunta():
    pregunta = random.choice(list(preguntas.keys()))
    respuestas = preguntas[pregunta]
    respuesta_correcta = respuestas[0]
    random.shuffle(respuestas)
    return pregunta, respuestas, respuesta_correcta

# Función principal del juego
def jugar_juego():
    print("Bienvenido al juego de magnitudes fundamentales.")
    print("Responde las siguientes preguntas:")
    print("----------------------------------------")
    puntaje = 0
    for _ in range(3):
        pregunta, respuestas, respuesta_correcta = obtener_pregunta()
        print(pregunta)
        for respuesta in respuestas:
            print(respuesta)
        eleccion = input("Elige la respuesta correcta (ingresa la letra correspondiente): ")
        if eleccion.lower() == respuesta_correcta[0].lower():
            print("¡Respuesta correcta!")
            puntaje += 1
        else:
            print("Respuesta incorrecta.")
        print("----------------------------------------")
    print("Juego terminado. Tu puntaje final es:", puntaje)

# Iniciar el juego
jugar_juego()
