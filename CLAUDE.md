# CLAUDE.md

Projeto de portfólio de dados: análise da qualidade do fornecimento de energia elétrica no Brasil com dados abertos da ANEEL. Pipeline: extração via API CKAN → PostgreSQL (raw → staging → dw em star schema) → views SQL analíticas → Power BI → relatório executivo.

## Comandos

```bash
# PostgreSQL: no ambiente atual usamos Postgres portable (ver docs/setup_postgres_portable.md).
# Comandos abreviados assumem que o servidor ja esta rodando.
"$USERPROFILE/pgsql/bin/pg_ctl.exe" -D "$USERPROFILE/pgdata" -l "$USERPROFILE/pgdata/server.log" start
python -m venv .venv && source .venv/Scripts/activate   # Windows (bash: .venv/Scripts/activate)
pip install -r requirements.txt
python -m src.test_connection             # valida conexao e schemas raw/staging/dw
python -m src.pipeline --full             # pipeline completo (extract → raw → staging → dw)
python -m src.pipeline --incremental      # reprocessa apenas o ano corrente
python -m src.quality.checks              # roda validações de data quality
```

Credenciais do banco em `.env` (copiar de `.env.example`). Nunca commitar `.env`.
`docker-compose.yml` fica como referência de arquitetura; setup real ver decisão D-007 e `docs/setup_postgres_portable.md`.

## Arquitetura

- `src/extract/` — cliente CKAN (`package_show` descobre URLs; download streaming com retry). Não hardcodar URLs de CSV.
- `src/load/` — carga 1:1 no schema `raw` (tudo TEXT, via COPY) e carga do `dw` (dims antes dos fatos).
- `src/transform/` — raw → staging: tipos, encoding, dedup, filtro do escopo (2020–2025; tarifas só subgrupo B1 convencional).
- `src/quality/` — checks de completude, unicidade do grão, domínio e integridade referencial; resultados em `staging.log_quality`.
- `sql/ddl/` — criação de schemas, dimensões e fatos. `sql/views/` — uma view por pergunta de negócio. `sql/checks/` — reconciliação staging × dw.
- Modelagem completa em `docs/` e no arquivo 04 do Claude Project.

## Convenções

- SQL: nunca `SELECT *`; identificadores snake_case; prefixos `dim_`, `fato_`, `vw_`, `stg_`, `log_`; operações destrutivas SEMPRE em arquivo `.sql` versionado, nunca inline.
- Python: queries parametrizadas (nunca f-string com valores); scripts idempotentes; `logging` estruturado, não `print`; type hints; credenciais só via `.env`.
- CSVs da ANEEL: `encoding='latin-1'`, `sep=';'`, `decimal=','` — sempre explícitos no `read_csv`.
- Commits pequenos, mensagem imperativa em inglês.

## Escopo — não expandir sem registrar decisão

Período 2020–2025. FORA do escopo: interrupções evento a evento (dezenas de GB), dados climáticos, IBGE, indicadores individuais (DIC/FIC/DMIC). Se uma tarefa exigir algo fora do escopo, alertar antes e sugerir registrar em `docs/registro_decisoes.md`.

## Grãos dos fatos (não violar)

- `fato_continuidade`: conjunto elétrico × mês
- `fato_reclamacao`: distribuidora × tipologia × mês
- `fato_tarifa`: distribuidora × vigência
- Cruzamentos entre fontes acontecem no nível distribuidora × período (continuidade agregada em views).
