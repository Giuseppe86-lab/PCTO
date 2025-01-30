import streamlit as st
import numpy as np
import math
from PIL import Image

# Caricamento dei loghi
logo_insubria = Image.open("Logoinsubria.png")
logo_manfredini = Image.open("Logo_Manfredini.png")

# Funzione per calcolare la previsione basata sul modello
# Coefficienti e intercept del modello
coefficients = {
    "fam_decile_red_eq": 0.072391,
    "fam_num_comp": 0.239496,
    "citiz_it": 0.174970,
    "educ": 0.084157,
    "fam_poverta": -0.734257,
    "crisis": -0.042236
}
intercept = 6.464741

def predict_log_spesa(fam_decile_red_eq, fam_num_comp, citiz_it, educ, fam_poverta, crisis, coefficients=coefficients):
    log_spesa = intercept
    log_spesa += coefficients["fam_decile_red_eq"] * fam_decile_red_eq
    log_spesa += coefficients["fam_num_comp"] * fam_num_comp
    log_spesa += coefficients["citiz_it"] * citiz_it
    log_spesa += coefficients["educ"] * educ
    log_spesa += coefficients["fam_poverta"] * fam_poverta
    log_spesa += coefficients["crisis"] * crisis
    return log_spesa

# Dizionario per mappare le etichette ai valori numerici
citiz_it_dict = {"Si": 1, "No": 0}
educ_dict = {"Primaria": 1, "Secondaria": 2, "Superiore": 3, "Universitaria": 4}
fam_poverta_dict = {"Si": 1, "No": 0}
crisis_dict = {"Nessuno": 0, "Moderato": 1, "Grave": 2}

# Configurazione della pagina
st.set_page_config(page_title="Previsione Spesa Totale", layout="centered")

# Intestazione
col1, col2 = st.columns(2)
with col1:
    st.image(logo_insubria, width=150)
with col2:
    st.image(logo_manfredini, width=150)

st.title("Previsione della Spesa Totale")
st.markdown(
    "Questo applicativo permette di stimare la spesa totale (in forma logaritmica) basandosi sui fattori socio-economici della famiglia."
)

# Input dell'utente tramite menu a tendina
fam_decile_red_eq = st.selectbox("Decile di Reddito Equivalente", options=list(range(1, 11)))
fam_num_comp = st.selectbox("Numero di Componenti Familiari", options=list(range(1, 8)))

# Mostrare solo le etichette, recuperando i valori dal dizionario
citiz_it_label = st.selectbox("Cittadinanza Italiana", options=list(citiz_it_dict.keys()))
educ_label = st.selectbox("Livello di Istruzione", options=list(educ_dict.keys()))
fam_poverta_label = st.selectbox("Condizione di Povertà", options=list(fam_poverta_dict.keys()))
crisis_label = st.selectbox("Impatto della Crisi", options=list(crisis_dict.keys()))

# Recuperare i valori numerici dal dizionario
citiz_it_value = citiz_it_dict[citiz_it_label]
educ_value = educ_dict[educ_label]
fam_poverta_value = fam_poverta_dict[fam_poverta_label]
crisis_value = crisis_dict[crisis_label]

# Calcolo della previsione
if st.button("Calcola Previsione"):
    log_spesa = predict_log_spesa(
        fam_decile_red_eq,
        fam_num_comp,
        citiz_it_value,
        educ_value,
        fam_poverta_value,
        crisis_value
    )
    spesa_tot = math.exp(log_spesa)

    st.success(f"La spesa totale stimata (in valore reale) è: {spesa_tot:.2f} €")
