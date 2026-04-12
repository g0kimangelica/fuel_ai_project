import subprocess
from dagster import asset, Definitions
from config import DB_PATH

import sys
from pathlib import Path

# remove project-local shadowing
sys.path = [p for p in sys.path if "/duckdb" not in p]

import duckdb

from ingestion.load_kaggle import main as load_kaggle_main

from agents.stg_sql_agent import stg_sql_agent, call_ollama, get_schema
from agents.dm_sql_agent import dm_sql_agent
from agents.python_agent import python_agent
from agents.yml_agent import yml_agent
from agents.reviewer_agent import reviewer_agent





# ----------------------------
# INGEST
# ----------------------------
@asset
def ingest_data():
    load_kaggle_main()
    return "ingested"


# ----------------------------
# STAGING SQL
# ----------------------------
@asset(deps=["ingest_data"])
def stg_model():
    con = duckdb.connect(str(DB_PATH))

    schema_str = get_schema(con, "raw_fuel")

    sql = stg_sql_agent(schema_str)

    final_sql = call_ollama(sql)

    return final_sql


# ----------------------------
# MART SQL
# ----------------------------
@asset(deps=["stg_model"])
def dm_model():
    con = duckdb.connect(str(DB_PATH))

    schema_str = get_schema(con, "stg_fuel")

    sql = dm_sql_agent(schema_str)

    final_sql = call_ollama(sql)

    return final_sql


# ----------------------------
# PYTHON MODEL
# ----------------------------
@asset(deps=["dm_model"])
def python_model():
    con = duckdb.connect(str(DB_PATH))

    schema_str = get_schema(con, "stg_fuel")

    code = python_agent(schema_str)

    final_code = call_ollama(code)

    return final_code


# ----------------------------
# YAML MODEL
# ----------------------------
@asset(deps=["python_model"])
def yml_model():
    con = duckdb.connect(str(DB_PATH))

    schema_str = get_schema(con, "stg_fuel")

    sql = dm_model()  # dependency output reused conceptually

    yaml = yml_agent(schema_str, sql)

    final_yaml = call_ollama(yaml)

    return final_yaml


# ----------------------------
# REVIEW STEP
# ----------------------------
@asset(deps=["yml_model"])
def review():
    con = duckdb.connect(str(DB_PATH))

    schema_str = get_schema(con, "stg_fuel")

    sql = dm_model()

    fixed_sql = reviewer_agent(schema_str, sql)

    return fixed_sql


# ----------------------------
# DBT RUN
# ----------------------------
@asset(deps=["review"])
def run_dbt():
    subprocess.run(["dbt", "run"], cwd="dbt_project", check=True)
    return "dbt_done"


# ----------------------------
# DBT TEST
# ----------------------------
@asset(deps=["run_dbt"])
def test_dbt():
    subprocess.run(["dbt", "test"], cwd="dbt_project", check=True)
    return "tests_passed"


# ----------------------------
# DEFINITIONS
# ----------------------------
defs = Definitions(
    assets=[
        ingest_data,
        stg_model,
        dm_model,
        python_model,
        yml_model,
        review,
        run_dbt,
        test_dbt,
    ]
)