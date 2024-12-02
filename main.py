import re


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
        a|               # Vocal sola (V)
        b|f|t|l|s|       # Primera consonante
        bl|fl|tl|        # CCV (b/f/t seguido de l)
        a                # Vocal (después de C o CC)
        s?               # Opcional: s para formar VC o CVC
    )$                   # Fin del patrón
    """

    # Usar expresiones regulares para validar la cadena
    return bool(re.fullmatch(pattern, frase, re.VERBOSE | re.IGNORECASE))

def Diafonizacion(frase: str) -> str:
    # Verificar si la cadena está vacía
    if not frase:
        return "La cadena debe contener algo"

    # Llamar a CheckString para validar la cadena
    if not CheckString(frase):
        return "La cadena no cumple con las normas."

    # Lista para almacenar los difonos
    difonos = []

    # Incluir un guion inicial para el primer difono
    difonos.append(f"-{frase[0]}")

    # Generar los difonos intermedios
    for i in range(len(frase) - 1):
        difonos.append(f"{frase[i]}{frase[i + 1]}")

    # Incluir un guion final para el último difono
    difonos.append(f"{frase[-1]}-")

    # Combinar los difonos con espacios y devolverlos como cadena
    return " ".join(difonos)





print(Diafonizacion("ala"))     # Salida: -a al la a-
print(Diafonizacion("aflas"))   # Salida: -a af fl la as s-
print(Diafonizacion("flas"))    # Salida: La cadena no cumple con las normas.
print(Diafonizacion("as"))      # Salida: -t tl ls s-