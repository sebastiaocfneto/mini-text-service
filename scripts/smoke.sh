#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BASE_URL:-http://localhost:8000}"

echo "==> Health"
curl -fsS "$BASE_URL/health" | cat
echo -e "\n"

echo "==> Classify examples"
curl -fsS -X POST "$BASE_URL/classify" -H 'Content-Type: application/json' -d '{"text":"Como faço para autenticar?"}' | cat
echo -e "\n"
curl -fsS -X POST "$BASE_URL/classify" -H 'Content-Type: application/json' -d '{"text":"Não funciona, deu erro no sistema."}' | cat
echo -e "\n"
curl -fsS -X POST "$BASE_URL/classify" -H 'Content-Type: application/json' -d '{"text":"Hoje registrei uma ocorrência no sistema."}' | cat
echo -e "\n"
