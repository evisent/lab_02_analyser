# streamstats

Консольная утилита на Python: **потоковый анализатор логов** в форматах CSV и JSONL. Пишет статистику в JSON-отчёт.

## Возможности

- Чтение логов из CSV
- Чтение логов из JSONL

## Установка

```bash
pip install -e .
```

## Использование

```bash
python -m streamstats analyze input.csv --format csv --output report.json
python -m streamstats analyze input.jsonl --format jsonl --output report.json
python -m streamstats analyze input.jsonl --format jsonl --output report.json --skip-invalid
```

## Структура

```
lab_02/
  pyproject.toml
  README.md
  .gitignore
  src/streamstats/
    __init__.py
    __main__.py
    models.py
    parsers.py
    analysis.py
    report.py
    errors.py
  tests/
    test_parsers.py
    test_analysis.py
    test_cli.py
```

## Тесты и линтер

```bash
python -m pytest
ruff check .
```