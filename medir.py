"""Mede tempo e número de comparações da inserção, da intercalação e do sorted().

Rodar:  python medir.py

Refaz do zero (sobrescrevendo, se existirem):
  - dados.csv               números brutos, uma linha por repetição
  - grafico_tempos.png      tempo médio x n
  - grafico_comparacoes.png comparações médias x n

Requer matplotlib:  pip install matplotlib
"""
import argparse
import csv
import gc
import math
import random
import statistics
import sys
import time
from itertools import repeat
from pathlib import Path

try:
    import matplotlib

    matplotlib.use("Agg")  # funciona sem janela (servidor, WSL, etc.)
    import matplotlib.pyplot as plt
    from matplotlib.ticker import ScalarFormatter
except ImportError:
    sys.exit("Falta o matplotlib. Instale com:  pip install matplotlib")

from ordenacao import (
    contar_comparacoes,
    ordenacao_por_insercao,
    ordenacao_por_intercalacao,
)

TAMANHOS = [5, 10, 20, 30, 50, 75, 100, 200, 500, 1000]
REPETICOES = 30  # mínimo exigido: 10
SEMENTE = 42  # fixa as listas sorteadas: as contagens de comparações se repetem

PASTA = Path(__file__).resolve().parent
ARQUIVO_CSV = PASTA / "dados.csv"
GRAFICO_TEMPOS = PASTA / "grafico_tempos.png"
GRAFICO_COMPARACOES = PASTA / "grafico_comparacoes.png"

METODOS = {
    "insercao": ordenacao_por_insercao,
    "intercalacao": ordenacao_por_intercalacao,
    "sorted": sorted,
}
ROTULOS = {
    "insercao": "Inserção",
    "intercalacao": "Intercalação",
    "sorted": "sorted() do Python",
}
ESTILOS = {  # cores distinguíveis também por daltônicos, e marcadores diferentes
    "insercao": ("#d55e00", "o"),
    "intercalacao": ("#0072b2", "s"),
    "sorted": ("#009e73", "^"),
}

COLUNAS = (
    ["n", "repeticao"]
    + [f"tempo_{m}_us" for m in METODOS]
    + [f"comp_{m}" for m in METODOS]
)


# ---------------------------------------------------------------------------
# Medição
# ---------------------------------------------------------------------------

def tempo_por_chamada_us(funcao, lista, chamadas):
    """Tempo médio de uma chamada, em microssegundos.

    Para listas pequenas uma única chamada dura menos que o ruído do relógio,
    então cronometramos várias chamadas seguidas sobre a mesma lista e
    dividimos. As funções não modificam a entrada, então isso é seguro.
    """
    inicio = time.perf_counter_ns()
    for _ in repeat(None, chamadas):
        funcao(lista)
    fim = time.perf_counter_ns()
    return (fim - inicio) / chamadas / 1000


def medir(repeticoes, semente):
    rng = random.Random(semente)
    linhas = []
    for n in TAMANHOS:
        chamadas = max(1, 1000 // n)
        for rep in range(1, repeticoes + 1):
            lista = list(range(n))
            rng.shuffle(lista)  # permutação aleatória de 0..n-1
            esperado = sorted(lista)
            linha = {"n": n, "repeticao": rep}

            # Tempo: sobre inteiros puros, sem nenhum embrulho de contagem.
            gc.collect()
            gc.disable()
            try:
                for nome, funcao in METODOS.items():
                    assert funcao(lista) == esperado  # confere e aquece
                    linha[f"tempo_{nome}_us"] = tempo_por_chamada_us(funcao, lista, chamadas)
            finally:
                gc.enable()

            # Comparações: mesma lista, em passada separada (não entra no tempo).
            for nome, funcao in METODOS.items():
                comparacoes, resultado = contar_comparacoes(funcao, lista)
                assert resultado == esperado
                linha[f"comp_{nome}"] = comparacoes

            linhas.append(linha)
        print(f"  n = {n:>4} ok ({repeticoes} repetições)", flush=True)
    return linhas


def salvar_csv(linhas):
    with open(ARQUIVO_CSV, "w", newline="", encoding="utf-8") as f:
        escritor = csv.DictWriter(f, fieldnames=COLUNAS)
        escritor.writeheader()
        for linha in linhas:
            escritor.writerow(
                {k: (f"{v:.4f}" if isinstance(v, float) else v) for k, v in linha.items()}
            )


# ---------------------------------------------------------------------------
# Resumo (médias) e ponto de virada
# ---------------------------------------------------------------------------

def resumir(linhas):
    """Devolve {n: {coluna: média}} a partir das linhas brutas."""
    resumo = {}
    for n in TAMANHOS:
        do_n = [l for l in linhas if l["n"] == n]
        resumo[n] = {
            col: statistics.mean(l[col] for l in do_n)
            for col in COLUNAS
            if col not in ("n", "repeticao")
        }
    return resumo


def ponto_de_virada(resumo, coluna_a, coluna_b):
    """Primeiro n em que b < a e continua assim em todos os n maiores.

    Devolve (ultimo_n_em_que_a_ganha, n_da_virada); o primeiro pode ser None.
    """
    ns = TAMANHOS
    for i, n in enumerate(ns):
        if all(resumo[m][coluna_b] < resumo[m][coluna_a] for m in ns[i:]):
            return (ns[i - 1] if i > 0 else None), n
    return ns[-1], None


def virgula(x, casas):
    return f"{x:.{casas}f}".replace(".", ",")


def imprimir_resumo(resumo):
    print("\nTempos médios (µs):")
    print("| n | Inserção | Intercalação | sorted() |")
    print("|---:|---:|---:|---:|")
    for n in TAMANHOS:
        r = resumo[n]
        print(
            f"| {n} | {virgula(r['tempo_insercao_us'], 2)} "
            f"| {virgula(r['tempo_intercalacao_us'], 2)} "
            f"| {virgula(r['tempo_sorted_us'], 2)} |"
        )

    print("\nComparações médias:")
    print("| n | Inserção | Intercalação | sorted() |")
    print("|---:|---:|---:|---:|")
    for n in TAMANHOS:
        r = resumo[n]
        print(
            f"| {n} | {virgula(r['comp_insercao'], 1)} "
            f"| {virgula(r['comp_intercalacao'], 1)} "
            f"| {virgula(r['comp_sorted'], 1)} |"
        )

    # log2(n!) é o mínimo de comparações que qualquer ordenação por comparação
    # precisa, em média, sobre permutações aleatórias (e ≈ n·log2(n) − 1,44·n).
    print("\nExtra — comparações do sorted() x limites teóricos:")
    print("| n | sorted() | n·log2(n) | log2(n!) | sorted()/(n·log2 n) | sorted()/log2(n!) |")
    print("|---:|---:|---:|---:|---:|---:|")
    for n in TAMANHOS:
        c = resumo[n]["comp_sorted"]
        n_log_n = n * math.log2(n)
        minimo = math.lgamma(n + 1) / math.log(2)
        print(
            f"| {n} | {virgula(c, 1)} | {virgula(n_log_n, 1)} | {virgula(minimo, 1)} "
            f"| {virgula(c / n_log_n, 2)} | {virgula(c / minimo, 2)} |"
        )

    for titulo, col_a, col_b in (
        ("tempo", "tempo_insercao_us", "tempo_intercalacao_us"),
        ("comparações", "comp_insercao", "comp_intercalacao"),
    ):
        antes, virada = ponto_de_virada(resumo, col_a, col_b)
        print(
            f"\nVirada ({titulo}): intercalação passa a ganhar em n = {virada} "
            f"(inserção ainda ganhava em n = {antes})."
        )


# ---------------------------------------------------------------------------
# Gráficos
# ---------------------------------------------------------------------------

def _formatar_eixos(ax, ylabel, titulo):
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xticks(TAMANHOS)
    ax.get_xaxis().set_major_formatter(ScalarFormatter())
    ax.minorticks_off()
    ax.set_xlabel("n (tamanho da lista, escala log)")
    ax.set_ylabel(ylabel)
    ax.set_title(titulo)
    ax.grid(True, which="major", alpha=0.3)
    ax.legend()


def grafico_tempos(resumo):
    fig, ax = plt.subplots(figsize=(8, 5))
    for nome in METODOS:
        cor, marcador = ESTILOS[nome]
        ax.plot(
            TAMANHOS,
            [resumo[n][f"tempo_{nome}_us"] for n in TAMANHOS],
            marker=marcador, color=cor, label=ROTULOS[nome],
        )
    _formatar_eixos(ax, "tempo médio (µs, escala log)", "Tempo de ordenação (média de repetições)")
    fig.tight_layout()
    fig.savefig(GRAFICO_TEMPOS, dpi=150)
    plt.close(fig)


def grafico_comparacoes(resumo):
    fig, ax = plt.subplots(figsize=(8, 5))
    for nome in METODOS:
        cor, marcador = ESTILOS[nome]
        ax.plot(
            TAMANHOS,
            [resumo[n][f"comp_{nome}"] for n in TAMANHOS],
            marker=marcador, color=cor, label=ROTULOS[nome],
        )
    ax.plot(
        TAMANHOS, [n * math.log2(n) for n in TAMANHOS],
        linestyle="--", color="gray", label="n·log2(n) (referência)",
    )
    _formatar_eixos(ax, "comparações médias (escala log)", "Número de comparações (média de repetições)")
    fig.tight_layout()
    fig.savefig(GRAFICO_COMPARACOES, dpi=150)
    plt.close(fig)


# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--repeticoes", type=int, default=REPETICOES,
                        help=f"repetições por tamanho (padrão {REPETICOES}, mínimo 10)")
    parser.add_argument("--semente", type=int, default=SEMENTE,
                        help=f"semente das listas aleatórias (padrão {SEMENTE})")
    args = parser.parse_args()
    if args.repeticoes < 10:
        parser.error("use pelo menos 10 repetições")

    print(f"Medindo n = {TAMANHOS} com {args.repeticoes} repetições cada...")
    linhas = medir(args.repeticoes, args.semente)
    salvar_csv(linhas)
    resumo = resumir(linhas)
    grafico_tempos(resumo)
    grafico_comparacoes(resumo)
    imprimir_resumo(resumo)
    print(f"\nGerados: {ARQUIVO_CSV.name}, {GRAFICO_TEMPOS.name}, {GRAFICO_COMPARACOES.name}")


if __name__ == "__main__":
    main()
