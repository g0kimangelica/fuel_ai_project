# AI-Assisted Data Pipeline (Fuel Price Analysis)

## Overview

This project is an ongoing experiment to evaluate how far AI-generated components can be used in a real-world data engineering workflow.

Using a global fuel price dataset, I designed a pipeline where different components (implemented as LLM-driven agents) generate parts of a dbt project — including SQL models, Python models, and YAML configurations.

The goal is not full automation, but to understand:

* Where AI can accelerate development
* Where it introduces risk or inconsistency
* What guardrails are required for reliability

---

## Architecture

Pipeline flow (simplified):

Kaggle Dataset
→ Python Ingestion
→ DuckDB (raw layer)
→ Staging SQL (generated)
→ Aggregation SQL (generated)
→ Python/dbt models
→ YAML (tests) generation
→ Review / validation step
→ Dagster orchestration
→ dbt run + dbt test

---

## Tech Stack

* **Data Source**: Kaggle (Global Fuel Prices)
* **Storage**: DuckDB
* **Transformation**: dbt (SQL + Python models)
* **Orchestration**: Dagster
* **LLM Layer**: Local models via Ollama
* **Language**: Python

---

## AI-Assisted Workflow

Instead of manually writing transformations, the pipeline uses a multi-step generation approach:

* **Component 1**: Generates staging SQL (data cleaning, typing, null handling)
* **Component 2**: Generates aggregation logic
* **Component 3**: Generates Python/dbt models
* **Component 4**: Generates YAML files with tests
* **Component 5**: Reviews outputs before execution

Each step is guided by schema context and expected outputs.

---

## Key Observations

This project surfaced a few practical insights:

### What Works Well

* Schema-driven SQL generation is relatively stable
* Basic transformations (casting, null handling) are consistent
* YAML/test generation is surprisingly useful as a baseline

### Where It Breaks

* Aggregation logic is less reliable
* Minor syntax issues still occur
* Outputs may look correct but require validation

### Engineering Takeaway

AI can accelerate development, but does not replace validation.
A review layer and testing remain essential for trustable pipelines.

---

## Local LLM Considerations

The project uses locally hosted models via Ollama to avoid external API dependency.

Trade-offs observed:

* Lower cost and more control
* Performance constraints on local hardware
* Occasional instability depending on model size

---

## Project Status

⚠️ Work in Progress

* Core generation flow implemented
* YAML generation and review working
* Aggregation layer still requires refinement
* End-to-end pipeline execution via Dagster in progress

---

## Getting Started

### 1. Clone the repository

```bash
git clone <your-repo-link>
cd <repo-name>
```

### 2. Set up environment

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Run ingestion

```bash
python ingest_data.py
```

### 4. Run Dagster

```bash
dagster dev
```

### 5. Execute pipeline

* Trigger jobs via Dagster UI
* Run dbt models and tests

---

## Future Improvements

* Add validation checkpoints before execution
* Improve aggregation logic generation
* Introduce retry/fallback mechanisms
* Optimize local model performance
* Add dashboard for insights

---

## Why This Project

This is not meant to be a polished demo, but a practical exploration.

As AI tooling becomes more integrated into data workflows, understanding its limitations is just as important as leveraging its strengths.

---

## Author

Data Engineer (14+ years experience) exploring practical applications of AI in modern data pipelines.
