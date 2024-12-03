#Alejandro Perez Dominguez
#Juan Jimenez Serrano
import re
from pydub import AudioSegment
import os

def CheckString(frase: str) -> bool:
    # Verificar si la frase contiene espacios o caracteres inválidos
    if any(char not in "aAbflmts?" for char in frase):
        return False

    # Verificar si la frase empieza por 'm'
    if frase.startswith('m'):
        return False

    # Verificar si la letra 'm' no está seguida de 's'
    if 'sm' in frase:
        return False

    #Verificar que la letra en la que termina es válida
    if not frase[-1] in ["?", "a", "s", "A"]:
        return False

    # Definir el patrón permitido
    pattern = r"""
    ^(                   # Inicio del patrón
        a?               # Opcional: Vocal sola (V)
        b|f|t|l|s|m|     # Primera consonante
        bl|fl|tl|        # CCV (b/f/t seguido de l)
        a                # Vocal (después de C o CC)
        s?               # Opcional: s para formar VC o CVC
    )+                       # Una o más veces
    \??                  # Opcional: literal '?' al final
    $                        # Fin del patrón
    """

    # Usar expresiones regulares para validar la cadena
    return bool(re.fullmatch(pattern, frase, re.VERBOSE | re.IGNORECASE))


def Diafonizacion(frase: str) -> list:

    # Lista para almacenar los difonos
    difonos = []

    if frase.endswith("?"):
        frase = frase[:-1] #le quita el ultimo caracter
    # Añadir un guion inicial para el primer difono
    difonos.append(f"-{frase[0]}")

    # Generar los difonos intermedios
    for i in range(len(frase) - 1):
        difonos.append(f"{frase[i]}{frase[i + 1]}")

    # Añadir un guion final para el último difono
    difonos.append(f"{frase[-1]}-")

    # Modificar los difonos que contienen una "A" mayúscula y borrar los fl, tl, bl
    difonos = [
        f"{difono}_acentuado" if 'A' in difono else difono #si contiene una A se transforma en []_acentuado, si no, se queda como esta
        for difono in difonos
        if difono not in ["fl", "tl", "bl"]
        #solo mantiene los que NO se encuentran en la lista [fl, tl, bl]
        #por tanto, los que tengan ese patron, los borra
    ]

    # Devolver la lista de difonos modificados
    return difonos


def CrearAudios(frase: str, output_filename: str):
    # Llamar a CheckString para validar la cadena
    if not CheckString(frase):
        print("La cadena no cumple con las normas.")
    else:
    # Definir la carpeta donde se encuentran los difonos
        difonos_folder = "./Difonos/"

        difonos = Diafonizacion(frase)

     # Inicializar un objeto AudioSegment vacío
        audio_output = AudioSegment.silent(duration=500)  # Empezamos con un silencio vacío

    # Definir la duración del crossfade en milisegundos (por ejemplo, 100 ms = 0.1 segundos)
        crossfade_duration = 13

    # Iterar sobre los difonos en la lista y concatenarlos
        for difono in difonos:

            difono_filename = difono + ".wav"
            difono_path = os.path.join(difonos_folder, difono_filename)

        # Comprobar si el archivo existe
            if os.path.exists(difono_path):
            # Cargar el archivo de audio del difono
                audio = AudioSegment.from_file(difono_path, format="wav")

            # Realizar el crossfade y concatenar con el audio actual
                audio_output = audio_output.append(audio, crossfade=crossfade_duration)
            else:
                print(f"El archivo {difono_filename} no se encontró en la carpeta de difonos.")
        audio_output = audio_output.append(AudioSegment.silent(duration=500))

    # Exportar el audio resultante a un archivo .wav
        audio_output.export(output_filename, format="wav")
        print(f"Archivo de audio generado: {output_filename}")


CrearAudios("blablablA", "salida.wav")

