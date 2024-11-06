#!/bin/bash
set -e
set -x

# Восстановление баз данных из дампов
pg_restore -U postgres -d mydb /docker-entrypoint-initdb.d/_goods.tar
pg_restore -U postgres -d mydb /docker-entrypoint-initdb.d/_institut_final.tar
