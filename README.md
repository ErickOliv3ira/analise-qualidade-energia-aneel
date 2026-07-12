# Análise da Qualidade do Fornecimento de Energia — ANEEL

> 🚧 Projeto em construção — Fase 0 (setup)

Pipeline completo de dados analisando o desempenho das distribuidoras de energia elétrica do Brasil (2020–2025) com dados abertos da ANEEL: DEC/FEC, limites regulatórios, compensações, reclamações e tarifas.

**Pergunta central:** quais distribuidoras entregam o pior serviço — e o consumidor está pagando caro por um serviço ruim?

## Arquitetura

Extração (API CKAN) → PostgreSQL `raw` → `staging` (data quality) → `dw` (star schema) → SQL analítico → Power BI → relatório executivo

## Como reproduzir

```bash
cp .env.example .env          # ajuste a senha
docker compose up -d          # PostgreSQL 16 com schemas raw/staging/dw
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m src.pipeline --full # (em construção)
```

## Documentação

- [Roadmap completo](docs/roadmap.md)
- [Status e progresso](docs/status_progresso.md)
- [Registro de decisões](docs/registro_decisoes.md)
- Dicionário de dados: em construção (Fase 1)

## Stack

PostgreSQL 16 (Docker) · Python 3.11 · SQL · Power BI · GitHub

---
*Uso de IA: Claude como apoio de pair programming e documentação, com decisões técnicas validadas manualmente contra os dicionários oficiais da ANEEL.*
