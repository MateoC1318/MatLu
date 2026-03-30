import streamlit as st

# Configuración de interfaz profesional
st.set_page_config(page_title="MatLu v8.2 - Ejecución Segura", page_icon="⚖️", layout="wide")

st.title("⚖️ MatLu: Gestión de Riesgo (Modo Seguro)")
st.markdown("---")

# --- SECCIÓN 1: EL PREDICTOR ---
st.header("1. 🧠 Diagnóstico de Tendencia")
col1, col2 = st.columns(2)
with col1:
    p_hoy = st.number_input("Precio Actual (Ej: 2760)", value=2760.0)
    p_antes = st.number_input("Precio Referencia (Hace 7 días)", value=2650.0)
with col2:
    animo = st.select_slider("Sentimiento", options=["Bajista", "Neutral", "Alcista"], value="Neutral")

# Lógica del Predictor
cambio = ((p_hoy - p_antes) / p_antes) * 100
prob_estimada = 52.0
if cambio > 0: prob_estimada += min(cambio * 1.5, 18)
else: prob_estimada -= min(abs(cambio) * 2, 20)
if animo == "Alcista": prob_estimada += 5
prob_estimada = max(min(prob_estimada, 85), 5) # Permitimos que baje hasta 5 para ver el riesgo

st.metric("Probabilidad Sugerida por MatLu", f"{prob_estimada:.1f}%", f"{cambio:.2f}% tendencia")

st.markdown("---")

# --- SECCIÓN 2: EJECUCIÓN (CON VÁLVULA DE SEGURIDAD) ---
st.header("2. 🎯 Dosis de Inversión Sugerida")

c1, c2, c3 = st.columns(3)

with c1:
    prob_mercado = st.number_input("Probabilidad que ves en la App (%)", value=prob_estimada)
    capital = st.number_input("Tu Capital Total", value=1000000)

with c2:
    precio_con = st.number_input("Precio del Contrato (1-100)", value=prob_mercado)
    margen_ventaja = st.slider("Tu Margen de Confianza Analítica (%)", 1, 10, 5)

with c3:
    riesgo_k = st.radio("Nivel de Riesgo (Kelly)", [0.1, 0.2], format_func=lambda x: f"Conservador ({x})")

# --- LÓGICA DE CÁLCULO CON VÁLVULA DE SEGURIDAD ---
# 1. Aplicamos el margen solo si la probabilidad base es razonable
p_operativa = (prob_mercado + margen_ventaja) / 100
q = 1 - p_operativa
b = (100 - precio_con) / precio_con if precio_con < 100 else 0

# 2. VÁLVULA DE SEGURIDAD: 
# Si la probabilidad es muy baja (ej: < 40%) o el precio es muy alto, no operamos.
if prob_mercado < 40.0:
    dosis_pct = 0
    motivo_error = "Probabilidad demasiado baja para invertir (Riesgo extremo)."
elif p_operativa <= (precio_con / 100):
    dosis_pct = 0
    motivo_error = "El precio es igual o mayor a la probabilidad (Sin ventaja)."
else:
    f_k = ((p_operativa * b) - q) / b
    dosis_pct = max(0, f_k * riesgo_k * 100)
    motivo_error = ""

# --- RESULTADO FINAL ---
st.markdown("### Resultado del Análisis")

if dosis_pct > 0:
    monto = capital * (dosis_pct / 100)
    st.success(f"### ✅ DOSIS SUGERIDA: {dosis_pct:.2f}% de tu capital")
    st.metric("Inversión en Dinero Real", f"${monto:,.0f}")
else:
    st.error(f"### 🛑 NO OPERAR")
    st.write(motivo_error if motivo_error else "Riesgo matemáticamente desfavorable.")

st.markdown("---")
st.caption("MatLu v8.2 - Con Válvula de Seguridad contra Riesgo Extremo.")
