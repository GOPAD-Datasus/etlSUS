### SINASC Variable Dictionary  
>For more details about the original version, visit the OpenDataSUS documentation [OpenDataSUS](https://diaad.s3.sa-east-1.amazonaws.com/sinasc/SINASC+-+Estrutura.pdf)  

# **MOTHER**  
### **Demographic Data**  
- `IDADEMAE`: Mother's age (in years)  
- `DTNASCMAE`: Mother's date of birth  
- `RACACORMAE`: Mother's race/color  
    - $1$ - White  
    - $2$ - Black  
    - $3$ - Asian  
    - $4$ - Mixed (Pardo)  
    - $5$ - Indigenous  
- `ESTCIVMAE`: Mother's marital status  
    - $1$ - Single  
    - $2$ - Married  
    - $3$ - Widowed  
    - $4$ - Legally separated/divorced  
    - $5$ - Common-law marriage  

### **Obstetric History**  
- `QTDFILVIVO`: Number of living children  
- `QTDFILMORT`: Number of fetal losses and abortions (also defined as Number of deceased children)  
- `QTDGESTANT`: Number of previous pregnancies  
- `QTDPARTNOR`: Number of previous vaginal deliveries  
- `QTDPARTCES`: Number of previous cesarean deliveries  
- `PARIDADE`: Defines whether it is the first pregnancy or if there have been multiple  
    - $0$ - Nulliparous  
    - $1$ – Multiparous  

### **Education**  
- `ESCMAE`: Education level, in completed years of study  
    - $1$ - None  
    - $2$ - 1 to 3 years  
    - $3$ - 4 to 7 years  
    - $4$ - 8 to 11 years  
    - $5$ - 12 or more years  
- `ESCMAE2010`: Education level according to the 2010 standard  
    - $0$ – No formal education  
    - $1$ – Elementary School I (1st to 4th grade)  
    - $2$ – Elementary School II (5th to 8th grade)  
    - $3$ – High School (formerly Secondary Education)  
    - $4$ – Incomplete Higher Education  
    - $5$ – Complete Higher Education  
- `SERIESCMAE`: Mother’s school grade. Between 1 and 8.  
- `ESCMAEAGR1`: Aggregated education level (2010 standard).  
    - $0$ – No Formal Education  
    - $1$ – Incomplete Elementary School I  
    - $2$ – Complete Elementary School I  
    - $3$ – Incomplete Elementary School II  
    - $4$ – Complete Elementary School II  
    - $5$ – Incomplete High School  
    - $6$ – Complete High School  
    - $7$ – Incomplete Higher Education  
    - $8$ – Complete Higher Education  
    - $10$ – Incomplete or Unspecified Elementary School I  
    - $11$ – Incomplete or Unspecified Elementary School II  
    - $12$ – Incomplete or Unspecified High School  

### **Residence and Place of Birth**  
> Municipality codes follow the [IBGE](https://www.ibge.gov.br/explica/codigos-dos-municipios.php) six-digit standard  
- `CODMUNNATU`: Municipality code of the mother's place of birth  
- `CODUFNATU`: State (UF) code of the mother's place of birth  
- `NATURALMAE`: If the mother is foreign-born, the country of birth code will be listed  
- `CODMUNRES`: Municipality code of residence  

### **Occupation**  
- `CODOCUPMAE`: Mother's occupation code ([CBO 2002](http://www.mtecbo.gov.br/cbosite/pages/informacoesGerais.jsf))  

---  

# **PREGNANCY AND PRENATAL CARE**  
### **Gestational Data**  
- `DTULTMENST`: Date of last menstruation  
- `SEMAGESTAC`: Number of gestational weeks  
- `GESTACAO`: Gestational weeks classification  
    - $1$ - Less than 22 weeks  
    - $2$ - 22 to 27 weeks  
    - $3$ - 28 to 31 weeks  
    - $4$ - 32 to 36 weeks  
    - $5$ - 37 to 41 weeks  
    - $6$ - 42 weeks or more  
- `GRAVIDEZ`: Type of pregnancy  
    - $1$ - Single  
    - $2$ - Twin  
    - $3$ - Triplet or more  

### **Prenatal Care**  
- `CONSPRENAT`: Number of prenatal visits  
- `CONSULTAS`: Prenatal visits classification  
    - $1$ - No visits  
    - $2$ - 1 to 3 visits  
    - $3$ - 4 to 6 visits  
    - $4$ - 7 or more visits  
- `MESPRENAT`: Month of gestation when prenatal care began  
- `KOTELCHUCK`: Kotelchuck Index for Prenatal Care Assessment  

---  

# **DELIVERY AND BIRTH**  
### **Delivery Event**  
- `DTNASC`: Date of birth  
- `HORANASC`: Time of birth
- `PARTO`: Type of delivery  
    - $1$ - Vaginal  
    - $2$ - Cesarean  
- `TPAPRESENT`: Type of presentation  
    - $1$ - Cephalic  
    - $2$ - Breech or podalic  
    - $3$ - Transverse  
- `STTRABPART`: Induced labor  
    - $1$ - Yes  
    - $2$ - No  
- `STCESPARTO`: Was the cesarean performed before labor began?  
    - $1$ - Yes  
    - $2$ - No  
    - $3$ - Not applicable  
- `TPROBSON`: Robson Group Code (system-generated value)  
- `TPNASCASSI`: Birth attended by?  
    - $1$ – Physician  
    - $2$ – Nurse or Midwife  
    - $3$ – Traditional Birth Attendant  
    - $4$ – Others  

### **Newborn Health**  
> Apgar is a vitality indicator, with scores between 0 (poor) and 10 (healthy)  
- `APGAR1`: Apgar at 1st minute  
- `APGAR5`: Apgar at 5th minute  
- `PESO`: Birth weight in grams  

---  

# **NEWBORN**  
### **Demographic Characteristics**  
- `SEXO`: Newborn's sex  
    - $0$ - Ignored  
    - $1$ - Male  
    - $2$ - Female  
- `RACACOR`: Newborn's race/color  
    - $1$ - White  
    - $2$ - Black  
    - $3$ - Asian  
    - $4$ - Mixed (Pardo)  
    - $5$ - Indigenous  

### **Anomalies**  
- `IDANOMAL`: Anomaly identified  
    - $0$ - No  
    - $1$ - Yes  
- `CODANOMAL`: [ICD-10](https://cid10.com.br/) anomaly code  

---  

# **PLACE OF BIRTH**  
- `LOCNASC`: Place of birth  
    - $1$ - Hospital  
    - $2$ - Other healthcare facilities  
    - $3$ - Home  
    - $4$ - Other  
    - $5$ - Indigenous village  
- `CODESTAB`: [CNES code](https://cnes.datasus.gov.br/) of the establishment where the birth occurred  
- `CODMUNNASC`: IBGE code of the municipality where the birth occurred  

---  

# **OTHER**  
### **Father**  
- `IDADEPAI`: Father's age in years  

### **Additional Methods and Status**  
- `TPMETESTIM`: Method used  
    - $1$ - Physical exam  
    - $2$ - Other method  
- `STDNEPIDEM`: Epidemiological DO (Declaração de Óbito) status  
    - $0$ - No  
    - $1$ - Yes  
- `STDNNOVA`: New DO status  
    - $0$ - No  
    - $1$ - Yes
