import streamlit as st

st.set_page_config(page_title="MatLu v4.0 - Gestión de Riesgo", page_icon="⚖️")

st.title("⚖️ MatLu: Gestión de Capital (Estilo Polymarket)")
st.markdown("---")

# --- 1. DIAGNÓSTICO DE PROBABILIDAD ---
st.header("1. Cálculo de Probabilidad (Win Rate)")
col_a, col_b = st.columns(2)

with col_a:
    p_actual = st.number_input("Precio Actual de la Acción/Activo", value=2760.0)
    p_anterior = st.number_input("Precio de Referencia (Hace 7-30 días)", value=2650.0)

with col_b:
    sentimiento = st.select_slider("Sentimiento del Mercado", 
                                   options=["Pesimista", "Neutral", "Optimista"], 
                                   value="Neutral")

# Lógica de Probabilidad Predictiva
cambio = ((p_actual - p_anterior) / p_anterior) * 100
prob_final = 52.0  # Base conservadora

if cambio > 0:
    prob_final += min(cambio * 1.5, 15)  # Suma por tendencia alcista
else:
    prob_final -= min(abs(cambio) * 2, 20)  # Resta por tendencia bajista

if sentimiento == "Optimista": prob_final += 5
if sentimiento == "Pesimista": prob_final -= 10

# Limites de seguridad
prob_final = max(min(prob_final, 85), 10)

st.metric("Tu Probabilidad de Éxito", f"{prob_final:.1f}%", f"{cambio:.2f}% tendencia")

st.markdown("---")

# --- 2. DOSIS DE INVERSIÓN (ESTILO POLYMARKET / KALSHI) ---
st.header("2. Dosis Sugerida (% del Capital)")

c1, c2 = st.columns(2)

with c1:
    # Si la acción vale 2760, usamos 27.6 como 'precio de contrato' para la fórmula
    precio_contrato = st.number_input("Precio del Contrato (Escala 1-100)", value=27.6)
    capital_total = st.number_input("Tu Capital Total (Opcional)", value=1000000)

with c2:
    # Forzamos fracción conservadora para no perder
    fraccion = st.radio("Nivel de Conservadurismo", [0.1, 0.2], 
                        format_func=lambda x: "Muy Conservador (0.1)" if x==0.1 else "Moderado (0.2)")

# CÁLCULO DE KELLY PARA PORCENTAJE
p = prob_final / 100
q = 1 - p
b = (100 - precio_contrato) / precio_contrato if precio_contrato < 100 else 0

if b > 0:
    # Calculamos el % de Kelly y lo multiplicamos por la fracción de seguridad
    porcentaje_kelly = ((p * b - q) / b) * fraccion
else:
    porcentaje_kelly = 0

# RESULTADO FINAL
st.subheader("Resultado del Análisis:")

if porcentaje_kelly > 0:
    porcentaje_final = porcentaje_kelly * 100
    monto_pesos = capital_total * porcentaje_kelly
    
    st.success(f"### 📈 Dosis Sugerida: {porcentaje_final:.2f}% de tu capital")
    st.write(f"Si tu capital es **${capital_total:,.0f}**, invierte: **${monto_pesos:,.0f}**")
    st.info("Este porcentaje te permite ganar sin arriesgar tu estabilidad financiera.")
else:
    st.error("### 🛑 No Invertir")
    st.write("La probabilidad es muy baja o el precio está muy caro según este modelo.")

st.markdown("---")
st.caption("MatLu v4.0 - Gestión de riesgo profesional y conservadora.")
