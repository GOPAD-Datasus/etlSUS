# ETL-DataSUS

[![License: LGPL 2.1](https://img.shields.io/badge/License-LGPL_2.1-g)](https://opensource.org/license/lgpl-2-1)
![Python](https://img.shields.io/badge/python-3.9_|_3.10_|_3.11_|_3.12-blue.svg)
[![Python package](https://github.com/GOPAD-Datasus/ETL-DataSUS/actions/workflows/python-package.yml/badge.svg)](https://github.com/GOPAD-Datasus/ETL-DataSUS/actions/workflows/python-package.yml)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.16916158.svg)](https://doi.org/10.5281/zenodo.16916158)

A streamlined ETL (Extract, Transform, Load) pipeline designed to process Brazil's public healthcare data (DataSUS) from raw CSV files into analysis-ready datasets, using simple YAML files for configuration.

## The Problem

Brazil's SUS (Sistema Único de Saúde) provides a wealth of public health data, but it often requires significant cleaning, type handling, and transformation before it can be used for analysis. Manually writing scripts for each dataset is time-consuming and error-prone.

## The Solution

ETL-DataSUS automates this process. You define the extraction sources and transformation rules in declarative YAML configuration files. The library then handles the entire pipeline: downloading the data, applying your transformations, and loading it into a PostgreSQL database.

## 🚀 Quick Start

### 1. Installation

```bash
poetry add git+https://github.com/GOPAD-Datasus/ETL-DataSUS.git
```

### 2. Configure Your Environment

Copy `.env-example` to `.env` and set your directories and database connection:

```bash
# .env
INPUT_DIR=./input   # Where to find your YAML configs
BASE_DIR=./data     # Where to store raw/processed files

DB_HOST=localhost
DB_NAME=datasus
DB_USER=postgres
DB_PASSWORD=your_password
```

### 3. Create Configuration Files

**Define your data sources in `input/input.yaml`:**
```yaml
prefix: DN
files:
  2012: https://s3.sa-east-1.amazonaws.com/ckan.saude.gov.br/SINASC/csv/SINASC_2012.csv
```

**Define transformations in `input/DN2012.yaml`:**
```yaml
name: 'DN2012'
read_variables:
  dtype:
    'DTNASC': str
    'DTNASCMAE': str
transformations:
  replace_values:
    'DTNASCMAE': 
      '24120198': '24121980' # Fix a common date typo
```

### 4. Run the Pipeline

```python
from etlsus import extract, transform, load

# Run the entire ETL process
extract('input/input.yaml', verbose=True)
transform('input/DN2012.yaml', verbose=True)
load('sinasc', if_exists='append', chunksize=500)
```

## 📌 Key Features

- **Declarative Configuration:** Define data sources and cleaning logic in YAML, not complex code.
- **Flexible Transformations:** Use a built-in handler system for common data cleaning tasks (value replacement, column renaming, etc.).
- **Generic Rules:** Apply a set of standard transformations to all files using a `generic.yaml` config.
- **Database Ready:** Efficiently load processed data directly into PostgreSQL.

## 📁 Project Structure

After running, your data directory (`BASE_DIR`) will look like this:

```
./data
├── raw/           # Downloaded CSV files
└── processed/     # Cleaned and transformed files
```

## Limitations

- Currently only supports CSV source files and PARQUET output files.
- Each CSV file requires a corresponding YAML configuration file.
## 📝 License
[LGNU](LICENSE) | © GOPAD 2025