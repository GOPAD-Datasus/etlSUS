### Dicionário de Variáveis do SINASC
>Para mais detalhes sobre a versão original visite a documentação do OpenDataSUS [OpenDataSUS](https://diaad.s3.sa-east-1.amazonaws.com/sinasc/SINASC+-+Estrutura.pdf)

# **MÃE**
### **Dados Demográficos**
- `IDADEMAE` : Idade da mãe (em anos)
- `DTNASCMAE` : Data de nascimento da mãe 
- `RACACORMAE` : Cor/raça da mãe 
    - $1$ - Branca
    - $2$ - Preta
    - $3$ - Amarela
    - $4$ - Parda
    - $5$ - Indígena
- `ESTCIVMAE` : Situação conjugal da mãe
    - $1$ - Solteira
    - $2$ - Casada
    - $3$ - Viúva
    - $4$ - Separada judicialmente/divorciada
    - $5$ - União estável 

### **Histórico Obstétrico**
- `QTDFILVIVO` : Número de filhos vivos 
- `QTDFILMORT` : Número de perdas fetais e abortos (também definida como Número de filhos mortos)
- `QTDGESTANT` : Número de gestações anteriores 
- `QTDPARTNOR` : Número de partos vaginais anteriores 
- `QTDPARTCES`  : Número de partos cesáreos anteriores 
- `PARIDADE` : Define se é a primeira gravidez ou se teve mais de uma
    - $0$ - Nulípara
    - $1$ – Multípara

### **Escolaridade**
- `ESCMAE` : Escolaridade, em anos de estudo concluídos
    - $1$ - Nenhuma
    - $2$ - 1 a 3 anos
    - $3$ - 4 a 7 anos
    - $4$ - 8 a 11 anos
    - $5$ - 12 ou mais anos
- `ESCMAE2010` : Escolaridade no padrão de 2010
    - $0$ – Sem escolaridade
    - $1$ – Fundamental I (1a a 4a série)
    - $2$ – Fundamental II (5a a 8a série)
    - $3$ – Médio (antigo 2o Grau)
    - $4$ – Superior incompleto
    - $5$ – Superior completo
- `SERIESCMAE` : Série escolar da mãe. Entre 1 a 8.
- `ESCMAEAGR1` : Escolaridade 2010 agregada. 
    - $0$ – Sem Escolaridade
    - $1$ – Fundamental I Incompleto
    - $2$ – Fundamental I Completo
    - $3$ – Fundamental II Incompleto
    - $4$ – Fundamental II Completo
    - $5$ – Ensino Médio Incompleto
    - $6$ – Ensino Médio Completo
    - $7$ – Superior Incompleto
    - $8$ – Superior Completo
    - $10$ – Fundamental I Incompleto ou Inespecífico
    - $11$ – Fundamental II Incompleto ou Inespecífico
    - $12$ – Ensino Médio Incompleto ou Inespecífico

### **Residência e Naturalidade**
> Códigos de município utilizam o padrão do [IBGE](https://www.ibge.gov.br/explica/codigos-dos-municipios.php) de seis dígitos
- `CODMUNNATU` : Código do município de naturalidade (nascimento) da mãe
- `CODUFNATU` : Código UF de naturalidade
- `NATURALMAE` : Se a mãe for estrangeira, constará o código do país de nascimento 
- `CODMUNRES` : Código do município de residência 

### **Ocupação**
- `CODOCUPMAE` : Código [CBO 2002](http://www.mtecbo.gov.br/cbosite/pages/informacoesGerais.jsf) de ocupação da mãe 

---

# **GRAVIDEZ E PRÉ-NATAL**
### **Dados Gestacionais**
- `DTULTMENST` : Data da última menstruação
- `SEMAGESTAC` : Número de semanas de gestação 
- `GESTACAO` : Classificação de semanas de gestação
    - $1$ - Menos de 22 semanas
    - $2$ - 22 a 27 semanas
    - $3$ - 28 a 31 semanas
    - $4$ - 32 a 36 semanas
    - $5$ - 37 a 41 semanas
    - $6$ - 42 semanas ou mais 
- `GRAVIDEZ` : Tipo de gravidez
    - $1$ - Única
    - $2$ - Dupla
    - $3$ - Tripla ou mais 

### **Acompanhamento Pré-Natal**
- `CONSPRENAT` : Número de consultas pré‐natal 
- `CONSULTAS` : Classificação de consultas de pré‐natal
    - $1$ - Nenhuma consulta
    - $2$ - de 1 a 3 consultas
    - $3$ - de 4 a 6 consultas
    - $4$ - 7 ou mais consultas
- `MESPRENAT` : Mês de gestação onde se iniciou o pré‐natal 
- `KOTELCHUCK` : índice de Kotelchuck para Avaliação da assistência pré-natal

---

# **PARTO E NASCIMENTO**
### **Evento do Parto**
- `DTNASC` : Data do nascimento 
- `HORANASC`: Hora do nascimento
- `PARTO` : Tipo de parto
    - $1$ - Vaginal
    - $2$ - Cesário  
- `TPAPRESENT` : Tipo de apresentação
    - $1$ - Cefálico
    - $2$ - Pélvica ou podálica
    - $3$ - Transversa 
- `STTRABPART` : Trabalho de parto induzido
    - $1$ - Sim
    - $2$ - Não
- `STCESPARTO` : Cesárea ocorreu antes do trabalho de parto iniciar?
    - $1$ - Sim
    - $2$ - Não
    - $3$ - Não se aplica  
- `TPROBSON` : Código do Grupo de Robson (valor gerado pelo sistema)
- `TPNASCASSI`: Nascimento foi assistido por? 
    - $1$ – Médico
    - $2$ – Enfermagem ou Obstetriz
    - $3$ – Parteira
    - $4$ – Outros

### **Saúde do Recém-Nascido**
> Apgar é um indicador de vitalidade, com valores entre 0 (ruim) e 10 (saudável)
- `APGAR1` : Apgar no 1° minuto 
- `APGAR5` : Apgar no 5° minuto 
- `PESO` : Peso ao nascer em gramas

---

# **RECÉM-NASCIDO**
### **Características Demográficas**
- `SEXO` : Sexo do recém nascido
    - $0$ - Ignorado 
    - $1$ - Masculino
    - $2$ - Feminino
- `RACACOR` : Cor/raça do recém nascido
    - $1$ - Branca
    - $2$ - Preta
    - $3$ - Amarela
    - $4$ - Parda
    - $5$ - Indígena 

### **Anomalias**
- `IDANOMAL` : Anomalia identificada
    - $0$ - Não 
    - $1$ - Sim
- `CODANOMAL` : Código [CID-10](https://cid10.com.br/) da anomalia 

---

# **LOCAL DO NASCIMENTO**
- `LOCNASC` : Local de nascimento
    - $1$ - Hospital
    - $2$ - Outros estabelecimentos de saúde
    - $3$ - Domicílio
    - $4$ - Outros
    - $5$ - Aldeia Indígena 
- `CODESTAB`  : [Código CNES](https://cnes.datasus.gov.br/) do estabelecimento onde ocorreu o nascimento
- `CODMUNNASC` : Código IBGE onde ocorreu o nascimento

---

# **OUTROS**
### **Pai**
- `IDADEPAI` : Idade do pai em anos 

### **Métodos e Status Adicionais**
- `TPMETESTIM` : Método utilizado
    - $1$ - Exame físico
    - $2$ - Outro método
- `STDNEPIDEM` : Status de DO Epidemiológica
    - $0$ - Não 
    - $1$ - Sim
- `STDNNOVA` : Status de DO Nova
    - $0$ - Não 
    - $1$ - Sim
