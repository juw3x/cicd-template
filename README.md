# CI/CD template: GitHub Actions + Docker + Trivy + GHCR

Готовый шаблон репозитория: берёте, нажимаете **Use this template**, и получаете рабочий пайплайн
для контейнеризированного приложения. Демо-приложение — FastAPI (`/` и `/health`);
пайплайн можно адаптировать под любой язык (см. `docs/adr/0001-tooling-choices.md`).

## Что делает пайплайн

```
PR / push в main
   │
   ├─ Lint        Ruff (проверка + формат)
   ├─ Hadolint    проверка Dockerfile
   ├─ Tests       pytest + coverage, матрица Python 3.11 / 3.12
   │
   └─ Build & Scan (после успеха выше)
        ├─ docker build (кэш GitHub Actions)
        ├─ Trivy: падает при CRITICAL/HIGH с доступным исправлением
        └─ Smoke test: контейнер стартует и отвечает на /health

push в main / тег vX.Y.Z  →  Publish: сборка и пуш образа в ghcr.io/<owner>/<repo>
```

Дополнительно: Dependabot раз в неделю предлагает обновления GitHub Actions, pip и Docker-образов.

## Быстрый старт

1. Загрузите содержимое в новый репозиторий GitHub (или включите *Template repository* в его настройках).
2. Откройте `LICENSE` и замените `<ВАШЕ ИМЯ>`.
3. Сделайте push в `main` — запустятся `CI` и `Publish image`.
4. Образ появится в разделе **Packages** репозитория: `ghcr.io/<owner>/<repo>`.
5. Релиз: `git tag v1.0.0 && git push origin v1.0.0` — образ получит теги `1.0.0`, `1.0`.

Секреты вручную добавлять не нужно: публикация использует встроенный `GITHUB_TOKEN`
(права `packages: write` заданы в `publish.yml`).

## Локальная разработка

```bash
python -m venv .venv && source .venv/bin/activate
make install      # зависимости
make lint         # ruff
make test         # pytest + coverage
make docker-build && make docker-run   # http://localhost:8000/health
```

## Структура

```
app/                  приложение
tests/                тесты
Dockerfile            multi-stage, non-root, HEALTHCHECK
.github/workflows/    ci.yml, publish.yml
.github/dependabot.yml
docs/adr/             записи об архитектурных решениях
```

## Как адаптировать под свой стек

- Замените job `lint` и `test` в `ci.yml` на команды вашего языка.
- Положите свой `Dockerfile` — этапы `build-scan` и `publish` от языка не зависят.
- Порог Trivy меняется в `severity` и `exit-code` (`ci.yml`).

## Известные ограничения

- Образ после публикации не подписывается (например, cosign), SBOM не генерируется.
- Деплой не включён: шаблон заканчивается публикацией образа (CD-часть — следующий шаг, например GitOps).

## Лицензия

MIT
