GOVERNANCE_QUESTIONS = [
    # ============ SEZIONE 1: TRASPARENZA AMMINISTRATIVA ============
    {
        "category": "Trasparenza Amministrativa",
        "subcategory": "Accesso agli atti",
        "text": "L'ente garantisce l'accesso civico generalizzato (FOIA) e la pubblicazione proattiva delle informazioni?",
        "hint": "Il D.Lgs. 33/2013 e il FOIA (Freedom of Information Act italiano, D.Lgs. 97/2016) prevedono l'obbligo di pubblicazione di dati, informazioni e documenti. L'accesso civico generalizzato consente a chiunque di richiedere dati e documenti detenuti dalla PA, anche senza motivazione. La pubblicazione proattiva va oltre l'obbligo minimo, rendendo disponibili informazioni utili ai cittadini.",
        "options": [
            {"text": "L'ente pubblica solo il minimo obbligatorio, con ritardi e lacune", "score": 1},
            {"text": "Pubblicazione degli obblighi di legge con alcune carenze", "score": 2},
            {"text": "Pubblicazione regolare degli obblighi con sezione Amministrazione Trasparente aggiornata", "score": 3},
            {"text": "Pubblicazione proattiva oltre gli obblighi, con dati aperti e facilmente accessibili", "score": 4},
            {"text": "Trasparenza totale con open data, API pubbliche, dashboard interattive e pubblicazione in tempo reale", "score": 5}
        ],
        "weight": 1.5,
        "order": 1,
        "target_type": "pa"
    },
    {
        "category": "Trasparenza Amministrativa",
        "subcategory": "Pubblicazione dati",
        "text": "L'ente pubblica i dati relativi a bilanci, spese, contratti e incarichi in formato aperto e riutilizzabile?",
        "hint": "Open data: dati pubblicati in formati aperti (CSV, JSON, XML) con licenze che ne consentono il riutilizzo. Include: bilancio di previsione e consuntivo, indicatori di tempestività dei pagamenti, elenco contratti pubblici, incarichi e consulenze, patrimonio immobiliare. Il CAD (Codice dell'Amministrazione Digitale) promuove il principio 'open by default'.",
        "options": [
            {"text": "I dati non sono pubblicati o sono disponibili solo in formato PDF non strutturato", "score": 1},
            {"text": "Pubblicazione parziale in formati non sempre riutilizzabili", "score": 2},
            {"text": "Pubblicazione regolare dei principali dataset in formato aperto", "score": 3},
            {"text": "Open data completi con catalogo strutturato e aggiornamento periodico", "score": 4},
            {"text": "Piattaforma open data con API, aggiornamento automatico, linked data e visualizzazioni interattive", "score": 5}
        ],
        "weight": 1.4,
        "order": 2,
        "target_type": "pa"
    },
    {
        "category": "Trasparenza Amministrativa",
        "subcategory": "Anticorruzione",
        "text": "L'ente ha adottato e attua efficacemente il Piano Triennale per la Prevenzione della Corruzione e della Trasparenza (PTPCT)?",
        "hint": "Il PTPCT (ora integrato nel PIAO — Piano Integrato di Attività e Organizzazione) è obbligatorio per tutte le PA. Include: mappatura dei rischi corruttivi, misure di prevenzione, responsabile della prevenzione (RPCT), formazione del personale, whistleblowing, rotazione degli incarichi, conflitto di interessi.",
        "options": [
            {"text": "Il PTPCT è formale e non effettivamente attuato", "score": 1},
            {"text": "Attuazione parziale con alcune misure implementate", "score": 2},
            {"text": "Attuazione regolare delle principali misure con monitoraggio annuale", "score": 3},
            {"text": "Attuazione completa con monitoraggio periodico, formazione e whistleblowing attivo", "score": 4},
            {"text": "Sistema integrato anticorruzione con cultura dell'integrità diffusa, monitoraggio continuo e miglioramento proattivo", "score": 5}
        ],
        "weight": 1.4,
        "order": 3,
        "target_type": "pa"
    },

    # ============ SEZIONE 2: TRACCIABILITÀ DELLE DECISIONI ============
    {
        "category": "Tracciabilità delle Decisioni",
        "subcategory": "Processi decisionali",
        "text": "I processi decisionali dell'ente sono documentati, tracciabili e accessibili ai cittadini?",
        "hint": "Tracciabilità: ogni decisione deve avere un percorso documentato dall'istruttoria alla deliberazione finale. Include: verbali delle riunioni, motivazioni delle decisioni, pareri tecnici, iter procedimentale. Strumenti: protocollo informatico, gestione documentale, albo pretorio online, registro delle delibere.",
        "options": [
            {"text": "I processi decisionali non sono documentati in modo sistematico", "score": 1},
            {"text": "Documentazione parziale, principalmente per gli atti formali obbligatori", "score": 2},
            {"text": "Documentazione completa degli atti con pubblicazione sull'albo pretorio", "score": 3},
            {"text": "Tracciabilità completa con iter documentato, motivazioni esplicite e accesso digitale", "score": 4},
            {"text": "Piena tracciabilità con registro digitale delle decisioni, timeline pubblica, motivazioni dettagliate e possibilità di feedback", "score": 5}
        ],
        "weight": 1.5,
        "order": 4,
        "target_type": "pa"
    },
    {
        "category": "Tracciabilità delle Decisioni",
        "subcategory": "Protocollo e gestione documentale",
        "text": "L'ente utilizza un sistema di protocollo informatico e gestione documentale conforme alle normative?",
        "hint": "Il protocollo informatico (DPR 445/2000, CAD) è obbligatorio per tutte le PA. La gestione documentale include: classificazione, fascicolazione, conservazione digitale a norma, firma digitale, PEC. Sistemi avanzati: workflow documentali, integrazione con i servizi online, interoperabilità tra enti.",
        "options": [
            {"text": "Protocollo ancora prevalentemente cartaceo o sistema informatico obsoleto", "score": 1},
            {"text": "Protocollo informatico di base senza gestione documentale integrata", "score": 2},
            {"text": "Protocollo informatico con gestione documentale e conservazione digitale", "score": 3},
            {"text": "Sistema integrato con workflow, firma digitale, PEC e fascicolazione automatica", "score": 4},
            {"text": "Piattaforma documentale avanzata con AI per classificazione, interoperabilità tra enti e accesso cittadino", "score": 5}
        ],
        "weight": 1.3,
        "order": 5,
        "target_type": "pa"
    },
    {
        "category": "Tracciabilità delle Decisioni",
        "subcategory": "Registri trasparenti",
        "text": "L'ente utilizza registri digitali trasparenti per la tracciabilità di procedimenti, appalti e concessioni?",
        "hint": "Registri trasparenti: albo pretorio online, registro dei contratti, registro degli accessi civici, registro dei conflitti di interesse, registro dei lobbisti. Tecnologie avanzate: blockchain per la certificazione temporale, timestamping, audit trail automatici, log immutabili.",
        "options": [
            {"text": "Non esistono registri digitali trasparenti oltre gli obblighi minimi", "score": 1},
            {"text": "Albo pretorio online e registro contratti di base", "score": 2},
            {"text": "Registri digitali per i principali procedimenti con accesso pubblico", "score": 3},
            {"text": "Sistema completo di registri digitali con ricerca avanzata e audit trail", "score": 4},
            {"text": "Registri digitali avanzati con certificazione temporale, immutabilità, API pubbliche e interoperabilità", "score": 5}
        ],
        "weight": 1.2,
        "order": 6,
        "target_type": "pa"
    },

    # ============ SEZIONE 3: PARTECIPAZIONE DEI CITTADINI ============
    {
        "category": "Partecipazione dei Cittadini",
        "subcategory": "Strumenti di partecipazione",
        "text": "L'ente mette a disposizione strumenti digitali per la partecipazione attiva dei cittadini ai processi decisionali?",
        "hint": "Strumenti di partecipazione: consultazioni pubbliche online, bilancio partecipativo, sondaggi e questionari, piattaforme di e-democracy, forum tematici, assemblee digitali. La partecipazione può essere: informativa (l'ente informa), consultiva (l'ente chiede opinioni), deliberativa (i cittadini co-decidono).",
        "options": [
            {"text": "Non esistono strumenti digitali per la partecipazione dei cittadini", "score": 1},
            {"text": "Presenza sui social media con interazione limitata", "score": 2},
            {"text": "Alcuni strumenti di consultazione online (sondaggi, moduli di feedback)", "score": 3},
            {"text": "Piattaforma di partecipazione con consultazioni, proposte e bilancio partecipativo", "score": 4},
            {"text": "Ecosistema di e-democracy con deliberazione partecipata, co-progettazione, monitoraggio civico e feedback loop", "score": 5}
        ],
        "weight": 1.5,
        "order": 7,
        "target_type": "pa"
    },
    {
        "category": "Partecipazione dei Cittadini",
        "subcategory": "Consultazioni pubbliche",
        "text": "L'ente conduce consultazioni pubbliche strutturate prima di decisioni rilevanti?",
        "hint": "Consultazioni pubbliche: processo formale in cui l'ente raccoglie opinioni, proposte e osservazioni dei cittadini prima di adottare atti di rilevanza generale. Include: avviso pubblico, periodo di consultazione, raccolta contributi, analisi e risposta ai contributi, pubblicazione degli esiti. Esempi: piani urbanistici, regolamenti, bilancio.",
        "options": [
            {"text": "Non vengono condotte consultazioni pubbliche", "score": 1},
            {"text": "Consultazioni solo quando obbligatorie per legge, con partecipazione minima", "score": 2},
            {"text": "Consultazioni periodiche su temi rilevanti con pubblicazione degli esiti", "score": 3},
            {"text": "Processo strutturato di consultazione con piattaforma dedicata e analisi dei contributi", "score": 4},
            {"text": "Consultazioni sistematiche con deliberazione partecipata, risposta ai contributi e integrazione nei processi decisionali", "score": 5}
        ],
        "weight": 1.3,
        "order": 8,
        "target_type": "pa"
    },
    {
        "category": "Partecipazione dei Cittadini",
        "subcategory": "Monitoraggio civico",
        "text": "L'ente promuove il monitoraggio civico dei progetti e delle politiche pubbliche da parte dei cittadini?",
        "hint": "Monitoraggio civico: i cittadini verificano l'attuazione di progetti e politiche pubbliche. Include: accesso ai dati di avanzamento dei progetti, piattaforme di segnalazione, report di monitoraggio partecipato, community di monitoraggio. Esempi: Monithon (monitoraggio fondi UE), OpenCoesione, FixMyStreet.",
        "options": [
            {"text": "Non esiste alcuna forma di monitoraggio civico", "score": 1},
            {"text": "I cittadini possono fare segnalazioni ma senza un processo strutturato", "score": 2},
            {"text": "Piattaforma di segnalazione con risposta dell'ente", "score": 3},
            {"text": "Programma di monitoraggio civico con dati aperti e community attiva", "score": 4},
            {"text": "Ecosistema di monitoraggio civico con dati in tempo reale, dashboard pubbliche, community e co-valutazione", "score": 5}
        ],
        "weight": 1.2,
        "order": 9,
        "target_type": "pa"
    },

    # ============ SEZIONE 4: STRUMENTI DIGITALI PER LA GOVERNANCE ============
    {
        "category": "Strumenti Digitali per la Governance",
        "subcategory": "Piattaforme digitali",
        "text": "L'ente utilizza piattaforme digitali dedicate per la governance e la trasparenza?",
        "hint": "Piattaforme per la governance: portale istituzionale conforme alle Linee Guida AgID, sezione Amministrazione Trasparente, portale open data, piattaforma di partecipazione, app per i servizi al cittadino. Conformità: Linee Guida di design per i siti web della PA, accessibilità (WCAG 2.1), usabilità.",
        "options": [
            {"text": "Sito web istituzionale obsoleto e non conforme alle linee guida", "score": 1},
            {"text": "Sito web aggiornato ma con funzionalità limitate di trasparenza", "score": 2},
            {"text": "Portale conforme con Amministrazione Trasparente e servizi online di base", "score": 3},
            {"text": "Piattaforma integrata con open data, partecipazione e servizi digitali avanzati", "score": 4},
            {"text": "Ecosistema digitale completo con portale, app, open data, partecipazione, AI e personalizzazione dei servizi", "score": 5}
        ],
        "weight": 1.3,
        "order": 10,
        "target_type": "pa"
    },
    {
        "category": "Strumenti Digitali per la Governance",
        "subcategory": "Strumenti collaborativi",
        "text": "L'ente utilizza strumenti collaborativi digitali per il lavoro interno e la co-progettazione con i cittadini?",
        "hint": "Strumenti collaborativi interni: suite di produttività (Microsoft 365, Google Workspace), piattaforme di project management, videoconferenza, intranet. Per la co-progettazione: piattaforme di crowdsourcing, wiki collaborative, mappe partecipate, laboratori digitali.",
        "options": [
            {"text": "Non vengono utilizzati strumenti collaborativi digitali", "score": 1},
            {"text": "Utilizzo di email e strumenti base senza collaborazione strutturata", "score": 2},
            {"text": "Suite di collaborazione interna con alcuni strumenti di co-progettazione", "score": 3},
            {"text": "Piattaforma collaborativa completa per il lavoro interno e la co-progettazione con stakeholder", "score": 4},
            {"text": "Ecosistema collaborativo avanzato con digital workplace, co-design, laboratori virtuali e community management", "score": 5}
        ],
        "weight": 1.1,
        "order": 11,
        "target_type": "pa"
    },
    {
        "category": "Strumenti Digitali per la Governance",
        "subcategory": "Identità digitale e servizi online",
        "text": "L'ente offre servizi online accessibili tramite identità digitale (SPID, CIE) e piattaforme nazionali?",
        "hint": "Servizi online: istanze, pagamenti (pagoPA), certificati, prenotazioni, segnalazioni. Identità digitale: SPID, CIE (Carta d'Identità Elettronica). Piattaforme nazionali: pagoPA, IO (app dei servizi pubblici), ANPR, PDND (Piattaforma Digitale Nazionale Dati). Il PNRR prevede la migrazione dei servizi su piattaforme digitali.",
        "options": [
            {"text": "Nessun servizio online o solo informazioni statiche sul sito", "score": 1},
            {"text": "Alcuni servizi online con modulistica scaricabile", "score": 2},
            {"text": "Servizi online con SPID/CIE e integrazione pagoPA", "score": 3},
            {"text": "Ampia gamma di servizi digitali integrati con piattaforme nazionali (IO, pagoPA, ANPR)", "score": 4},
            {"text": "Servizi completamente digitali, proattivi, personalizzati e integrati con PDND e interoperabilità tra enti", "score": 5}
        ],
        "weight": 1.3,
        "order": 12,
        "target_type": "pa"
    },

    # ============ SEZIONE 5: COMPETENZE E FORMAZIONE ============
    {
        "category": "Competenze e Formazione",
        "subcategory": "Competenze del personale",
        "text": "Il personale dell'ente possiede competenze adeguate in materia di trasparenza, governance digitale e partecipazione?",
        "hint": "Competenze necessarie: normativa sulla trasparenza (D.Lgs. 33/2013, FOIA), anticorruzione (L. 190/2012), CAD, GDPR, gestione documentale, open data, comunicazione pubblica, facilitazione della partecipazione, strumenti digitali. Il Piano della Formazione deve includere queste competenze.",
        "options": [
            {"text": "Competenze insufficienti, nessuna formazione specifica", "score": 1},
            {"text": "Competenze di base con formazione occasionale", "score": 2},
            {"text": "Formazione periodica sugli obblighi normativi principali", "score": 3},
            {"text": "Piano formativo strutturato su trasparenza, governance digitale e partecipazione", "score": 4},
            {"text": "Programma di sviluppo continuo con certificazioni, community of practice e knowledge sharing", "score": 5}
        ],
        "weight": 1.2,
        "order": 13,
        "target_type": "pa"
    },
    {
        "category": "Competenze e Formazione",
        "subcategory": "Responsabile della Trasparenza",
        "text": "Il Responsabile della Prevenzione della Corruzione e della Trasparenza (RPCT) è adeguatamente supportato?",
        "hint": "Il RPCT è una figura obbligatoria (L. 190/2012) che coordina le attività di prevenzione della corruzione e trasparenza. Deve avere: autonomia, risorse, supporto organizzativo, accesso alle informazioni, formazione specifica. Il supporto include: staff dedicato, strumenti informatici, budget, collaborazione dei dirigenti.",
        "options": [
            {"text": "Il RPCT è nominato formalmente ma senza supporto effettivo", "score": 1},
            {"text": "Supporto minimo, il RPCT opera prevalentemente da solo", "score": 2},
            {"text": "Supporto adeguato con risorse e collaborazione dei dirigenti", "score": 3},
            {"text": "RPCT con staff dedicato, strumenti avanzati e piena collaborazione organizzativa", "score": 4},
            {"text": "RPCT integrato nella governance con ruolo strategico, risorse adeguate e cultura dell'integrità diffusa", "score": 5}
        ],
        "weight": 1.3,
        "order": 14,
        "target_type": "pa"
    },
    {
        "category": "Competenze e Formazione",
        "subcategory": "Formazione alla partecipazione",
        "text": "L'ente forma i cittadini e le associazioni all'uso degli strumenti di partecipazione e monitoraggio?",
        "hint": "Formazione alla partecipazione: laboratori civici, tutorial online, guide all'uso delle piattaforme, accompagnamento delle associazioni, educazione civica digitale. L'obiettivo è ridurre il digital divide nella partecipazione e garantire che tutti i cittadini possano esercitare i propri diritti.",
        "options": [
            {"text": "Non viene fornita alcuna formazione ai cittadini", "score": 1},
            {"text": "Informazioni generiche sul sito web", "score": 2},
            {"text": "Guide e tutorial disponibili online per gli strumenti principali", "score": 3},
            {"text": "Programma di formazione con laboratori, tutorial e accompagnamento", "score": 4},
            {"text": "Ecosistema formativo con laboratori civici, mentoring, community e co-progettazione dei percorsi formativi", "score": 5}
        ],
        "weight": 1.1,
        "order": 15,
        "target_type": "pa"
    },

    # ============ SEZIONE 6: CONFORMITÀ PNRR E NORMATIVA ============
    {
        "category": "Conformità PNRR e Normativa",
        "subcategory": "Principi PNRR",
        "text": "L'ente rispetta i principi trasversali del PNRR (parità di genere, giovani, inclusione, DNSH)?",
        "hint": "Principi PNRR: parità di genere (gender mainstreaming), protezione e valorizzazione dei giovani, superamento dei divari territoriali, inclusione delle persone con disabilità, DNSH (Do No Significant Harm — non arrecare danno significativo all'ambiente). Questi principi devono essere integrati in tutte le attività finanziate.",
        "options": [
            {"text": "I principi PNRR non sono considerati nelle attività dell'ente", "score": 1},
            {"text": "Consapevolezza dei principi ma applicazione limitata", "score": 2},
            {"text": "Applicazione dei principi nelle attività finanziate dal PNRR", "score": 3},
            {"text": "Integrazione sistematica dei principi in tutte le attività con monitoraggio", "score": 4},
            {"text": "Principi PNRR integrati nella strategia dell'ente con indicatori, reporting e miglioramento continuo", "score": 5}
        ],
        "weight": 1.4,
        "order": 16,
        "target_type": "pa"
    },
    {
        "category": "Conformità PNRR e Normativa",
        "subcategory": "Gestione finanziaria",
        "text": "L'ente applica i principi di sana gestione finanziaria e prevenzione del doppio finanziamento?",
        "hint": "Sana gestione finanziaria (Reg. UE 2018/1046): economia, efficienza, efficacia nell'uso delle risorse. Prevenzione doppio finanziamento: garantire che le stesse spese non siano finanziate da più fonti UE/nazionali. Include: sistema di contabilità separata, tracciabilità delle spese, controlli incrociati, audit trail.",
        "options": [
            {"text": "Non esistono procedure specifiche per la gestione finanziaria dei fondi UE", "score": 1},
            {"text": "Procedure di base con tracciabilità limitata", "score": 2},
            {"text": "Contabilità separata per i fondi UE con controlli periodici", "score": 3},
            {"text": "Sistema strutturato con tracciabilità completa, controlli incrociati e audit trail", "score": 4},
            {"text": "Sistema integrato di gestione finanziaria con automazione, controlli in tempo reale e reporting avanzato", "score": 5}
        ],
        "weight": 1.3,
        "order": 17,
        "target_type": "pa"
    },
    {
        "category": "Conformità PNRR e Normativa",
        "subcategory": "GDPR e protezione dati",
        "text": "L'ente è conforme al GDPR nella gestione dei dati personali dei cittadini, anche nell'ambito della partecipazione digitale?",
        "hint": "GDPR (Reg. UE 2016/679): consenso informato, minimizzazione dei dati, diritto all'oblio, portabilità, DPO (Data Protection Officer), DPIA (Data Protection Impact Assessment), registro dei trattamenti. Nella partecipazione digitale: anonimizzazione dei contributi se richiesto, sicurezza delle piattaforme, informativa chiara.",
        "options": [
            {"text": "Conformità GDPR carente con rischi significativi", "score": 1},
            {"text": "Conformità di base con DPO nominato ma implementazione parziale", "score": 2},
            {"text": "Conformità adeguata con registro trattamenti, informative e misure di sicurezza", "score": 3},
            {"text": "Conformità completa con DPIA, formazione, procedure di data breach e privacy by design", "score": 4},
            {"text": "Eccellenza nella protezione dati con privacy by design/default, audit periodici e cultura della privacy diffusa", "score": 5}
        ],
        "weight": 1.2,
        "order": 18,
        "target_type": "pa"
    },

    # ============ SEZIONE 7: MODELLI MIGLIORATIVI E BUONE PRATICHE ============
    {
        "category": "Modelli Migliorativi",
        "subcategory": "Benchmarking",
        "text": "L'ente confronta le proprie pratiche di governance trasparente con quelle di altri enti e best practice nazionali/internazionali?",
        "hint": "Benchmarking: confronto sistematico con altri enti per identificare best practice. Fonti: ANAC (Autorità Nazionale Anticorruzione), AgID, OECD, Transparency International, Open Government Partnership. Include: analisi comparativa, visite studio, partecipazione a reti e community di pratica.",
        "options": [
            {"text": "Non viene effettuato alcun benchmarking", "score": 1},
            {"text": "Confronto occasionale e informale con altri enti", "score": 2},
            {"text": "Partecipazione a reti e confronto periodico su alcune aree", "score": 3},
            {"text": "Benchmarking strutturato con analisi comparativa e piano di miglioramento", "score": 4},
            {"text": "Benchmarking continuo con partecipazione attiva a reti internazionali, condivisione di best practice e innovazione", "score": 5}
        ],
        "weight": 1.1,
        "order": 19,
        "target_type": "pa"
    },
    {
        "category": "Modelli Migliorativi",
        "subcategory": "Co-progettazione",
        "text": "L'ente pratica la co-progettazione di servizi e politiche con cittadini, associazioni e stakeholder?",
        "hint": "Co-progettazione: processo in cui l'ente e i cittadini/stakeholder progettano insieme servizi, politiche o interventi. Include: laboratori di co-design, tavoli di lavoro multi-stakeholder, hackathon civici, living lab. La co-progettazione va oltre la consultazione: i cittadini sono co-autori delle soluzioni.",
        "options": [
            {"text": "Non esiste alcuna forma di co-progettazione", "score": 1},
            {"text": "Coinvolgimento occasionale di stakeholder in fase avanzata dei progetti", "score": 2},
            {"text": "Tavoli di lavoro con stakeholder per alcuni progetti rilevanti", "score": 3},
            {"text": "Processo strutturato di co-progettazione con metodologie partecipative", "score": 4},
            {"text": "Ecosistema di co-progettazione con living lab, hackathon civici, community attive e innovazione sociale", "score": 5}
        ],
        "weight": 1.3,
        "order": 20,
        "target_type": "pa"
    },
    {
        "category": "Modelli Migliorativi",
        "subcategory": "Miglioramento continuo",
        "text": "L'ente ha un processo di miglioramento continuo della governance trasparente basato su dati e feedback?",
        "hint": "Miglioramento continuo: ciclo PDCA applicato alla governance. Include: raccolta feedback dai cittadini, analisi dei dati di utilizzo dei servizi, valutazione dell'efficacia delle misure di trasparenza, revisione periodica delle procedure, innovazione dei processi. Strumenti: customer satisfaction, analytics, audit interni.",
        "options": [
            {"text": "Non esiste un processo di miglioramento continuo", "score": 1},
            {"text": "Miglioramenti reattivi in risposta a criticità o reclami", "score": 2},
            {"text": "Raccolta periodica di feedback con alcune azioni di miglioramento", "score": 3},
            {"text": "Processo strutturato con KPI, feedback sistematico e piano di miglioramento", "score": 4},
            {"text": "Cultura del miglioramento continuo con analytics, innovazione dei processi, benchmarking e citizen satisfaction", "score": 5}
        ],
        "weight": 1.2,
        "order": 21,
        "target_type": "pa"
    },
]

GOVERNANCE_CATEGORIES = [
    "Trasparenza Amministrativa",
    "Tracciabilità delle Decisioni",
    "Partecipazione dei Cittadini",
    "Strumenti Digitali per la Governance",
    "Competenze e Formazione",
    "Conformità PNRR e Normativa",
    "Modelli Migliorativi"
]
