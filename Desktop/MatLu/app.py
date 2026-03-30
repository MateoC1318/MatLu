import streamlit as st

st.set_page_config(page_title="MatLu v3.0 - Escudo Financiero", page_icon="🛡️")

st.title("🛡️ MatLu: Terminal Conservadora")
st.markdown("---")

# --- 1. PREDICCIÓN BASADA EN DATOS ---
st.header("1. Diagnóstico de Estabilidad")
col_a, col_b = st.columns(2)

with col_a:
    p_actual = st.number_input("Precio Actual (Ej: VOO a 470)", value=470.0)
    p_antes = st.number_input("Precio hace 1 mes", value=450.0)

with col_b:
    noticias = st.select_slider("Sentimiento Global", 
                               options=["Pesimista", "Cauteloso", "Neutral", "Optimista"], 
                               value="Neutral")

# Lógica Conservadora
cambio = ((p_actual - p_antes) / p_antes) * 100
prob_base = 52 # Empezamos casi en 50/50 por prudencia
if cambio > 0: prob_base += min(cambio, 10)
if noticias == "Optimista": prob_base += 5
if noticias == "Pesimista": prob_base -= 10

st.metric("Probabilidad Conservadora", f"{prob_base:.1f}%", f"{cambio:.2f}% tendencia")

st.markdown("---")

# --- 2. GESTIÓN DE RIESGO (KELLY) ---
st.header("2. Dosis de Inversión Sugerida")
c1, c2 = st.columns(2)

with c1:
    capital = st.number_input("Capital Total (COP o USD)", value=1000000)
    # Escalamos el precio para la fórmula
    precio_escala = st.number_input("Precio para Fórmula (1-99)", value=47.0)

with c2:
    # Bloqueamos el riesgo a niveles bajos para proteger al usuario
    riesgo = st.select_slider("Nivel de Riesgo (Fracción Kelly)", options=[0.1, 0.2], value=0.1)

# Cálculo Kelly
p = prob_base / 100
q = 1 - p
b = (100 - precio_escala) / precio_escala
f_k = (p * b - q) / b if b > 0 else 0
sugerencia = max(0, capital * f_k * riesgo)

if sugerencia > 0:
    st.success(f"✅ Invierte máximo: **{sugerencia:,.0f}**")
    st.info("Esta dosis protege tu capital contra caídas inesperadas.")
else:
    st.error("❌ No invertir: El riesgo es muy alto para un perfil conservador.")

st.markdown("---")
st.caption("MatLu v3.0 - Priorizando la preservación del capital.")
