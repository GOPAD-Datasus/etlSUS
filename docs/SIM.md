### SIM Variable Dictionary
>For more details about the original version, visit the OpenDataSUS documentation [OpenDataSUS](https://diaad.s3.sa-east-1.amazonaws.com/sim/Mortalidade_Geral+-+Estrutura.pdf)  

# DECEASED
### Demographic Characteristics
- `DTNASC`: Date of birth
- `IDADE`: Age of the deceased (unit + value)
- `SEXO`: Sex of the deceased
- `RACACOR`: Race/color
- `PESO`: Weight at birth (in grams)
- `ESTCIV`: Marital status

### Education
- `ESC`: Years of schooling (old format)
- `ESC2010`: Education level (2010 standard)
- `ESCFALAGR1`: Aggregated education level
- `SERIESCFAL`: School grade completed

### Occupation
- `OCUP`: Usual occupation (CBO 2002 - Brazilian Occupation Classification)

### Residence and Place of Birth
- `CODMUNRES`: Municipality of residence code
- `CODMUNNATU`: Municipality of birth code
- `NATURAL`: Place of birth (country/state)

---

# MOTHER
### Demographic Data
- `IDADEMAE`: Mother's age (in years)

### Obstetric History
- `QTDFILVIVO`: Number of live children
- `QTDFILMORT`: Number of deceased children (fetal losses/abortions)

### Education
- `ESCMAE`: Mother's years of schooling (old format)
- `ESCMAE2010`: Mother's education level (2010 standard)
- `ESCMAEAGR1`: Mother's aggregated education level (2010 format)
- `SERIESCMAE`: School grade completed by the mother

### Occupation
- `OCUPMAE`: Mother's usual occupation (CBO 2002)

### PREGNANCY
- `SEMAGESTAC`: Number of gestational weeks 
- `GESTACAO`: Gestational weeks classification
- `GRAVIDEZ`: Type of pregnancy (single, twin, etc.)
- `PARTO`: Type of delivery (vaginal, cesarean)

---

# DEATH
### Death Data
- `DTOBITO`: Date of death
- `HORAOBITO`: Time of death
- `LOCOCOR`: Place of death occurrence
- `CIRCOBITO`: Type of violent death (accident, suicide, etc.)
- `ACIDTRAB`: Death due to a work accident?
- `OBITOPARTO`: Death in relation to childbirth
- `OBITOGRAV`: Death during pregnancy
- `OBITOPUERP`: Death during the puerperium (postpartum period)
- `TPMORTEOCO`: Gestational situation at the time of death

### Causes of Death
- `CAUSABAS`: Underlying cause of death (from the death certificate)
- `CAUSABAS_O`: Underlying cause before reselection
- `CAUSAMAT`: Associated maternal cause
- `LINHAA`: Terminal cause (line A)
- `LINHAB`: Antecedent cause (line B)
- `LINHAC`: Antecedent cause (line C)
- `LINHAD`: Underlying cause (line D)
- `LINHAII`: Contributing causes (Part II)
- `ATESTADO`: ICD codes reported on the death certificate

### Assistance and Procedures
- `ASSISTMED`: Received medical assistance?
- `EXAME`: Examination performed
- `CIRURGIA`: Surgery performed
- `NECROPSIA`: Necropsy performed?

### LOCATION AND ESTABLISHMENT
- `CODMUNOCOR`: Municipality of death occurrence code
- `CODESTAB`: CNES code of the health establishment (National Registry of Health Establishments)

---

# INVESTIGATION
- `DTINVESTIG`: Investigation start date
- `DTCONINV`: Investigation conclusion date
- `FONTEINV`: Investigation source
- `FONTES`: Sources used in the investigation (combined)
- `TPNIVELINV`: Investigator's level (state, regional, municipal)
- `TPRESGINFO`: Investigation result (addition/correction of information)
- `ALTCAUSA`: Was the cause of death changed after investigation?
- `TPPOS`: Was the death investigated?
