
import streamlit as st
import fitz  # PyMuPDF
import io
import plotly.graph_objects as go

def calcula_capacitat_hipotecaria(ingressos_nets_mensuals, estalvis, deutes_mensuals, tipus_interes_anual, anys_hipoteca):
    quota_maxima = (ingressos_nets_mensuals - deutes_mensuals) * 0.35
    tipus_interes_mensual = tipus_interes_anual / 12 / 100
    n_pagaments = anys_hipoteca * 12

    if tipus_interes_mensual > 0:
        import_maxim_hipoteca = quota_maxima * ((1 - (1 + tipus_interes_mensual) ** -n_pagaments) / tipus_interes_mensual)
    else:
        import_maxim_hipoteca = quota_maxima * n_pagaments

    preu_maxim_habitatge = (import_maxim_hipoteca + estalvis) / 1.10
    return quota_maxima, import_maxim_hipoteca, preu_maxim_habitatge

# Configuració de la pàgina
st.set_page_config(page_title="Prequalificació de compradors", page_icon="🏠", layout="centered")

# CSS corporatiu
st.markdown("""
<style>
    body {
        background-color: #f0f8fb;
        font-family: 'Arial', sans-serif;
    }
    .main > div {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    h1, h2, h3 {
        color: #1986aa;
    }
    .stButton>button, .stDownloadButton>button {
        background-color: #1986aa;
        color: white;
        font-size: 16px;
        border-radius: 8px;
        padding: 10px 20px;
        border: none;
    }
    .stTextInput>div>input {
        border-radius: 6px;
        border: 1px solid #1986aa;
    }
</style>
""", unsafe_allow_html=True)

# Logo i títol
st.image("logo.png", width=150)
st.markdown("<h1 style='text-align:center;'>Agent de Prequalificació Hipotecària</h1>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# Formulari
st.subheader("Introdueix les dades del client")
nom_client = st.text_input("Nom del client")
ingressos = st.number_input("Ingressos nets mensuals (€)", min_value=0, value=2500)
estalvis = st.number_input("Estalvis disponibles (€)", min_value=0, value=40000)
deutes = st.number_input("Quotes mensuals de deutes (€)", min_value=0, value=300)
tipus_interes = st.number_input("Tipus d'interès anual (%)", min_value=0.0, value=3.5)
anys = st.slider("Anys de la hipoteca", min_value=5, max_value=35, value=30)

st.markdown("<hr>", unsafe_allow_html=True)

if st.button("Calcula la capacitat hipotecària"):
    quota, hipoteca, preu = calcula_capacitat_hipotecaria(ingressos, estalvis, deutes, tipus_interes, anys)
    st.markdown("<h2 style='text-align:center;'>Resultats</h2>", unsafe_allow_html=True)
    st.success(f"Quota màxima recomanada: **{quota:.2f} €**/mes")
    st.info(f"Import màxim de la hipoteca: **{hipoteca:.2f} €**")
    st.warning(f"Preu màxim de l'habitatge assumible: **{preu:.2f} €** (incloent despeses del 10%)")

    # Gauge amb Plotly
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=quota,
        title={'text': "Quota vs Ingressos"},
        gauge={
            'axis': {'range': [None, ingressos]},
            'bar': {'color': "#1986aa"},
            'steps': [
                {'range': [0, ingressos*0.35], 'color': "#d4f1f9"},
                {'range': [ingressos*0.35, ingressos], 'color': "#f0f8fb"}
            ],
            'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': ingressos*0.35}
        }
    ))
    st.plotly_chart(fig, use_container_width=True)

    # Generar PDF amb PyMuPDF
    pdf_buffer = io.BytesIO()
    doc = fitz.open()
    page = doc.new_page()

    text = f"""Informe de Prequalificació

Nom: {nom_client}

Ingressos: {ingressos} €
Estalvis: {estalvis} €
Deutes: {deutes} €
Tipus d'interès: {tipus_interes}%
Termini: {anys} anys

Resultats:
Quota màxima: {quota:.2f} €
Hipoteca màxima: {hipoteca:.2f} €
Preu màxim habitatge: {preu:.2f} €"""

    page.insert_text((50, 50), text, fontsize=12)
    doc.save(pdf_buffer)
    doc.close()

    st.download_button(
        label="Descarrega informe en PDF",
        data=pdf_buffer.getvalue(),
        file_name=f"prequalificacio_{nom_client or 'client'}.pdf",
        mime="application/pdf"
    )

# Footer
st.markdown("""
<hr>
<p style='text-align:center; font-size:14px;'>© 2025 Sergi Martín | Contacte: <a href='mailto:info@sergimartinrealtor.com'>info@sergimartinrealtor.com</a></p>
""", unsafe_allow_html=True)
