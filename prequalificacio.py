
import streamlit as st
import plotly.graph_objects as go
import base64
import fitz  # PyMuPDF
import os

# --- Configuración de la página ---
st.set_page_config(page_title="Agent Prequalificador", page_icon="🏠", layout="centered")

# --- Colores corporativos ---
CORPORATE_COLOR = "#1986aa"

# --- Mostrar logo y título ---
logo_path = "logo.png"
col1, col2 = st.columns([1, 4])
with col1:
    if os.path.exists(logo_path):
        st.image(logo_path, width=80)
    else:
        st.warning("⚠ Logo no disponible. Puja el fitxer 'logo.png'.")
with col2:
    st.markdown(f"<h1 style='color:{CORPORATE_COLOR};'>Agent Prequalificador</h1>", unsafe_allow_html=True)

st.write("Introdueix les dades del client per calcular el capital màxim d'hipoteca i el preu màxim de l'habitatge.")

# --- Formulario ---
with st.form("prequal_form"):
    nom = st.text_input("Nom del client")
    ingressos = st.number_input("Ingressos mensuals (€)", min_value=0.0, step=100.0)
    estalvis = st.number_input("Estalvis disponibles (€)", min_value=0.0, step=100.0)
    tipus_interes = st.number_input("Tipus d'interès (%)", min_value=0.0, step=0.1, value=3.0)
    anys = st.number_input("Termini (anys)", min_value=1, step=1, value=30)
    submit = st.form_submit_button("Calcular")

if submit:
    # --- Cálculo ---
    tipus_mensual = (tipus_interes / 100) / 12
    n_quotes = anys * 12
    quota_max = ingressos * 0.35
    import_max = quota_max * (1 - (1 + tipus_mensual) ** (-n_quotes)) / tipus_mensual
    preu_maxim = import_max + estalvis

    # --- Resultados ---
    st.subheader("Resultats")
    st.write(f"**Nom:** {nom}")
    st.write(f"**Quota màxima assumible:** {quota_max:,.2f} €")
    st.write(f"**Capital màxim hipoteca:** {import_max:,.2f} €")
    st.write(f"**Preu màxim habitatge:** {preu_maxim:,.2f} €")

    # --- Gauge ---
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=preu_maxim,
        title={"text": "Preu màxim (€)"},
        delta={"reference": import_max},
        gauge={
            "axis": {"range": [0, preu_maxim * 1.2]},
            "bar": {"color": CORPORATE_COLOR},
            "steps": [
                {"range": [0, preu_maxim * 0.8], "color": "lightgreen"},
                {"range": [preu_maxim * 0.8, preu_maxim * 1.2], "color": "lightcoral"}
            ]
        }
    ))
    st.plotly_chart(fig)

    # --- Exportar gauge como imagen PNG en /tmp ---
    gauge_img = "/tmp/gauge.png"
    try:
        fig.write_image(gauge_img)
    except Exception as e:
        st.error("No s'ha pogut generar la imatge del gauge. Comprova que 'kaleido' està instal·lat.")
        gauge_img = None

    # --- Generar PDF en /tmp ---
    pdf_file = "/tmp/prequalificacio.pdf"
    doc = fitz.open()
    page = doc.new_page()

    # Título
    page.insert_text((50, 50), "Informe Prequalificació", fontsize=20, color=(0.09, 0.52, 0.67))

    # Logo si existe
    if os.path.exists(logo_path):
        rect_logo = fitz.Rect(400, 20, 500, 100)
        page.insert_image(rect_logo, filename=logo_path)

    # Datos
    y = 120
    page.insert_text((50, y), f"Nom del client: {nom}", fontsize=14)
    y += 20
    page.insert_text((50, y), f"Quota màxima assumible: {quota_max:,.2f} €", fontsize=14)
    y += 20
    page.insert_text((50, y), f"Capital màxim hipoteca: {import_max:,.2f} €", fontsize=14)
    y += 20
    page.insert_text((50, y), f"Preu màxim habitatge: {preu_maxim:,.2f} €", fontsize=14)

    # Insertar gauge en el PDF si existe
    if gauge_img and os.path.exists(gauge_img):
        rect_gauge = fitz.Rect(50, y + 40, 350, y + 240)
        page.insert_image(rect_gauge, filename=gauge_img)

    # Guardar PDF
    doc.save(pdf_file)
    doc.close()

    # Botón para descargar PDF
    with open(pdf_file, "rb") as f:
        pdf_bytes = f.read()
        b64 = base64.b64encode(pdf_bytes).decode()
        href = f'<a href="data:application/octet-stream;base64,{b64}" download="prequalificacio.pdf">📥 Descarregar PDF</a>'
        st.markdown(href, unsafe_allow_html=True)
