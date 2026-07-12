-- Camadas do pipeline (executado automaticamente pelo Docker na primeira subida)
CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS dw;

COMMENT ON SCHEMA raw     IS 'Espelho 1:1 dos CSVs da ANEEL, tudo TEXT, sem transformacao';
COMMENT ON SCHEMA staging IS 'Dados tipados, limpos, deduplicados e filtrados ao escopo (2020-2025)';
COMMENT ON SCHEMA dw      IS 'Star schema: dimensoes e fatos para consumo analitico';
