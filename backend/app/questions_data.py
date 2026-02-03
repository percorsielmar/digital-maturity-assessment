DIGITAL_MATURITY_QUESTIONS = [
    # STRATEGIA DIGITALE
    {
        "category": "Strategia Digitale",
        "subcategory": "Visione e Leadership",
        "text": "L'organizzazione ha definito una strategia digitale chiara e documentata?",
        "options": [
            {"text": "Non esiste una strategia digitale", "score": 1},
            {"text": "Esistono iniziative sporadiche non coordinate", "score": 2},
            {"text": "Esiste una strategia parziale per alcuni settori", "score": 3},
            {"text": "Esiste una strategia digitale completa e condivisa", "score": 4},
            {"text": "La strategia digitale è integrata nella strategia aziendale e rivista periodicamente", "score": 5}
        ],
        "weight": 1.5,
        "order": 1,
        "target_type": "both"
    },
    {
        "category": "Strategia Digitale",
        "subcategory": "Visione e Leadership",
        "text": "Il top management è attivamente coinvolto nelle iniziative di trasformazione digitale?",
        "options": [
            {"text": "Il management non è coinvolto", "score": 1},
            {"text": "Coinvolgimento occasionale e passivo", "score": 2},
            {"text": "Supporto formale ma limitato coinvolgimento operativo", "score": 3},
            {"text": "Coinvolgimento attivo con sponsorship di progetti", "score": 4},
            {"text": "Leadership digitale proattiva con visione chiara", "score": 5}
        ],
        "weight": 1.3,
        "order": 2,
        "target_type": "both"
    },
    {
        "category": "Strategia Digitale",
        "subcategory": "Budget e Investimenti",
        "text": "Qual è il livello di investimento in tecnologie digitali?",
        "options": [
            {"text": "Investimenti minimi o assenti", "score": 1},
            {"text": "Investimenti occasionali per necessità urgenti", "score": 2},
            {"text": "Budget annuale definito ma limitato", "score": 3},
            {"text": "Budget significativo con pianificazione pluriennale", "score": 4},
            {"text": "Investimenti strategici con ROI monitorato", "score": 5}
        ],
        "weight": 1.2,
        "order": 3,
        "target_type": "both"
    },
    # INFRASTRUTTURA E TECNOLOGIA
    {
        "category": "Infrastruttura e Tecnologia",
        "subcategory": "Cloud e Infrastruttura",
        "text": "Qual è il livello di adozione di soluzioni cloud?",
        "options": [
            {"text": "Nessuna adozione cloud, tutto on-premise", "score": 1},
            {"text": "Uso limitato di servizi cloud (es. email)", "score": 2},
            {"text": "Adozione parziale con approccio ibrido", "score": 3},
            {"text": "Strategia cloud-first per nuovi progetti", "score": 4},
            {"text": "Infrastruttura completamente cloud-native", "score": 5}
        ],
        "weight": 1.2,
        "order": 4,
        "target_type": "both"
    },
    {
        "category": "Infrastruttura e Tecnologia",
        "subcategory": "Sistemi e Integrazione",
        "text": "I sistemi informativi sono integrati tra loro?",
        "options": [
            {"text": "Sistemi isolati senza integrazione", "score": 1},
            {"text": "Integrazione manuale tramite export/import", "score": 2},
            {"text": "Alcune integrazioni punto-punto", "score": 3},
            {"text": "Piattaforma di integrazione con API", "score": 4},
            {"text": "Architettura completamente integrata e interoperabile", "score": 5}
        ],
        "weight": 1.3,
        "order": 5,
        "target_type": "both"
    },
    {
        "category": "Infrastruttura e Tecnologia",
        "subcategory": "Cybersecurity",
        "text": "Qual è il livello di maturità della sicurezza informatica?",
        "options": [
            {"text": "Misure di sicurezza basilari o assenti", "score": 1},
            {"text": "Antivirus e firewall base", "score": 2},
            {"text": "Policy di sicurezza definite, backup regolari", "score": 3},
            {"text": "Framework di sicurezza completo, formazione periodica", "score": 4},
            {"text": "SOC, penetration test regolari, certificazioni (ISO 27001)", "score": 5}
        ],
        "weight": 1.5,
        "order": 6,
        "target_type": "both"
    },
    # PROCESSI E OPERAZIONI
    {
        "category": "Processi e Operazioni",
        "subcategory": "Automazione",
        "text": "Qual è il livello di automazione dei processi interni?",
        "options": [
            {"text": "Processi completamente manuali", "score": 1},
            {"text": "Uso di fogli di calcolo per gestione dati", "score": 2},
            {"text": "Alcuni processi digitalizzati con software dedicati", "score": 3},
            {"text": "Workflow automatizzati per processi chiave", "score": 4},
            {"text": "RPA e automazione intelligente diffusa", "score": 5}
        ],
        "weight": 1.2,
        "order": 7,
        "target_type": "both"
    },
    {
        "category": "Processi e Operazioni",
        "subcategory": "Documentale",
        "text": "Come viene gestita la documentazione?",
        "options": [
            {"text": "Prevalentemente cartacea", "score": 1},
            {"text": "Documenti digitali su file system locale", "score": 2},
            {"text": "Sistema documentale centralizzato", "score": 3},
            {"text": "DMS con workflow e versioning", "score": 4},
            {"text": "Gestione documentale intelligente con AI", "score": 5}
        ],
        "weight": 1.0,
        "order": 8,
        "target_type": "both"
    },
    {
        "category": "Processi e Operazioni",
        "subcategory": "Collaborazione",
        "text": "Quali strumenti di collaborazione digitale vengono utilizzati?",
        "options": [
            {"text": "Solo email tradizionale", "score": 1},
            {"text": "Email e condivisione file base", "score": 2},
            {"text": "Suite di collaborazione (Teams, Slack)", "score": 3},
            {"text": "Piattaforma integrata con videoconferenza e co-editing", "score": 4},
            {"text": "Digital workplace completo con intranet moderna", "score": 5}
        ],
        "weight": 1.0,
        "order": 9,
        "target_type": "both"
    },
    # DATI E ANALYTICS
    {
        "category": "Dati e Analytics",
        "subcategory": "Gestione Dati",
        "text": "Come vengono gestiti e governati i dati aziendali?",
        "options": [
            {"text": "Dati sparsi senza governance", "score": 1},
            {"text": "Dati in silos dipartimentali", "score": 2},
            {"text": "Database centralizzato per dati principali", "score": 3},
            {"text": "Data governance con owner e policy definite", "score": 4},
            {"text": "Data platform con catalogo, lineage e qualità", "score": 5}
        ],
        "weight": 1.3,
        "order": 10,
        "target_type": "both"
    },
    {
        "category": "Dati e Analytics",
        "subcategory": "Business Intelligence",
        "text": "Qual è il livello di utilizzo di analytics e reporting?",
        "options": [
            {"text": "Report manuali occasionali", "score": 1},
            {"text": "Report statici periodici", "score": 2},
            {"text": "Dashboard interattive per alcuni reparti", "score": 3},
            {"text": "BI self-service diffusa nell'organizzazione", "score": 4},
            {"text": "Advanced analytics con ML e AI predittiva", "score": 5}
        ],
        "weight": 1.2,
        "order": 11,
        "target_type": "both"
    },
    {
        "category": "Dati e Analytics",
        "subcategory": "Data-Driven",
        "text": "Le decisioni aziendali sono basate sui dati?",
        "options": [
            {"text": "Decisioni basate su intuizione ed esperienza", "score": 1},
            {"text": "Dati consultati occasionalmente", "score": 2},
            {"text": "KPI definiti per alcune aree", "score": 3},
            {"text": "Cultura data-driven con KPI diffusi", "score": 4},
            {"text": "Decisioni automatizzate basate su algoritmi", "score": 5}
        ],
        "weight": 1.2,
        "order": 12,
        "target_type": "both"
    },
    # COMPETENZE E CULTURA
    {
        "category": "Competenze e Cultura",
        "subcategory": "Competenze Digitali",
        "text": "Qual è il livello medio di competenze digitali del personale?",
        "options": [
            {"text": "Competenze digitali basilari o carenti", "score": 1},
            {"text": "Uso base di strumenti office", "score": 2},
            {"text": "Buona padronanza degli strumenti aziendali", "score": 3},
            {"text": "Competenze avanzate con specialisti interni", "score": 4},
            {"text": "Eccellenza digitale con continuous learning", "score": 5}
        ],
        "weight": 1.3,
        "order": 13,
        "target_type": "both"
    },
    {
        "category": "Competenze e Cultura",
        "subcategory": "Formazione",
        "text": "Esistono programmi di formazione digitale strutturati?",
        "options": [
            {"text": "Nessuna formazione digitale", "score": 1},
            {"text": "Formazione occasionale su richiesta", "score": 2},
            {"text": "Piano formativo annuale base", "score": 3},
            {"text": "Academy interna con percorsi strutturati", "score": 4},
            {"text": "Learning platform con contenuti personalizzati", "score": 5}
        ],
        "weight": 1.1,
        "order": 14,
        "target_type": "both"
    },
    {
        "category": "Competenze e Cultura",
        "subcategory": "Change Management",
        "text": "Come viene gestito il cambiamento organizzativo legato al digitale?",
        "options": [
            {"text": "Resistenza al cambiamento diffusa", "score": 1},
            {"text": "Cambiamento imposto senza accompagnamento", "score": 2},
            {"text": "Comunicazione e formazione per nuovi strumenti", "score": 3},
            {"text": "Programmi di change management strutturati", "score": 4},
            {"text": "Cultura dell'innovazione e miglioramento continuo", "score": 5}
        ],
        "weight": 1.2,
        "order": 15,
        "target_type": "both"
    },
    # CUSTOMER/CITIZEN EXPERIENCE
    {
        "category": "Customer Experience",
        "subcategory": "Canali Digitali",
        "text": "Quali canali digitali sono disponibili per clienti/cittadini?",
        "options": [
            {"text": "Solo contatto telefonico o di persona", "score": 1},
            {"text": "Sito web informativo base", "score": 2},
            {"text": "Portale con servizi online base", "score": 3},
            {"text": "Multicanalità (web, app, chat)", "score": 4},
            {"text": "Omnicanalità integrata con personalizzazione", "score": 5}
        ],
        "weight": 1.3,
        "order": 16,
        "target_type": "both"
    },
    {
        "category": "Customer Experience",
        "subcategory": "Servizi Online",
        "text": "Qual è il livello di digitalizzazione dei servizi offerti?",
        "options": [
            {"text": "Servizi solo in presenza", "score": 1},
            {"text": "Moduli scaricabili online", "score": 2},
            {"text": "Alcuni servizi completabili online", "score": 3},
            {"text": "Maggioranza dei servizi digitali end-to-end", "score": 4},
            {"text": "Servizi digitali proattivi e personalizzati", "score": 5}
        ],
        "weight": 1.4,
        "order": 17,
        "target_type": "both"
    },
    {
        "category": "Customer Experience",
        "subcategory": "Feedback",
        "text": "Come viene raccolto e gestito il feedback digitale?",
        "options": [
            {"text": "Nessuna raccolta sistematica di feedback", "score": 1},
            {"text": "Raccolta occasionale tramite survey", "score": 2},
            {"text": "Sistema di feedback su canali digitali", "score": 3},
            {"text": "Analisi sistematica con azioni di miglioramento", "score": 4},
            {"text": "Voice of customer integrata con AI e sentiment analysis", "score": 5}
        ],
        "weight": 1.0,
        "order": 18,
        "target_type": "both"
    },
    # INNOVAZIONE
    {
        "category": "Innovazione",
        "subcategory": "Tecnologie Emergenti",
        "text": "Qual è il livello di sperimentazione con tecnologie emergenti (AI, IoT, Blockchain)?",
        "options": [
            {"text": "Nessuna sperimentazione", "score": 1},
            {"text": "Consapevolezza ma nessuna azione", "score": 2},
            {"text": "Progetti pilota isolati", "score": 3},
            {"text": "Programma di innovazione strutturato", "score": 4},
            {"text": "Tecnologie emergenti in produzione con risultati misurabili", "score": 5}
        ],
        "weight": 1.0,
        "order": 19,
        "target_type": "both"
    },
    {
        "category": "Innovazione",
        "subcategory": "Ecosistema",
        "text": "L'organizzazione collabora con startup, università o partner tecnologici?",
        "options": [
            {"text": "Nessuna collaborazione esterna", "score": 1},
            {"text": "Collaborazioni occasionali con fornitori", "score": 2},
            {"text": "Partnership con alcuni provider tecnologici", "score": 3},
            {"text": "Ecosistema di partner per innovazione", "score": 4},
            {"text": "Open innovation con incubatori e venture", "score": 5}
        ],
        "weight": 0.9,
        "order": 20,
        "target_type": "both"
    }
]
