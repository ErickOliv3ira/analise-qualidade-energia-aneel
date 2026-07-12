---
name: revisar-fase
description: Revisão de qualidade ao final de uma fase do roadmap, verificando entregáveis contra o Definition of Done antes de avançar. Usar quando o usuário disser que encerrou uma fase.
---

Faça a revisão de encerramento da fase atual (verifique qual é em `docs/status_progresso.md`):

1. Compare o que existe no repositório com o checklist da fase em `docs/roadmap.md` — liste item a item: feito / parcial / faltando
2. Execute o que for verificável: scripts rodam? pipeline é idempotente? queries executam? checks de qualidade passam?
3. Revise o código novo da fase contra as convenções do CLAUDE.md (SELECT *, queries parametrizadas, logging, idempotência)
4. Avalie "apresentabilidade de portfólio": um recrutador entenderia esse entregável? O que falta documentar?
5. Verdito honesto: a fase está pronta ou não? Se não, liste o mínimo necessário para fechar
6. Se pronta, sugira rodar /atualizar-status e faça 2-3 perguntas de entrevista sobre o que foi construído nesta fase (para o usuário treinar a defesa técnica do projeto)
