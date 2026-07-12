# Prompts para as sessões do Claude Code

> Este arquivo é seu guia de uso — pode ficar no repo ou fora dele.
> O contexto permanente já está no CLAUDE.md (lido automaticamente em toda sessão),
> então os prompts abaixo são curtos de propósito: eles só dizem O QUE fazer agora.

## Antes de tudo (uma vez só)

```bash
cd ~/projetos
mkdir analise-qualidade-energia-aneel   # ou extraia o zip
cd analise-qualidade-energia-aneel
git init
claude                                   # inicia o Claude Code
```

Dica: use **Plan Mode** (Shift+Tab) nas tarefas maiores — o Claude propõe o plano
antes de tocar nos arquivos, e você aprova.

## Comandos customizados já incluídos (.claude/skills/)

| Comando | Quando usar |
|---------|-------------|
| `/atualizar-status` | Fim de cada sessão — atualiza docs/status_progresso.md |
| `/registrar-decisao` | Tomou uma decisão de modelagem/escopo — grava no log |
| `/revisar-fase` | Fechou uma fase — auditoria contra o Definition of Done + perguntas de entrevista |

---

## Sessão 1 — Fase 0 (setup)

```
Leia o CLAUDE.md e docs/roadmap.md. Estamos na Fase 0.
O esqueleto do repo já existe (docker-compose, requirements, .env.example, DDL dos schemas).
Tarefas desta sessão:
1. Suba o PostgreSQL com docker compose e confirme que os schemas raw, staging e dw foram criados
2. Crie o venv, instale as dependências e valide a conexão Python -> PostgreSQL com um script mínimo de teste usando as credenciais do .env
3. Faça o commit inicial com mensagem adequada
Não avance para a Fase 1. Ao final, rode /atualizar-status.
```

## Sessão 2 — Fase 1 (EDA)

```
Estamos na Fase 1 (veja docs/status_progresso.md).
Baixe uma AMOSTRA de cada fonte listada em docs/dicionario_dados.md usando a API CKAN
(datastore_search com limit pequeno serve para amostra).
Crie notebooks/01_eda_fontes.ipynb analisando: shape, tipos, nulos, domínios,
chaves candidatas e o grão real de cada arquivo.
Objetivo crítico: confirmar como fazer join entre as fontes (código da distribuidora).
Vá fonte por fonte e me mostre os achados antes de seguir para a próxima.
```

## Sessão 3 — Fase 1 (fechamento)

```
Com base no notebook de EDA, preencha docs/dicionario_dados.md com as colunas
que vamos usar e proponha as regras de data quality por tabela.
Se algum grão descoberto contradisser a modelagem do CLAUDE.md, pare e me avise —
decisão de modelagem é minha. Depois rode /registrar-decisao para o que definirmos
e /revisar-fase.
```

## Sessão 4+ — Fase 2 (extração)

```
Fase 2. Implemente src/extract/aneel_client.py:
- descobre URLs dos CSVs via package_show (nunca hardcodar URL de download)
- download em streaming para data/raw/ com retry, timeout e log
- registra em raw.log_extracao (arquivo, tamanho, linhas, hash, timestamp)
Depois a carga 1:1 no schema raw via COPY, tudo TEXT.
Requisito inegociável: idempotência (rodar 2x não duplica).
Implemente em blocos pequenos e me explique cada decisão de design — vou precisar
defender esse código em entrevista.
```

## Fases 3-5 — padrão de prompt

```
Fase [N]. Consulte o checklist da fase em docs/roadmap.md e docs/status_progresso.md.
Implemente [item específico do checklist].
Siga as convenções do CLAUDE.md. Blocos pequenos, explicando as decisões.
```

## Regras de ouro das sessões

1. **Uma fase por sessão** (ou menos). Contexto curto = código melhor.
2. **Peça em blocos pequenos** e leia cada trecho antes de aceitar — o projeto é
   para entrevista; você precisa saber defender cada linha.
3. **Fim de sessão:** /atualizar-status → commit → atualizar arquivos 05/06 no
   Claude Project (para o chat continuar de onde o Code parou).
4. Se o Claude propuser algo fora do escopo, a resposta é: "registre como fase 2".
5. Erro de ambiente (Docker, psycopg2, encoding)? Cole o erro cru — não descreva.
