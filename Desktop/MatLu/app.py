import streamlit as st
import requests
import pandas as pd

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="MatLu - Análisis de Riesgo Kalshi", layout="wide")
st.title("📊 MatLu: Monitor de Inversión Segura")
st.markdown("---")

# --- PARÁMETROS DE SEGURIDAD ---
MARGEN_SEGURIDAD = 0.15  # 15% de ventaja sobre el mercado
FRACCION_KELLY = 0.10    # Solo arriesgar el 10% de lo que sugiera Kelly

# --- LÓGICA DEL ALGORITMO ---
def analizar_inversion(prob_real, precio_k, capital):
    b = (1.0 / precio_k) - 1  # Ganancia neta
    p = prob_real
    q = 1 - p
    
    # Filtro 1: Margen de Ventaja
    if p < (precio_k + MARGEN_SEGURIDAD):
        return "🔴 NO INVERTIR: Margen de seguridad insuficiente.", 0, "Bajo"
    
    # Filtro 2: Valor Esperado
    ev = (p * b) - q
    if ev <= 0:
        return "🟡 ESPERAR: Riesgo matemático detectado.", 0, "Neutro"
    
    # Filtro 3: Cálculo de inversión (Kelly Conservador)
    f_kelly = ((b * p) - q) / b
    monto = capital * (f_kelly * FRACCION_KELLY)
    
    return "🟢 INVERSIÓN SEGURA", round(monto, 2), "Alto"

# --- INTERFAZ DE USUARIO ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Configuración de Mercado")
    capital = st.number_input("Tu Capital Total ($)", value=1000)
    precio_mercado = st.slider("Precio en Kalshi (centavos)", 0.01, 0.99, 0.65)
    st.info(f"El mercado cree que hay un {int(precio_mercado*100)}% de probabilidad.")

with col2:
    st.subheader("Análisis de Datos Externos")
    prob_externa = st.slider("Tu Probabilidad (basada en FRED/Datos)", 0.01, 0.99, 0.85)
    st.write(f"Tu análisis sugiere un {int(prob_externa*100)}% de probabilidad.")

# --- RESULTADO ---
st.markdown("### Resultado del Análisis")
status, monto_sugerido, nivel = analizar_inversion(prob_externa, precio_mercado, capital)

if "🟢" in status:
    st.success(f"**{status}**")
    st.metric("Inversión Sugerida", f"${monto_sugerido}")
    st.warning(f"Regla de oro: No exceder el 2% de tu capital total por evento.")
else:
    st.error(status)

# Historial de simulación (Para tu semana de prueba)
st.markdown("---")
st.subheader("📝 Registro de Simulación de la Semana")
if 'historial' not in st.session_state:
    st.session_state.historial = []

if st.button("Registrar esta operación para seguimiento"):
    st.session_state.historial.append({"Precio": precio_mercado, "Prob": prob_externa, "Decisión": status})
    st.write("Operación guardada localmente.")

st.table(pd.DataFrame(st.session_state.historial))