# 05 — Status e Progresso

> **Arquivo vivo.** Ao concluir itens numa conversa, pedir ao Claude o texto atualizado deste arquivo e substituí-lo no conhecimento do projeto. É ele que dá continuidade entre conversas.

**Fase atual:** Fase 0 — Setup do ambiente
**Última atualização:** 12/07/2026
**Próxima ação:** criar repositório no GitHub e docker-compose do PostgreSQL

---

## Fase 0 — Setup (2–3 dias)
- [ ] Repositório `analise-qualidade-energia-aneel` criado no GitHub
- [ ] Estrutura de pastas
- [ ] `docker-compose.yml` (PostgreSQL 16 + volume)
- [ ] venv + `requirements.txt`
- [ ] `.env` / `.env.example`
- [ ] Schemas `raw`, `staging`, `dw` criados
- [ ] Primeiro commit + README inicial

## Fase 1 — Exploração e dicionário (1 semana)
- [ ] Amostras baixadas + dicionários oficiais lidos
- [ ] `01_eda_fontes.ipynb` (shape, tipos, nulos, domínios, chaves)
- [ ] Grão real de cada fonte confirmado
- [ ] Estratégia de join entre fontes validada (de-para se necessário)
- [ ] `docs/dicionario_dados.md`
- [ ] Regras de data quality definidas

## Fase 2 — Extração (1 semana)
- [ ] `src/extract/aneel_client.py` (CKAN package_show + download streaming, retry)
- [ ] `raw.log_extracao`
- [ ] Carga 1:1 no schema `raw` (COPY)
- [ ] Idempotência testada

## Fase 3 — ETL + Data Quality (1–2 semanas)
- [ ] Transformações raw → staging (tipos, encoding, dedup, filtro 2020–2025/B1)
- [ ] `src/quality/checks.py` (completude, unicidade, domínio, integridade)
- [ ] `staging.log_quality`
- [ ] `docs/data_quality.md`

## Fase 4 — Data Warehouse (1 semana)
- [ ] DDL de dims e fatos em `sql/ddl/`
- [ ] Diagrama dbdiagram → `docs/img/star_schema.png`
- [ ] Carga de dimensões e fatos
- [ ] Queries de reconciliação em `sql/checks/`

## Fase 5 — SQL Analítico (1 semana)
- [ ] `vw_ranking_distribuidoras`
- [ ] `vw_evolucao_dec_fec`
- [ ] `vw_transgressao_limites`
- [ ] `vw_tarifa_vs_qualidade`
- [ ] `vw_reclamacoes_vs_continuidade`
- [ ] `vw_mapa_uf`

## Fase 6 — Dashboard Power BI (1–2 semanas)
- [ ] Nivelamento DAX (2 dias)
- [ ] Página Visão Executiva
- [ ] Página Ranking
- [ ] Página Mapa do Brasil
- [ ] Página Tarifa × Qualidade
- [ ] Página Reclamações
- [ ] Segmentações globais

## Fase 7 — Relatório e publicação (1 semana)
- [ ] `docs/relatorio_executivo.md`
- [ ] README final (arquitetura, reprodução, prints, uso de IA)
- [ ] Post no LinkedIn

## Fase 8 — Automação (paralela)
- [ ] `pipeline.py` orquestrador com logging
- [ ] `--full` / `--incremental`
- [ ] (Opcional) GitHub Actions com checks de qualidade

---

## Bloqueios / pendências atuais

*(nenhum)*

## Ideias estacionadas (fase 2 — NÃO implementar agora)

- Cruzamento com dados climáticos e IBGE
- IASC se não couber na v1
- Publicação no Power BI Service
