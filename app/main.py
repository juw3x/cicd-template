"""Минимальное типовое веб-приложение (FastAPI) для демонстрации CI/CD."""

import os

from fastapi import FastAPI

APP_VERSION = os.getenv("APP_VERSION", "dev")

app = FastAPI(title="cicd-template-app", version=APP_VERSION)


@app.get("/")
def index() -> dict[str, str]:
    return {"message": "Hello from CI/CD template", "version": APP_VERSION}


@app.get("/health")
def health() -> dict[str, str]:
    """Эндпоинт для проверки живости (liveness/healthcheck)."""
    return {"status": "ok"}
