
import streamlit as st
import plotly.graph_objects as go
from fpdf import FPDF
import base64

# --- Configuración de la página ---
st.set_page_config(page_title="Agent Prequalificador", page_icon="🏠", layout="centered")

# --- Colores corporativos ---
CORPORATE_COLOR = "#1986aa"

# --- CSS personalizado ---
custom_css = f"""
<style>
    .main {{
        background-color: #f9f9f9;
    }}
    .stButton>button {{
        background-color: {CORPORATE_COLOR};
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 16px;
    }}
    .stButton>button:hover {{
        background-color: #146b88;
    }}
    footer {{
        visibility: hidden;
    }}
    .custom-footer {{
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: {CORPORATE_COLOR};
        color: white;
        text-align: center;
        padding: 10px;
        font-size: 14px;
    }}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# --- Header con logo a la izquierda ---
logo_path = "logo.png"  # Asegúrate de tener este archivo en el repositorio
header_html = f"""
<div style='display:flex; align-items:center; justify-content:center;'>
    <img src='{logo_path}' style='height:60px; margin-right:15px;'>
    <h1 style='color:{CORPORATE_COLOR};'>Agent Prequalificador</h1>
</div>
"""
st.markdown(header_html, unsafe_allow_html=True)

st.write("Completa el formulari per calcular el preu màxim de l'habitatge que pots comprar.")

# --- Formulario ---
with st.form("prequal_form"):
    nom = st.text_input("Nom del client")
    ingressos = st.number_input("Ingressos mensuals (€)", min_value=0.0, step=100.0)
    estalvis = st.number_input("Estalvis disponibles (€)", min_value=0.0, step=100.0)
    tipus_interes = st.number_input("Tipus d'interès (%)", min_value=0.0, step=0.1, value=3.0)
    anys = st.number_input("Termini (anys)", min_value=1, step=1, value=30)
    submit = st.form_submit_button("Calcular")

if submit:
    # --- Cálculo del precio máximo ---
    tipus_mensual = (tipus_interes / 100) / 12
    n_quotes = anys * 12

    # Regla del 35% de ingresos para la cuota máxima
    quota_max = ingressos * 0.35

    # Fórmula inversa para calcular el importe máximo financiable
    import_max = quota_max * (1 - (1 + tipus_mensual) ** (-n_quotes)) / tipus_mensual

    # Precio máximo = importe máximo + estalvis
    preu_maxim = import_max + estalvis

    # --- Resultados ---
    st.subheader("Resultats")
    st.write(f"**Nom:** {nom}")
    st.write(f"**Quota màxima assumible:** {quota_max:,.2f} €")
    st.write(f"**Import màxim a finançar:** {import_max:,.2f} €")
    st.write(f"**Preu màxim habitatge:** {preu_maxim:,.2f} €")

    # --- Gauge con Plotly ---
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=preu_maxim,
        title={"text": "Preu màxim (€)"},
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

    # --- Generar PDF con soporte Unicode ---
    class PDF(FPDF):
        def header(self):
            try:
                self.image(logo_path, 10, 8, 33)
            except:
                pass
            self.set_font("DejaVu", "", 16)
            self.set_text_color(25, 134, 170)
            self.cell(0, 10, "Informe Prequalificació", ln=True, align="C")

        def footer(self):
            self.set_y(-15)
            self.set_font("DejaVu", "", 8)
            self.cell(0, 10, "Agent Prequalificador - Contacte: info@empresa.com", align="C")

    pdf = PDF()
    pdf.add_font('DejaVu', '', 'DejaVuSans.ttf', uni=True)
    pdf.set_font('DejaVu', '', 12)
    pdf.add_page()
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, f"Nom del client: {nom}", ln=True)
    pdf.cell(0, 10, f"Quota màxima assumible: {quota_max:,.2f} €", ln=True)
    pdf.cell(0, 10, f"Import màxim a finançar: {import_max:,.2f} €", ln=True)
    pdf.cell(0, 10, f"Preu màxim habitatge: {preu_maxim:,.2f} €", ln=True)

    pdf_file = "prequalificacio.pdf"
    pdf.output(pdf_file)

    # --- Botón para descargar PDF ---
    with open(pdf_file, "rb") as f:
        pdf_bytes = f.read()
        b64 = base64.b64encode(pdf_bytes).decode()
        href = f'<a href="data:application/octet-stream;base64,{b64}" download="prequalificacio.pdf">📥 Descarregar PDF</a>'
        st.markdown(href, unsafe_allow_html=True)

# --- Footer personalizado en la app ---
st.markdown("<div class='custom-footer'>Agent Prequalificador © 2025 | Contacte: info@empresa.com</div>", unsafe_allow_html=True)
