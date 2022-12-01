

def normalizar_nombres(input_str: str) -> str:
    import re

    return re.sub('( |\n|\t|\-|\.)+', ' ', input_str).strip()