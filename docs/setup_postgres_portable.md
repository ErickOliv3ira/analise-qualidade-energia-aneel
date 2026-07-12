# Setup do PostgreSQL portable (sem Docker)

> Usado quando a máquina não permite Docker/WSL (ex.: PC corporativo sem admin). Ver decisão **D-007** em `registro_decisoes.md`.

## Layout no disco

```
%USERPROFILE%\pgsql\        # binários (bin\, lib\, share\, ...)
%USERPROFILE%\pgdata\       # cluster de dados (criado pelo initdb)
```

## Instalação inicial (uma única vez)

1. Baixar o ZIP dos binários da [EnterpriseDB — PostgreSQL 16 Windows x86-64](https://www.enterprisedb.com/download-postgresql-binaries).
2. Extrair para `%USERPROFILE%\` (vai criar a pasta `pgsql\`).
3. Inicializar o cluster:
   ```bat
   "%USERPROFILE%\pgsql\bin\initdb.exe" -D "%USERPROFILE%\pgdata" -U aneel_user -A scram-sha-256 -E UTF8 --pwfile=<(echo change_me)
   ```
   *(no Git Bash use `pwfile` apontando para um arquivo temporário com a senha em uma linha)*
4. Ajustar `postgresql.conf` (opcional) para escutar apenas em `localhost`.

## Start / stop no dia a dia

```bat
:: subir
"%USERPROFILE%\pgsql\bin\pg_ctl.exe" -D "%USERPROFILE%\pgdata" -l "%USERPROFILE%\pgdata\server.log" start

:: parar
"%USERPROFILE%\pgsql\bin\pg_ctl.exe" -D "%USERPROFILE%\pgdata" stop
```

Não precisa de admin — o cluster roda como o próprio usuário.

## Criar banco e schemas do projeto

```bat
"%USERPROFILE%\pgsql\bin\createdb.exe" -U aneel_user aneel
"%USERPROFILE%\pgsql\bin\psql.exe" -U aneel_user -d aneel -f sql\ddl\000_create_schemas.sql
```

## Verificação

```bash
python -m src.test_connection
```

Deve imprimir `Schemas OK: ['dw', 'raw', 'staging']`.

## Notas

- `docker-compose.yml` foi mantido no repositório como referência de arquitetura, mas o caminho suportado no ambiente atual é este.
- Toda a modelagem SQL (DDL, views, checks) é 100% compatível — Postgres é Postgres.
