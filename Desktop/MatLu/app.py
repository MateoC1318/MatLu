import streamlit as st

st.set_page_config(page_title="MatLu - Gestión de Riesgo", page_icon="📈")

st.title("🛡️ MatLu: Terminal de Inversión")
st.markdown("---")

# --- SECCIÓN 1: CRITERIO DE KELLY ---
st.header("1. ¿Cuánto invertir? (Criterio de Kelly)")

col1, col2 = st.columns(2)

with col1:
    capital_total = st.number_input("Tu Capital Total (COP)", min_value=0, value=1000000, step=50000)
    precio_kelly = st.number_input("Precio Escalado (Ej: 27.6 para Ecopetrol)", min_value=0.1, max_value=99.0, value=27.6)

with col2:
    probabilidad = st.slider("Tu Probabilidad de Éxito (%)", 0, 100, 60)
    fraccion_kelly = st.select_slider("Fracción de Kelly (Riesgo)", options=[0.1, 0.25, 0.5, 1.0], value=0.25)

# Cálculo de Kelly
p = probabilidad / 100
q = 1 - p
b = (100 - precio_kelly) / precio_kelly

if b > 0:
    f_kelly = (p * b - q) / b
    inversion_sugerida = capital_total * f_kelly * fraccion_kelly
else:
    f_kelly = 0
    inversion_sugerida = 0

if inversion_sugerida > 0:
    st.success(f"✅ Inversión Sugerida: **${inversion_sugerida:,.0f} COP**")
else:
    st.error("❌ No invertir: El precio es muy alto para tu probabilidad.")

st.markdown("---")

# --- SECCIÓN 2: CALCULADORA DE GANANCIA NETA ---
st.header("2. Proyección de Ganancia Real")

c1, c2 = st.columns(2)

with c1:
    p_compra = st.number_input("Precio de Compra Real (Ej: 2760)", min_value=0, value=2760)
    monto_pago = st.number_input("Monto a invertir ($)", min_value=0, value=int(inversion_sugerida) if inversion_sugerida > 0 else 50000)

with c2:
    p_venta = st.number_input("Precio de Venta Objetivo (Ej: 3000)", min_value=0, value=3000)
    comision_fija = st.number_input("Comisión de la App (COP)", min_value=0, value=10000)

# Cálculos de Ganancia
pct_cambio = ((p_venta - p_compra) / p_compra) * 100
ganancia_bruta = (monto_pago / p_compra) * (p_venta - p_compra)
ganancia_neta = ganancia_bruta - (comision_fija * 2) # Compra y Venta

st.subheader("Resultado del Diagnóstico:")

if ganancia_neta > 0:
    st.info(f"Subida esperada: **{pct_cambio:.2f}%**")
    st.success(f"Ganancia Neta Estimada: **${ganancia_neta:,.0f} COP** (restando comisiones)")
else:
    st.warning(f"Atención: Con una subida del {pct_cambio:.2f}%, las comisiones se comen tu ganancia. Quedarías con: **${ganancia_neta:,.0f} COP**")

st.markdown("---")
st.caption("MatLu v2.0 - Herramienta de apoyo para la toma de decisiones financieras.")
