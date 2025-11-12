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

# Logo corporatiu (ha de ser un fitxer local, ex. logo.png)
st.image("logo.png", width=150)

st.title("Calculadora Hipotecària Corporativa")

# Funció per calcular capital màxim i preu màxim
def calcular_maxims(ingressos_mensuals, despeses_mensuals, tipus_interes, anys, percentatge_quota=0.35, percentatge_financament=0.8):
    # Capacitat de pagament mensual
    capacitat_quota = (ingressos_mensuals - despeses_mensuals) * percentatge_quota
    # Fórmula hipoteca: quota = capital * i / (1 - (1+i)^-n)
    i = tipus_interes / 12 / 100
    n = anys * 12
    capital_maxim = capacitat_quota * (1 - (1 + i) ** -n) / i
    # Preu màxim habitatge assumint percentatge de finançament
    preu_maxim = capital_maxim / percentatge_financament
    return round(capital_maxim, 2), round(preu_maxim, 2)

# Inputs
ingressos = st.number_input("Ingressos mensuals (€)", min_value=0)
despeses = st.number_input("Despeses mensuals (€)", min_value=0)
tipus_interes = st.number_input("Tipus d'interès (%)", min_value=0.0)
anys = st.number_input("Termini (anys)", min_value=1)

if st.button("Calcular màxims"):
    capital, preu = calcular_maxims(ingressos, despeses, tipus_interes, anys)
    st.success(f"Capital màxim hipoteca: {capital} €")
    st.success(f"Preu màxim habitatge: {preu} €")

    # Gauge per visualitzar percentatge d'ús de capacitat
    valor_gauge = 75
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=valor_gauge,
        title={'text': "Qualificació"},
        gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "#1986aa"}}
    ))
    st.plotly_chart(fig)
