# Inserção x Intercalação

Comparação entre a ordenação por inserção (insertion sort) e a ordenação por intercalação (merge sort), com o `sorted()` do Python como referência.

## Arquivos

| arquivo | o que é |
|---|---|
| `ordenacao.py` | as funções `insercao` e `intercalacao` |
| `testes.py` | testes que provam que as duas ordenam certo |
| `medir.py` | roda as medições e gera o CSV e os gráficos |
| `dados.csv` | os números brutos das medições (uma linha por repetição) |
| `grafico_tempo.png` | gráfico dos tempos médios |
| `grafico_comparacoes.png` | gráfico das comparações médias |
| `RELATORIO.md` | a análise dos resultados |

## Requisitos

- Python 3.8 ou mais novo
- matplotlib

```bash
pip install matplotlib
```

## Como rodar

Entre na pasta do projeto e rode os testes:

```bash
python testes.py
```

Depois rode as medições:

```bash
python medir.py
```

O `medir.py` apaga e recria `dados.csv`, `grafico_tempo.png` e `grafico_comparacoes.png`, e mostra no terminal uma tabela com as médias. Leva alguns segundos.

## Como as medições são feitas

- Tamanhos: n = 5, 10, 20, 30, 50, 75, 100, 200, 500 e 1000.
- Para cada n são geradas 50 listas aleatórias. As três funções (inserção, intercalação e `sorted()`) ordenam as mesmas listas, e o resultado é a média das 50 repetições.
- O tempo é medido com `time.perf_counter()`.
- As comparações são contadas envolvendo cada número em uma classe `Contador`, que soma 1 a cada chamada de `__lt__` (`<`). As duas implementações só comparam usando `<`, igual ao `sorted()`, então a mesma contagem vale para os três.
- A semente aleatória é fixa (`random.seed(2026)`), então as listas, e portanto as comparações, são sempre as mesmas. Os tempos mudam um pouco de uma execução para outra e de uma máquina para outra.

## Colunas do `dados.csv`

| coluna | significado |
|---|---|
| `algoritmo` | `insercao`, `intercalacao` ou `sorted` |
| `n` | tamanho da lista |
| `repeticao` | número da repetição (1 a 50) |
| `tempo_s` | tempo da ordenação em segundos |
| `comparacoes` | número de comparações feitas |
