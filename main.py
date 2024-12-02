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


print(CheckString("abls"))  # True
print(CheckString("ab"))    # True
print(CheckString("mbs"))   # False (empieza por 'm')
print(CheckString("fl"))    # False (termina sin vocal)
print(CheckString("flas"))  # True
print(CheckString("as"))    # False ('m' seguida de 's')