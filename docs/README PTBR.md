# etlSUS

[![License: LGPL 2.1](https://img.shields.io/badge/License-LGPL_2.1-g)](https://opensource.org/license/lgpl-2-1)
![Python](https://img.shields.io/badge/python-3.9_|_3.10_|_3.11_|_3.12-blue.svg)
[![Python package](https://github.com/GOPAD-Datasus/ETL-DataSUS/actions/workflows/python-package.yml/badge.svg)](https://github.com/GOPAD-Datasus/ETL-DataSUS/actions/workflows/python-package.yml)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.16916158.svg)](https://doi.org/10.5281/zenodo.16916158)

Um pipeline de ETL (Extract, Transform, Load) com opiniões definidas, projetado para processar os dados públicos de saúde do Brasil (DataSUS) a partir de arquivos CSV brutos, transformando-os em conjuntos de dados prontos para análise.

## Visão Geral

### O Problema

O SUS (Sistema Único de Saúde) do Brasil fornece dados extensivos de saúde pública, mas eles exigem um pré-processamento específico de domínio antes da análise. Isso inclui remover colunas desnecessárias, lidar com valores ausentes e otimizar tipos de dados. Escrever manualmente scripts para essas transformações em cada conjunto de dados é demorado e propenso a erros.

### A Solução

O etlSUS automatiza todo o processo. Basta especificar o conjunto de dados, e a biblioteca cuida do download, transformação e carregamento dos dados em um banco de dados e/ou da mesclagem de todos os arquivos.

## 🚀 Começo Rápido

### 1. Instalação

```bash
poetry add git+https://github.com/GOPAD-Datasus/ETL-DataSUS.git
```

### 2. Execute o Pipeline

```python
from etlsus import pipeline


if __name__ == '__main__':
    pipeline(
        dataset='SINASC',  # Escolha entre 'SINASC' ou 'SIM'
        data_dir='caminho/para/diretorio/de/dados',
    )
```

## 📌 Funcionalidades

- **Interface Simples:** Selecione seu conjunto de dados (SINASC e SIM) e especifique o diretório base
- **Processamento Automatizado:** Cuida automaticamente do download, transformação e carregamento
- **Transformações Otimizadas:** Remove colunas e valores irrelevantes preservando o valor analítico
  - [Dicionário SIM (PT)](SIM%20PTBR.md)[ (EN)](SIM.md)
  - [Dicionário SINASC (PT)](SINASC%20PTBR.md)[ (EN)](SINASC.md)
- **Múltiplos Formatos de Saída:**
  - Exportação direta para bancos de dados relacionais
  - Arquivo único mesclado para análise multi-anual
  - Múltiplos arquivos

## 📁 Estrutura do Projeto

Após executar o pipeline, seu diretório de dados será organizado da seguinte forma:

```
# Usando data_dir = "./data"

./data
├── raw/                  # Arquivos CSV baixados
├── processed/            # Arquivos limpos e transformados
└── dataset.parquet.gzip  # (Opcional) Arquivo mesclado
```

## Limitação

- Suporta apenas arquivos de saída no formato PARQUET.

## 📝 Licença
[LGNU](LICENSE) | © GOPAD 2025