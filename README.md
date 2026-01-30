# etlSUS

[![License: LGPL 2.1](https://img.shields.io/badge/License-LGPL_2.1-g)](https://opensource.org/license/lgpl-2-1)
![Python](https://img.shields.io/badge/python-3.9_|_3.10_|_3.11_|_3.12-blue.svg)
[![Python package](https://github.com/GOPAD-Datasus/ETL-DataSUS/actions/workflows/python-package.yml/badge.svg)](https://github.com/GOPAD-Datasus/ETL-DataSUS/actions/workflows/python-package.yml)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.16916158.svg)](https://doi.org/10.5281/zenodo.16916158)

>Docs are also available in Portuguese [(PT)](docs/README%20PTBR.md)

An opinionated ETL (Extract, Transform, Load) pipeline designed to process Brazil's public healthcare data (DataSUS) from raw CSV files into analysis-ready datasets.

## Overview

### The Problem

Brazil's SUS (Sistema Único de Saúde) provides extensive public health data, but it requires domain-specific preprocessing before analysis. This includes removing unnecessary columns, handling missing values, and optimizing data types. Manually scripting these transformations for each dataset is time-consuming and error-prone.

### The Solution

etlSUS automates the entire process. Simply specify the dataset, and the library handles downloading, transforming, and loading the data into a database and/or merging all files.

## 🚀 Quick Start

### 1. Installation

```bash
poetry add git+https://github.com/GOPAD-Datasus/ETL-DataSUS.git
```

### 2. Run the Pipeline

```python
from etlsus import pipeline


if __name__ == '__main__':
    pipeline(
        dataset='SINASC',  # Choose between 'SINASC' or 'SIM'
        base_dir='path/to/project/dir',
    )
```

## 📌 Features

- **Simple Interface:** Select your dataset (SINASC and SIM) and specify the base directory
- **Automated Processing:** Handles download, transformation, and loading automatically
- **Optimized Transformations:** Removes irrelevant columns and values while preserving analytical value
  - [SIM Dictionary (EN)](docs/SIM.md)[ (PT)](docs/SIM%20PTBR.md)
  - [SINASC Dictionary (EN)](docs/SINASC.md)[ (PT)](docs/SINASC%20PTBR.md)
- **Multiple Output Formats:**
  - Direct export to relational databases
  - Merged single file for multi-year analysis
  - Multiple files

## 📁 Project Structure

After running the pipeline, your data directory will be organized as follows:

```
./data
├── raw/                  # Downloaded CSV files
├── processed/            # Cleaned and transformed files
└── dataset.parquet.gzip  # (Optional) Merged file
```

## Limitation

- Supports only PARQUET output files.

## 📝 License
[LGNU](LICENSE) | © GOPAD 2025