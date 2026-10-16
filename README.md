# Ordenação por inserção × ordenação por intercalação

Implementação dos dois algoritmos, testes, medição de tempo e de número de
comparações (com o `sorted()` do Python como referência) e análise dos
resultados.

## Requisitos

- Python 3 (testado com 3.12 e 3.13; usa apenas recursos básicos da linguagem)
- matplotlib, só para os gráficos:

```
pip install matplotlib
```

## Como rodar

Todos os comandos são executados dentro da pasta do projeto. Em alguns sistemas
o comando é `python3` em vez de `python`.

**Testes** (35 testes; incluem lista vazia, um elemento, todos iguais, já
ordenada e invertida):

```
python testes.py
```

**Medição completa** (costuma levar menos de um minuto):

```
python medir.py
```

Isso refaz do zero, sobrescrevendo se já existirem:

| arquivo gerado | conteúdo |
|---|---|
| `dados.csv` | números brutos, uma linha por repetição |
| `grafico_tempos.png` | tempo médio × n |
| `grafico_comparacoes.png` | comparações médias × n |

No final, o script imprime no terminal as tabelas de médias, a tabela do extra
(comparações do `sorted()` × n·log2(n)) e o ponto de virada.

Opções (não são necessárias):

```
python medir.py --repeticoes 50   # padrão: 30 (mínimo aceito: 10)
python medir.py --semente 7       # padrão: 42
```

## Arquivos

| arquivo | o que é |
|---|---|
| `ordenacao.py` | os dois métodos de ordenação e o contador de comparações |
| `testes.py` | testes que provam que ordenam certo |
| `medir.py` | roda as medições e gera o CSV e os gráficos |
| `dados.csv` | os números brutos das medições |
| `RELATORIO.md` | a análise |
| `grafico_tempos.png`, `grafico_comparacoes.png` | os gráficos usados no relatório |

## Formato do `dados.csv`

Colunas: `n`, `repeticao`, `tempo_insercao_us`, `tempo_intercalacao_us`,
`tempo_sorted_us`, `comp_insercao`, `comp_intercalacao`, `comp_sorted`.
Tempos em microssegundos. São 10 tamanhos × 30 repetições = 300 linhas.

## Sobre a reprodutibilidade

- As listas aleatórias usam semente fixa, então **o número de comparações da
  inserção e da intercalação sai idêntico** a cada execução, em qualquer máquina.
  As do `sorted()` podem variar um pouco entre versões do Python.
- Os **tempos variam um pouco** a cada execução e dependem da máquina. Os valores
  do `RELATORIO.md` vêm da execução que gerou o `dados.csv` entregue. Na sua
  máquina os números absolutos serão outros, mas a ordem entre os métodos e o
  formato das curvas deve se manter.
