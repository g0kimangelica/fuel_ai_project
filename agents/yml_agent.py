import re
import requests
import duckdb
from pathlib import Path

DB_PATH = "db_storage/fuel.db"
MODEL = "mistral"
OLLAMA_URL = "http://localhost:11434/api/generate"

MODEL_NAME = "fuel_mart"

SOURCE_TABLE = "stg_fuel"

OUTPUT_PATH = "dbt_project/models/marts/schema.yml"


def call_ollama(prompt: str) -> str:
    response = requests.post(
        OLLAMA_URL,
        json={"model": MODEL, "prompt": prompt, "stream": False},
        #timeout=120
    )
    return response.json().get("response", "")


def get_schema(con):
    schema = con.execute(f"DESCRIBE {SOURCE_TABLE}").fetchall()
    return "\n".join([f"{c[0]}: {c[1]}" for c in schema])


def yml_agent(schema_str: str, sql: str) -> str:
    return f"""
Generate dbt schema.yml

MODEL: {MODEL_NAME}

SCHEMA:
{schema_str}

SQL:
{sql}

RULES:
- match fuel mart model
- add not_null for country
- add unique if applicable

OUTPUT:
ONLY YAML
"""


def generate(sql_model: str):
    con = duckdb.connect(DB_PATH)

    schema_str = get_schema(con)

    yml = call_ollama(yml_agent(schema_str, sql_model))

    Path(OUTPUT_PATH).parent.mkdir(parents=True, exist_ok=True)
    Path(OUTPUT_PATH).write_text(yml)

    print("✅ YAML GENERATED")


if __name__ == "__main__":
    print("run via pipeline")