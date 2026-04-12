import re
import requests
import duckdb
from pathlib import Path

# ----------------------------
# CONFIG
# ----------------------------
DB_PATH = "db_storage/fuel.db"
MODEL = "mistral"
OLLAMA_URL = "http://localhost:11434/api/generate"

OUTPUT_PATH = "dbt_project/models/staging/stg_fuel.sql"


# ----------------------------
# CLEAN SQL
# ----------------------------
def clean_sql(text: str) -> str:
    text = re.sub(r"```sql", "", text, flags=re.IGNORECASE)
    text = re.sub(r"```", "", text)
    return text.strip()


# ----------------------------
# OLLAMA CALL
# ----------------------------
def call_ollama(prompt: str) -> str:
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        },
        timeout=120
    )

    if response.status_code != 200:
        raise Exception(f"Ollama error: {response.text}")

    return response.json().get("response", "")


# ----------------------------
# SCHEMA
# ----------------------------
def get_schema(con, table_name: str) -> str:
    schema = con.execute(f"DESCRIBE {table_name}").fetchall()
    return "\n".join([f"{c[0]}: {c[1]}" for c in schema])


# ----------------------------
# PROMPT
# ----------------------------
def stg_sql_agent(schema_str: str) -> str:
    return f"""
You are a senior data engineer.

TASK:
Create a DBT STAGING model for DuckDB.

SOURCE: raw_fuel

SCHEMA:
{schema_str}

RULES:
- cast correct data types
- convert empty strings to NULL
- standardize column names
- NO joins
- NO aggregations
- NO business logic

OUTPUT:
ONLY SQL
"""


# ----------------------------
# RUN
# ----------------------------
def generate():
    con = duckdb.connect(DB_PATH)
    schema = get_schema(con, "raw_fuel")

    prompt = stg_sql_agent(schema)
    sql = clean_sql(call_ollama(prompt))

    Path(OUTPUT_PATH).parent.mkdir(parents=True, exist_ok=True)
    Path(OUTPUT_PATH).write_text(sql)

    print("✅ STAGING MODEL GENERATED")
    print(sql)


if __name__ == "__main__":
    generate()