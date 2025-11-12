
import streamlit as st
import plotly.graph_objects as go
from fpdf import FPDF
import math
import base64

# --- Configuració de la pàgina ---
st.set_page_config(page_title="Agent Prequalificador", page_icon="🏠", layout="centered")

# --- Colors corporatius ---
CORPORATE_COLOR = (25, 134, 170)  # #1986aa

# --- Header ---
st.markdown(f"<h1 style='color:#1986aa;text-align:center;'>Agent Prequalificador</h1>", unsafe_allow_html=True)
st.write("Completa el formulari per calcular la teva prequalificació hipotecària.")

# --- Formulari ---
with st.form("prequal_form"):
    nom = st.text_input("Nom del client")
    ingressos = st.number_input("Ingressos mensuals (€)", min_value=0.0, step=100.0)
    estalvis = st.number_input("Estalvis disponibles (€)", min_value=0.0, step=100.0)
    preu_habitatge = st.number_input("Preu habitatge desitjat (€)", min_value=0.0, step=1000.0)
    tipus_interes = st.number_input("Tipus d'interès (%)", min_value=0.0, step=0.1, value=3.0)
    anys = st.number_input("Termini (anys)", min_value=1, step=1, value=30)
    submit = st.form_submit_button("Calcular")

if submit:
    # --- Càlcul hipotecari ---
    tipus_mensual = (tipus_interes / 100) / 12
    n_quotes = anys * 12
    import_financiar = preu_habitatge - estalvis
    quota = import_financiar * tipus_mensual / (1 - (1 + tipus_mensual) ** (-n_quotes))

    percent_financament = (import_financiar / preu_habitatge) * 100

    # --- Resultats ---
    st.subheader("Resultats")
    st.write(f"**Nom:** {nom}")
    st.write(f"**Import a finançar:** {import_financiar:,.2f} €")
    st.write(f"**Quota mensual estimada:** {quota:,.2f} €")
    st.write(f"**Percentatge finançament:** {percent_financament:.2f}%")

    # --- Gauge amb Plotly ---
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=percent_financament,
        title={"text": "Finançament (%)"},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": "#1986aa"},
            "steps": [
                {"range": [0, 80], "color": "lightgreen"},
                {"range": [80, 100], "color": "lightcoral"}
            ]
        }
    ))
    st.plotly_chart(fig)

    # --- Generar PDF amb fpdf2 ---
    class PDF(FPDF):
        def header(self):
            try:
                self.image("logo.png", 10, 8, 33)  # Logo corporatiu
            except:
                pass
            self.set_font("Arial", "B", 16)
            self.set_text_color(*CORPORATE_COLOR)
            self.cell(0, 10, "Informe Prequalificació", ln=True, align="C")

        def footer(self):
            self.set_y(-15)
            self.set_font("Arial", "I", 8)
            self.cell(0, 10, f"Pàgina {self.page_no()}", align="C")

    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", "", 12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, f"Nom del client: {nom}", ln=True)
    pdf.cell(0, 10, f"Import a finançar: {import_financiar:,.2f} €", ln=True)
    pdf.cell(0, 10, f"Quota mensual estimada: {quota:,.2f} €", ln=True)
    pdf.cell(0, 10, f"Percentatge finançament: {percent_financament:.2f}%", ln=True)

    pdf_file = "prequalificacio.pdf"
    pdf.output(pdf_file)

    # --- Botó per descarregar PDF ---
    with open(pdf_file, "rb") as f:
        pdf_bytes = f.read()
        b64 = base64.b64encode(pdf_bytes).decode()
        href = f'<a href="data:application/octet-stream;base64,{b64}" download="prequalificacio.pdf">📥 Descarregar PDF</a>'
        st.markdown(href, unsafe_allow_html=True)
