# Análise de Performance TikTok Shop

Projeto de portfólio em análise de dados para e-commerce: a análise de performance de uma loja **fictícia** no TikTok Shop Brasil (beleza, moda, casa e eletrônicos) ao longo de 24 semanas, de 01/06 a 15/11/2026.

> **Os dados são simulados.** Foram gerados por um script Python com parâmetros plausíveis de mercado (participação por canal, conversão, ticket médio, reembolso). Nenhum número pertence a uma loja real.

## Perguntas de negócio

1. Quais canais trazem faturamento, e quais convertem?
2. Vale mais a pena investir em creators grandes ou pequenos?
3. Onde a loja está perdendo margem?
4. Quando a audiência compra?
5. Quanto pesam as datas de calendário (Dia dos Pais, 9.9, 11.11)?

## Principais achados

| Tema | Achado |
|---|---|
| Visão geral | R$ 6,89 mi de GMV, 91,5 mil pedidos, ticket médio de R$ 75,33 e conversão de 5,0% |
| Canais | **Live** gerou 39% do GMV, com conversão de 6,8%: 2,2x a dos vídeos da própria loja (3,1%) |
| Creators | **Micro creators** (10–100 mil seguidores) retornaram **6,9x** o investimento; os **macro** (>500 mil), **2,1x** |
| Reembolso | **Moda** devolve 10,4% do GMV (beleza: 3,8%). A calça wide leg, campeã de vendas, tem 16,8% de reembolso |
| Horário | Pico de pedidos às **21h**; domingo é o melhor dia |
| Calendário | A semana do **11.11** faturou **3,2x** a média das demais |

## Recomendações

- **Live:** fixar uma grade de lives no horário nobre (20h–22h) e usar o almoço para lives curtas de oferta.
- **Creators:** migrar parte da taxa fixa paga a creators grandes para mais amostras e comissão maior para micro e nano creators.
- **Produto:** revisar tabela de medidas, fotos e demonstração de caimento dos itens de moda com reembolso acima de 10% antes de investir mais tráfego neles.
- **Calendário:** aquecer o 12.12 com creators duas semanas antes e reforçar estoque dos itens mais vendidos em live.

## Métricas usadas

| Métrica | Definição |
|---|---|
| GMV | Valor bruto das vendas, antes de reembolsos, taxas e frete |
| CTR | Cliques ÷ impressões |
| Conversão | Pedidos ÷ cliques |
| Taxa de reembolso | Valor reembolsado ÷ GMV |
| ROI de creator | GMV atribuído ÷ (comissão de 12% + taxa fixa + custo das amostras) |

## Estrutura

```
gerar_dados.py          gera os dados simulados (semente fixa, resultado reproduzível)
analise.py              calcula todos os indicadores acima
dados/
  vendas_semanais.csv   impressões, cliques, pedidos, GMV e reembolsos por semana × canal × categoria
  creators.csv          48 creators afiliados: seguidores, vídeos, GMV, comissão, taxa fixa, amostras
  pedidos_por_hora.csv  pedidos por dia da semana × hora
  top_produtos.csv      12 produtos: preço, pedidos, GMV, taxa de reembolso, nota
```

## Como rodar

Requer apenas Python 3, sem bibliotecas externas.

```bash
python gerar_dados.py   # recria os CSVs em ./dados
python analise.py       # imprime os indicadores
```

## Dashboard

Os resultados também estão em um dashboard interativo, com gráfico semanal por canal, funil, ROI de creators, mapa de calor de horários e tabela de produtos.
