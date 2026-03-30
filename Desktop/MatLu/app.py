import streamlit as st

st.set_page_config(page_title="MatLu - Análisis de Riesgo", page_icon="📈")

st.title("🩺 MatLu: Diagnóstico de Inversión")
st.write("Calcula la 'dosis' exacta para tus operaciones en Polymarket o Kalshi.")

# --- PANEL LATERAL ---
with st.sidebar:
    st.header("Configuración")
    capital_total = st.number_input("Tu Capital Total (USD)", value=100.0)
    fraccion_kelly = st.slider("Nivel de Riesgo (Fracción de Kelly)", 0.1, 1.0, 0.25)

# --- ENTRADA DE DATOS (MÉTODO MANUAL) ---
st.subheader("Datos del Mercado")
col1, col2 = st.columns(2)

with col1:
    evento = st.text_input("Nombre del Evento", "NBA: Philadelphia vs Miami")
    precio_si = st.number_input("Precio del 'SÍ' (en centavos)", min_value=1, max_value=99, value=45)

with col2:
    tu_probabilidad = st.number_input("Tu Probabilidad Estimada (%)", min_value=1, max_value=99, value=55)

# --- CÁLCULOS MATEMÁTICOS ---
p = tu_probabilidad / 100
q = 1 - p
b = (100 - precio_si) / precio_si  # Cuánto ganas por cada dólar invertido

# Criterio de Kelly
f_kelly = (p * b - q) / b
sugerencia_dinero = f_kelly * capital_total * fraccion_kelly

# --- RESULTADOS ---
st.divider()
if f_kelly > 0:
    st.success(f"✅ ¡Oportunidad detectada en {evento}!")
    st.metric("Inversión Recomendada", f"${max(0, sugerencia_dinero):.2f} USD")
    st.write(f"Tu ventaja sobre el mercado es del **{((p - (precio_si/100))*100):.1f}%**")
else:
    st.error("❌ No invertir. El precio es muy alto para tu probabilidad.")
    st.write("La matemática no favorece esta operación en este momento.")

st.info("Nota: Si el precio es 45¢ y tú crees que la probabilidad es 55%, el sistema te dirá cuánto apostar.")
