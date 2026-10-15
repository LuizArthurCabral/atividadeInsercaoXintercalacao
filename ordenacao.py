def insercao(lista):
    a = list(lista)
    for i in range(1, len(a)):
        chave = a[i]
        j = i - 1
        while j >= 0 and chave < a[j]:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = chave
    return a


def intercalacao(lista):
    if len(lista) <= 1:
        return list(lista)

    meio = len(lista) // 2
    esquerda = intercalacao(lista[:meio])
    direita = intercalacao(lista[meio:])

    resultado = []
    i = j = 0
    while i < len(esquerda) and j < len(direita):
        if direita[j] < esquerda[i]:
            resultado.append(direita[j])
            j += 1
        else:
            resultado.append(esquerda[i])
            i += 1
    resultado.extend(esquerda[i:])
    resultado.extend(direita[j:])
    return resultado
