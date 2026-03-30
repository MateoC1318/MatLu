import streamlit as st

st.title("🧠 MatLu: Predictor de Probabilidades")

# --- SECCIÓN DE PREDICCIÓN (EL "OJO" DE LA APP) ---
st.header("1. Diagnóstico de Tendencia")
st.info("Ingresa los datos de la gráfica de trii para que MatLu calcule la probabilidad.")

col_a, col_b = st.columns(2)
with col_a:
    precio_actual = st.number_input("Precio Actual (Ej: 2760)", value=2760)
    precio_hace_una_semana = st.number_input("Precio hace 7 días", value=2600)

with col_b:
    tendencia_noticias = st.select_slider("Sentimiento del Mercado/Noticias", 
                                          options=["Muy Malo", "Bajista", "Neutral", "Alcista", "Excelente"], 
                                          value="Neutral")

# LÓGICA DE PREDICCIÓN AUTOMÁTICA
# Si el precio actual es mayor al de hace una semana, la probabilidad sube
cambio_precio = ((precio_actual - precio_hace_una_semana) / precio_hace_una_semana) * 100

# Base de probabilidad
prob_calculada = 50 

# Ajuste por tendencia de precio
if cambio_precio > 0:
    prob_calculada += min(cambio_precio * 2, 20) # Sube hasta 20% más si va al alza
else:
    prob_calculada -= min(abs(cambio_precio) * 2, 20)

# Ajuste por noticias
ajuste_noticias = {"Muy Malo": -20, "Bajista": -10, "Neutral": 0, "Alcista": 10, "Excelente": 20}
prob_calculada += ajuste_noticias[tendencia_noticias]

# Limitar entre 0 y 100
prob_calculada = max(min(prob_calculada, 95), 5)

st.metric(label="Probabilidad Predicha por MatLu", value=f"{prob_calculada:.0f}%", delta=f"{cambio_precio:.2f}% de tendencia")

st.markdown("---")

# --- EL RESTO DE TU CALCULADORA DE KELLY ---
# (Usa el valor de 'prob_calculada' automáticamente)
st.write(f"Utilizando **{prob_calculada:.0f}%** para calcular tu inversión de Kelly...")
# ... aquí seguiría el código de Kelly usando esa variable
