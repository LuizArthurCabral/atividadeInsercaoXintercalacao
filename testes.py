import random
import unittest

from ordenacao import insercao, intercalacao


class TestOrdenacao(unittest.TestCase):
    def verificar(self, lista):
        for ordenar in [insercao, intercalacao]:
            with self.subTest(algoritmo=ordenar.__name__, lista=lista):
                self.assertEqual(ordenar(lista), sorted(lista))

    def test_lista_vazia(self):
        self.verificar([])

    def test_um_elemento(self):
        self.verificar([42])

    def test_todos_iguais(self):
        self.verificar([7] * 15)

    def test_ja_ordenada(self):
        self.verificar(list(range(30)))

    def test_invertida(self):
        self.verificar(list(range(30, 0, -1)))

    def test_dois_elementos(self):
        self.verificar([2, 1])
        self.verificar([1, 2])

    def test_negativos_e_repetidos(self):
        self.verificar([3, -1, 0, 3, -5, 2, -1, 0])

    def test_aleatorias(self):
        for _ in range(100):
            n = random.randint(0, 100)
            self.verificar([random.randint(-50, 50) for _ in range(n)])

    def test_nao_altera_a_original(self):
        lista = [3, 1, 2]
        insercao(lista)
        intercalacao(lista)
        self.assertEqual(lista, [3, 1, 2])


if __name__ == "__main__":
    unittest.main()
