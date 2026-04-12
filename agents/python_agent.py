import re
import requests
import duckdb
from pathlib import Path

DB_PATH = "db_storage/fuel.db"
MODEL = "mistral"
OLLAMA_URL = "http://localhost:11434/api/generate"

SOURCE_TABLE = "stg_fuel"

OUTPUT_PATH = "dbt_project/models/python/fuel_insights.py"


def call_ollama(prompt: str) -> str:
    response = requests.post(
        OLLAMA_URL,
        json={"model": MODEL, "prompt": prompt, "stream": False},
        timeout=120
    )
    if response.status_code != 200:
        raise Exception(response.text)
    return response.json().get("response", "")


def get_schema(con, table_name: str) -> str:
    schema = con.execute(f"DESCRIBE {table_name}").fetchall()
    return "\n".join([f"{c[0]}: {c[1]}" for c in schema])


def python_agent(schema_str: str) -> str:
    return f"""
You are a senior data scientist.

DATASET: fuel (but must be reusable later)

SOURCE:
dbt.ref('{SOURCE_TABLE}')

SCHEMA:
{schema_str}

TASK:
- compute summary stats
- detect trends over time (if date exists)
- group by country
- correlation if numeric exists

OUTPUT:
ONLY PYTHON CODE
"""


def generate():
    con = duckdb.connect(DB_PATH)

    schema_str = get_schema(con, SOURCE_TABLE)

    code = call_ollama(python_agent(schema_str))

    Path(OUTPUT_PATH).parent.mkdir(parents=True, exist_ok=True)
    Path(OUTPUT_PATH).write_text(code)

    print("✅ PYTHON GENERATED")
    print(code)


if __name__ == "__main__":
    generate()