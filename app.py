import streamlit as st
import pandas as pd
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials
import time

# =================================================================
# 1. CONNESSIONE A GOOGLE SHEETS
# =================================================================
def get_bacheca():
    try:
        creds_dict = st.secrets["gcp_service_account"]
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
        client = gspread.authorize(creds)
        # Sostituisci "Bacheca" con il nome esatto della scheda nel tuo foglio
        sheet = client.open_by_url(st.secrets["private_gsheets_url"]).worksheet("Bacheca")
        return sheet
    except Exception as e:
        st.error(f"Errore di connessione: {e}")
        return None

# =================================================================
# 2. CONFIGURAZIONE E DESIGN (Anti Dark-Mode)
# =================================================================
st.set_page_config(page_title="SuPeR Hub Comunicazioni", page_icon="📡", layout="centered")

st.markdown("""
<style>
    header {visibility: hidden !important;}
    /* FORZA TEMA CHIARO */
    .stApp { background-color: #ffffff !important; }
    html, body, [class*="css"], p, h1, h2, h3, label { color: #1a1a1a !important; }
    
    /* STILE MESSAGGIO */
    .msg-card {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border-left: 6px solid #800020;
        margin-bottom: 15px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    .msg-header { color: #888; font-size: 12px; margin-bottom: 5px; }
    .msg-content { font-size: 18px; font-weight: 500; }
    
    /* BOTTONE */
    .stButton>button { width: 100%; border-radius: 10px; height: 3.5em; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# =================================================================
# 3. INTERFACCIA UTENTE
# =================================================================
st.title("📡 SuPeR HUB")
st.subheader("Comunicazioni Inter-Sede")

# Identificazione sede
mia_sede = st.selectbox("TU SEI A:", ["Roma Nord", "Roma Sud", "Milano"])

st.divider()

# --- INVIO NUOVO MESSAGGIO ---
with st.expander("🆕 SCRIVI UN NUOVO MESSAGGIO"):
    destinatario = st.selectbox("PER CHI?", ["TUTTE LE SEDI", "Roma Nord", "Roma Sud", "Milano"])
    testo = st.text_area("Cosa vuoi comunicare?", placeholder="Es: Password Wi-Fi cambiata in: 12345... oppure: Gino arriva alle 15:00")
    
    if st.button("PUBBLICA IN BACHECA 📌", type="primary"):
        if not testo:
            st.warning("Non puoi inviare un messaggio vuoto!")
        else:
            with st.spinner("Invio in corso..."):
                sheet = get_bacheca()
                if sheet:
                    ora = datetime.now().strftime("%d/%m %H:%M")
                    sheet.append_row([ora, mia_sede, destinatario, testo])
                    st.success("Messaggio pubblicato!")
                    time.sleep(1)
                    st.rerun()

st.write("")
st.write("### 📢 ULTIME COMUNICAZIONI")

# --- LETTURA BACHECA ---
sheet = get_bacheca()
if sheet:
    # Leggiamo tutto e trasformiamo in lista di dizionari
    data = sheet.get_all_records()
    if data:
        # Filtriamo per mostrare solo i messaggi destinati alla mia sede o a tutte
        # E mostriamo solo gli ultimi 10 per non appesantire
        df = pd.DataFrame(data)
        messaggi_rilevanti = df[(df['Per_Sede'] == "TUTTE LE SEDI") | (df['Per_Sede'] == mia_sede)]
        
        # Invertiamo l'ordine per avere i più recenti in alto
        per_visualizzare = messaggi_rilevanti.tail(10).iloc[::-1]

        for _, m in per_visualizzare.iterrows():
            st.markdown(f"""
            <div class="msg-card">
                <div class="msg-header">🗓️ {m['Data']} | Da: <b>{m['Da_Sede']}</b> per: <b>{m['Per_Sede']}</b></div>
                <div class="msg-content">{m['Messaggio']}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("La bacheca è vuota. Sii il primo a scrivere!")

# --- FOOTER ---
st.write("")
st.write("---")
st.markdown(f"""
    <div style="text-align: center;">
        <p style="font-weight:bold; margin-bottom:5px;">SuPeR | Logistics Hub</p>
        <a href="https://wa.me/393929334563" style="color: #25D366; text-decoration: none; font-weight: bold;">💬 ASSISTENZA WHATSAPP</a><br><br>
        <div style="color: #888; font-size: 12px;">
            Powered by <a href="https://www.superstart.it" target="_blank" style="color: #b00000; text-decoration: none; font-weight: bold;">SuPeR</a> & Streamlit
        </div>
    </div>
""", unsafe_allow_html=True)
