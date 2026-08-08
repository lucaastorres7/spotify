## FastAPI Template
### Stack

- FastAPI + Uvicorn
- structlog (logs estruturados — console em dev, JSON em prod)
- pydantic-settings (config via `.env`)
- pytest
- ruff (lint + format)
- uv (gerenciador de pacotes)

### Como rodar

1. Instalar `uv`
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
2. Sincronizar as dependências
```bash
uv sync
```
3. Rodar o servidor
```bash
uv run dev
```

Servidor sobe em `http://localhost:8000`.

### Configuração

Todas as variáveis são centralizadas em [src/app/config.py](src/app/config.py) e podem ser definidas no `.env`.

Segue abaixo uma tabela com as variáveis padrões:
| Variável       | Default | Descrição                                                            |
|----------------|---------|----------------------------------------------------------------------|
| `SERVICE_NAME` | `app`   | Nome do serviço, aparece em todos os logs                            |
| `ENV`          | `dev`   | `dev` ou `prod` — controla formato do log (console/JSON) e reload    |
| `VERSION`      | `0.0.1` | Versão exibida nos logs                                              |
| `LOG_LEVEL`    | `INFO`  | Nível de log                                                         |

### Testes

```bash
uv run pytest
```

### Lint e formatação

```bash
uv run ruff check .
uv run ruff format .
```

O workflow [.github/workflows/ci.yml](.github/workflows/ci.yml) roda lint, `format --check` e pytest em todo push/PR.

### Docker

```bash
docker build -t app .
docker run -p 8000:8000 -e ENV=prod app
```

### Estrutura

```
src/app/
  main.py       # bootstrap da app: logging, middlewares, rotas
  config.py     # Settings
  logging/      # setup do structlog + middleware de request-id
  routes/       # routers
tests/          # testes
```

### Usando como base para um novo serviço

1. Copie este repositório.
2. Defina `SERVICE_NAME` no `.env`.
3. Adicione suas rotas em `src/app/routes/` e registre em `src/app/routes/__init__.py` e `src/app/main.py`.
4. `uv sync && uv run dev`.
