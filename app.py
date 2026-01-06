import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# -----------------------------------------------------------------------------
# 1. CONFIGURAZIONE E TESTI
# -----------------------------------------------------------------------------

# NOMI DELLE DIMENSIONI
DIMENSIONI = [
    "Autonomia e competenza\n(A&C)",
    "Potere personale\n(S-E)",
    "Coerenza e significato\n(C&M)",
    "Impatto e futuro\n(I&F)",
    "Flessibilità evolutiva\n(F-A)"
]

# DOMANDE
DOMANDE = [
    {"id": "q1", "testo": "Sento che le mie attività quotidiane riflettono i miei valori e le mie convinzioni personali.", "dim": 0, "reverse": False},
    {"id": "q2", "testo": "Quando affronto un compito difficile, ho fiducia nella mia capacità di padroneggiarlo con le risorse a mia disposizione.", "dim": 0, "reverse": False},
    {"id": "q3", "testo": "Mi capita spesso di svolgere il mio lavoro solo perché mi è stato imposto, senza sentirlo veramente 'mio'.", "dim": 0, "reverse": True},
    {"id": "q4", "testo": "Di fronte a un problema lavorativo, mi attivo immediatamente per modificare gli elementi che sono sotto il mio controllo.", "dim": 1, "reverse": False},
    {"id": "q5", "testo": "Sento di avere l'autorità e la capacità necessarie per influenzare i processi decisionali che riguardano il mio ruolo.", "dim": 1, "reverse": False},
    {"id": "q6", "testo": "Ho la sensazione che la mia crescita professionale dipenda più dal caso o dalle decisioni altrui che dal mio impegno.", "dim": 1, "reverse": True},
    {"id": "q7", "testo": "Comprendo chiaramente come il mio lavoro si inserisce nel quadro generale e negli obiettivi dell'organizzazione.", "dim": 2, "reverse": False},
    {"id": "q8", "testo": "Considero le sfide lavorative come occasioni che valgono l'investimento di tempo ed energia.", "dim": 2, "reverse": False},
    {"id": "q9", "testo": "Molto spesso mi sembra che le richieste che ricevo siano confuse, imprevedibili o prive di una logica chiara.", "dim": 2, "reverse": True},
    {"id": "q10", "testo": "Mi impegno attivamente per trasmettere le mie conoscenze e competenze ai colleghi o ai collaboratori più giovani.", "dim": 3, "reverse": False},
    {"id": "q11", "testo": "Mi dà soddisfazione sapere che i risultati del mio lavoro avranno un impatto positivo sugli altri anche in futuro.", "dim": 3, "reverse": False},
    {"id": "q12", "testo": "Tendo a focalizzarmi esclusivamente sui miei task individuali, senza preoccuparmi della crescita del team o del contesto.", "dim": 3, "reverse": True},
    {"id": "q13", "testo": "Quando vivo un fallimento professionale, riesco a recuperare velocemente l'equilibrio e a ripartire.", "dim": 4, "reverse": False},
    {"id": "q14", "testo": "Considero i cambiamenti organizzativi inattesi come opportunità per sviluppare nuove competenze.", "dim": 4, "reverse": False},
    {"id": "q15", "testo": "In periodi di forte stress, faccio fatica a trovare soluzioni creative e tendo a irrigidirmi sulle vecchie abitudini.", "dim": 4, "reverse": True},
]

# OPZIONI ANAGRAFICHE
OPT_GENERE = ["Maschile", "Femminile", "Non binario", "Non risponde"]
OPT_ETA = ["Meno di 20 anni", "21-30 anni", "31-40 anni", "41-50 anni", "51-60 anni", "61-70 anni", "Più di 70 anni"]
OPT_SCOLARITA = ["Licenza media", "Qualifica professionale", "Diploma di maturità", "Laurea triennale", "Laurea magistrale, specialistica o a ciclo unico", "Diploma post laurea"]

# OPZIONI SCALA LIKERT A 6 PUNTI
OPZIONI_RISPOSTA = {
    1: "Per nulla",
    2: "Poco",
    3: "Abbastanza",
    4: "Molto",
    5: "Moltissimo",
    6: "Totalmente"
}

# -----------------------------------------------------------------------------
# 2. FUNZIONI LOGICHE
# -----------------------------------------------------------------------------

def calcola_punteggi(risposte_utente):
    punteggi_dim = [0] * 5
    totale = 0
    for q in DOMANDE:
        val_raw = risposte_utente[q['id']]
        # FORMULA REVERSE PER SCALA 6 PUNTI: 7 - val
        punteggio = 7 - val_raw if q['reverse'] else val_raw
        punteggi_dim[q['dim']] += punteggio
        totale += punteggio
    return totale, punteggi_dim

def get_feedback_narrativo(totale):
    """
    Restituisce colore, titolo, sottotitolo e testo dettagliato in base ai 6 range forniti.
    Range Totale: 15 (min) - 90 (max)
    """
    
    # RANGE 1: 15-30 (Profondamente latente)
    if 15 <= totale <= 30:
        colore = "#FF4B4B" # Rosso
        livello = "IMPATTO LATENTE"
        desc = "**Impatto profondamente latente**"
        dett = ("In base ai risultati del test sembrebbe che tu viva al momento una fase di profondo adattamento “passivo”. "
                "Non mostri nessuna consapevolezza delle tue potenzialità e non sai, di conseguenza, di quali risorse puoi disporre "
                "e quali ti potrebbero servire per attuarle. L’azione suggerita è di lavorare prima di qualunque altra sulla "
                "consapevolezza attraverso degli strumenti di autovalutazione che ti consentano di valutare i tuoi punti di forza "
                "e le aree di sviluppo: certamente scoprirai di non essere così debole come ti presenti.")

    # RANGE 2: 31-45 (Parzialmente latente)
    elif 31 <= totale <= 45:
        colore = "#FF4B4B" # Rosso
        livello = "IMPATTO LATENTE"
        desc = "**Impatto parzialmente latente**"
        dett = ("In base ai risultati del test sembrebbe che tu viva al momento una fase prevalente di adattamento “passivo”. "
                "Non mostri grande consapevolezza delle tue potenzialità e non sembri, di conseguenza, sapere di quali risorse "
                "puoi già ora disporre e di quali ti servirebbe impadronirti per attuarle. L’azione suggerita è di lavorare "
                "innanzitutto sulla consapevolezza attraverso degli strumenti di autovalutazione che ti consentano di valutare "
                "i tuoi punti di forza e le aree di sviluppo e sulla base di quanto emerge costruire un piano di sviluppo personale.")

    # RANGE 3: 46-57 (Parzialmente emergente)
    elif 46 <= totale <= 57:
        colore = "#FFC300" # Giallo
        livello = "IMPATTO EMERGENTE"
        desc = "**Impatto parzialmente emergente**"
        dett = ("In base ai risultati del test mostri una certa consapevolezza delle tue potenzialità, nonché delle risorse "
                "di cui disponi anche se magari mostri una certa discontinuità nel loro utilizzo nell’attuarle. "
                "L’azione suggerita quindi è di focalizzarti sullo sviluppo delle soft skill che potrebbero consentirti "
                "di trasformare le tue potenzialità in possibilità praticabili mediante il ricorso a strumenti facilitanti l’autoapprendimento.")

    # RANGE 4: 58-70 (Evidentemente emergente)
    elif 58 <= totale <= 70:
        colore = "#FFC300" # Giallo
        livello = "IMPATTO EMERGENTE"
        desc = "**Impatto evidentemente emergente**"
        dett = ("In base ai risultati del test mostri una buona consapevolezza delle tue potenzialità, nonché dei tuoi punti di forza "
                "e di debolezza. Conosci le tue risorse anche se non sempre mostri di saperle utilizzare per attuarle. "
                "L’azione suggerita quindi è di focalizzarti sul potenziamento delle soft skill di cui disponi e che ti consentirebbero "
                "di trasformare le tue potenzialità in possibilità praticabili mediante il ricorso a strumenti facilitanti l’autoapprendimento.")

    # RANGE 5: 71-80 (Inizialmente generativo)
    elif 71 <= totale <= 80:
        colore = "#4CAF50" # Verde
        livello = "IMPATTO GENERATIVO"
        desc = "**Impatto inizialmente generativo**"
        dett = ("Dimostri di avere un motore di competenza e benessere performante: sei consapevole delle tue potenzialità e delle "
                "tue risorse personali e sai usarle. L’azione suggerita è dunque quella di farlo anche mettendole a disposizione "
                "degli altri, sviluppando una migliore visione sistemica ed una leadership empowering.")

    # RANGE 6: 81-90 (Pienamente generativo)
    else: # 81-90
        colore = "#4CAF50" # Verde
        livello = "IMPATTO GENERATIVO"
        desc = "**Impatto pienamente generativo**"
        dett = ("Dimostri di avere un motore di competenza e benessere molto performante: sei consapevole delle tue potenzialità "
                "e delle tue risorse personali, che usi per costruire e realizzarti. L’azione suggerita è dunque quella di metterle "
                "a disposizione anche degli altri, rafforzando la tua visione sistemica e la leadership empowering.")
            
    return colore, livello, desc, dett

def plot_radar_chart(punteggi_dim, colore_riempimento):
    N = len(DIMENSIONI)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist() + [0]
    values = punteggi_dim + [punteggi_dim[0]]
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    plt.xticks(angles[:-1], DIMENSIONI, size=9, color="#333333")
    ax.set_yticklabels([])
    
    # Asse Y: Max punteggio possibile è 18 (3 item * 6 pt). Mettiamo 20 per margine.
    ax.set_ylim(0, 20)
    
    ax.plot(angles, values, color=colore_riempimento, linewidth=2, linestyle='solid')
    ax.fill(angles, values, color=colore_riempimento, alpha=0.6)

    # Configurazione cerchio esterno
    ax.spines['polar'].set_visible(True)
    ax.spines['polar'].set_color('#333333')
    ax.spines['polar'].set_linewidth(3) # Spessore linea aumentato
    ax.grid(color='#DDDDDD', linestyle='--', alpha=0.5)
    return fig

# -----------------------------------------------------------------------------
# 3. SALVATAGGIO SU GOOGLE SHEETS
# -----------------------------------------------------------------------------

def salva_su_google_sheet(dati_anagrafici, risposte, totale, livello):
    try:
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds_dict = st.secrets["gcp_service_account"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)

        sheet_name = st.secrets["private_sheet_name"]
        sheet = client.open(sheet_name).sheet1

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        valori_risposte = [risposte[q['id']] for q in DOMANDE]

        row = [
            timestamp,
            dati_anagrafici['nome'],
            dati_anagrafici['genere'],
            dati_anagrafici['eta'],
            dati_anagrafici['scolarita']
        ] + valori_risposte + [totale, livello]

        sheet.append_row(row)
        return True
    except Exception as e:
        st.error(f"Errore nel salvataggio: {e}")
        return False

# -----------------------------------------------------------------------------
# 4. MAIN APP
# -----------------------------------------------------------------------------

def main():
    st.set_page_config(page_title="Genera - Questionario", page_icon="⭕", layout="centered")

    try:
        # Assicurati che il file 'image_2.png' sia nella stessa cartella
        st.image("GENERA Logo Colore.png", use_column_width=True)
    except FileNotFoundError:
        st.error("Logo non trovato. Caricare il file 'GENERA Logo Colore.png'.")

    st.markdown("---")

    if 'submitted' not in st.session_state:
        st.session_state.submitted = False

    if not st.session_state.submitted:
        with st.expander("ℹ️ Informazioni", expanded=False):
            st.write("Compila il questionario per scoprire il tuo profilo d'impatto.")

        with st.form("questionario_form"):
            st.subheader("1. Dati Anagrafici")
            nome = st.text_input("Nome o Codice Identificativo")
            col1, col2 = st.columns(2)
            with col1:
                genere = st.selectbox("Genere", OPT_GENERE)
                eta = st.selectbox("Età", OPT_ETA)
            with col2:
                scolarita = st.selectbox("Scolarità", OPT_SCOLARITA)

            st.subheader("2. Valutazione Dimensioni")
            risposte = {}
            for index, q in enumerate(DOMANDE):
                if index > 0 and DOMANDE[index]['dim'] != DOMANDE[index-1]['dim']:
                    st.markdown("---")
                st.markdown(f"**{q['testo']}**")
                
                # Scala a 6 punti
                risposte[q['id']] = st.radio(
                    f"R{index}", 
                    [1, 2, 3, 4, 5, 6], 
                    format_func=lambda x: OPZIONI_RISPOSTA[x], 
                    horizontal=True, 
                    key=q['id'], 
                    label_visibility="collapsed"
                )

            st.markdown("---")
            invio = st.form_submit_button("CALCOLA E INVIA", type="primary")

            if invio:
                if not nome:
                    st.warning("Inserisci il Nome o Codice per procedere.")
                else:
                    totale, punteggi_dim = calcola_punteggi(risposte)
                    colore, livello, desc, dett = get_feedback_narrativo(totale)

                    anagrafica = {"nome": nome, "genere": genere, "eta": eta, "scolarita": scolarita}

                    if "gcp_service_account" in st.secrets:
                        with st.spinner("Salvataggio risultati in corso..."):
                            success = salva_su_google_sheet(anagrafica, risposte, totale, livello)
                        if success:
                            st.success("Risultati salvati con successo!")
                            st.session_state.risultati = (totale, punteggi_dim, colore, livello, desc, dett)
                            st.session_state.submitted = True
                            st.rerun()
                    else:
                        st.error("Configurazione Database mancante (Secrets).")

    else:
        totale, punteggi_dim, colore, livello, desc, dett = st.session_state.risultati
        
        # Output Risultati
        st.markdown(f"<div style='text-align:center; padding:20px; background:{colore}20; border-radius:15px; border:2px solid {colore}; margin-bottom:20px;'><h2 style='color:{colore}; margin:0;'>{livello}</h2><h3>Totale: {totale} / 90</h3></div>", unsafe_allow_html=True)

        c1, c2 = st.columns([1, 1])
        with c1:
            st.pyplot(plot_radar_chart(punteggi_dim, colore))
        with c2:
            st.markdown(f"### {desc}") # Es: Impatto parzialmente emergente
            st.info(dett) # Testo lungo
            st.markdown("**Dettaglio Dimensioni:**")
            for d, p in zip(DIMENSIONI, punteggi_dim):
                # Percentuale calcolata su 18 (3 item * 6 pt)
                st.progress(int((p/18)*100), text=f"{d.replace(chr(10),' ')}: {p} pt")

        if st.button("Compila un nuovo questionario"):
            st.session_state.submitted = False
            st.rerun()

if __name__ == "__main__":
    main()
