import csv
import math
import random
import time

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from ordenacao import insercao, intercalacao

TAMANHOS = [5, 10, 20, 30, 50, 75, 100, 200, 500, 1000]
REPETICOES = 50
ALGORITMOS = {"insercao": insercao, "intercalacao": intercalacao, "sorted": sorted}
CORES = {"insercao": "#2a78d6", "intercalacao": "#eb6834", "sorted": "#1baf7a"}


class Contador:
    comparacoes = 0

    def __init__(self, valor):
        self.valor = valor

    def __lt__(self, outro):
        Contador.comparacoes += 1
        return self.valor < outro.valor


random.seed(2026)
linhas = []
for n in TAMANHOS:
    listas = [[random.random() for _ in range(n)] for _ in range(REPETICOES)]
    for nome, ordenar in ALGORITMOS.items():
        for repeticao, lista in enumerate(listas, 1):
            inicio = time.perf_counter()
            ordenar(lista)
            tempo = time.perf_counter() - inicio

            Contador.comparacoes = 0
            ordenar([Contador(x) for x in lista])

            linhas.append([nome, n, repeticao, tempo, Contador.comparacoes])

with open("dados.csv", "w", newline="") as arquivo:
    escritor = csv.writer(arquivo)
    escritor.writerow(["algoritmo", "n", "repeticao", "tempo_s", "comparacoes"])
    escritor.writerows(linhas)


def media(nome, n, coluna):
    valores = [linha[coluna] for linha in linhas if linha[0] == nome and linha[1] == n]
    return sum(valores) / len(valores)


tempos = {nome: [media(nome, n, 3) * 1000 for n in TAMANHOS] for nome in ALGORITMOS}
comparacoes = {nome: [media(nome, n, 4) for n in TAMANHOS] for nome in ALGORITMOS}

print("| n | tempo inserção (ms) | tempo intercalação (ms) | tempo sorted (ms) "
      "| comp. inserção | comp. intercalação | comp. sorted | n log2 n |")
print("|---|---|---|---|---|---|---|---|")
for i, n in enumerate(TAMANHOS):
    print(f"| {n} | {tempos['insercao'][i]:.4f} | {tempos['intercalacao'][i]:.4f} "
          f"| {tempos['sorted'][i]:.4f} | {comparacoes['insercao'][i]:.1f} "
          f"| {comparacoes['intercalacao'][i]:.1f} | {comparacoes['sorted'][i]:.1f} "
          f"| {n * math.log2(n):.1f} |")

plt.figure(figsize=(8, 5))
for nome in ALGORITMOS:
    plt.plot(TAMANHOS, tempos[nome], marker="o", linewidth=2, color=CORES[nome], label=nome)
plt.xscale("log")
plt.yscale("log")
plt.xlabel("n (tamanho da lista)")
plt.ylabel("tempo médio (ms)")
plt.title(f"Tempo médio de ordenação ({REPETICOES} repetições)")
plt.grid(True, which="both", alpha=0.3)
plt.legend()
plt.savefig("grafico_tempo.png", dpi=120, bbox_inches="tight")
plt.close()

plt.figure(figsize=(8, 5))
for nome in ALGORITMOS:
    plt.plot(TAMANHOS, comparacoes[nome], marker="o", linewidth=2, color=CORES[nome], label=nome)
plt.plot(TAMANHOS, [n * math.log2(n) for n in TAMANHOS], "--", color="gray", label="n log2 n")
plt.xscale("log")
plt.yscale("log")
plt.xlabel("n (tamanho da lista)")
plt.ylabel("comparações médias")
plt.title(f"Número médio de comparações ({REPETICOES} repetições)")
plt.grid(True, which="both", alpha=0.3)
plt.legend()
plt.savefig("grafico_comparacoes.png", dpi=120, bbox_inches="tight")
plt.close()

print("\nGerados: dados.csv, grafico_tempo.png, grafico_comparacoes.png")
