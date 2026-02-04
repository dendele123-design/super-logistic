import streamlit as st
import pandas as pd
from datetime import datetime
import time

# --- CONFIGURAZIONE ---
st.set_page_config(page_title="SuPeR Logistics Manager", page_icon="🚌", layout="wide")

# CSS per look professionale e pulito
st.markdown("""
<style>
    header {visibility: hidden !important;}
    .stApp { background-color: #ffffff !important; }
    .status-box { padding: 20px; border-radius: 10px; text-align: center; color: white; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.title("🚌 SuPeR Logistics - HUB Centrale")
st.write("Coordinamento sedi: Roma Nord | Roma Sud | Milano")

# NAVIGAZIONE
menu = st.sidebar.radio("FUNZIONI:", ["🏠 Dashboard Flotta", "🔧 Segnalazione Guasti", "📡 Comunicazioni Inter-Sede"])

# --- 1. DASHBOARD FLOTTA ---
if menu == "🏠 Dashboard Flotta":
    st.subheader("Stato Mezzi in Tempo Reale")
    
    # Esempio di dati che verrebbero letti da Google Sheets
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Totale Mezzi", "45")
    col2.metric("In Servizio", "32", delta="🟢 OK")
    col3.metric("Disponibili", "8", delta="🟡 Disponibili")
    col4.metric("In Officina", "5", delta="-2", delta_color="inverse")

    st.write("---")
    st.write("🔍 **Dettaglio per Sede:**")
    # Qui caricheremmo la tabella dal foglio Google
    df_mezzi = pd.DataFrame({
        "Mezzo": ["Pullman 01", "MiniBus 05", "NCC BMW 02", "Pullman 08"],
        "Sede": ["Roma Nord", "Milano", "Roma Sud", "Milano"],
        "Stato": ["🟢 Disponibile", "🔴 Guasto", "🟢 Disponibile", "🟡 In Servizio"],
        "Ultimo Controllo": ["02/02/2024", "01/02/2024", "04/02/2024", "03/02/2024"]
    })
    st.table(df_mezzi)

# --- 2. SEGNALAZIONE GUASTI ---
elif menu == "🔧 Segnalazione Guasti":
    st.subheader("Nuova Segnalazione Tecnica")
    with st.container(border=True):
        mezzo = st.selectbox("Seleziona il mezzo:", ["Pullman 01", "MiniBus 05", "NCC BMW 02"])
        gravita = st.select_slider("Gravità guasto:", options=["Lieve (Marciante)", "Media", "Bloccante (Fermo)"])
        descrizione = st.text_area("Descrivi il problema:")
        foto = st.file_uploader("Carica foto guasto (Opzionale)")
    
    if st.button("INVIA ALL'OFFICINA 🛠️", type="primary"):
        st.success(f"Segnalazione inviata correttamente per il {mezzo}. La sede di riferimento è stata notificata.")

# --- 3. COMUNICAZIONI INTER-SEDE ---
elif menu == "📡 Comunicazioni Inter-Sede":
    st.subheader("Diario di Bordo Condiviso")
    
    with st.expander("➕ Invia comunicazione a un'altra sede"):
        da_sede = st.selectbox("Dalla sede:", ["Roma Nord", "Roma Sud", "Milano"])
        a_sede = st.selectbox("Alla sede:", ["Tutte", "Roma Nord", "Roma Sud", "Milano"])
        messaggio = st.text_area("Messaggio importante:")
        st.button("PUBBLICA SULLA BACHECA 📌")

    st.write("---")
    st.write("📌 **Ultime comunicazioni:**")
    st.info("**Milano -> Roma Nord:** L'autista Rossi è in ritardo causa traffico A1. Pullmann 12 previsto alle 12:30.")
    st.warning("**Roma Sud -> Tutte:** Ricordarsi rinnovo assicurazione entro venerdì per flotta NCC.")

# --- FOOTER ---
st.sidebar.divider()
st.sidebar.markdown("Powered by **SuPeR** | Logistics Edition")
