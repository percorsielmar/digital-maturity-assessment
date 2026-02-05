# Audit di Secondo Livello - Domande dettagliate
# Tipi di domanda: text, select, multiselect

LEVEL2_QUESTIONS = [
    # ============ SEZIONE 1: ANAGRAFICA ============
    {
        "id": 1,
        "category": "Anagrafica",
        "subcategory": "Dati Aziendali",
        "code": "1.1",
        "text": "Inserire la ragione sociale dell'impresa",
        "type": "text",
        "required": True,
        "options": None,
        "hint": "Inserire il nome completo dell'azienda come risulta dalla visura camerale"
    },
    {
        "id": 2,
        "category": "Anagrafica",
        "subcategory": "Dati Aziendali",
        "code": "1.2",
        "text": "Selezionare la forma societaria",
        "type": "select",
        "required": True,
        "options": [
            {"value": "srl", "text": "SRL (soc. di capitale)"},
            {"value": "spa", "text": "SPA (soc. di capitale)"},
            {"value": "srls", "text": "SRLs (soc. di capitale)"},
            {"value": "sapa", "text": "Sapa (soc. di capitale)"},
            {"value": "snc", "text": "SNC (soc. di persone)"},
            {"value": "sas", "text": "SAS (soc. di persone)"},
            {"value": "ss", "text": "S.s. (soc. di persone)"},
            {"value": "coop", "text": "Società cooperativa"},
            {"value": "consortile", "text": "Società consortile"},
            {"value": "altro", "text": "Altro"}
        ],
        "hint": "Selezionare la forma giuridica dell'impresa"
    },
    {
        "id": 3,
        "category": "Anagrafica",
        "subcategory": "Dati Aziendali",
        "code": "1.3",
        "text": "Inserire il codice fiscale/P.IVA dell'impresa",
        "type": "text",
        "required": True,
        "options": None,
        "hint": "Inserire il codice fiscale o la partita IVA dell'azienda"
    },
    {
        "id": 4,
        "category": "Anagrafica",
        "subcategory": "Contatti",
        "code": "1.4",
        "text": "Inserire un indirizzo email a cui collegare il questionario",
        "type": "text",
        "required": True,
        "options": None,
        "hint": "Email principale per le comunicazioni relative all'audit"
    },
    {
        "id": 5,
        "category": "Anagrafica",
        "subcategory": "Sede",
        "code": "1.5",
        "text": "Selezionare la provincia in cui si trova la sede dell'impresa",
        "type": "select",
        "required": True,
        "options": [
            {"value": "AG", "text": "Agrigento"}, {"value": "AL", "text": "Alessandria"}, {"value": "AN", "text": "Ancona"},
            {"value": "AO", "text": "Aosta"}, {"value": "AR", "text": "Arezzo"}, {"value": "AP", "text": "Ascoli Piceno"},
            {"value": "AT", "text": "Asti"}, {"value": "AV", "text": "Avellino"}, {"value": "BA", "text": "Bari"},
            {"value": "BT", "text": "Barletta-Andria-Trani"}, {"value": "BL", "text": "Belluno"}, {"value": "BN", "text": "Benevento"},
            {"value": "BG", "text": "Bergamo"}, {"value": "BI", "text": "Biella"}, {"value": "BO", "text": "Bologna"},
            {"value": "BZ", "text": "Bolzano"}, {"value": "BS", "text": "Brescia"}, {"value": "BR", "text": "Brindisi"},
            {"value": "CA", "text": "Cagliari"}, {"value": "CL", "text": "Caltanissetta"}, {"value": "CB", "text": "Campobasso"},
            {"value": "CE", "text": "Caserta"}, {"value": "CT", "text": "Catania"}, {"value": "CZ", "text": "Catanzaro"},
            {"value": "CH", "text": "Chieti"}, {"value": "CO", "text": "Como"}, {"value": "CS", "text": "Cosenza"},
            {"value": "CR", "text": "Cremona"}, {"value": "KR", "text": "Crotone"}, {"value": "CN", "text": "Cuneo"},
            {"value": "EN", "text": "Enna"}, {"value": "FM", "text": "Fermo"}, {"value": "FE", "text": "Ferrara"},
            {"value": "FI", "text": "Firenze"}, {"value": "FG", "text": "Foggia"}, {"value": "FC", "text": "Forlì-Cesena"},
            {"value": "FR", "text": "Frosinone"}, {"value": "GE", "text": "Genova"}, {"value": "GO", "text": "Gorizia"},
            {"value": "GR", "text": "Grosseto"}, {"value": "IM", "text": "Imperia"}, {"value": "IS", "text": "Isernia"},
            {"value": "SP", "text": "La Spezia"}, {"value": "AQ", "text": "L'Aquila"}, {"value": "LT", "text": "Latina"},
            {"value": "LE", "text": "Lecce"}, {"value": "LC", "text": "Lecco"}, {"value": "LI", "text": "Livorno"},
            {"value": "LO", "text": "Lodi"}, {"value": "LU", "text": "Lucca"}, {"value": "MC", "text": "Macerata"},
            {"value": "MN", "text": "Mantova"}, {"value": "MS", "text": "Massa-Carrara"}, {"value": "MT", "text": "Matera"},
            {"value": "ME", "text": "Messina"}, {"value": "MI", "text": "Milano"}, {"value": "MO", "text": "Modena"},
            {"value": "MB", "text": "Monza e della Brianza"}, {"value": "NA", "text": "Napoli"}, {"value": "NO", "text": "Novara"},
            {"value": "NU", "text": "Nuoro"}, {"value": "OR", "text": "Oristano"}, {"value": "PD", "text": "Padova"},
            {"value": "PA", "text": "Palermo"}, {"value": "PR", "text": "Parma"}, {"value": "PV", "text": "Pavia"},
            {"value": "PG", "text": "Perugia"}, {"value": "PU", "text": "Pesaro e Urbino"}, {"value": "PE", "text": "Pescara"},
            {"value": "PC", "text": "Piacenza"}, {"value": "PI", "text": "Pisa"}, {"value": "PT", "text": "Pistoia"},
            {"value": "PN", "text": "Pordenone"}, {"value": "PZ", "text": "Potenza"}, {"value": "PO", "text": "Prato"},
            {"value": "RG", "text": "Ragusa"}, {"value": "RA", "text": "Ravenna"}, {"value": "RC", "text": "Reggio Calabria"},
            {"value": "RE", "text": "Reggio Emilia"}, {"value": "RI", "text": "Rieti"}, {"value": "RN", "text": "Rimini"},
            {"value": "RM", "text": "Roma"}, {"value": "RO", "text": "Rovigo"}, {"value": "SA", "text": "Salerno"},
            {"value": "SS", "text": "Sassari"}, {"value": "SV", "text": "Savona"}, {"value": "SI", "text": "Siena"},
            {"value": "SR", "text": "Siracusa"}, {"value": "SO", "text": "Sondrio"}, {"value": "SU", "text": "Sud Sardegna"},
            {"value": "TA", "text": "Taranto"}, {"value": "TE", "text": "Teramo"}, {"value": "TR", "text": "Terni"},
            {"value": "TO", "text": "Torino"}, {"value": "TP", "text": "Trapani"}, {"value": "TN", "text": "Trento"},
            {"value": "TV", "text": "Treviso"}, {"value": "TS", "text": "Trieste"}, {"value": "UD", "text": "Udine"},
            {"value": "VA", "text": "Varese"}, {"value": "VE", "text": "Venezia"}, {"value": "VB", "text": "Verbano-Cusio-Ossola"},
            {"value": "VC", "text": "Vercelli"}, {"value": "VR", "text": "Verona"}, {"value": "VV", "text": "Vibo Valentia"},
            {"value": "VI", "text": "Vicenza"}, {"value": "VT", "text": "Viterbo"}
        ],
        "hint": "Selezionare la provincia della sede legale o operativa"
    },
    {
        "id": 6,
        "category": "Anagrafica",
        "subcategory": "Contatti",
        "code": "1.6",
        "text": "Inserire il numero di telefono del compilatore o dell'impresa",
        "type": "text",
        "required": True,
        "options": None,
        "hint": "Numero di telefono per eventuali contatti"
    },
    {
        "id": 7,
        "category": "Anagrafica",
        "subcategory": "Compilatore",
        "code": "1.7",
        "text": "Inserire il nome del compilatore",
        "type": "text",
        "required": True,
        "options": None,
        "hint": "Nome della persona che compila il questionario"
    },
    {
        "id": 8,
        "category": "Anagrafica",
        "subcategory": "Compilatore",
        "code": "1.8",
        "text": "Inserire il cognome del compilatore",
        "type": "text",
        "required": True,
        "options": None,
        "hint": "Cognome della persona che compila il questionario"
    },
    {
        "id": 9,
        "category": "Anagrafica",
        "subcategory": "Compilatore",
        "code": "1.9",
        "text": "Inserire il ruolo del compilatore nell'impresa",
        "type": "select",
        "required": True,
        "options": [
            {"value": "imprenditore", "text": "Imprenditore/socio/proprietario"},
            {"value": "ad", "text": "Amministratore delegato/Direttore Generale"},
            {"value": "manager", "text": "Responsabile area/Manager"},
            {"value": "impiegato", "text": "Impiegato"},
            {"value": "altro", "text": "Altro"}
        ],
        "hint": "Ruolo ricoperto all'interno dell'azienda"
    },
    {
        "id": 10,
        "category": "Anagrafica",
        "subcategory": "Sede",
        "code": "1.10",
        "text": "Nel caso in cui l'impresa abbia più sedi/stabilimenti, per quale di questi si sta effettuando la valutazione?",
        "type": "select",
        "required": True,
        "options": [
            {"value": "unica", "text": "L'impresa ha un'unica sede/stabilimento"},
            {"value": "globale", "text": "L'impresa ha più stabilimenti, e la valutazione è fatta a livello globale"},
            {"value": "specifica", "text": "L'impresa ha più stabilimenti e la valutazione viene fatta per la sede per cui è stata immessa la provincia"}
        ],
        "hint": "Indicare se la valutazione riguarda una sede specifica o l'intera azienda"
    },
    {
        "id": 11,
        "category": "Anagrafica",
        "subcategory": "Settore",
        "code": "1.11",
        "text": "In quale dei seguenti settori si colloca prevalentemente l'attività dell'impresa?",
        "type": "select",
        "required": True,
        "options": [
            {"value": "A", "text": "A - Agricoltura, silvicoltura e pesca"},
            {"value": "B", "text": "B - Estrazione di minerali da cave e miniere"},
            {"value": "C", "text": "C - Attività manifatturiere"},
            {"value": "D", "text": "D - Fornitura di energia elettrica, gas, vapore e aria condizionata"},
            {"value": "E", "text": "E - Fornitura di acqua; reti fognarie, attività di gestione dei rifiuti e risanamento"},
            {"value": "F", "text": "F - Costruzioni"},
            {"value": "G", "text": "G - Commercio all'ingrosso e al dettaglio; riparazione di autoveicoli e motocicli"},
            {"value": "H", "text": "H - Trasporto e magazzinaggio"},
            {"value": "I", "text": "I - Attività dei servizi di alloggio e di ristorazione"},
            {"value": "J", "text": "J - Servizi di informazione e comunicazione"},
            {"value": "K", "text": "K - Attività finanziarie e assicurative"},
            {"value": "L", "text": "L - Attività immobiliari"},
            {"value": "M", "text": "M - Attività professionali, scientifiche e tecniche"},
            {"value": "N", "text": "N - Noleggio, agenzie di viaggio, servizi di supporto alle imprese"},
            {"value": "O", "text": "O - Amministrazione pubblica e difesa, assicurazione sociale obbligatoria"},
            {"value": "P", "text": "P - Istruzione"},
            {"value": "Q", "text": "Q - Sanità e assistenza sociale"},
            {"value": "R", "text": "R - Attività artistiche, sportive, di intrattenimento e divertimento"},
            {"value": "S", "text": "S - Altre attività di servizi"}
        ],
        "hint": "Codice ATECO principale dell'attività"
    },
    {
        "id": 12,
        "category": "Anagrafica",
        "subcategory": "Settore",
        "code": "1.12",
        "text": "Più in dettaglio in quale dei seguenti sotto-settori si colloca prevalentemente l'attività dell'impresa?",
        "type": "select",
        "required": False,
        "options": [
            {"value": "agricoltura", "text": "Coltivazioni agricole"},
            {"value": "animali", "text": "Produzione di prodotti animali"},
            {"value": "caccia", "text": "Caccia, cattura di animali e servizi connessi"},
            {"value": "silvicoltura", "text": "Silvicoltura ed utilizzo di aree forestali"},
            {"value": "pesca", "text": "Pesca e acquacoltura"}
        ],
        "hint": "Sotto-settore specifico (se applicabile al settore A)",
        "conditional": {"question_id": 11, "value": "A"}
    },
    {
        "id": 13,
        "category": "Anagrafica",
        "subcategory": "Dimensione",
        "code": "1.13",
        "text": "Indicare il numero di addetti (indipendentemente dalla forma contrattuale)",
        "type": "select",
        "required": True,
        "options": [
            {"value": "0-9", "text": "0-9"},
            {"value": "10-49", "text": "10-49"},
            {"value": "50-249", "text": "50-249"},
            {"value": "250-499", "text": "250-499"},
            {"value": "500+", "text": "Uguale o maggiore di 500"}
        ],
        "hint": "Numero totale di dipendenti e collaboratori"
    },
    {
        "id": 14,
        "category": "Anagrafica",
        "subcategory": "Dimensione",
        "code": "1.14",
        "text": "Indicare il fatturato realizzato dall'azienda nell'ultimo anno",
        "type": "select",
        "required": True,
        "options": [
            {"value": "<500k", "text": "Minore di 500.000 €"},
            {"value": "500k-1m", "text": "Tra 500.000 e 1 Mln€"},
            {"value": "1m-2m", "text": "Tra 1 Mln€ e 2 Mln€"},
            {"value": "2m-5m", "text": "Tra 2 Mln€ e 5 Mln€"},
            {"value": "5m-10m", "text": "Tra 5 Mln€ e 10 Mln€"},
            {"value": "10m-25m", "text": "Tra 10 Mln€ e 25 Mln€"},
            {"value": "25m-50m", "text": "Tra 25 Mln€ e 50 Mln€"},
            {"value": "50m-100m", "text": "Tra 50 Mln€ e 100 Mln€"},
            {"value": ">100m", "text": "Oltre 100 Mln€"}
        ],
        "hint": "Fatturato dell'ultimo esercizio fiscale"
    },
    {
        "id": 15,
        "category": "Anagrafica",
        "subcategory": "Mercato",
        "code": "1.15",
        "text": "Indicare in quale tipo di mercato opera l'impresa",
        "type": "select",
        "required": True,
        "options": [
            {"value": "b2c", "text": "Business to Consumer (la vendita viene effettuata direttamente al cliente finale)"},
            {"value": "b2b", "text": "Business to Business (la vendita viene effettuata verso altre imprese)"}
        ],
        "hint": "Tipologia principale di clientela"
    },
    {
        "id": 16,
        "category": "Anagrafica",
        "subcategory": "Certificazioni",
        "code": "1.16",
        "text": "Indicare quali certificazioni, di sistema o di prodotto, possiede l'impresa",
        "type": "multiselect",
        "required": True,
        "options": [
            {"value": "iso9001", "text": "UNI EN ISO 9001 per i sistemi di gestione della qualità"},
            {"value": "iso14001", "text": "UNI EN ISO 14001 per i sistemi di gestione ambientale"},
            {"value": "ohsas18001", "text": "BS OHSAS 18001 per i sistemi di gestione della sicurezza e della salute nei luoghi di lavoro"},
            {"value": "iso50001", "text": "UNI CEI EN ISO 50001 per i sistemi di gestione dell'energia"},
            {"value": "sa8000", "text": "SA 8000 impatto sull'etica e sul sociale"},
            {"value": "prodotto", "text": "Certificazioni di prodotto (es. Dop/Igp, biologico, ecolabel, ecc.)"},
            {"value": "nessuna", "text": "Nessuna certificazione"},
            {"value": "altro", "text": "Altro"}
        ],
        "hint": "Selezionare tutte le certificazioni possedute"
    },
    {
        "id": 17,
        "category": "Anagrafica",
        "subcategory": "Agevolazioni",
        "code": "1.17",
        "text": "Indicare di quali agevolazioni nazionali per la digitalizzazione ha usufruito l'impresa",
        "type": "multiselect",
        "required": True,
        "options": [
            {"value": "nessuna", "text": "Nessuna"},
            {"value": "industria40", "text": "Credito d'imposta Industria 4.0"},
            {"value": "formazione40", "text": "Credito d'imposta Formazione 4.0"},
            {"value": "innovazione", "text": "Credito d'imposta R&S e Innovazione"},
            {"value": "voucher", "text": "Voucher digitalizzazione"},
            {"value": "altro", "text": "Altro"}
        ],
        "hint": "Agevolazioni fiscali o contributi ricevuti per la digitalizzazione"
    },
    {
        "id": 18,
        "category": "Anagrafica",
        "subcategory": "Presenza Online",
        "code": "1.18",
        "text": "Con quali strumenti è presente on-line l'impresa",
        "type": "select",
        "required": True,
        "options": [
            {"value": "no", "text": "L'impresa per propria scelta strategica non è presente online"},
            {"value": "si", "text": "L'impresa per propria scelta strategica è presente online"}
        ],
        "hint": "Indicare se l'azienda ha una presenza digitale"
    },
    {
        "id": 19,
        "category": "Anagrafica",
        "subcategory": "Presenza Online",
        "code": "1.18a",
        "text": "Selezionare i canali online utilizzati",
        "type": "multiselect",
        "required": False,
        "options": [
            {"value": "sito", "text": "Sito web aziendale"},
            {"value": "ecommerce", "text": "E-commerce proprio"},
            {"value": "marketplace", "text": "Marketplace (Amazon, eBay, ecc.)"},
            {"value": "social", "text": "Social media (Facebook, Instagram, LinkedIn, ecc.)"},
            {"value": "app", "text": "App mobile"},
            {"value": "altro", "text": "Altro"}
        ],
        "hint": "Canali digitali attraverso cui l'azienda è presente online",
        "conditional": {"question_id": 18, "value": "si"}
    },
    {
        "id": 20,
        "category": "Anagrafica",
        "subcategory": "CRM",
        "code": "1.20",
        "text": "Quali strumenti usa l'impresa per la gestione dei contatti e interazione con i clienti/utenti",
        "type": "multiselect",
        "required": True,
        "options": [
            {"value": "nessuno", "text": "Nessuno strumento aziendale"},
            {"value": "crm", "text": "Software CRM"},
            {"value": "email", "text": "Email marketing"},
            {"value": "chat", "text": "Chat/Chatbot"},
            {"value": "call", "text": "Call center"},
            {"value": "social", "text": "Social media"},
            {"value": "altro", "text": "Altro"}
        ],
        "hint": "Strumenti per gestire le relazioni con i clienti"
    },
    {
        "id": 21,
        "category": "Anagrafica",
        "subcategory": "Export",
        "code": "1.21",
        "text": "L'impresa esporta in mercati internazionali?",
        "type": "select",
        "required": True,
        "options": [
            {"value": "si", "text": "SI"},
            {"value": "no", "text": "NO"}
        ],
        "hint": "Indicare se l'azienda opera sui mercati esteri"
    },
    {
        "id": 22,
        "category": "Anagrafica",
        "subcategory": "Export",
        "code": "1.21a",
        "text": "Indicare in quali paesi l'azienda esporta",
        "type": "multiselect",
        "required": False,
        "options": [
            {"value": "europa", "text": "Paesi europei (Francia, Germania, ...)"},
            {"value": "uk", "text": "Regno Unito"},
            {"value": "asia", "text": "Asia (Cina, India, Arabia saudita e/o Emirati Arabi)"},
            {"value": "russia", "text": "Russia"},
            {"value": "nordamerica", "text": "Nord America (U.S.A, Canada, ...)"},
            {"value": "sudamerica", "text": "Centro e Sud America (Messico, Brasile, ...)"},
            {"value": "africa", "text": "Africa"},
            {"value": "altro", "text": "Altro"}
        ],
        "hint": "Mercati di esportazione",
        "conditional": {"question_id": 21, "value": "si"}
    },
    {
        "id": 23,
        "category": "Anagrafica",
        "subcategory": "Export",
        "code": "1.21b",
        "text": "Quale è la dimensione di fatturato che l'azienda realizza sui mercati internazionali (in percentuale sul fatturato totale)?",
        "type": "select",
        "required": False,
        "options": [
            {"value": "<10", "text": "meno del 10%"},
            {"value": "10-39", "text": "dal 10% al 39%"},
            {"value": "40-59", "text": "dal 40% al 59%"},
            {"value": "60+", "text": "uguale o superiore al 60%"}
        ],
        "hint": "Percentuale del fatturato derivante dall'export",
        "conditional": {"question_id": 21, "value": "si"}
    },
    {
        "id": 24,
        "category": "Anagrafica",
        "subcategory": "COVID",
        "code": "1.22",
        "text": "L'impatto del COVID 19 l'ha portata a informarsi o applicare tecnologie di impresa 4.0 o tecnologie digitali?",
        "type": "select",
        "required": True,
        "options": [
            {"value": "si", "text": "SI"},
            {"value": "no", "text": "NO"}
        ],
        "hint": "Impatto della pandemia sulla digitalizzazione aziendale"
    },
    
    # ============ SEZIONE 2: CONTABILITÀ, FINANZA E PROCESSI DECISIONALI ============
    {
        "id": 25,
        "category": "Contabilità e Finanza",
        "subcategory": "Gestione Contabile",
        "code": "2.1",
        "text": "Le attività di contabilità e finanza sono gestite:",
        "type": "select",
        "required": True,
        "options": [
            {"value": "1", "text": "Attraverso consulenti/fornitori esterni (esternalizzate) o non sono realizzate", "score": 1},
            {"value": "2", "text": "Prevalentemente in modo non digitale", "score": 2},
            {"value": "3", "text": "In modo digitale senza integrazione con le altre funzioni aziendali", "score": 3},
            {"value": "4", "text": "In modo digitale, inoltre i dati e le informazioni sono condivisi immediatamente ed automaticamente con gli operatori appartenenti ad altre funzioni", "score": 4},
            {"value": "5", "text": "In modo digitale e le informazioni sono integrate con quelle di altre funzioni aziendali, condivise immediatamente e processate automaticamente per misurare le prestazioni e/o prendere decisioni sulle attività", "score": 5}
        ],
        "hint": "Valutare il livello di digitalizzazione delle attività contabili e finanziarie (fatture, pagamenti, riscossioni, flusso finanziario)"
    },
    {
        "id": 26,
        "category": "Contabilità e Finanza",
        "subcategory": "Processi Decisionali",
        "code": "2.2",
        "text": "Indicare in che modo vengono prese le decisioni all'interno dell'impresa:",
        "type": "select",
        "required": True,
        "options": [
            {"value": "1", "text": "Esclusivamente sulla base dell'esperienza dell'imprenditore / del manager", "score": 1},
            {"value": "2", "text": "In base ad una strategia che parte dalle opportunità che si presentano e dalle azioni dei concorrenti", "score": 2},
            {"value": "3", "text": "In base ad una strategia chiara e definita e supportata da dati oggettivi provenienti dal mercato", "score": 3},
            {"value": "4", "text": "In base ad una strategia chiara e definita e supportata da dati oggettivi provenienti sia dal mercato che dall'interno (altre funzioni aziendali)", "score": 4},
            {"value": "5", "text": "In base ad una strategia proattiva e costantemente rivista e aggiornata basata sull'interazione costante con il mercato e con le funzioni aziendali interne al fine di testare nuovi prodotti e servizi e di far emergere nuove opportunità di business", "score": 5}
        ],
        "hint": "Valutare come vengono prese le decisioni strategiche (nuove strategie, nuovi prodotti/servizi)"
    },
    
    # ============ SEZIONE 3: CLIENTI E MERCATI ============
    {
        "id": 27,
        "category": "Clienti e Mercati",
        "subcategory": "Marketing",
        "code": "3.1",
        "text": "Le attività di raccolta di informazioni dal mercato sono gestite:",
        "type": "select",
        "required": True,
        "options": [
            {"value": "1", "text": "Attraverso consulenti/fornitori esterni (esternalizzate) o non sono realizzate", "score": 1},
            {"value": "2", "text": "Prevalentemente in modo non digitale", "score": 2},
            {"value": "3", "text": "In modo digitale senza integrazione con le altre funzioni aziendali", "score": 3},
            {"value": "4", "text": "In modo digitale, inoltre i dati e le informazioni sono condivisi immediatamente ed automaticamente con gli operatori appartenenti ad altre funzioni", "score": 4},
            {"value": "5", "text": "In modo digitale e le informazioni sono integrate con quelle di altre funzioni aziendali, condivise immediatamente e processate automaticamente per misurare le prestazioni e/o prendere decisioni sulle attività", "score": 5}
        ],
        "hint": "Valutare come vengono raccolte e gestite le informazioni sulle esigenze dei clienti e la loro soddisfazione"
    },
    {
        "id": 28,
        "category": "Clienti e Mercati",
        "subcategory": "Vendite",
        "code": "3.2",
        "text": "Le attività di vendita sono gestite:",
        "type": "select",
        "required": True,
        "options": [
            {"value": "1", "text": "Attraverso consulenti/fornitori esterni (esternalizzate) o non sono realizzate", "score": 1},
            {"value": "2", "text": "Prevalentemente in modo non digitale", "score": 2},
            {"value": "3", "text": "In modo digitale senza integrazione con le altre funzioni aziendali", "score": 3},
            {"value": "4", "text": "In modo digitale, inoltre i dati e le informazioni sono condivisi immediatamente ed automaticamente con gli operatori appartenenti ad altre funzioni", "score": 4},
            {"value": "5", "text": "In modo digitale e le informazioni sono integrate con quelle di altre funzioni aziendali, condivise immediatamente e processate automaticamente per misurare le prestazioni e/o prendere decisioni sulle attività", "score": 5}
        ],
        "hint": "Valutare la gestione degli aspetti commerciali (agenti, preventivi, ordini, contratti, fatturazione)"
    },
    {
        "id": 29,
        "category": "Clienti e Mercati",
        "subcategory": "Post Vendita",
        "code": "3.3",
        "text": "Le attività di assistenza al cliente e i servizi post vendita sono gestite:",
        "type": "select",
        "required": True,
        "options": [
            {"value": "1", "text": "Attraverso consulenti/fornitori esterni (esternalizzate) o non sono realizzate", "score": 1},
            {"value": "2", "text": "Prevalentemente in modo non digitale", "score": 2},
            {"value": "3", "text": "In modo digitale senza integrazione con le altre funzioni aziendali", "score": 3},
            {"value": "4", "text": "In modo digitale, inoltre i dati e le informazioni sono condivisi immediatamente ed automaticamente con gli operatori appartenenti ad altre funzioni", "score": 4},
            {"value": "5", "text": "In modo digitale e le informazioni sono integrate con quelle di altre funzioni aziendali, condivise immediatamente e processate automaticamente per misurare le prestazioni e/o prendere decisioni sulle attività", "score": 5}
        ],
        "hint": "Valutare la gestione dell'assistenza tecnica e dei servizi post vendita"
    },
    
    # ============ SEZIONE 4: TECNOLOGIE ============
    {
        "id": 30,
        "category": "Tecnologie",
        "subcategory": "Sistemi Informativi",
        "code": "4.1",
        "text": "Le attività relative alla gestione delle informazioni attraverso i sistemi informativi sono realizzate:",
        "type": "select",
        "required": True,
        "options": [
            {"value": "1", "text": "Attraverso consulenti/fornitori esterni (esternalizzate) o non sono realizzate", "score": 1},
            {"value": "2", "text": "Prevalentemente in modo non digitale", "score": 2},
            {"value": "3", "text": "In modo digitale senza integrazione con le altre funzioni aziendali", "score": 3},
            {"value": "4", "text": "In modo digitale, inoltre i dati e le informazioni sono condivisi immediatamente ed automaticamente con gli operatori appartenenti ad altre funzioni", "score": 4},
            {"value": "5", "text": "In modo digitale e le informazioni sono integrate con quelle di altre funzioni aziendali, condivise immediatamente e processate automaticamente per misurare le prestazioni e/o prendere decisioni sulle attività", "score": 5}
        ],
        "hint": "Valutare il funzionamento e la gestione del sistema informativo aziendale e delle infrastrutture di comunicazione"
    },
    {
        "id": 31,
        "category": "Tecnologie",
        "subcategory": "R&D",
        "code": "4.2",
        "text": "Le attività di progettazione, ricerca e sviluppo sono gestite:",
        "type": "select",
        "required": True,
        "options": [
            {"value": "1", "text": "Attraverso consulenti/fornitori esterni (esternalizzate) o non sono realizzate", "score": 1},
            {"value": "2", "text": "Prevalentemente in modo non digitale", "score": 2},
            {"value": "3", "text": "In modo digitale senza integrazione con le altre funzioni aziendali", "score": 3},
            {"value": "4", "text": "In modo digitale, inoltre i dati e le informazioni sono condivisi immediatamente ed automaticamente con gli operatori appartenenti ad altre funzioni", "score": 4},
            {"value": "5", "text": "In modo digitale e le informazioni sono integrate con quelle di altre funzioni aziendali, condivise immediatamente e processate automaticamente per misurare le prestazioni e/o prendere decisioni sulle attività", "score": 5}
        ],
        "hint": "Valutare le attività progettuali per il miglioramento di prodotti/servizi e processi"
    },
    {
        "id": 32,
        "category": "Tecnologie",
        "subcategory": "Proprietà Intellettuale",
        "code": "4.3",
        "text": "Indicare se l'impresa possiede qualcuno tra i seguenti strumenti di protezione della proprietà intellettuale",
        "type": "multiselect",
        "required": True,
        "options": [
            {"value": "brevetti", "text": "Brevetti"},
            {"value": "modelli", "text": "Modelli di utilità"},
            {"value": "disegni", "text": "Disegni ornamentali"},
            {"value": "marchi", "text": "Marchi"},
            {"value": "nessuno", "text": "Nessuno dei precedenti"}
        ],
        "hint": "Strumenti di tutela della proprietà intellettuale posseduti"
    },
    {
        "id": 33,
        "category": "Tecnologie",
        "subcategory": "Tecnologie Abilitanti",
        "code": "4.4",
        "text": "Indicare quali delle seguenti tecnologie sono presenti all'interno dell'impresa, o si intende acquistare in futuro",
        "type": "multiselect",
        "required": True,
        "options": [
            {"value": "cloud", "text": "Cloud Computing"},
            {"value": "bigdata", "text": "Big Data e Analytics"},
            {"value": "ai", "text": "Intelligenza Artificiale / Machine Learning"},
            {"value": "iot", "text": "Internet of Things (IoT)"},
            {"value": "robotica", "text": "Robotica avanzata"},
            {"value": "stampa3d", "text": "Stampa 3D / Additive Manufacturing"},
            {"value": "ar_vr", "text": "Realtà Aumentata / Realtà Virtuale"},
            {"value": "blockchain", "text": "Blockchain"},
            {"value": "cybersecurity", "text": "Cybersecurity avanzata"},
            {"value": "erp", "text": "ERP / Sistemi gestionali integrati"},
            {"value": "mes", "text": "MES (Manufacturing Execution System)"},
            {"value": "plm", "text": "PLM (Product Lifecycle Management)"},
            {"value": "nessuna", "text": "Nessuna delle precedenti"}
        ],
        "hint": "Tecnologie digitali e abilitanti presenti o pianificate"
    }
]

# Categorie per il report
LEVEL2_CATEGORIES = [
    "Anagrafica",
    "Contabilità e Finanza", 
    "Clienti e Mercati",
    "Tecnologie"
]
