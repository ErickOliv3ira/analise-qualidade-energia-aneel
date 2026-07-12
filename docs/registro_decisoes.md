# 06 — Registro de Decisões

> **Arquivo vivo.** Uma entrada por decisão relevante (escopo, modelagem, técnica). Formato: contexto → decisão → motivo. Decisões aqui registradas não devem ser reabertas sem motivo forte.

---

## D-001 — Período de análise: 2020–2025
**Data:** 12/07/2026
**Contexto:** dados da ANEEL existem desde 2010; volume completo inflaria ETL e banco local.
**Decisão:** limitar a 2020–2025 (recurso `indicadores-continuidade-coletivos-2020-2029` cobre o período).
**Motivo:** 6 anos bastam para tendência e sazonalidade; mantém o projeto executável em máquina local.

## D-002 — Interrupções evento a evento fora do escopo
**Data:** 12/07/2026
**Decisão:** usar apenas os indicadores coletivos (DEC/FEC), não o dataset de interrupções individuais.
**Motivo:** dezenas de GB; DEC/FEC já é a agregação oficial e responde às perguntas de negócio.

## D-003 — Arquitetura em 3 schemas (raw / staging / dw)
**Data:** 12/07/2026
**Decisão:** PostgreSQL local via Docker com camadas separadas; raw tudo TEXT, staging tipado, dw dimensional.
**Motivo:** rastreabilidade, reprocessamento sem novo download e narrativa profissional de pipeline.

## D-004 — Extração via API CKAN (package_show) + download streaming
**Data:** 12/07/2026
**Decisão:** descobrir URLs dos CSVs dinamicamente via API; não hardcodar URLs; não paginar datastore para arquivos grandes.
**Motivo:** robustez a mudanças no portal + atende o requisito "extração via API" do portfólio.

## D-005 — Tarifas restritas ao subgrupo B1 convencional
**Data:** 12/07/2026
**Decisão:** análise tarifa×qualidade usa apenas tarifa residencial B1 (TE+TUSD).
**Motivo:** comparabilidade entre distribuidoras e aderência à narrativa (consumidor residencial).

## D-006 — Cruzamentos entre fontes no nível distribuidora × período
**Data:** 12/07/2026
**Decisão:** continuidade (grão conjunto) é agregada para distribuidora nas views de cruzamento com reclamações e tarifas.
**Motivo:** grãos incompatíveis entre fontes; distribuidora é o nível comum e o nível das perguntas de negócio.

---

## Modelo para novas entradas

## D-0XX — Título curto
**Data:**
**Contexto:**
**Decisão:**
**Motivo:**
