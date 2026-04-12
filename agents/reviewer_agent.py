import requests

MODEL = "mistral"
OLLAMA_URL = "http://localhost:11434/api/generate"


SOURCE_TABLE = "stg_fuel"


def call_ollama(prompt: str) -> str:
    response = requests.post(
        OLLAMA_URL,
        json={"model": MODEL, "prompt": prompt, "stream": False},
        timeout=120
    )
    return response.json().get("response", "")


def reviewer_agent(schema_str: str, sql: str) -> str:
    return f"""
You are a strict SQL validator.

SOURCE TABLE: {SOURCE_TABLE}

SCHEMA:
{schema_str}

SQL:
{sql}

RULES:
- must be valid DuckDB SQL
- only use stg_fuel
- fix syntax errors
- ensure valid CTEs

OUTPUT:
ONLY FIXED SQL
"""


def review(schema_str: str, sql: str) -> str:
    return call_ollama(reviewer_agent(schema_str, sql))