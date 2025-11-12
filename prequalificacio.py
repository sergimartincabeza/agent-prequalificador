import streamlit as st
import plotly.graph_objects as go
import fitz  # PyMuPDF per crear PDF

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
    # Afegim estalvis al capital disponible
    capital_total = capital_maxim + estalvis
    preu_maxim = capital_total / percentatge_financament
    return round(capital_total, 2), round(preu_maxim, 2), round(capacitat_quota, 2)

# Funció per generar gauge i guardar imatge
def generar_gauge(valor, fitxer="gauge.png"):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=valor,
        title={'text': "Qualificació"},
        gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "#1986aa"}}
    ))
    fig.write_image(fitxer)
    return fitxer

# Funció per crear PDF corporatiu
def crear_pdf(nom_client, capital, preu, quota, gauge_img, logo_img="logo.png"):
    doc = fitz.open()
    page = doc.new_page()

    # Afegir logo
    try:
        rect_logo = fitz.Rect(50, 50, 200, 150)
        page.insert_image(rect_logo, filename=logo_img)
    except:
        pass

    # Afegir text
    text = f"Informe de Prequalificació

Nom del client: {nom_client}
Capital total disponible (incloent estalvis): {capital} €
Preu màxim habitatge: {preu} €
Quota màxima assumible: {quota} €"
    page.insert_text((50, 200), text, fontsize=14, color=(0, 0, 0))

    # Afegir gauge
    try:
        rect_gauge = fitz.Rect(50, 300, 300, 500)
        page.insert_image(rect_gauge, filename=gauge_img)
    except:
        pass

    pdf_file = "informe_prequalificacio.pdf"
    doc.save(pdf_file)
    doc.close()
    return pdf_file

# Inputs
nom_client = st.text_input("Nom del client")
ingressos = st.number_input("Ingressos mensuals (€)", min_value=0)
despeses = st.number_input("Despeses mensuals (€)", min_value=0)
estalvis = st.number_input("Estalvis previs (€)", min_value=0)
tipus_interes = st.number_input("Tipus d'interès (%)", min_value=0.0)
anys = st.number_input("Termini (anys)", min_value=1)

if st.button("Generar informe PDF"):
    capital, preu, quota_max = calcular_maxims(ingressos, despeses, tipus_interes, anys, estalvis)
    st.success(f"Nom del client: {nom_client}")
    st.success(f"Capital total disponible (incloent estalvis): {capital} €")
    st.success(f"Preu màxim habitatge: {preu} €")
    st.info(f"Quota màxima assumible: {quota_max} €")

    percentatge = min(100, round((capital / (preu if preu > 0 else 1)) * 100, 2))
    gauge_img = generar_gauge(percentatge)

    pdf_file = crear_pdf(nom_client, capital, preu, quota_max, gauge_img)

    with open(pdf_file, "rb") as f:
        st.download_button("Descarregar PDF corporatiu", f, file_name=pdf_file)
