# Roadmap Completo — Projeto 1: Qualidade do Fornecimento de Energia (ANEEL)

**Autor:** Erick Gonçalves Oliveira
**Objetivo do projeto:** Demonstrar um fluxo profissional completo de Analytics Engineering — extração via API, ETL com Data Quality, Data Warehouse dimensional, SQL analítico, dashboard em Power BI e relatório executivo.
**Duração estimada:** 5 a 6 semanas (ritmo part-time, ~1h30/dia útil + fins de semana)

---

## 1. Contexto de negócio (narrativa do projeto)

Uma consultoria de energia foi contratada para avaliar o desempenho das distribuidoras de energia elétrica do Brasil e responder: **quais distribuidoras entregam o pior serviço, e o consumidor está pagando caro por um serviço ruim?**

Esse enquadramento é importante: no README e no relatório final, você conta a história como consultor, não como "estudante fazendo exercício".

## 2. Escopo

### 2.1 Perguntas de negócio (definitivas)

1. Quais distribuidoras têm o pior desempenho de continuidade (DEC/FEC) e quais violam os limites regulatórios da ANEEL?
2. Existe correlação entre tarifa cobrada e qualidade entregue? (paga-se mais por um serviço melhor?)
3. Quais estados e regiões concentram os piores indicadores?
4. As reclamações dos consumidores acompanham a piora dos indicadores técnicos?
5. Quanto as distribuidoras pagaram em compensações por transgressão de limites, e quais são as reincidentes?

### 2.2 Recorte (o que ENTRA)

- **Período:** 2020 a 2025 (6 anos — suficiente para tendência e sazonalidade sem inflar o ETL)
- **Granularidade principal:** distribuidora × mês
- **Drill-down:** conjunto elétrico (unidade geográfica da ANEEL, com município/UF)
- **Indicadores:** DEC, FEC, limites regulatórios, compensações pagas, reclamações por tipologia, tarifas TE/TUSD residenciais (subgrupo B1)

### 2.3 Fora de escopo (o que NÃO entra — anote isso no README)

- Dataset de **interrupções evento a evento** (registra cada queda de energia do país — dezenas de GB; o DEC/FEC já é a agregação oficial disso)
- Dados climáticos e cruzamento com IBGE (possível "fase 2" — deixe documentado como evolução futura)
- Indicadores individuais (DIC/FIC/DMIC) — só os coletivos

> Regra de ouro: escopo fechado é o que separa projeto concluído de projeto abandonado. Resista a expandir antes de entregar a v1.

## 3. Fontes de dados (confirmadas no portal da ANEEL)

Todas no Portal de Dados Abertos da ANEEL: **https://dadosabertos.aneel.gov.br**

| # | Dataset | O que contém | Uso no projeto |
|---|---------|-------------|----------------|
| 1 | **Indicadores Coletivos de Continuidade (DEC e FEC)** — `/dataset/indicadores-coletivos-de-continuidade-dec-e-fec` | Valores apurados de DEC/FEC por conjunto elétrico, limites regulatórios, compensações pagas e atributos físico-elétricos dos conjuntos. Recurso `indicadores-continuidade-coletivos-2020-2029` cobre exatamente o período do escopo | Fato principal + dimensão de conjuntos |
| 2 | **Reclamações no 1º e 2º nível da Distribuidora** — `/dataset/reclamacoes-no-1o-e-2o-niveis-da-distribuidora` | Quantidade de reclamações por distribuidora e tipologia (arquivos separados por ano: 2023, 2024, 2025 + histórico 2010–2022) | Fato de reclamações |
| 3 | **Tarifas de aplicação das distribuidoras** — `/dataset/tarifas-distribuidoras-energia-eletrica` | Valores de TE e TUSD homologados nos reajustes tarifários, por distribuidora, subgrupo e modalidade | Fato de tarifas (filtrar B1 residencial convencional) |
| 4 | *(Bônus)* **IASC — Índice ANEEL de Satisfação do Consumidor** | Pesquisa anual de satisfação por distribuidora | KPI extra de percepção — cruza lindamente com DEC/FEC |

**Como extrair:** o portal roda em **CKAN**, então além do download direto dos CSVs você tem API REST:
- Metadados do dataset: `GET https://dadosabertos.aneel.gov.br/api/3/action/package_show?id=<nome-do-dataset>`
- Consulta paginada aos dados: `GET .../api/3/action/datastore_search?resource_id=<id>&limit=32000&offset=0`

**Estratégia recomendada:** use a API CKAN no `package_show` para descobrir programaticamente a URL dos CSVs e baixá-los via `requests` (streaming). Isso conta como "extração via API" no portfólio e é mais robusto que paginar o datastore para arquivos grandes.

⚠️ **Atenção:** os CSVs da ANEEL costumam vir com encoding `latin-1`/`cp1252`, separador `;` e decimal `,`. Trate isso explicitamente no `pd.read_csv` — e documente no README (é exatamente o tipo de detalhe que entrevistador gosta de ouvir).

## 4. Stack e arquitetura

| Camada | Ferramenta | Observação |
|--------|-----------|------------|
| Linguagem | Python 3.11+ | `requests`, `pandas`, `sqlalchemy`, `psycopg2-binary`, `python-dotenv` |
| Banco | PostgreSQL 16 | Local via Docker (`docker compose up -d`) — já demonstra Docker de brinde |
| Transformação | SQL (views + procedures leves) e pandas | ETL "ELT-like": carga bruta primeiro, transformação dentro do banco |
| Visualização | Power BI Desktop | Conexão direta ao PostgreSQL |
| Modelagem | dbdiagram.io | Exportar PNG do diagrama para o README |
| Versionamento | Git + GitHub | Commits pequenos e mensagens descritivas desde o dia 1 |
| Documentação | Markdown + dicionário de dados | README, `docs/` e um `CLAUDE.md` com convenções (você já domina esse padrão) |

### Arquitetura de dados (3 camadas no PostgreSQL)

```
CSV/API ANEEL ──▶ data/raw/ (arquivos originais, intocados)
                     │
                     ▼
              schema RAW ────▶ schema STAGING ────▶ schema DW
              (espelho 1:1     (tipado, limpo,       (star schema:
               dos CSVs,        deduplicado,          fatos + dimensões)
               tudo TEXT)       validado)
```

Manter os três schemas separados (`raw`, `staging`, `dw`) é o que dá cara de pipeline profissional — e rende ótima explicação em entrevista.

## 5. Modelagem dimensional (Star Schema — rascunho v1)

### Dimensões

- **dim_distribuidora** — sk, código ANEEL, nome, sigla, UF principal, região
- **dim_conjunto** — sk, código do conjunto, nome, município, UF, distribuidora, atributos físico-elétricos (extensão de rede, nº de consumidores)
- **dim_tempo** — sk (YYYYMMDD ou YYYYMM), ano, mês, nome do mês, trimestre, semestre
- **dim_tipologia_reclamacao** — sk, tipologia, grupo (comercial, técnica, atendimento)

### Fatos

- **fato_continuidade** — grão: conjunto × mês → dec_apurado, fec_apurado, dec_limite, fec_limite, flag_transgressao_dec, flag_transgressao_fec, valor_compensacao, qtd_consumidores
- **fato_reclamacao** — grão: distribuidora × tipologia × mês → qtd_reclamacoes_n1, qtd_reclamacoes_n2
- **fato_tarifa** — grão: distribuidora × vigência → tarifa_te, tarifa_tusd, tarifa_total_b1, data_inicio_vigencia, data_fim_vigencia

> Validar o grão real na Fase 1 (EDA) antes de cravar o DDL — a periodicidade do DEC/FEC apurado pode ser mensal e anual no mesmo arquivo (campo indicador de período). Isso é decisão de modelagem que você documenta.

## 6. Roadmap detalhado por fases

### Fase 0 — Setup do ambiente (2–3 dias)

- [ ] Criar repositório `analise-qualidade-energia-aneel` no GitHub (público)
- [ ] Estrutura de pastas (ver seção 8)
- [ ] `docker-compose.yml` com PostgreSQL 16 + volume persistente
- [ ] Ambiente virtual Python + `requirements.txt`
- [ ] `.env` com credenciais do banco (e `.env.example` commitado — nunca o `.env` real)
- [ ] Criar schemas `raw`, `staging`, `dw` no banco
- [ ] Primeiro commit + README inicial com a proposta do projeto

**Entregável:** ambiente rodando + repo público com README de intenção.

### Fase 1 — Exploração e dicionário de dados (1 semana)

- [ ] Baixar manualmente uma amostra de cada CSV e abrir os dicionários de dados oficiais (PDFs no próprio portal)
- [ ] Notebook `01_eda_fontes.ipynb`: shape, tipos, nulos, domínios, chaves candidatas de cada fonte
- [ ] Confirmar grão real de cada arquivo (conjunto×mês? distribuidora×ano?)
- [ ] Mapear como fazer o join entre fontes (código da distribuidora — verificar se é consistente entre datasets; pode exigir tabela de-para)
- [ ] Escrever `docs/dicionario_dados.md` com as colunas que serão usadas
- [ ] Decidir e registrar as regras de qualidade (ex.: DEC não pode ser negativo, conjunto sem distribuidora é órfão, etc.)

**Entregável:** dicionário de dados + decisões de modelagem registradas.
**Risco desta fase:** descobrir que o join entre reclamações (nível distribuidora) e continuidade (nível conjunto) exige agregação — é esperado, resolva agregando continuidade para distribuidora×mês na camada DW.

### Fase 2 — Extração (1 semana)

- [ ] `src/extract/aneel_client.py`: cliente da API CKAN (package_show → lista recursos → baixa CSVs com retry e timeout)
- [ ] Download em streaming para `data/raw/` com nome padronizado (`fonte_ano_dataextracao.csv`)
- [ ] Log de extração (arquivo, tamanho, linhas, hash MDF5, timestamp) em tabela `raw.log_extracao`
- [ ] Carga 1:1 dos CSVs no schema `raw` (tudo como TEXT — fidelidade total à origem)
- [ ] Script idempotente: rodar duas vezes não pode duplicar dados

**Entregável:** `python -m src.extract` popula o schema `raw` do zero.

### Fase 3 — ETL + Data Quality (1 a 2 semanas)

- [ ] Transformações `raw → staging`: conversão de tipos (decimal `,`→`.`), encoding, padronização de nomes de colunas (snake_case), deduplicação, tratamento de nulos
- [ ] Filtro do recorte: 2020–2025; tarifas apenas subgrupo B1 convencional
- [ ] Módulo `src/quality/checks.py` com validações automatizadas:
  - Completude (% nulos por coluna crítica)
  - Unicidade da chave do grão
  - Domínio (DEC/FEC ≥ 0; UF válida; datas dentro do período)
  - Integridade referencial (todo conjunto tem distribuidora)
- [ ] Resultados dos checks gravados em `staging.log_quality` — vira até visual no dashboard
- [ ] Relatório de qualidade em `docs/data_quality.md` (quantas linhas entraram, quantas foram rejeitadas e por quê)

**Entregável:** staging limpo + relatório de Data Quality versionado.

### Fase 4 — Data Warehouse (1 semana)

- [ ] DDL das dimensões e fatos em `sql/ddl/` (arquivos `.sql` versionados, identificadores com colchetes/aspas conforme convenção, sem `SELECT *`)
- [ ] Diagrama no dbdiagram.io → exportar PNG para `docs/img/star_schema.png`
- [ ] Carga das dimensões (com surrogate keys) e depois dos fatos
- [ ] `dim_tempo` gerada por script (2019–2026 para folga)
- [ ] Testes de reconciliação: totais do DW batem com staging? (query de conferência versionada)

**Entregável:** DW populado + diagrama no README.

### Fase 5 — SQL Analítico (1 semana)

Criar views em `sql/views/` respondendo cada pergunta de negócio — cada view comentada com a pergunta que responde:

- [ ] `vw_ranking_distribuidoras` — ranking anual por DEC/FEC com `RANK() OVER (PARTITION BY ano ...)`
- [ ] `vw_evolucao_dec_fec` — variação YoY com `LAG()` e média móvel 12 meses com janela deslizante
- [ ] `vw_transgressao_limites` — % de conjuntos acima do limite por distribuidora + total de compensações (CTE + agregação condicional)
- [ ] `vw_tarifa_vs_qualidade` — tarifa B1 × DEC por distribuidora/ano (base do scatter no Power BI)
- [ ] `vw_reclamacoes_vs_continuidade` — reclamações por 10 mil consumidores × DEC, por distribuidora/mês
- [ ] `vw_mapa_uf` — indicadores agregados por estado

**Entregável:** ≥6 views demonstrando CTEs, window functions e joins dimensionais.

### Fase 6 — Dashboard Power BI (1 a 2 semanas)

Como seu Power BI é básico, reserve os primeiros 2 dias para nivelamento dirigido: relacionamentos, medidas DAX básicas (`CALCULATE`, `DIVIDE`, time intelligence) e formatação condicional.

Páginas do relatório:

- [ ] **Visão Executiva** — cards (DEC médio Brasil, FEC médio, total compensações, % conjuntos em transgressão) + tendência mensal
- [ ] **Ranking de Distribuidoras** — tabela com formatação condicional + top/bottom 10
- [ ] **Mapa do Brasil** — DEC médio por UF (mapa coroplético)
- [ ] **Tarifa × Qualidade** — dispersão tarifa B1 vs DEC, com linha de tendência e destaque de outliers
- [ ] **Reclamações** — tipologias mais frequentes + correlação visual com indicadores técnicos
- [ ] Segmentações globais: ano, região, distribuidora

**Entregável:** `.pbix` no repo + prints de cada página no README.

### Fase 7 — Relatório executivo + publicação (1 semana)

- [ ] `docs/relatorio_executivo.md` (ou PDF): 5 perguntas → 5 respostas com número, gráfico e recomendação de negócio
- [ ] README final: contexto, arquitetura (diagrama), como reproduzir (`docker compose up` + 3 comandos), prints do dashboard, aprendizados, uso documentado de IA
- [ ] Post no LinkedIn: problema → abordagem → 3 insights → link do repo
- [ ] (Opcional) publicar o relatório no Power BI Service com link público

**Entregável:** projeto publicável e "entrevistável".

### Fase 8 — Automação (paralelo às fases 5–7)

- [ ] `pipeline.py` orquestrando extract → load raw → staging → dw → quality report, com logging estruturado
- [ ] Parâmetro `--full` vs `--incremental` (reprocessa tudo ou só o ano corrente)
- [ ] (Diferencial) GitHub Actions rodando os testes de qualidade a cada push

**Entregável:** pipeline executável em um comando — é o que transforma "análise" em "engenharia".

## 7. KPIs e definições

| KPI | Definição | Fonte |
|-----|-----------|-------|
| DEC | Duração equivalente de interrupção por unidade consumidora (horas) | Dataset 1 |
| FEC | Frequência equivalente de interrupção (nº de interrupções) | Dataset 1 |
| % Transgressão | Conjuntos com DEC ou FEC acima do limite ÷ total de conjuntos | Dataset 1 |
| Compensações (R$) | Valor pago por violação de limites | Dataset 1 |
| Reclamações /10k UC | Reclamações ÷ consumidores × 10.000 | Datasets 1 + 2 |
| Tarifa B1 (R$/MWh) | TE + TUSD residencial convencional | Dataset 3 |
| Índice Qualidade-Preço | Ranking composto DEC normalizado × tarifa normalizada (seu score proprietário) | Derivado |

## 8. Estrutura do repositório

```
analise-qualidade-energia-aneel/
├── README.md
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── data/
│   └── raw/              # CSVs originais (gitignored se > 100MB; senão, amostra)
├── notebooks/
│   └── 01_eda_fontes.ipynb
├── src/
│   ├── extract/          # cliente CKAN + downloads
│   ├── load/             # cargas raw e dw
│   ├── transform/        # raw → staging
│   ├── quality/          # checks de data quality
│   └── pipeline.py       # orquestrador
├── sql/
│   ├── ddl/              # criação de schemas, dims e fatos
│   ├── views/            # SQL analítico (uma view por pergunta)
│   └── checks/           # queries de reconciliação
├── dashboards/
│   └── qualidade_energia.pbix
└── docs/
    ├── dicionario_dados.md
    ├── data_quality.md
    ├── relatorio_executivo.md
    └── img/              # star schema, prints do dashboard
```

## 9. Critérios de "pronto" (Definition of Done)

- [ ] Pipeline roda do zero em máquina limpa seguindo só o README
- [ ] As 5 perguntas de negócio têm resposta explícita no relatório executivo
- [ ] Star schema documentado com diagrama
- [ ] ≥6 views SQL com CTEs e window functions
- [ ] Dashboard com ≥5 páginas e prints no README
- [ ] Relatório de Data Quality com regras e resultados
- [ ] Post publicado no LinkedIn

## 10. Riscos e mitigações

| Risco | Impacto | Mitigação |
|-------|---------|-----------|
| Encoding/separador quebrado nos CSVs | ETL falha silenciosamente | Tratar `encoding` e `sep` explícitos + checks de qualidade desde a Fase 2 |
| Códigos de distribuidora inconsistentes entre datasets | Joins errados | Fase 1 dedica tempo à conciliação; criar tabela de-para se necessário |
| Portal ANEEL fora do ar / URLs mudam | Extração quebra | Guardar CSVs em `data/raw/`; extração com retry; URLs descobertas via API, não hardcoded |
| Volume do CSV de continuidade (milhões de linhas) | Lentidão local | Carga com `COPY` do PostgreSQL (não `INSERT` linha a linha); filtrar 2020+ já no staging |
| Scope creep (vontade de adicionar clima, IBGE...) | Projeto nunca termina | Seção 2.3 é contrato: v1 fecha, extras viram "fase 2" no README |
| Power BI básico atrasar Fase 6 | Cronograma estoura | 2 dias de nivelamento dirigido + começar por visuais simples (cards, barras, tabela) |

---

*Uso de IA neste projeto: Claude como apoio para planejamento, revisão de código e documentação — decisões de modelagem e análise validadas manualmente contra os dicionários oficiais da ANEEL. (Manter esta nota no README — transparência conta pontos.)*
