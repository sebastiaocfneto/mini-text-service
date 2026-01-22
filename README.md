# Mini Text Service (DevOps/MLOps Exercise)

Solução **simples e reprodutível** para classificação textual via API HTTP, com empacotamento em Docker.

## O que este repositório entrega

- Serviço HTTP (FastAPI) com endpoints:
  - `GET /health`
  - `GET /info`
  - `POST /echo`
  - `POST /classify`
- Classificador **por regras** (heurísticas) para 3 classes:
  - `pergunta`, `relato`, `reclamacao`
- `Dockerfile`, `docker-compose.yml` e `Makefile` para execução e testes reprodutíveis
- Testes automatizados com `pytest`

## Arquitetura e pipeline (visão rápida)

```
Client -> /classify (HTTP JSON)
       -> validação (Pydantic)
       -> strategy = rules
       -> classify_rules(text)
       -> resposta {category, confidence, elapsed_ms}
```

**Por que regras?** A avaliação pede uma solução simples e reprodutível; regras removem dependências de treinamento/artefatos
e focam no controle do pipeline.

## Requisitos

- Docker + Docker Compose (recomendado)
- Opcional: Python 3.11+ (apenas se quiser rodar/testar sem Docker)

## Como executar (recomendado: Docker)

Subir o serviço:

```bash
make up
```

Em outro terminal, validar saúde:

```bash
curl -fsS http://localhost:8000/health
```

Classificar:

```bash
curl -fsS -X POST http://localhost:8000/classify \
  -H 'Content-Type: application/json' \
  -d '{"text":"Como faço para autenticar?"}'
```

Rodar um smoke test (exemplos):

```bash
./scripts/smoke.sh
```

Derrubar o ambiente:

```bash
make down
```

## Como testar

### Testes dentro do Docker (mais reprodutível)

```bash
make test-docker
```

### Testes localmente (sem Docker)

```bash
python -m venv .venv
. .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate  # Windows PowerShell
pip install -r requirements.txt
pytest -q
```

## Decisões DevOps/MLOps (curtas)

- **Reprodutibilidade:** dependências travadas via `requirements.txt` e execução em container.
- **Observabilidade mínima:** endpoint `/health` + `HEALTHCHECK` no Dockerfile.
- **Testabilidade:** suíte `pytest` cobrindo casos base e erros de validação/estratégia.
- **Baixa abstração:** FastAPI + Docker/Compose, sem camadas extras.

## Limitações

- Classificação por regras é **heurística** (não aprende, não generaliza bem).
- Foco em português e em padrões simples (pergunta/reclamação/relato).
- Sem persistência, fila ou rastreio de métricas (mantido propositalmente minimalista).

## Possíveis evoluções (se fosse para produção)

- Adicionar nova `strategy="model"` carregando um artefato versionado (ex: `joblib`/`onnx`) no startup.
- Versionamento de modelo e rastreio de experimento (MLflow) e artefatos (S3/MinIO).
- Métricas Prometheus + tracing (OpenTelemetry) e logs estruturados (JSON).
- Pipeline CI: lint + testes + build/push da imagem.

## Referências

- FastAPI: https://fastapi.tiangolo.com/
- Uvicorn: https://www.uvicorn.org/
- Dockerfile reference: https://docs.docker.com/reference/dockerfile/
