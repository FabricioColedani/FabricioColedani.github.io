def convertir_temperatura(valor, unidad_origen, unidad_destino):
    if unidad_origen == "C" and unidad_destino == "F":
        return (valor * 9/5) + 32
    elif unidad_origen == "F" and unidad_destino == "C":
        return (valor - 32) * 5/9
    elif unidad_origen == "C" and unidad_destino == "K":
        return valor + 273.15
    elif unidad_origen == "K" and unidad_destino == "C":
        return valor - 273.15
    elif unidad_origen == "F" and unidad_destino == "K":
        celsius = (valor - 32) * 5/9
        return celsius + 273.15
    elif unidad_origen == "K" and unidad_destino == "F":
        celsius = valor - 273.15
        return (celsius * 9/5) + 32
    else:
        return valor  # Las unidades son las mismas, no se realiza ninguna conversión

def main():
    print("Bienvenido al juego de conversiones de magnitudes.")
    print("Elige una opción:")
    print("1. Conversión de temperatura")
    print("2. Salir")

    opcion = input("Opción: ")

    if opcion == "1":
        valor = float(input("Ingresa el valor de temperatura: "))
        unidad_origen = input("Ingresa la unidad de temperatura de origen (C, F, K): ")
        unidad_destino = input("Ingresa la unidad de temperatura de destino (C, F, K): ")

        resultado = convertir_temperatura(valor, unidad_origen.upper(), unidad_destino.upper())
        print(f"{valor}{unidad_origen} equivale a {resultado}{unidad_destino}")

    elif opcion == "2":
        print("Gracias por jugar. ¡Hasta luego!")

    else:
        print("Opción inválida. Por favor, elige una opción válida.")

if __name__ == '__main__':
    main()