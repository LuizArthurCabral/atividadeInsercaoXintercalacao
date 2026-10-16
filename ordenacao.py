"""Ordenação por inserção e ordenação por intercalação (merge sort).

Os dois métodos recebem uma lista e devolvem uma NOVA lista ordenada, sem
modificar a original. Ambos só usam o operador ``<`` para comparar elementos,
e ambos são estáveis (elementos iguais mantêm a ordem original).

Para contar comparações sem alterar o código dos algoritmos, o módulo traz a
classe ``ElementoContado``, que embrulha um valor e conta cada chamada de
``__lt__``. A função ``contar_comparacoes`` usa essa classe com qualquer método
de ordenação (inclusive o ``sorted`` do Python).
"""


def ordenacao_por_insercao(lista):
    """Ordena por inserção: O(n^2) no pior caso e no caso médio, O(n) se já ordenada."""
    a = list(lista)
    for i in range(1, len(a)):
        chave = a[i]
        j = i - 1
        # Desloca para a direita os elementos maiores que a chave.
        while j >= 0 and chave < a[j]:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = chave
    return a


def _intercalar(esquerda, direita):
    """Junta duas listas já ordenadas em uma só, de forma estável."""
    resultado = []
    i = j = 0
    while i < len(esquerda) and j < len(direita):
        # Só pega da direita se ela for estritamente menor: empates saem da
        # esquerda primeiro, o que garante a estabilidade.
        if direita[j] < esquerda[i]:
            resultado.append(direita[j])
            j += 1
        else:
            resultado.append(esquerda[i])
            i += 1
    resultado.extend(esquerda[i:])
    resultado.extend(direita[j:])
    return resultado


def ordenacao_por_intercalacao(lista):
    """Ordena por intercalação (merge sort): O(n log n) em todos os casos."""
    if len(lista) <= 1:
        return list(lista)
    meio = len(lista) // 2
    esquerda = ordenacao_por_intercalacao(lista[:meio])
    direita = ordenacao_por_intercalacao(lista[meio:])
    return _intercalar(esquerda, direita)


class ElementoContado:
    """Embrulha um valor e conta quantas vezes ele é comparado com ``<``."""

    __slots__ = ("valor", "contador")

    def __init__(self, valor, contador):
        self.valor = valor
        self.contador = contador  # lista de um elemento, compartilhada

    def __lt__(self, outro):
        self.contador[0] += 1
        return self.valor < outro.valor


def contar_comparacoes(metodo, lista):
    """Executa ``metodo`` sobre ``lista`` e devolve ``(comparacoes, resultado)``.

    ``metodo`` é qualquer função que ordena usando ``<`` (os dois algoritmos
    deste módulo ou o ``sorted`` do Python). ``resultado`` volta com os valores
    originais, já ordenados.
    """
    contador = [0]
    embrulhada = [ElementoContado(x, contador) for x in lista]
    ordenada = metodo(embrulhada)
    return contador[0], [e.valor for e in ordenada]
