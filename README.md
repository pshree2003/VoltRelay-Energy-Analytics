# VoltRelay Energy Battery‑Swapping Network – Analytical Project

## Overview
This repository contains an **end‑to‑end data‑analytics** project for the **VoltRelay Energy** battery‑swapping network.  The goal is to explore the operational data, answer a set of core business‑driven analytical questions, and produce actionable insights and recommendations.

### Core analytical questions
1. **Network Performance Over Time** – How does the network evolve (transactions, utilisation, availability) month‑by‑month?
2. **Service Failures & Customer Experience** – Frequency, types and impact of failures on riders.
3. **Station & Geographic Patterns** – Spatial distribution of usage, demand hotspots and under‑served areas.
4. **Battery & Equipment Performance** – Degradation, churn and maintenance metrics.
5. **Pricing & Partner Economics** – Revenue, partner payouts and price‑elasticity signals.
6. **Root‑Cause Analysis of Rider Retention** – Factors associated with churn vs. repeat usage.

The notebook will answer each question with clean datasets, visualisations, statistical summaries and business‑focused take‑aways.

## Repository structure
```
voltrelay-analytics/
├─ data/                     # top‑level data folder (ignored by git)
│   ├─ raw/                  # original CSV/JSON files as provided
│   └─ processed/            # derived, clean datasets (do not edit raw data)
├─ notebooks/                # Jupyter/Colab notebooks
│   └─ analysis.ipynb        # main end‑to‑end analysis notebook
├─ src/                      # reusable Python modules
│   └─ __init__.py
├─ config/                   # project‑wide constants & settings
│   └─ constants.py
├─ figures/                  # exported visualisations (PNG, SVG, etc.)
├─ tables/                   # LaTeX/Markdown tables used in reports
├─ reports/                  # final written report & executive summary
├─ presentation/             # slide deck, script for 3‑minute video
├─ requirements.txt          # pip‑installable dependencies
├─ README.md                 # **this** file
└─ .gitignore                # files/folders not to track
```

## Getting started
1. **Clone** the repository (or copy the folder) to your local machine.
2. **Install dependencies** – see `requirements.txt`.
3. **Place raw data** files inside `data/raw/` preserving the original filenames.
4. Open `notebooks/analysis.ipynb` in Google Colab or a local Jupyter environment and run all cells.

## Contributing & reproducibility
- All transformations are performed programmatically; raw data remain untouched.
- Any new analysis should be added as additional notebooks or modules under `src/`.
- Results are stored in `data/processed/` and visual assets in `figures/`.

---
*Prepared by the lead Data Analyst / Scientist / Python Engineer.*
