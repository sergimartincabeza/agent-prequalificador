# Prequalificació Hipotecària amb FPDF

## Instruccions
1. Afegeix el teu logo com `logo.png` al mateix directori.
2. Instal·la les dependències:
   ```bash
   pip install -r requirements.txt
   ```
3. Executa l'aplicació:
   ```bash
   streamlit run prequalificacio.py
   ```

## Funcionalitats
- Camp per nom del client
- Calcula capital total (hipoteca + estalvis) i preu màxim habitatge
- Mostra quota màxima assumible
- Gauge amb percentatge de qualificació
- Generació automàtica de PDF amb logo, resultats i gauge
- Substitució del símbol € per EUR per evitar errors
