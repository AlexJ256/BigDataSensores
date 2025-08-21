import streamlit as st
import requests
import pandas as pd

#Para ejecutar "streamlit run app.py"


API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Sensores api", layout="wide")

st.title("Sensores")

def obtener_datos(endpoint):
    try:
        response = requests.get(f"{API_URL}/{endpoint}")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error al obtener {endpoint}")
            return {}
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        return {}

st.subheader("Medidas de Temperatura")
temp_data = obtener_datos("temperatura")
#st.write(temp_data)

if temp_data:
    st.metric("Última lectura", f"{temp_data['ultima_medida']['valor']} °C")

    df_temp = pd.DataFrame(temp_data["ultimas_10_medidas"])
    st.line_chart(df_temp.set_index("timestamp")["valor"])

st.subheader("Medidas de Humedad")
hum_data = obtener_datos("humedad")

if hum_data:
    st.metric("Última lectura", f"{hum_data['ultima_medida']['valor']} %")

    df_hum = pd.DataFrame(hum_data["historial_de_humedad"])
    st.line_chart(df_hum.set_index("timestamp")["valor"])

st.subheader("Medidas de ph")
ph_data = obtener_datos("ph")

if ph_data:
    df_ph = pd.DataFrame(ph_data["Historial_de_ph"])
    st.line_chart(df_ph.set_index("timestamp")["valor"])
