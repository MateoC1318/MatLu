import streamlit as st

st.set_page_config(page_title="MatLu v8.0 - Ejecución Activa", page_icon="⚖️", layout="wide")

st.title("⚖️ MatLu: Gestión de Riesgo (Modo Operación Activa)")
st.markdown("---")

# --- SECCIÓN 1: EL PREDICTOR ---
st.header("1. 🧠 Diagnóstico de Tendencia")
col1, col2 = st.columns(2)
with col1:
    p_hoy = st.number_input("Precio Actual (Ej: 2760)", value=2760.0)
    p_antes = st.number_input("Precio Referencia (Hace 7 días)", value=2650.0)
with col2:
    animo = st.select_slider("Sentimiento", options=["Bajo", "Neutral", "Alto"], value="Neutral")

# Lógica del Predictor
cambio = ((p_hoy - p_antes) / p_antes) * 100
prob_estimada = 52.0
if cambio > 0: prob_estimada += min(cambio * 1.5, 15)
else: prob_estimada -= min(abs(cambio) * 2, 20)
if animo == "Alto": prob_estimada += 5
prob_estimada = max(min(prob_estimada, 85), 15)

st.metric("Probabilidad Sugerida", f"{prob_estimada:.1f}%", f"{cambio:.2f}% tendencia")

st.markdown("---")

# --- SECCIÓN 2: EJECUCIÓN (CON SOBREESTIMACIÓN DE VENTAJA) ---
st.header("2. 🎯 Dosis de Inversión Sugerida")
st.info("Este módulo asume un margen de ventaja del 5% sobre el precio del mercado para permitir la operación.")

c1, c2, c3 = st.columns(3)

with c1:
    # Si en Polymarket ves 60, aquí pones 60. El código hará el resto.
    prob_mercado = st.number_input("Probabilidad que ves en la App (%)", value=prob_estimada)
    capital = st.number_input("Tu Capital Total", value=1000000)

with c2:
    precio_con = st.number_input("Precio del Contrato (1-100)", value=prob_mercado)
    # Aquí está el truco: le sumamos un margen de 'ventaja de analista'
    margen_ventaja = st.slider("Margen de Ventaja Personal (%)", 1, 10, 5)

with c3:
    riesgo_k = st.radio("Nivel de Conservadurismo", [0.1, 0.2], format_func=lambda x: f"Conservador ({x})")

# --- LÓGICA DE SOBREESTIMACIÓN ---
# Nuestra probabilidad real para el cálculo será lo que vemos + el margen
p_operativa = (prob_mercado + margen_ventaja) / 100
q = 1 - p_operativa
b = (100 - precio_con) / precio_con if precio_con < 100 else 0

# Ahora p siempre será mayor a (precio_con/100) gracias al margen
if p_operativa > (precio_con / 100):
    f_k = ((p_operativa * b) - q) / b
    dosis_pct = f_k * riesgo_k * 100
else:
    dosis_pct = 0

# --- RESULTADO ---
if dosis_pct > 0:
    monto = capital * (dosis_pct / 100)
    st.success(f"### ✅ DOSIS SUGERIDA: {dosis_pct:.2f}% de tu capital")
    st.metric("Inversión en Dinero", f"${monto:,.0f}")
    st.write(f"*(Basado en una probabilidad ajustada de {prob_mercado + margen_ventaja}% frente a un precio de {precio_con})*")
else:
    st.error("🛑 Riesgo excesivo. Ni con el margen de ventaja es seguro invertir.")

st.markdown("---")
st.caption("MatLu v8.0 - Optimizada para operar en mercados eficientes.")
