#Alejandro Perez Dominguez
#Juan Jimenez Serrano
import re
from pydub import AudioSegment
import os

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


    # Lista para almacenar los difonos
    difonos = []

    # Añadir un guion inicial para el primer difono
    difonos.append(f"-{frase[0]}")

    # Generar los difonos intermedios
    for i in range(len(frase) - 1):
        difonos.append(f"{frase[i]}{frase[i + 1]}")

    # Añadir un guion final para el último difono
    difonos.append(f"{frase[-1]}-")

    # Modificar los difonos que contienen una "A" mayúscula
    for i in range(len(difonos)):
        if 'A' in difonos[i]:
            difonos[i] = f"{difonos[i]}_acentuado"  # Añadir '_acentuado' si contiene 'A'

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
        crossfade_duration = 20  # Puedes modificar esta duración según lo necesites

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


CrearAudios("fAstaba", "salida.wav")

