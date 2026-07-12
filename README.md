# Análise da Qualidade do Fornecimento de Energia — ANEEL

> 🚧 Projeto em construção — Fase 0 (setup)

Pipeline completo de dados analisando o desempenho das distribuidoras de energia elétrica do Brasil (2020–2025) com dados abertos da ANEEL: DEC/FEC, limites regulatórios, compensações, reclamações e tarifas.

**Pergunta central:** quais distribuidoras entregam o pior serviço — e o consumidor está pagando caro por um serviço ruim?

## Arquitetura

Extração (API CKAN) → PostgreSQL `raw` → `staging` (data quality) → `dw` (star schema) → SQL analítico → Power BI → relatório executivo

## Como reproduzir

```bash
cp .env.example .env                     # ajuste a senha
# subir PostgreSQL 16 (ver docs/setup_postgres_portable.md — caminho suportado no ambiente atual)
python -m venv .venv && source .venv/Scripts/activate   # Windows
pip install -r requirements.txt
python -m src.test_connection            # valida conexao e schemas
python -m src.pipeline --full            # (em construção)
```

> **Nota:** `docker-compose.yml` está no repo como referência de arquitetura. O ambiente de desenvolvimento atual roda o Postgres portable (sem Docker) — ver decisão **D-007** e o guia em [`docs/setup_postgres_portable.md`](docs/setup_postgres_portable.md).

## Documentação

- [Roadmap completo](docs/roadmap.md)
- [Status e progresso](docs/status_progresso.md)
- [Registro de decisões](docs/registro_decisoes.md)
- Dicionário de dados: em construção (Fase 1)

## Stack

PostgreSQL 16 · Python 3.12 · SQL · Power BI · GitHub

---
*Uso de IA: Claude como apoio de pair programming e documentação, com decisões técnicas validadas manualmente contra os dicionários oficiais da ANEEL.*
