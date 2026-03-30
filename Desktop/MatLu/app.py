import streamlit as st

st.set_page_config(page_title="MatLu v6.0 - Centro de Mando", page_icon="📈")

st.title("📈 MatLu: Inteligencia & Gestión de Riesgo")
st.markdown("---")

# --- SECCIÓN 1: PREDICCIÓN AUTOMÁTICA (EL ADIVINO) ---
st.header("1. 🧠 Diagnóstico de Probabilidad (Predictor)")
st.info("Usa esta sección para que MatLu analice la tendencia por ti.")

col1, col2 = st.columns(2)
with col1:
    p_hoy = st.number_input("Precio Actual (Ej: 2760)", value=2760.0, key="p1")
    p_pasado = st.number_input("Precio hace 1 semana", value=2650.0, key="p2")
with col2:
    animo = st.select_slider("Sentimiento del Mercado", 
                             options=["Baja", "Neutral", "Alta"], value="Neutral")

# Lógica del Predictor
cambio_pct = ((p_hoy - p_pasado) / p_pasado) * 100
prob_auto = 52.0
if cambio_pct > 0: prob_auto += min(cambio_pct * 1.5, 15)
else: prob_auto -= min(abs(cambio_pct) * 2, 20)
if animo == "Alta": prob_auto += 5
if animo == "Baja": prob_auto -= 10
prob_auto = max(min(prob_auto, 85), 15)

st.metric("Probabilidad Sugerida", f"{prob_auto:.1f}%", f"{cambio_pct:.2f}% de tendencia")

st.markdown("---")

# --- SECCIÓN 2: ENTRADA MANUAL (ESTILO POLYMARKET) ---
st.header("2. 🎯 Dosis por Probabilidad Directa")
st.info("Usa esta sección si ya tienes un porcentaje de Polymarket o Kalshi.")

c1, c2 = st.columns(2)
with c1:
    # AQUÍ COLOCAS LO QUE ESTÁS VIENDO EN LA OTRA APP
    prob_manual = st.number_input("Probabilidad que estás viendo (%)", 
                                  min_value=1.0, max_value=99.0, value=prob_auto, step=1.0)
    capital = st.number_input("Tu Capital Total", value=1000000, step=50000)
with c2:
    precio_con = st.number_input("Precio del Contrato (Escala 1-100)", 
                                 min_value=1.0, max_value=99.0, value=50.0)
    riesgo_k = st.radio("Nivel de Conservadurismo", [0.1, 0.2], 
                        format_func=lambda x: "Muy Conservador (0.1)" if x==0.1 else "Moderado (0.2)")

# Cálculo de Dosis Final (Kelly)
p = prob_manual / 100
q = 1 - p
b_val = (100 - precio_con) / precio_con if precio_con < 100 else 0

if b_val > 0:
    f_k = ((p * b_val) - q) / b_val
    dosis_pct = max(0, f_k * riesgo_k * 100)
else:
    dosis_pct = 0

# --- RESULTADO FINAL ---
if dosis_pct > 0:
    monto_final = capital * (dosis_pct / 100)
    st.success(f"### ✅ DOSIS SUGERIDA: {dosis_pct:.2f}%")
    st.metric("Inversión en Pesos/Dólares", f"${monto_final:,.0f}")
else:
    st.error("🛑 No es seguro invertir con estos datos.")

st.markdown("---")
st.caption("MatLu v6.0 - Combinando predicción y gestión manual.")
