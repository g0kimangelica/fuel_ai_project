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

OUTPUT_PATH = "dbt_project/models/marts/agent_mart.sql"


# ----------------------------
# CLEAN SQL
# ----------------------------
def clean_sql(text: str) -> str:
    text = re.sub(r"```sql", "", text, flags=re.IGNORECASE)
    text = re.sub(r"```", "", text)
    return text.strip()


# ----------------------------
# OLLAMA
# ----------------------------
def call_ollama(prompt: str) -> str:
    response = requests.post(
        OLLAMA_URL,
        json={"model": MODEL, "prompt": prompt, "stream": False},
        timeout=120
    )

    if response.status_code != 200:
        raise Exception(response.text)

    return response.json().get("response", "")


# ----------------------------
# SCHEMA
# ----------------------------
def get_schema(con):
    schema = con.execute("DESCRIBE stg_fuel").fetchall()
    return "\n".join([f"{c[0]}: {c[1]}" for c in schema])


# ----------------------------
# PROMPT
# ----------------------------
def dm_sql_agent(schema_str: str) -> str:
    return f"""
You are a senior analytics engineer.

TASK:
Create a DBT MART model using stg_fuel.

SCHEMA:
{schema_str}

RULES:
- MUST use stg_fuel
- NO raw tables
- MUST be domain agnostic
- MUST support monthly aggregation if date exists
- MUST compute trends (current vs previous period)

OUTPUT:
ONLY SQL
"""


# ----------------------------
# RUN
# ----------------------------
def generate():
    con = duckdb.connect(DB_PATH)
    schema = get_schema(con)

    prompt = dm_sql_agent(schema)
    sql = clean_sql(call_ollama(prompt))

    Path(OUTPUT_PATH).parent.mkdir(parents=True, exist_ok=True)
    Path(OUTPUT_PATH).write_text(sql)

    print("✅ MART MODEL GENERATED")
    print(sql)


if __name__ == "__main__":
    generate()