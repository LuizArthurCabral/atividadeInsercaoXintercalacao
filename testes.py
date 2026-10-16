"""Testes dos dois métodos de ordenação.

Rodar:  python testes.py
"""
import math
import random
import unittest
from itertools import permutations

from ordenacao import (
    ElementoContado,
    contar_comparacoes,
    ordenacao_por_insercao,
    ordenacao_por_intercalacao,
)


class CasosDeOrdenacao:
    """Testes comuns aos dois algoritmos (as subclasses definem ``metodo``)."""

    metodo = None

    # --- casos difíceis exigidos ---------------------------------------

    def test_lista_vazia(self):
        self.assertEqual(self.metodo([]), [])

    def test_um_elemento(self):
        self.assertEqual(self.metodo([7]), [7])

    def test_todos_os_elementos_iguais(self):
        self.assertEqual(self.metodo([5] * 10), [5] * 10)

    def test_lista_ja_ordenada(self):
        entrada = list(range(20))
        self.assertEqual(self.metodo(entrada), list(range(20)))

    def test_lista_invertida(self):
        entrada = list(range(20, 0, -1))
        self.assertEqual(self.metodo(entrada), list(range(1, 21)))

    # --- outros casos ---------------------------------------------------

    def test_dois_elementos(self):
        self.assertEqual(self.metodo([2, 1]), [1, 2])
        self.assertEqual(self.metodo([1, 2]), [1, 2])

    def test_com_repetidos(self):
        self.assertEqual(self.metodo([3, 1, 2, 3, 1, 2]), [1, 1, 2, 2, 3, 3])

    def test_negativos_e_zero(self):
        self.assertEqual(self.metodo([0, -3, 5, -1, 2]), [-3, -1, 0, 2, 5])

    def test_strings(self):
        self.assertEqual(
            self.metodo(["banana", "abacate", "caju"]),
            ["abacate", "banana", "caju"],
        )

    def test_aleatorias_contra_sorted(self):
        rng = random.Random(1)
        for _ in range(300):
            n = rng.randint(0, 60)
            entrada = [rng.randint(-20, 20) for _ in range(n)]  # com repetidos
            self.assertEqual(self.metodo(entrada), sorted(entrada), entrada)

    def test_permutacoes_grandes(self):
        rng = random.Random(2)
        for n in (100, 257, 1000):
            entrada = list(range(n))
            rng.shuffle(entrada)
            self.assertEqual(self.metodo(entrada), list(range(n)))

    def test_nao_modifica_a_entrada(self):
        entrada = [4, 2, 9, 1]
        copia = list(entrada)
        self.metodo(entrada)
        self.assertEqual(entrada, copia)

    def test_devolve_lista_nova(self):
        for entrada in ([], [1], [2, 1]):
            self.assertIsNot(self.metodo(entrada), entrada)

    def test_estabilidade(self):
        class Item:
            def __init__(self, chave, rotulo):
                self.chave, self.rotulo = chave, rotulo

            def __lt__(self, outro):
                return self.chave < outro.chave

        itens = [Item(2, "a"), Item(1, "b"), Item(2, "c"), Item(1, "d")]
        self.assertEqual([i.rotulo for i in self.metodo(itens)], ["b", "d", "a", "c"])


class TestInsercao(CasosDeOrdenacao, unittest.TestCase):
    metodo = staticmethod(ordenacao_por_insercao)

    def test_contagem_casos_extremos(self):
        n = 10
        for entrada, esperado in (
            ([], 0),
            ([1], 0),
            (list(range(n)), n - 1),  # melhor caso: já ordenada
            (list(range(n, 0, -1)), n * (n - 1) // 2),  # pior caso: invertida
            ([5] * n, n - 1),  # todos iguais: 1 comparação por elemento
        ):
            comparacoes, resultado = contar_comparacoes(ordenacao_por_insercao, entrada)
            self.assertEqual(comparacoes, esperado, entrada)
            self.assertEqual(resultado, sorted(entrada))


class TestIntercalacao(CasosDeOrdenacao, unittest.TestCase):
    metodo = staticmethod(ordenacao_por_intercalacao)

    def test_contagem_casos_extremos(self):
        # Para n = 8 (potência de 2), ordenada e invertida custam (n/2)*log2(n) = 12.
        for entrada, esperado in (
            ([], 0),
            ([1], 0),
            ([2, 1], 1),
            (list(range(8)), 12),
            (list(range(8, 0, -1)), 12),
        ):
            comparacoes, resultado = contar_comparacoes(ordenacao_por_intercalacao, entrada)
            self.assertEqual(comparacoes, esperado, entrada)
            self.assertEqual(resultado, sorted(entrada))

    def test_limite_superior_de_comparacoes(self):
        # Pior caso do merge sort: n*ceil(log2 n) - 2^ceil(log2 n) + 1.
        rng = random.Random(3)
        n = 64
        teto = n * 6 - 2**6 + 1
        for _ in range(100):
            entrada = list(range(n))
            rng.shuffle(entrada)
            comparacoes, _ = contar_comparacoes(ordenacao_por_intercalacao, entrada)
            self.assertLessEqual(comparacoes, teto)


class TestMediaExata(unittest.TestCase):
    """Média de comparações sobre TODAS as permutações (base do RELATORIO.md, seção 4)."""

    @staticmethod
    def media_exata(metodo, n):
        todas = list(permutations(range(n)))
        return sum(contar_comparacoes(metodo, list(p))[0] for p in todas) / len(todas)

    def test_valores_exatos_para_n_pequeno(self):
        esperado = {  # n: (inserção, intercalação)
            2: (1.0, 1.0),
            3: (8 / 3, 8 / 3),
            4: (59 / 12, 14 / 3),
            5: (463 / 60, 43 / 6),
        }
        for n, (ins, inter) in esperado.items():
            self.assertAlmostEqual(self.media_exata(ordenacao_por_insercao, n), ins, places=9)
            self.assertAlmostEqual(self.media_exata(ordenacao_por_intercalacao, n), inter, places=9)

    def test_intercalacao_usa_menos_comparacoes_a_partir_de_n_4(self):
        for n in range(4, 9):
            self.assertLess(
                self.media_exata(ordenacao_por_intercalacao, n),
                self.media_exata(ordenacao_por_insercao, n),
                f"n = {n}",
            )


class TestContagem(unittest.TestCase):
    def test_elemento_contado_conta_cada_lt(self):
        contador = [0]
        a, b = ElementoContado(1, contador), ElementoContado(2, contador)
        self.assertTrue(a < b)
        self.assertFalse(b < a)
        self.assertEqual(contador[0], 2)

    def test_contar_comparacoes_com_sorted(self):
        rng = random.Random(4)
        entrada = list(range(100))
        rng.shuffle(entrada)
        comparacoes, resultado = contar_comparacoes(sorted, entrada)
        self.assertEqual(resultado, list(range(100)))
        self.assertGreaterEqual(comparacoes, 99)  # precisa olhar todos os elementos
        self.assertLessEqual(comparacoes, 100 * math.ceil(math.log2(100)))


if __name__ == "__main__":
    unittest.main(verbosity=2)
