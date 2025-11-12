import streamlit as st
import plotly.graph_objects as go
from fpdf import FPDF

# Injectar CSS corporatiu
st.markdown("""
    <style>
    .main {background-color: #f9f9f9;}
    .stButton>button {
        background-color: #1986aa;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 16px;
    }
    .stTextInput>div>input, .stNumberInput>div>input {
        border: 2px solid #1986aa;
        border-radius: 6px;
    }
    </style>
""", unsafe_allow_html=True)

# Logo corporatiu
st.image("logo.png", width=150)

st.title("Prequalificació Hipotecària")

# Funció per calcular capital màxim i preu màxim (incloent estalvis)
def calcular_maxims(ingressos_mensuals, despeses_mensuals, tipus_interes, anys, estalvis, percentatge_quota=0.35, percentatge_financament=0.8):
    capacitat_quota = (ingressos_mensuals - despeses_mensuals) * percentatge_quota
    i = tipus_interes / 12 / 100
    n = anys * 12
    if i == 0:
        capital_maxim = capacitat_quota * n
    else:
        capital_maxim = capacitat_quota * (1 - (1 + i) ** -n) / i
    capital_total = capital_maxim + estalvis
    preu_maxim = capital_total / percentatge_financament
    return round(capital_total, 2), round(preu_maxim, 2), round(capacitat_quota, 2)

# Funció per calcular índex de solvència
def calcular_score(estalvis, preu_maxim, quota_max, tipus_interes):
    score = (
        (estalvis / (preu_maxim * 0.2)) * 40 +  # fins a 40 punts per estalvis
        (quota_max / 1000) * 40 +               # fins a 40 punts per quota
        (100 - tipus_interes) * 0.2             # fins a 20 punts per tipus d'interès
    )
    return min(100, max(0, round(score, 2)))

# Funció per obtenir text explicatiu
def nivell_solvencia(score):
    if score < 40:
        return "Solvència baixa: risc alt, cal millorar estalvis o reduir despeses."
    elif score < 70:
        return "Solvència mitjana: possible, però cal ajustar condicions."
    else:
        return "Solvència alta: molt bona capacitat per comprar."

# Funció per mostrar gauge amb colors
def mostrar_gauge(score):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={'text': "Índex de Solvència"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "#1986aa"},
            'steps': [
                {'range': [0, 40], 'color': 'red'},
                {'range': [40, 70], 'color': 'yellow'},
                {'range': [70, 100], 'color': 'green'}
            ]
        }
    ))
    st.plotly_chart(fig)
    st.write(f"**{nivell_solvencia(score)}**")

# Funció per crear PDF corporatiu amb FPDF (incloent score i text)
def crear_pdf(nom_client, capital, preu, quota, score, logo_img="logo.png"):
    pdf = FPDF()
    pdf.add_page()
    try:
        pdf.image(logo_img, x=10, y=8, w=40)
    except:
        pass
    pdf.set_font("Arial", size=14)
    pdf.set_text_color(25, 134, 170)
    pdf.cell(200, 10, txt="Informe de Prequalificació", ln=True, align="C")
    pdf.ln(10)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Nom del client: {nom_client}", ln=True)
    pdf.cell(200, 10, txt=f"Capital total disponible (incloent estalvis): {capital} EUR", ln=True)
    pdf.cell(200, 10, txt=f"Preu màxim habitatge: {preu} EUR", ln=True)
    pdf.cell(200, 10, txt=f"Quota màxima assumible: {quota} EUR", ln=True)
    pdf.cell(200, 10, txt=f"Índex de solvència: {score}/100", ln=True)
    pdf.multi_cell(0, 10, txt=f"Comentari: {nivell_solvencia(score)}")
    pdf.output("informe_prequalificacio.pdf")
    return "informe_prequalificacio.pdf"

# Inputs
nom_client = st.text_input("Nom del client")
ingressos = st.number_input("Ingressos mensuals (EUR)", min_value=0)
despeses = st.number_input("Despeses mensuals (EUR)", min_value=0)
estalvis = st.number_input("Estalvis previs (EUR)", min_value=0)
tipus_interes = st.number_input("Tipus d'interès (%)", min_value=0.0)
anys = st.number_input("Termini (anys)", min_value=1)

if st.button("Generar informe PDF"):
    capital, preu, quota_max = calcular_maxims(ingressos, despeses, tipus_interes, anys, estalvis)
    score = calcular_score(estalvis, preu, quota_max, tipus_interes)
    st.success(f"Nom del client: {nom_client}")
    st.success(f"Capital total disponible (incloent estalvis): {capital} EUR")
    st.success(f"Preu màxim habitatge: {preu} EUR")
    st.info(f"Quota màxima assumible: {quota_max} EUR")
    st.warning(f"Índex de solvència: {score}/100")
    mostrar_gauge(score)
    pdf_file = crear_pdf(nom_client, capital, preu, quota_max, score)
    with open(pdf_file, "rb") as f:
        st.download_button("Descarregar PDF corporatiu", f, file_name=pdf_file)
