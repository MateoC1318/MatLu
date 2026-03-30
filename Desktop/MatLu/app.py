import streamlit as st

# Configuración de interfaz profesional
st.set_page_config(page_title="MatLu v7.0 - Centro de Mando", page_icon="⚖️", layout="wide")

st.title("⚖️ MatLu: Inteligencia & Gestión de Riesgo")
st.markdown("---")

# --- SECCIÓN 1: EL PREDICTOR (PARA ADIVINAR) ---
st.header("1. 🧠 Módulo de Diagnóstico (Tendencia)")
st.info("Ingresa precios históricos para que MatLu estime una probabilidad basada en la inercia.")

col1, col2 = st.columns(2)
with col1:
    p_hoy = st.number_input("Precio Actual (Ej: 2760)", value=2760.0, key="p_actual")
    p_semana = st.number_input("Precio hace 7 días", value=2650.0, key="p_pasado")
with col2:
    sentimiento = st.select_slider("Sentimiento del Mercado", 
                                   options=["Bajista", "Neutral", "Alcista"], 
                                   value="Neutral")

# Lógica del Predictor Automático
cambio_pct = ((p_hoy - p_semana) / p_semana) * 100
prob_estimada = 52.0 # Punto de partida conservador

if cambio_pct > 0:
    prob_estimada += min(cambio_pct * 1.2, 18) # Bonus por subida
else:
    prob_estimada -= min(abs(cambio_pct) * 1.5, 20) # Penaliza por caída

if sentimiento == "Alcista": prob_estimada += 5
if sentimiento == "Bajista": prob_estimada -= 10

# Límites de seguridad (No pasar de 85% para no ser arrogante)
prob_estimada = max(min(prob_estimada, 85), 15)

st.metric("Probabilidad Sugerida por MatLu", f"{prob_estimada:.1f}%", f"{cambio_pct:.2f}% tendencia")

st.markdown("---")

# --- SECCIÓN 2: CALCULADORA DE DOSIS (ESTILO POLYMARKET) ---
st.header("2. 🎯 Módulo de Ejecución (Dosis)")
st.info("Aquí decides cuánto invertir. Compara lo que 'crees' (Sección 1) vs lo que el mercado 'cobra' (Precio Contrato).")

c1, c2, c3 = st.columns(3)

with c1:
    # Puedes usar la prob_estimada de arriba o escribir la de Polymarket
    prob_final = st.number_input("Tu Probabilidad de Éxito (%)", 
                                 min_value=1.0, max_value=99.0, 
                                 value=prob_estimada, step=1.0)
    capital = st.number_input("Tu Capital Total", value=1000000, step=50000)

with c2:
    # El precio que ves en la app (Polymarket / Kalshi / trii escalado)
    precio_mercado = st.number_input("Precio del Contrato (Escala 1-100)", 
                                     min_value=1.0, max_value=99.0, value=50.0)

with c3:
    # Fracción de Kelly (Conservador)
    riesgo_k = st.radio("Nivel de Riesgo (Kelly)", [0.1, 0.2], 
                        format_func=lambda x: f"Conservador ({x})")

# --- LÓGICA DE CÁLCULO (CRITERIO DE KELLY) ---
p = prob_final / 100
q = 1 - p
# Ventaja (b): Lo que recibes por cada unidad arriesgada
b_factor = (100 - precio_mercado) / precio_mercado if precio_mercado < 100 else 0

# Solo hay inversión si nuestra probabilidad p es MAYOR al precio implícito del mercado
if p > (precio_mercado / 100):
    f_kelly = ((p * b_factor) - q) / b_factor
    dosis_final_pct = f_kelly * riesgo_k * 100
else:
    dosis_final_pct = 0

# --- RESULTADO DEL DIAGNÓSTICO ---
st.markdown("### Resultado del Análisis")

if dosis_final_pct > 0:
    monto_invertir = capital * (dosis_final_pct / 100)
    st.success(f"### ✅ DOSIS RECOMENDADA: {dosis_final_pct:.2f}% de tu capital")
    st.metric("Inversión en Dinero Real", f"${monto_invertir:,.0f} COP/USD")
    st.write("👉 *Hay una ventaja matemática. El mercado está subestimando la probabilidad.*")
else:
    st.error("### 🛑 NO OPERAR")
    st.write("El precio del mercado es igual o mayor a tu probabilidad estimada. No hay ventaja estratégica.")

st.markdown("---")
st.caption("MatLu v7.0 - Sistema Integrado de Predicción y Gestión de Riesgo.")
