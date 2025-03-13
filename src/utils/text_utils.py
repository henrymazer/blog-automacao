def numero_para_extenso(num):
    """Convert a number to its written form in Portuguese."""
    extenso = {
        1: "primeiro",
        2: "segundo",
        3: "terceiro",
        4: "quarto",
        5: "quinto"
    }
    return extenso.get(num, str(num))

def posicao_inversa(pos, total):
    """Convert a position to its inverse form in Portuguese."""
    if pos == total:
        return "último"
    elif pos == total - 1:
        return "penúltimo"
    elif pos == total - 2:
        return "antepenúltimo"
    return str(pos)
