import streamlit as st
import plotly.graph_objects as go
from fpdf import FPDF

# Injectar CSS per disseny corporatiu
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

# Funció per calcular quota hipotecària
def calcular_quota(import_hipoteca, tipus_interes, anys):
    i = tipus_interes / 12 / 100
    n = anys * 12
    quota = import_hipoteca * i / (1 - (1 + i) ** -n)
    return round(quota, 2)

# Funció per generar gauge i guardar imatge
def generar_gauge(valor, fitxer="gauge.png"):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=valor,
        title={'text': "Qualificació"},
        gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "#1986aa"}}
    ))
    fig.update_layout(paper_bgcolor="#f9f9f9")
    fig.write_image(fitxer)
    return fitxer

# Funció per crear PDF
def crear_pdf(nom_client, import_hipoteca, quota, gauge_img):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.set_text_color(25, 134, 170)
    pdf.cell(200, 10, txt="Informe Prequalificació", ln=True, align="C")
    pdf.ln(10)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Nom del client: {nom_client}", ln=True)
    pdf.cell(200, 10, txt=f"Import hipoteca: {import_hipoteca} €", ln=True)
    pdf.cell(200, 10, txt=f"Quota mensual estimada: {quota} €", ln=True)
    pdf.ln(10)
    pdf.image(gauge_img, x=50, y=80, w=100)
    fitxer_pdf = "informe.pdf"
    pdf.output(fitxer_pdf)
    return fitxer_pdf

# --- STREAMLIT ---
st.title("Prequalificació Hipotecària")
st.subheader("Disseny corporatiu amb color #1986aa")

nom_client = st.text_input("Nom del client")
import_hipoteca = st.number_input("Import hipoteca (€)", min_value=0)
tipus_interes = st.number_input("Tipus d'interès (%)", min_value=0.0)
anys = st.number_input("Termini (anys)", min_value=1)

if st.button("Generar informe corporatiu"):
    quota = calcular_quota(import_hipoteca, tipus_interes, anys)
    st.success(f"Quota mensual estimada: {quota} €")

    valor_gauge = 75
    gauge_img = generar_gauge(valor_gauge)

    fitxer_pdf = crear_pdf(nom_client, import_hipoteca, quota, gauge_img)

    with open(fitxer_pdf, "rb") as f:
        st.download_button("Descarregar PDF corporatiu", f, file_name="informe.pdf")

# Secció futura per gràfics comparatius
st.markdown("""
---
### Gràfics comparatius (propera versió)
Aquí afegirem gràfics per comparar diferents escenaris hipotecaris.
""")
