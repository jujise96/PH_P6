#Alejandro Perez Dominguez
#Juan Jimenez Serrano
import re
import pydub
from pydub import AudioSegment

def CheckString(frase: str) -> bool:
    # Verificar si la frase contiene espacios o caracteres inválidos
    if any(char not in "aAbflmts" for char in frase):
        return False

    # Verificar si la frase empieza por 'm'
    if frase.startswith('m'):
        return False

    # Verificar si la letra 'm' no está seguida de 's'
    if 'ms' in frase:
        return False


    # Definir el patrón permitido
    pattern = r"""
    ^(                   # Inicio del patrón
        a?               # Vocal sola (V)
        b|f|t|l|s|m|     # Primera consonante
        bl|fl|tl|        # CCV (b/f/t seguido de l)
        a                # Vocal (después de C o CC)
        s?               # Opcional: s para formar VC o CVC
    )+                       # Una o más veces
    $                        # Fin del patrón
    """

    # Usar expresiones regulares para validar la cadena
    return bool(re.fullmatch(pattern, frase, re.VERBOSE | re.IGNORECASE))


def Diafonizacion(frase: str) -> list:
    # Llamar a CheckString para validar la cadena
    if not CheckString(frase):
        raise ValueError("La cadena no cumple con las normas.")

    # Lista para almacenar los difonos
    difonos = []

    # Añadir un guion inicial para el primer difono
    difonos.append(f"-{frase[0]}")

    # Generar los difonos intermedios
    for i in range(len(frase) - 1):
        difonos.append(f"{frase[i]}{frase[i + 1]}")

    # Añadir un guion final para el último difono
    difonos.append(f"{frase[-1]}-")

    # Devolver la lista de difonos
    return difonos





# Cargar los dos archivos de audio
audio1 = AudioSegment.from_file("./sample_data/audio1.wav", format="wav")
audio2 = AudioSegment.from_file("./sample_data/audio2.wav", format="wav")

# Definir la duración del crossfade en milisegundos (por ejemplo, 1000 ms = 1 segundo)
crossfade_duration = 100  # Duración del crossfade en milisegundos

# Realizar el crossfade
audio_output = audio1.append(audio2, crossfade=crossfade_duration)

# Guardar el resultado
audio_output.export("salida.wav", format="wav")


print(Diafonizacion("ala"))     # Salida: -a al la a-
print(Diafonizacion("aflas"))   # Salida: -a af fl la as s-
print(Diafonizacion("flas"))    # Salida: La cadena no cumple con las normas.
print(Diafonizacion("as"))      # Salida: -t tl ls s-