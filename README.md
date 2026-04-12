# Fuel AI Pipeline — LLM-Assisted Data Engineering Experiment

## Executive Summary

This project explores how LLMs can be safely integrated into a structured data engineering pipeline to accelerate transformation logic generation while maintaining execution reliability through validation gates.

Rather than building an autonomous “AI agent system”, this project evaluates a more realistic architecture:

> LLMs as code generation accelerators, not execution engines.

The focus is on **reliability, failure modes, and validation design** in AI-assisted data workflows.

---

## Why this matters

Modern data engineering stacks are increasingly experimenting with LLM-assisted development for:

* SQL generation
* dbt scaffolding
* test creation
* transformation logic drafting

However, production systems still require:

* deterministic execution
* reproducibility
* testable transformations
* schema integrity

This project investigates the gap between:

> “code that looks correct” vs “code that is actually correct”

---

## System Overview

### System and Data Flow Architecture

<img width="919" height="1301" alt="image" src="https://github.com/user-attachments/assets/3ea7141f-e9f1-476e-88f6-1395e7e54987" />

---

## Design Principles

This system is intentionally designed as a **non-autonomous LLM-assisted pipeline**.

### 1. Separation of responsibilities

Each LLM component is responsible for a single transformation stage.

### 2. Validation-first execution

No generated output is executed without passing a review layer.

### 3. Deterministic orchestration

Dagster ensures reproducibility and controlled execution order.

---

## LLM-Assisted Components (not autonomous agents)

The pipeline uses structured LLM-assisted generation steps:

* **Staging Generator**

  * schema-based cleaning
  * type casting
  * null handling logic

* **Aggregation Generator**

  * KPI generation
  * grouped analytics
  * country/time-based aggregations

* **Model Generator**

  * dbt SQL models
  * Python/dbt hybrid models

* **Test Generator**

  * YAML schema definitions
  * dbt tests

* **Validation Layer**

  * reviews generated outputs before execution
  * prevents unsafe or incorrect SQL from running


---

## Key Findings

### What works well

✔ Staging transformations (schema-driven SQL)

✔ dbt model scaffolding

✔ YAML + test generation

✔ Boilerplate acceleration

---

### Where it breaks down

⚠ Aggregation logic inconsistency

⚠ Semantically incorrect but syntactically valid SQL

⚠ Requires human validation for execution safety


---

## Engineering Insight

This experiment reinforces a key principle:

> LLMs are effective for accelerating development, but not reliable for execution-critical logic without validation layers.

The real system is not the LLM — it is the **guardrail architecture around it**.

---

## System Design Perspective

If evaluated as a production architecture, the key challenge is:

> How do we integrate probabilistic code generation into deterministic data pipelines?

### Core conflict

* LLMs are probabilistic
* Data pipelines require determinism

---

### Solution approach used

This system implements a **validation-first LLM pipeline architecture**:

1. LLM generates transformation logic
2. Outputs are isolated per pipeline stage
3. Validation layer reviews logic correctness
4. Only validated outputs are executed
5. Dagster ensures reproducible orchestration

---

### Trade-offs

✔ Faster development cycle

✔ Reduced boilerplate engineering effort

✔ Improved flexibility in early-stage pipeline design

❌ Requires validation overhead

❌ Cannot be fully autonomous


---

## Tech Stack

* Python
* DuckDB
* dbt
* Dagster
* Ollama (local LLM execution)
* Kaggle dataset

---

## Current Status

This is a work-in-progress experimental system.

* Core pipeline implemented
* LLM generation for all layers functional
* YAML/test generation working
* Aggregation layer requires refinement
* End-to-end orchestration still being improved

---

## Future Improvements

* Improve aggregation logic reliability
* Add stronger validation / rule-based checks
* Introduce retry + fallback generation mechanisms
* Enhance observability of generated SQL quality
* Add architecture visualization dashboard

---

## Key Takeaway

This is not an AI automation system.

It is an experiment in:

> making probabilistic LLM outputs safe enough for deterministic data workflows.

---

## Author

Senior Data Engineer (14+ years experience)
Exploring practical applications of LLMs in modern data engineering systems.
