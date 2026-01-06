import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

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

# CONFIGURAZIONE ITEM (DOMANDE)
# Testi inseriti esattamente come forniti. 
# Gli item (R) hanno "reverse": True.
DOMANDE = [
    # --- DIMENSIONE 1: Autonomia e competenza (A&C) ---
    {
        "id": "q1", 
        "testo": "Sento che le mie attività quotidiane riflettono i miei valori e le mie convinzioni personali.", 
        "dim": 0, 
        "reverse": False
    },
    {
        "id": "q2", 
        "testo": "Quando affronto un compito difficile, ho fiducia nella mia capacità di padroneggiarlo con le risorse a mia disposizione.", 
        "dim": 0, 
        "reverse": False
    },
    {
        "id": "q3", 
        "testo": "Mi capita spesso di svolgere il mio lavoro solo perché mi è stato imposto, senza sentirlo veramente 'mio'.", 
        "dim": 0, 
        "reverse": True # (R)
    },

    # --- DIMENSIONE 2: Potere personale (S-E) ---
    {
        "id": "q4", 
        "testo": "Di fronte a un problema lavorativo, mi attivo immediatamente per modificare gli elementi che sono sotto il mio controllo.", 
        "dim": 1, 
        "reverse": False
    },
    {
        "id": "q5", 
        "testo": "Sento di avere l'autorità e la capacità necessarie per influenzare i processi decisionali che riguardano il mio ruolo.", 
        "dim": 1, 
        "reverse": False
    },
    {
        "id": "q6", 
        "testo": "Ho la sensazione che la mia crescita professionale dipenda più dal caso o dalle decisioni altrui che dal mio impegno.", 
        "dim": 1, 
        "reverse": True # (R)
    }, 

    # --- DIMENSIONE 3: Coerenza e significato (C&M) ---
    {
        "id": "q7", 
        "testo": "Comprendo chiaramente come il mio lavoro si inserisce nel quadro generale e negli obiettivi dell'organizzazione.", 
        "dim": 2, 
        "reverse": False
    },
    {
        "id": "q8", 
        "testo": "Considero le sfide lavorative come occasioni che valgono l'investimento di tempo ed energia.", 
        "dim": 2, 
        "reverse": False
    },
    {
        "id": "q9", 
        "testo": "Molto spesso mi sembra che le richieste che ricevo siano confuse, imprevedibili o prive di una logica chiara.", 
        "dim": 2, 
        "reverse": True # (R)
    },

    # --- DIMENSIONE 4: Impatto e futuro (I&F) ---
    {
        "id": "q10", 
        "testo": "Mi impegno attivamente per trasmettere le mie conoscenze e competenze ai colleghi o ai collaboratori più giovani.", 
        "dim": 3, 
        "reverse": False
    },
    {
        "id": "q11", 
        "testo": "Mi dà soddisfazione sapere che i risultati del mio lavoro avranno un impatto positivo sugli altri anche in futuro.", 
        "dim": 3, 
        "reverse": False
    },
    {
        "id": "q12", 
        "testo": "Tendo a focalizzarmi esclusivamente sui miei task individuali, senza preoccuparmi della crescita del team o del contesto.", 
        "dim": 3, 
        "reverse": True # (R)
    },

    # --- DIMENSIONE 5: Flessibilità evolutiva (F-A) ---
    {
        "id": "q13", 
        "testo": "Quando vivo un fallimento professionale, riesco a recuperare velocemente l'equilibrio e a ripartire.", 
        "dim": 4, 
        "reverse": False
    },
    {
        "id": "q14", 
        "testo": "Considero i cambiamenti organizzativi inattesi come opportunità per sviluppare nuove competenze.", 
        "dim": 4, 
        "reverse": False
    },
    {
        "id": "q15", 
        "testo": "In periodi di forte stress, faccio fatica a trovare soluzioni creative e tendo a irrigidirmi sulle vecchie abitudini.", 
        "dim": 4, 
        "reverse": True # (R)
    },
]

# OPZIONI ANAGRAFICHE
OPT_GENERE = ["Maschile", "Femminile", "Non binario", "Non risponde"]
OPT_ETA = ["Meno di 20 anni", "21-30 anni", "31-40 anni", "41-50 anni", "51-60 anni", "61-70 anni", "Più di 70 anni"]
OPT_SCOLARITA = ["Licenza media", "Qualifica professionale", "Diploma di maturità", "Laurea triennale", "Laurea magistrale, specialistica o a ciclo unico", "Diploma post laurea"]

# OPZIONI SCALA LIKERT
OPZIONI_RISPOSTA = {
    1: "Per nulla",
    2: "Poco",
    3: "Abbastanza",
    4: "Molto",
    5: "Moltissimo"
}

# -----------------------------------------------------------------------------
# 2. FUNZIONI DI SUPPORTO (Calcolo e Grafica)
# -----------------------------------------------------------------------------

def calcola_punteggi(risposte_utente):
    punteggi_dim = [0] * 5
    totale = 0
    
    for q in DOMANDE:
        val_raw = risposte_utente[q['id']]
        
        # Gestione Item Reverse (R)
        # Se R: 1->5, 2->4, 3->3, 4->2, 5->1 (Formula: 6 - valore)
        if q['reverse']:
            punteggio = 6 - val_raw
        else:
            punteggio = val_raw
            
        punteggi_dim[q['dim']] += punteggio
        totale += punteggio

    return totale, punteggi_dim

def get_feedback_narrativo(totale):
    """
    Restituisce colore, titolo e descrizioni in base alle soglie:
    < 31: Rosso (Latente)
    31-54: Giallo (Emergente)
    >= 55: Verde (Generativo)
    """
    # Logica sottocategorie basata su divisione equa dei range
    
    if totale < 31:
        colore = "#FF4B4B" # Rosso
        livello = "IMPATTO LATENTE"
        # Range 0-30. Soglia interna a 15.
        if totale < 16:
            desc = "**Profondamente Latente**"
            dett = "Il potenziale è ancora del tutto inespresso o bloccato."
        else:
            desc = "**Parzialmente Latente**"
            dett = "Si intravedono i primi segnali, ma l'impatto non è ancora tangibile."
            
    elif 31 <= totale <= 54:
        colore = "#FFC300" # Giallo
        livello = "IMPATTO EMERGENTE"
        # Range 31-54 (24 pt). Metà è 42/43.
        if totale <= 42:
            desc = "**Parzialmente Emergente**"
            dett = "L'impatto inizia a manifestarsi in contesti specifici o intermittenti."
        else:
            desc = "**Evidentemente Emergente**"
            dett = "L'impatto è visibile e chiaro, anche se forse non ancora sistemico."
            
    else: # >= 55
        colore = "#4CAF50" # Verde
        livello = "IMPATTO GENERATIVO"
        # Range 55-75 (20 pt). Metà è 65.
        if totale < 65:
            desc = "**Inizialmente Generativo**"
            dett = "Il soggetto produce valore autonomamente e con costanza."
        else:
            desc = "**Compiutamente Generativo**"
            dett = "L'impatto è sistemico, sostenibile e moltiplicatore."
            
    return colore, livello, desc, dett

def plot_radar_chart(punteggi_dim, colore_riempimento):
    """
    Genera il grafico a radar iscritto in un cerchio (Logo Genera).
    """
    N = len(DIMENSIONI)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    angles += [angles[0]] # Chiudi il cerchio
    
    # Chiudi i dati
    values = punteggi_dim + [punteggi_dim[0]]
    
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    
    # Orientamento (Nord in alto) e senso orario/antiorario
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    
    # Label Assi
    plt.xticks(angles[:-1], DIMENSIONI, size=9, color="#333333")
    
    # Nascondi etichette radiali (numeri sull'asse Y) per pulizia
    ax.set_yticklabels([])
    
    # Scala fissa: max possibile è 15 (3 domande * 5 pt). Impostiamo 16 per margine.
    ax.set_ylim(0, 16)
    
    # Disegna il Poligono (Dati Utente)
    ax.plot(angles, values, color=colore_riempimento, linewidth=2, linestyle='solid')
    ax.fill(angles, values, color=colore_riempimento, alpha=0.6)
    
    # Disegna il Cerchio Esterno (Logo Genera)
    ax.spines['polar'].set_visible(True)
    ax.spines['polar'].set_color('#333333')
    ax.spines['polar'].set_linewidth(2)
    
    # Griglia interna leggera
    ax.grid(color='#DDDDDD', linestyle='--', alpha=0.5)
    
    return fig

# -----------------------------------------------------------------------------
# 3. INTERFACCIA WEB (MAIN)
# -----------------------------------------------------------------------------

def main():
    st.set_page_config(page_title="Genera - Questionario", page_icon="⭕", layout="centered")
    
    # --- HEADER E LOGO ---
    st.markdown("<h1 style='text-align: center; color: #333;'>GENERA</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: #666;'>Questionario di Valutazione dell'Impatto Personale</h4>", unsafe_allow_html=True)
    st.markdown("---")

    # --- INTRODUZIONE (Obiettivi, Struttura, Metodologia) ---
    with st.expander("ℹ️ Informazioni sul Questionario (Obiettivi e Metodologia)", expanded=False):
        st.markdown("""
        ### Obiettivi
        Il presente strumento è stato ideato per mappare e restituire un'immagine chiara della tua capacità di **generare impatto** nel contesto attuale. L'obiettivo è fornirti consapevolezza sulle tue leve di forza e sulle aree di potenziale sviluppo.

        ### Struttura
        Il modello si fonda su **5 Dimensioni** chiave che rappresentano i pilastri dell'impatto personale (Autonomia, Potere, Coerenza, Impatto Futuro, Flessibilità). Il feedback finale sarà restituito attraverso un **profilo grafico** (un poligono iscritto in un cerchio) e un **profilo narrativo**.

        ### Metodologia
        Il questionario si compone di **15 item** più una breve sezione anagrafica.
        Per ogni affermazione, ti chiediamo di esprimere il tuo grado di accordo su una scala da 1 ("Per nulla") a 5 ("Moltissimo").
        *Non esistono risposte giuste o sbagliate: rispondi con sincerità per ottenere un profilo il più possibile autentico.*
        """)

    st.markdown("---")

    # --- FORM DI INSERIMENTO ---
    with st.form("questionario_form"):
        
        # 1. SEZIONE ANAGRAFICA
        st.subheader("1. Dati Anagrafici")
        
        # Nome/ID
        nome = st.text_input("Nome o Codice Identificativo")
        
        col1, col2 = st.columns(2)
        with col1:
            genere = st.selectbox("Genere", OPT_GENERE)
            eta = st.selectbox("Età", OPT_ETA)
        with col2:
            scolarita = st.selectbox("Scolarità", OPT_SCOLARITA)
            
        st.write("") # Spazio vuoto
        
        # 2. SEZIONE QUESTIONARIO (15 Item)
        st.subheader("2. Valutazione Dimensioni")
        risposte = {}
        
        for index, q in enumerate(DOMANDE):
            # Separatore visivo al cambio di dimensione
            if index > 0 and DOMANDE[index]['dim'] != DOMANDE[index-1]['dim']:
                st.markdown("---")
            
            st.markdown(f"**{index+1}. {q['testo']}**")
            risposte[q['id']] = st.radio(
                label=f"Risposta item {index+1}",
                options=[1, 2, 3, 4, 5],
                format_func=lambda x: f"{x} - {OPZIONI_RISPOSTA[x]}",
                key=q['id'],
                horizontal=True,
                label_visibility="collapsed"
            )
            st.write("") # Spaziatura

        st.markdown("---")
        submitted = st.form_submit_button("CALCOLA IL MIO PROFILO", type="primary")

    # --- RISULTATI ---
    if submitted:
        if not nome:
            st.warning("Per favore inserisci almeno un Nome o Codice identificativo per procedere.")
        else:
            # Calcolo
            totale, punteggi_dim = calcola_punteggi(risposte)
            colore, livello, desc_breve, dettaglio = get_feedback_narrativo(totale)
            
            st.divider()
            
            # Box Risultato Principale
            st.markdown(f"""
            <div style='text-align: center; padding: 20px; background-color: {colore}20; border-radius: 15px; border: 2px solid {colore}; margin-bottom: 20px;'>
                <h2 style='color: {colore}; margin:0; text-transform: uppercase;'>{livello}</h2>
                <h3 style='margin-top: 10px; color: #333;'>Punteggio Totale: {totale} / 75</h3>
            </div>
            """, unsafe_allow_html=True)
            
            col_sx, col_dx = st.columns([1, 1])

            with col_sx:
                st.markdown("#### Profilo Grafico")
                fig = plot_radar_chart(punteggi_dim, colore)
                st.pyplot(fig)

            with col_dx:
                st.markdown("#### Profilo Narrativo")
                st.markdown(f"### {desc_breve}")
                st.info(f"{dettaglio}", icon="💡")
                
                st.markdown("---")
                st.markdown("**Dettaglio per Dimensione:**")
                for nome_dim, p in zip(DIMENSIONI, punteggi_dim):
                    # Calcolo percentuale relativa (max 15 pt per dim)
                    perc = int((p / 15) * 100) 
                    st.caption(f"{nome_dim.replace(chr(10), ' ')}")
                    st.progress(perc, text=f"{p}/15 pt")

            # Reset o fine
            st.balloons()

if __name__ == "__main__":
    main()
