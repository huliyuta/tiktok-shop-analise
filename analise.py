"""Calcula os indicadores do projeto a partir dos CSVs em ./dados.

Uso: python analise.py   (só biblioteca padrão, sem dependências)
"""
import csv
from collections import defaultdict
from pathlib import Path

DADOS = Path(__file__).parent / "dados"


def ler(nome):
    with open(DADOS / nome, encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def brl(v):
    return f"R$ {v:,.0f}".replace(",", ".")


def pct(v):
    return f"{v * 100:.1f}%".replace(".", ",")


vendas = ler("vendas_semanais.csv")
creators = ler("creators.csv")
horario = ler("pedidos_por_hora.csv")
produtos = ler("top_produtos.csv")

# ------------------------------------------------------------- visão geral
gmv = sum(float(r["gmv"]) for r in vendas)
pedidos = sum(int(r["pedidos"]) for r in vendas)
cliques = sum(int(r["cliques"]) for r in vendas)
reemb = sum(float(r["valor_reembolsado"]) for r in vendas)
print("VISÃO GERAL (24 semanas)")
print(f"  GMV ............ {brl(gmv)}")
print(f"  Pedidos ........ {pedidos:,}".replace(",", "."))
print("  Ticket médio ... R$ " + f"{gmv / pedidos:.2f}".replace(".", ","))
print(f"  Conversão ...... {pct(pedidos / cliques)}")
print(f"  Reembolso ...... {pct(reemb / gmv)}")

# ------------------------------------------------------------- canais
canal = defaultdict(lambda: defaultdict(float))
for r in vendas:
    c = canal[r["canal"]]
    for k in ("gmv", "impressoes", "cliques", "pedidos", "valor_reembolsado"):
        c[k] += float(r[k])
print("\nFUNIL POR CANAL")
print(f"  {'canal':<18}{'GMV':>14}{'part.':>8}{'CTR':>8}{'conv.':>8}{'reemb.':>8}")
for nome, c in sorted(canal.items(), key=lambda x: -x[1]["gmv"]):
    print(f"  {nome:<18}{brl(c['gmv']):>14}{pct(c['gmv'] / gmv):>8}"
          f"{pct(c['cliques'] / c['impressoes']):>8}{pct(c['pedidos'] / c['cliques']):>8}"
          f"{pct(c['valor_reembolsado'] / c['gmv']):>8}")

# ------------------------------------------------------------- categorias
cat = defaultdict(lambda: [0.0, 0.0])
for r in vendas:
    cat[r["categoria"]][0] += float(r["gmv"])
    cat[r["categoria"]][1] += float(r["valor_reembolsado"])
print("\nREEMBOLSO POR CATEGORIA")
for nome, (g, rb) in sorted(cat.items(), key=lambda x: -x[1][1] / x[1][0]):
    print(f"  {nome:<14}{pct(rb / g):>8}")

# ------------------------------------------------------------- picos
semanas = defaultdict(float)
for r in vendas:
    semanas[r["semana"]] += float(r["gmv"])
pico = max(semanas, key=semanas.get)
media_outras = (gmv - semanas[pico]) / (len(semanas) - 1)
x_pico = f"{semanas[pico] / media_outras:.1f}".replace(".", ",")
print(f"\nSEMANA DE PICO: {pico} ({x_pico}x a média das demais)")

# ------------------------------------------------------------- creators
tier = defaultdict(lambda: [0, 0.0, 0.0])
for r in creators:
    t = tier[r["tier"]]
    t[0] += 1
    t[1] += float(r["gmv"])
    t[2] += float(r["comissao"]) + float(r["taxa_fixa"]) + float(r["custo_amostras"])
print("\nROI POR PORTE DE CREATOR (GMV ÷ custo total)")
for nome, (n, g, custo) in tier.items():
    roi = f"{g / custo:.1f}".replace(".", ",")
    print(f"  {nome:<22}{n:>4} creators{roi:>8}x")

# ------------------------------------------------------------- horário
por_hora, por_dia = defaultdict(int), defaultdict(int)
for r in horario:
    por_hora[int(r["hora"])] += int(r["pedidos"])
    por_dia[r["dia"]] += int(r["pedidos"])
print(f"\nHORÁRIO DE PICO: {max(por_hora, key=por_hora.get)}h · MELHOR DIA: {max(por_dia, key=por_dia.get)}")

# ------------------------------------------------------------- produtos
print("\nPRODUTOS COM REEMBOLSO ACIMA DE 10%")
for p in sorted(produtos, key=lambda p: -float(p["taxa_reembolso"])):
    if float(p["taxa_reembolso"]) > 0.10:
        print(f"  {p['produto']:<32}{pct(float(p['taxa_reembolso'])):>8}  ({p['pedidos']} pedidos)")
