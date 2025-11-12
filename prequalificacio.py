
import streamlit as st

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

# Mostra el logotip
st.image("logo.png", width=150)

# Títol amb color corporatiu
st.markdown("<h1 style='color:#1986aa; font-family:Arial;'>Agent de Prequalificació Hipotecària</h1>", unsafe_allow_html=True)
st.markdown("<p style='font-size:18px;'>Estima la capacitat hipotecària del teu client de manera ràpida i senzilla.</p>", unsafe_allow_html=True)

# Formulari
st.subheader("Introdueix les dades del client")
ingressos = st.number_input("Ingressos nets mensuals (€)", min_value=0, value=2500)
estalvis = st.number_input("Estalvis disponibles (€)", min_value=0, value=40000)
deutes = st.number_input("Quotes mensuals de deutes (€)", min_value=0, value=300)
tipus_interes = st.number_input("Tipus d'interès anual (%)", min_value=0.0, value=3.5)
anys = st.slider("Anys de la hipoteca", min_value=5, max_value=35, value=30)

if st.button("Calcula la capacitat hipotecària"):
    quota, hipoteca, preu = calcula_capacitat_hipotecaria(ingressos, estalvis, deutes, tipus_interes, anys)
    st.subheader("Resultats")
    st.success(f"Quota màxima recomanada: **{quota:.2f} €**/mes")
    st.info(f"Import màxim de la hipoteca: **{hipoteca:.2f} €**")
    st.warning(f"Preu màxim de l'habitatge assumible: **{preu:.2f} €** (incloent despeses del 10%)")

# Footer amb informació de contacte actualitzada
st.markdown("""
<hr>
<p style='text-align:center; font-size:14px;'>© 2025 Sergi Martín | Contacte: <a href='mailto:info@sergimartinrealtor.com'>info@sergimartinrealtor.com</a></p>
""", unsafe_allow_html=True)
