"""Gera dados SIMULADOS de uma loja fictícia no TikTok Shop Brasil (jun–nov/2026).

Nenhum dado aqui é real. Os parâmetros (participação por canal, conversão, ticket,
reembolso) foram escolhidos para refletir padrões plausíveis do mercado e criar
uma história analisável para portfólio.

Uso: python gerar_dados.py   (gera os CSVs em ./dados)
"""
import csv
import math
import random
from datetime import date, timedelta
from pathlib import Path

random.seed(1111)
OUT = Path(__file__).parent / "dados"
OUT.mkdir(exist_ok=True)

# ---------------------------------------------------------------- vendas semanais
CANAIS = {
    # canal: (participação no GMV, CTR impressão→clique, conversão clique→pedido, mult. reembolso)
    "Live":              (0.34, 0.045, 0.068, 1.25),
    "Vídeo de afiliado": (0.30, 0.026, 0.049, 1.00),
    "Vídeo da loja":     (0.14, 0.019, 0.031, 0.95),
    "Vitrine":           (0.12, 0.032, 0.038, 0.90),
    "Busca":             (0.10, 0.065, 0.056, 0.85),
}
CATEGORIAS = {
    # categoria: (participação, ticket médio R$, taxa de reembolso)
    "Beleza":      (0.38, 62.0, 0.035),
    "Moda":        (0.30, 89.0, 0.098),
    "Casa":        (0.17, 74.0, 0.045),
    "Eletrônicos": (0.15, 139.0, 0.060),
}

inicio = date(2026, 6, 1)  # segunda-feira
semanas = 24               # até a semana de 09/11 (11.11)


def fator_sazonal(semana: date, canal: str, categoria: str) -> float:
    f = 1.0
    if semana == date(2026, 11, 9):            # 11.11
        f *= 2.6 if canal == "Live" else 2.1
    elif semana == date(2026, 11, 2):          # aquecimento do 11.11
        f *= 1.3
    if semana == date(2026, 8, 3) and categoria == "Eletrônicos":  # Dia dos Pais
        f *= 1.9
    if semana in (date(2026, 9, 7), date(2026, 9, 14)) and canal == "Live":  # 9.9
        f *= 1.35
    return f


with open(OUT / "vendas_semanais.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["semana", "canal", "categoria", "impressoes", "cliques", "pedidos",
                "gmv", "pedidos_reembolsados", "valor_reembolsado"])
    for i in range(semanas):
        semana = inicio + timedelta(weeks=i)
        total = 180_000 * (1.028 ** i)  # crescimento de ~2,8% por semana
        for canal, (sh_c, ctr, conv, mult_r) in CANAIS.items():
            # Live ganha espaço ao longo do período (a loja aumentou a frequência das lives)
            sh = sh_c * (1 + (0.012 * i if canal == "Live" else -0.003 * i))
            for cat, (sh_k, ticket, reemb) in CATEGORIAS.items():
                gmv = total * sh * sh_k * fator_sazonal(semana, canal, cat) * random.uniform(0.88, 1.12)
                tk = ticket * random.uniform(0.94, 1.06) * (0.92 if canal == "Live" else 1.0)
                pedidos = max(1, round(gmv / tk))
                gmv = round(pedidos * tk, 2)
                cliques = round(pedidos / (conv * random.uniform(0.9, 1.1)))
                impressoes = round(cliques / (ctr * random.uniform(0.9, 1.1)))
                taxa_r = reemb * mult_r * random.uniform(0.8, 1.2)
                ped_r = round(pedidos * taxa_r)
                val_r = round(ped_r * tk, 2)
                w.writerow([semana.isoformat(), canal, cat, impressoes, cliques, pedidos,
                            f"{gmv:.2f}", ped_r, f"{val_r:.2f}"])

# ---------------------------------------------------------------- creators (afiliados)
TIERS = {
    # tier: (qtd, seguidores min/max, GMV min/max, taxa fixa min/max)
    "Nano (<10 mil)":       (20, 2_000, 9_900, 3_000, 18_000, 0, 0),
    "Micro (10–100 mil)":   (16, 10_000, 99_000, 15_000, 60_000, 0, 1_000),
    "Médio (100–500 mil)":  (8, 100_000, 480_000, 40_000, 90_000, 4_000, 8_000),
    "Macro (>500 mil)":     (4, 520_000, 2_400_000, 70_000, 160_000, 25_000, 45_000),
}
COMISSAO = 0.12
CUSTO_AMOSTRA = 55.0

with open(OUT / "creators.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["creator", "tier", "seguidores", "videos", "views", "pedidos", "gmv",
                "comissao", "taxa_fixa", "custo_amostras"])
    n = 0
    for tier, (qtd, smin, smax, gmin, gmax, fmin, fmax) in TIERS.items():
        for _ in range(qtd):
            n += 1
            seg = round(math.exp(random.uniform(math.log(smin), math.log(smax))))
            gmv = round(random.uniform(gmin, gmax), 2)
            pedidos = round(gmv / random.uniform(68, 84))
            videos = random.randint(4, 14) if "Macro" not in tier else random.randint(2, 4)
            views = round(seg * videos * random.uniform(0.35, 1.6))
            taxa = round(random.uniform(fmin, fmax), -2) if fmax else 0
            amostras = videos * CUSTO_AMOSTRA
            w.writerow([f"CR-{n:03d}", tier, seg, videos, views, pedidos, f"{gmv:.2f}",
                        f"{gmv * COMISSAO:.2f}", f"{taxa:.2f}", f"{amostras:.2f}"])

# ---------------------------------------------------------------- pedidos por hora (lives)
DIAS = ["seg", "ter", "qua", "qui", "sex", "sáb", "dom"]
PESO_DIA = [0.85, 0.9, 1.15, 0.95, 0.8, 0.9, 1.3]
with open(OUT / "pedidos_por_hora.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["dia", "ordem_dia", "hora", "pedidos"])
    for d, (dia, peso) in enumerate(zip(DIAS, PESO_DIA)):
        for h in range(24):
            noite = math.exp(-((h - 21) ** 2) / 4.5)       # pico 20h–22h
            almoco = 0.35 * math.exp(-((h - 12.5) ** 2) / 2)
            base = 0.04 if 1 <= h <= 7 else 0.12
            pedidos = round(1500 * peso * (noite + almoco + base) * random.uniform(0.9, 1.1))
            w.writerow([dia, d, h, pedidos])

# ---------------------------------------------------------------- top produtos
PRODUTOS = [
    ("SKU-101", "Sérum vitamina C 30 ml", "Beleza", 59.9, 0.022, 4.8),
    ("SKU-102", "Protetor solar facial FPS 50", "Beleza", 64.9, 0.018, 4.7),
    ("SKU-103", "Kit pincéis de maquiagem 12 peças", "Beleza", 49.9, 0.041, 4.5),
    ("SKU-201", "Calça wide leg alfaiataria", "Moda", 119.9, 0.168, 3.9),
    ("SKU-202", "Vestido midi canelado", "Moda", 99.9, 0.121, 4.2),
    ("SKU-203", "Cropped de tricô", "Moda", 69.9, 0.064, 4.5),
    ("SKU-301", "Organizador acrílico de maquiagem", "Casa", 79.9, 0.072, 4.3),
    ("SKU-302", "Garrafa térmica 1 L", "Casa", 69.9, 0.031, 4.7),
    ("SKU-401", "Fone bluetooth TWS", "Eletrônicos", 129.9, 0.094, 4.1),
    ("SKU-402", "Luminária LED de mesa", "Eletrônicos", 89.9, 0.038, 4.6),
    ("SKU-403", "Mini ventilador portátil", "Eletrônicos", 59.9, 0.047, 4.4),
    ("SKU-104", "Lip tint hidratante", "Beleza", 34.9, 0.015, 4.8),
]
with open(OUT / "top_produtos.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["sku", "produto", "categoria", "preco", "pedidos", "gmv",
                "taxa_reembolso", "nota_media"])
    for sku, nome, cat, preco, reemb, nota in PRODUTOS:
        pedidos = random.randint(1_400, 6_500)
        if sku == "SKU-201":
            pedidos = 5_870  # campeão de vendas da Moda, e de devoluções
        w.writerow([sku, nome, cat, f"{preco:.2f}", pedidos, f"{pedidos * preco:.2f}",
                    f"{reemb:.3f}", f"{nota:.1f}"])

print("CSVs gerados em", OUT)
