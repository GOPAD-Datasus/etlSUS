### Dicionário de Variáveis do SIM
>Para mais detalhes sobre a versão original visite a documentação do OpenDataSUS [OpenDataSUS](https://s3.sa-east-1.amazonaws.com/ckan.saude.gov.br/SIM/Dicionario_SIM_2025.pdf)

# FALECIDO
### Características Demográficas
- `DTNASC` : Data de nascimento
- `IDADE` : Idade do falecido (unidade + valor)
- `SEXO` : Sexo do falecido
- `RACACOR` : Raça/cor
- `PESO` : Peso ao nascer (em gramas)
- `ESTCIV` : Situação conjugal

### Escolaridade
- `ESC` : Escolaridade em anos (formato antigo)
- `ESC2010` : Escolaridade (padrão 2010)
- `ESCFALAGR1` : Escolaridade agregada
- `SERIESCFAL` : Série escolar concluída

### Ocupação 
- `OCUP` : Ocupação habitual (CBO 2002)

### Residência e Naturalidade
- `CODMUNRES` : Código do município de residência
- `CODMUNNATU` : Código do município de naturalidade
- `NATURAL` : Naturalidade (país/UF)

---

# MÃE
### Dados Demográficos
- `IDADEMAE` : Idade da mãe (em anos)

### Histórico Obstétrico
- `QTDFILVIVO` : Número de filhos vivos
- `QTDFILMORT` : Número de filhos mortos (perdas fetais/abortos)

### Escolaridade
- `ESCMAE` : Escolaridade da mãe em anos (formato antigo)
- `ESCMAE2010` : Escolaridade da mãe (padrão 2010)
- `ESCMAEAGR1` : Escolaridade da mãe agregada (formato 2010)
- `SERIESCMAE` : Série escolar concluída pela mãe

### Ocupação
- `OCUPMAE` : Ocupação habitual da mãe (CBO 2002)

### GRAVIDEZ
- `SEMAGESTAC` : Número de semanas de gestação
- `GESTACAO` : Classificação de semanas de gestação
- `GRAVIDEZ` : Tipo de gravidez (única, dupla, etc.)
- `PARTO` : Tipo de parto (vaginal, cesáreo)

---

# ÓBITO
### Dados do Óbito
- `DTOBITO` : Data do óbito
- `HORAOBITO`: Hora do óbito
- `LOCOCOR` : Local de ocorrência do óbito
- `CIRCOBITO` : Tipo de morte violenta (acidente, suicídio, etc.)
- `ACIDTRAB` : Óbito por acidente de trabalho?
- `OBITOPARTO` : Morte em relação ao parto
- `OBITOGRAV` : Óbito na gravidez
- `OBITOPUERP` : Óbito no puerpério
- `TPMORTEOCO` : Situação gestacional em que ocorreu o óbito

### Causas do Óbito
- `CAUSABAS` : Causa básica da DO
- `CAUSABAS_O` : Causa básica antes da resseleção
- `CAUSAMAT` : Causa materna associada
- `LINHAA` : Causa terminal (linha A)
- `LINHAB` : Causa antecedente (linha B)
- `LINHAC` : Causa antecedente (linha C)
- `LINHAD` : Causa básica (linha D)
- `LINHAII` : Causas contribuintes (Parte II)
- `ATESTADO` : CIDs informados no atestado

### Assistência e Procedimentos
- `ASSISTMED` : Recebeu assistência médica?
- `EXAME` : Realização de exame
- `CIRURGIA` : Realização de cirurgia
- `NECROPSIA` : Necropsia realizada?

### LOCAL E ESTABELECIMENTO
- `CODMUNOCOR` : Código do município de ocorrência do óbito
- `CODESTAB` : Código CNES do estabelecimento

---

# INVESTIGAÇÃO
- `DTINVESTIG` : Data da investigação
- `DTCONINV` : Data da conclusão da investigação
- `FONTEINV` : Fonte da investigação
- `FONTES` : Fontes utilizadas na investigação (combinado)
- `TPNIVELINV` : Nível do investigador (estadual, regional, municipal)
- `TPRESGINFO` : Resultado da investigação (acréscimo/correção de info)
- `ALTCAUSA` : Houve alteração da causa após investigação?
- `TPPOS` : Óbito investigado?
