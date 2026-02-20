# ALLEGATO A — DESCRIZIONE TECNICA DELLA PIATTAFORMA

## "Digital Maturity Assessment Platform"

### Al Contratto di Noleggio Piattaforma Software

---

## 1. PANORAMICA GENERALE

La **Digital Maturity Assessment Platform** (di seguito "Piattaforma") è un sistema software web-based multi-portale progettato per la somministrazione, analisi e reportistica di assessment rivolti a Piccole e Medie Imprese (PMI) e Pubbliche Amministrazioni (PA), nell'ambito del programma European Digital Innovation Hub — Rome Digital Innovation Hub (R.O.M.E. DIH).

La Piattaforma eroga **tre servizi distinti** attraverso portali dedicati:

| Portale | Programma | Target | Colore UI |
|---------|-----------|--------|-----------|
| **Digital Maturity Assessment** | Valutazione maturità digitale | PMI + PA | Blu |
| **Audit UNI/PdR 56002** | Gestione dell'Innovazione — Conformità ISO 56002 | PMI + PA | Verde (emerald) |
| **Governance Trasparente** | Formazione e consulenza governance PA | Solo PA | Ambra (amber) |

La Piattaforma consente di:
- Somministrare questionari strutturati specifici per ciascun programma
- Calcolare automaticamente punteggi multidimensionali di maturità/conformità
- Generare report professionali con gap analysis e raccomandazioni operative
- Gestire l'intero ciclo di vita degli assessment tramite pannello di amministrazione unificato
- Produrre documentazione conforme ai requisiti di rendicontazione UE
- Identificare visivamente il tipo di servizio erogato (colori e badge per programma)

---

## 2. URL DI ACCESSO E CREDENZIALI

### 2.1 Portali utente (frontend)

| Portale | URL di produzione |
|---------|-------------------|
| **Maturità Digitale** | `https://digital-maturity-assessment.vercel.app/` |
| **Audit UNI/PdR 56002** | `https://digital-maturity-assessment.vercel.app/iso56002` |
| **Governance Trasparente** | `https://digital-maturity-assessment.vercel.app/governance` |
| **Pannello Admin** | `https://digital-maturity-assessment.vercel.app/admin` |

### 2.2 Backend API

| Risorsa | URL |
|---------|-----|
| **API Base** | `https://digital-maturity-assessment.onrender.com/api` |
| **Health Check** | `https://digital-maturity-assessment.onrender.com/health` |
| **Root Info** | `https://digital-maturity-assessment.onrender.com/` |

### 2.3 Infrastruttura e gestione

| Servizio | URL Dashboard |
|----------|---------------|
| **Backend hosting** | Render Dashboard (render.com) |
| **Frontend hosting** | Vercel Dashboard (vercel.com) |
| **Database** | Neon Console (console.neon.tech) |
| **Repository codice** | `https://github.com/percorsielmar/digital-maturity-assessment` |

### 2.4 Variabili d'ambiente

Le credenziali e configurazioni sensibili sono gestite tramite variabili d'ambiente server-side, mai incluse nel codice sorgente:

| Variabile | Dove | Descrizione |
|-----------|------|-------------|
| `DATABASE_URL` | Backend (Render) | Stringa di connessione PostgreSQL (Neon) |
| `ADMIN_SECRET` | Backend (Render) | Chiave di accesso pannello amministrativo |
| `OPENAI_API_KEY` | Backend (Render) | Chiave API OpenAI per assistente AI |
| `GOOGLE_CLIENT_ID` | Backend (Render) | Client ID per autenticazione Google OAuth |
| `VITE_API_URL` | Frontend (Vercel) | URL del backend: `https://digital-maturity-assessment.onrender.com/api` |

### 2.5 Autenticazione utenti

Ogni portale ha la propria pagina di login/registrazione. L'accesso avviene tramite:
- **Codice di accesso** (generato automaticamente alla registrazione) + **password**
- **Google Login** (OAuth 2.0) — disponibile su tutti i portali

L'organizzazione viene associata al programma (`dma`, `iso56002`, `governance`) al momento della registrazione. Il login è unico: il sistema riconosce automaticamente il programma dell'organizzazione e mostra la dashboard appropriata.

---

## 3. ARCHITETTURA DEL SISTEMA

### 3.1 Architettura generale

La Piattaforma adotta un'architettura **client-server a tre livelli** (three-tier architecture) con **routing multi-portale** sul frontend:

```
┌─────────────────────────────────────────────────────────────┐
│                       LIVELLO 1                              │
│                 FRONTEND (Presentazione)                      │
│            React 18 + TypeScript + Vite                       │
│            Hosting: Vercel (CDN globale)                      │
│            Protocollo: HTTPS (TLS 1.3)                       │
│                                                              │
│   /              → Portale Maturità Digitale (blu)           │
│   /iso56002      → Portale Audit 56002 (verde)               │
│   /governance    → Portale Governance Trasparente (ambra)     │
│   /admin         → Pannello Amministrazione                  │
│   /dashboard     → Dashboard utente (program-aware)          │
│   /assessment/:id → Pagina assessment (program-aware)        │
│   /report/:id    → Pagina report                             │
└────────────────────────────┬────────────────────────────────┘
                             │ REST API (JSON)
┌────────────────────────────▼────────────────────────────────┐
│                       LIVELLO 2                              │
│                 BACKEND (Logica applicativa)                  │
│            Python 3.11 + FastAPI (async)                      │
│            Hosting: Render (container Docker)                 │
│            Protocollo: HTTPS (TLS 1.3)                       │
│                                                              │
│   /api/auth/*              → Autenticazione (tutti i prog.)  │
│   /api/questions/          → Domande DMA                     │
│   /api/questions-iso56002/ → Domande 56002                   │
│   /api/questions-governance/→ Domande Governance             │
│   /api/assessments/*       → Assessment (tutti i prog.)      │
│   /api/admin/*             → Amministrazione                 │
│   /api/assistant/*         → Assistente AI                   │
└────────────────────────────┬────────────────────────────────┘
                             │ SQL (async)
┌────────────────────────────▼────────────────────────────────┐
│                       LIVELLO 3                              │
│                 DATABASE (Persistenza dati)                   │
│            PostgreSQL 15 (Neon — serverless)                  │
│            Connessione: SSL/TLS encrypted                    │
│            Backup: automatico giornaliero                    │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 Stack tecnologico

| Componente | Tecnologia | Versione | Licenza |
|------------|-----------|----------|---------|
| **Frontend framework** | React | 18.x | MIT |
| **Build tool** | Vite | 5.x | MIT |
| **Linguaggio frontend** | TypeScript | 5.x | Apache 2.0 |
| **Styling** | Tailwind CSS | 3.x | MIT |
| **Icone** | Lucide React | latest | ISC |
| **Generazione DOCX** | docx.js | latest | MIT |
| **Markdown rendering** | react-markdown | latest | MIT |
| **Routing** | react-router-dom | 6.x | MIT |
| **Backend framework** | FastAPI | 0.100+ | MIT |
| **Linguaggio backend** | Python | 3.11 | PSF |
| **ORM** | SQLAlchemy | 2.x (async) | MIT |
| **Database** | PostgreSQL | 15 | PostgreSQL License |
| **AI Assistant** | OpenAI API | GPT-3.5-turbo | Commerciale |
| **HTTP Client** | httpx | latest | BSD |
| **Auth Google** | google-auth | latest | Apache 2.0 |

### 3.3 Infrastruttura cloud

| Servizio | Provider | Funzione | SLA Provider |
|----------|----------|----------|-------------|
| **Backend hosting** | Render | Container Docker, auto-scaling | 99.95% |
| **Frontend hosting** | Vercel | CDN globale, edge network | 99.99% |
| **Database** | Neon (PostgreSQL) | DB serverless, auto-scaling | 99.95% |
| **Certificati SSL** | Let's Encrypt (via provider) | Crittografia HTTPS | Automatico |
| **DNS** | Gestito dai provider | Risoluzione domini | 99.99% |

---

## 4. MODULI FUNZIONALI

### 4.1 Modulo di Registrazione e Autenticazione

**Descrizione:** Sistema di gestione delle identità dei beneficiari (organizzazioni) con registrazione, login, autenticazione Google e controllo degli accessi multi-programma.

**Funzionalità:**
- Registrazione organizzazione con dati anagrafici completi (ragione sociale, tipologia, settore, dimensione, codice fiscale/P.IVA, email, telefono, responsabile)
- Associazione automatica al programma in base al portale di registrazione
- Autenticazione tramite codice di accesso e password con hashing sicuro (bcrypt)
- Autenticazione tramite Google OAuth 2.0
- Generazione automatica di codici di accesso univoci
- Gestione sessioni con token JWT (scadenza configurabile)
- Differenziazione per tipologia: PMI (Impresa) e Pubblica Amministrazione
- Reset password da pannello amministrativo

**Modello dati — Organization:**

| Campo | Tipo | Descrizione |
|-------|------|-------------|
| id | Integer (PK) | Identificativo univoco |
| name | String(255) | Ragione sociale |
| type | String(50) | Tipologia: `azienda` o `pa` |
| sector | String(100) | Settore di attività |
| size | String(50) | Dimensione organizzazione |
| access_code | String(100) | Codice di accesso univoco |
| hashed_password | String(255) | Password crittografata (bcrypt) |
| email | String(255) | Email di contatto |
| fiscal_code | String(50) | Codice Fiscale / Partita IVA |
| phone | String(50) | Numero di telefono |
| admin_name | String(255) | Nome e cognome responsabile |
| **program** | **String(50)** | **Programma: `dma`, `iso56002`, `governance`** |
| created_at | DateTime | Data di registrazione |

**Modello dati — Assessment:**

| Campo | Tipo | Descrizione |
|-------|------|-------------|
| id | Integer (PK) | Identificativo univoco |
| organization_id | Integer (FK) | Riferimento all'organizzazione |
| level | Integer | Livello: 1 (base) o 2 (avanzato) |
| status | String(50) | Stato: `in_progress`, `completed` |
| responses | JSON | Risposte dell'utente |
| scores | JSON | Punteggi calcolati per area |
| gap_analysis | JSON | Analisi gap per area |
| report | Text | Report generato (Markdown) |
| audit_sheet | Text | Scheda audit (Markdown) |
| maturity_level | Float | Livello di maturità complessivo (1-5) |
| created_at | DateTime | Data di creazione |
| completed_at | DateTime | Data di completamento |

---

### 4.2 Portale 1 — Digital Maturity Assessment (DMA)

**URL:** `/`
**Colore:** Blu (`from-primary-600 to-primary-900`)
**Target:** PMI e PA

#### Assessment di Livello 1 (Base)

Questionario strutturato per la valutazione della maturità digitale, articolato in **6 aree tematiche** con **18 domande** a risposta multipla pesata.

| Area | Sottocategorie | N. Domande |
|------|---------------|------------|
| **Strategia Digitale** | Visione e Leadership, Budget e Investimenti | 3 |
| **Infrastruttura e Tecnologia** | Cloud e Infrastruttura, Sistemi e Integrazione, Cybersecurity | 3 |
| **Processi e Operazioni** | Automazione, Documentale, Collaborazione | 3 |
| **Dati e Analytics** | Gestione Dati, Business Intelligence, Data-Driven | 3 |
| **Competenze e Cultura** | Competenze Digitali, Formazione, Change Management | 3 |
| **Customer Experience** | Canali Digitali, Personalizzazione, Feedback | 3 |

#### Assessment di Livello 2 (Avanzato)

Questionario approfondito accessibile solo dopo il completamento del Livello 1. Comprende domande a risposta aperta, selezione singola e selezione multipla.

| Area | Descrizione |
|------|-------------|
| **Anagrafica** | Dati aziendali dettagliati (ragione sociale, forma societaria, P.IVA, ATECO, fatturato, dipendenti, sede) |
| **Contabilità e Finanza** | Sistemi contabili, gestione finanziaria, fatturazione elettronica, pagamenti digitali |
| **Clienti e Mercati** | CRM, canali di vendita, e-commerce, marketing digitale, presenza online |
| **Tecnologie** | Infrastruttura IT, software gestionale, cloud, cybersecurity, innovazione tecnologica |

**Tipologie di domanda Livello 2:** `text` (risposta aperta), `select` (selezione singola), `multiselect` (selezione multipla)

#### Report generato
- Report di Maturità Digitale con gap analysis e raccomandazioni
- Scheda di Audit per rendicontazione UE
- Documentazione DIH completa (report + audit + profili)

---

### 4.3 Portale 2 — Audit Propedeutico UNI/PdR 56002

**URL:** `/iso56002`
**Colore:** Verde emerald (`from-emerald-600 to-emerald-900`)
**Target:** PMI e PA
**Endpoint domande:** `/api/questions-iso56002/`

Questionario di audit propedeutico alla certificazione UNI/PdR 56002 (Gestione dell'Innovazione), articolato in **8 aree tematiche** con **25 domande** a risposta multipla pesata.

| Area | N. Domande | Riferimento norma |
|------|------------|-------------------|
| **Contesto dell'Organizzazione** | 3 | Clausola 4 |
| **Leadership** | 3 | Clausola 5 |
| **Pianificazione** | 3 | Clausola 6 |
| **Supporto** | 4 | Clausola 7 |
| **Attività Operative** | 4 | Clausola 8 |
| **Valutazione delle Prestazioni** | 3 | Clausola 9 |
| **Miglioramento** | 3 | Clausola 10 |
| **Strumenti e Metodi** | 2 | Annex |

**Caratteristiche:**
- 5 opzioni di risposta con punteggio da 1 (non conforme) a 5 (eccellenza)
- Pesi differenziati (1.0 – 1.5) per riflettere la criticità delle clausole
- Hint esplicativi con riferimenti alla norma UNI/PdR 56002
- Solo assessment di Livello 1 (nessun Livello 2)

#### Report generato
- Report di conformità UNI/PdR 56002 con analisi per clausola
- Gap analysis rispetto ai requisiti della norma
- Piano di certificazione con azioni correttive prioritizzate
- Raccomandazioni per il percorso formativo (2 giornate)

---

### 4.4 Portale 3 — Governance Trasparente

**URL:** `/governance`
**Colore:** Ambra (`from-amber-600 to-amber-900`)
**Target:** Solo Pubblica Amministrazione
**Endpoint domande:** `/api/questions-governance/`

Questionario di assessment per il programma di Governance Trasparente nella PA, articolato in **7 aree tematiche** con **21 domande** a risposta multipla pesata.

| Area | N. Domande | Focus |
|------|------------|-------|
| **Trasparenza Amministrativa** | 3 | Pubblicazione atti, accesso civico, obblighi informativi |
| **Tracciabilità delle Decisioni** | 3 | Documentazione iter, protocollo digitale, audit trail |
| **Partecipazione dei Cittadini** | 3 | Consultazioni pubbliche, bilancio partecipativo, feedback |
| **Strumenti Digitali per la Governance** | 3 | Piattaforme deliberative, open data, interoperabilità |
| **Competenze e Formazione** | 3 | Formazione personale, cultura trasparenza, leadership |
| **Conformità PNRR e Normativa** | 3 | Sana gestione finanziaria, DNSH, parità di genere |
| **Modelli Migliorativi** | 3 | Benchmarking, ciclo PDCA, innovazione governance |

**Caratteristiche:**
- 5 opzioni di risposta con punteggio da 1 (assente) a 5 (eccellenza)
- Pesi differenziati per area
- Registrazione forzata come tipo `pa` (selettore tipologia nascosto)
- Solo assessment di Livello 1

#### Report generato
- Report di Governance Trasparente con analisi per area
- Gap analysis rispetto alle best practice di governance
- **Percorso formativo completo** (5 sessioni):
  - 3 giornate in presenza (4h ciascuna): Trasparenza, Partecipazione, Governance PNRR
  - 2 sessioni online (2h ciascuna): Analisi pratiche + Follow-up
  - Attività asincrone + report operativo
- Sezione conformità PNRR (sana gestione finanziaria, DNSH, parità di genere, obblighi comunicazione)
- Termine previsto: 30 aprile 2026

---

### 4.5 Motore di Analisi e Scoring

**Descrizione:** Algoritmo proprietario per il calcolo dei punteggi, la gap analysis e la determinazione del livello complessivo. L'algoritmo è identico per tutti e tre i programmi, applicato ai rispettivi set di domande.

**Algoritmo di scoring:**

1. **Raccolta risposte:** Per ogni domanda, viene registrata l'opzione selezionata con il relativo punteggio (1-5)
2. **Ponderazione:** Il punteggio di ogni risposta viene moltiplicato per il peso (weight) della domanda
3. **Normalizzazione per categoria:** Per ogni area tematica, il punteggio normalizzato è calcolato come:
   ```
   Score_categoria = Σ(punteggio_i × peso_i) / Σ(peso_i)
   ```
4. **Punteggio complessivo:** Media ponderata di tutte le risposte:
   ```
   Overall_maturity = Σ(punteggio_i × peso_i) / Σ(peso_i) per tutte le domande
   ```
5. **Determinazione livello:** Arrotondamento del punteggio complessivo alla scala 1-5

**Scala di maturità/conformità (5 livelli):**

| Livello | Punteggio | DMA | ISO 56002 | Governance |
|---------|-----------|-----|-----------|------------|
| 1 | 1.0 – 1.4 | Iniziale | Non conforme | Assente |
| 2 | 1.5 – 2.4 | Gestito | Parzialmente conforme | Base |
| 3 | 2.5 – 3.4 | Definito | Conforme con gap | Strutturato |
| 4 | 3.5 – 4.4 | Quant. Gestito | Conforme | Avanzato |
| 5 | 4.5 – 5.0 | Ottimizzato | Eccellenza | Eccellenza |

**Gap Analysis automatizzata:**
Per ogni area tematica viene calcolato:
- **Current score**: Punteggio attuale normalizzato
- **Target score**: 5 (eccellenza)
- **Gap**: Differenza tra target e current
- **Priorità**: Alta (gap > 2), Media (gap > 1), Bassa (gap ≤ 1)

---

### 4.6 Modulo di Generazione Report

**Descrizione:** Sistema di generazione automatica di documentazione professionale in formato Markdown e DOCX, con report specifici per ciascun programma.

**Documenti generati (comuni a tutti i programmi):**

#### a) Report principale (specifico per programma)
- Intestazione istituzionale (Rome Digital Innovation Hub in collaborazione con Il Borgo Urbano)
- Dati del beneficiario (nome, tipologia, settore, dimensione)
- Punteggio complessivo e livello
- Punteggi per area tematica con analisi dettagliata
- Gap analysis con priorità di intervento
- Raccomandazioni operative personalizzate
- Formato: Markdown + esportazione DOCX (font Courier New)

#### b) Scheda di Audit
- Formato sintetico per rendicontazione UE (max 1 pagina)
- Dati essenziali del beneficiario e dell'assessment
- Riepilogo punteggi e livello
- Metodologia applicata
- Intestazione Rome Digital Innovation Hub + Il Borgo Urbano

#### c) Documentazione DIH Completa
- Pacchetto unico: Report + Scheda Audit + Profili professionali
- Formato: Markdown (.md)

#### d) CV Figure Professionali
- CV sintetico di Alexander Schneider (Esperto Trasformazione Digitale)
- CV sintetico di Elmar Schneider (Analista Innovazione di Processo)

#### e) Foglio Ore per Assessment
- Riepilogo ore per figura professionale (40 ore totali per assessment)
- Dettaglio attività svolte con ore per ciascuna
- Riepilogo complessivo con importi (tariffa 250 €/h)
- Spazio firme (responsabile progetto e beneficiario)

**Generazione DOCX (frontend):**
- Conversione automatica da Markdown a formato Microsoft Word (.docx)
- Font: Courier New (monospaced professionale)
- Intestazioni gerarchiche (H1, H2, H3)
- Paragrafi formattati con spaziatura professionale
- Elenchi puntati e grassetti
- Download diretto dal browser

---

### 4.7 Assistente AI Integrato

**Descrizione:** Chatbot intelligente basato su OpenAI GPT-3.5-turbo che assiste i beneficiari durante la compilazione del questionario.

**Funzionalità:**
- Spiegazione in linguaggio semplice del significato di ogni domanda
- Esempi pratici per ogni opzione di risposta
- Suggerimenti personalizzati in base alla situazione descritta dall'utente
- Contestualizzazione per tipologia di organizzazione (impresa/PA) e settore
- Interfaccia conversazionale integrata nella pagina di assessment

**Specifiche tecniche:**
- Modello: OpenAI GPT-3.5-turbo
- Max tokens per risposta: 500
- Temperatura: 0.7 (bilanciamento creatività/precisione)
- Timeout: 30 secondi
- Fallback: suggerimento dalla guida (hint) in caso di indisponibilità AI

---

### 4.8 Pannello di Amministrazione

**URL:** `/admin`
**Autenticazione:** Chiave amministrativa (`ADMIN_SECRET`)

**Descrizione:** Dashboard di gestione completa e unificata per tutti e tre i programmi, con identificazione visiva immediata del tipo di servizio.

**Identificazione visiva per programma:**

| Programma | Badge | Colore sfondo | Bordo sinistro |
|-----------|-------|---------------|----------------|
| Maturità Digitale | `MATURITÀ DIGITALE` | Bianco | Blu |
| Audit 56002 | `AUDIT 56002` | Verde chiaro (emerald-50) | Verde (emerald-500) |
| Governance | `GOVERNANCE` | Ambra chiaro (amber-50) | Ambra (amber-500) |

**Funzionalità:**

#### Gestione Organizzazioni
- Elenco completo con badge colorato per programma
- Filtri e ricerca
- Visualizzazione dettagli anagrafici (nome, tipo, settore, dimensione, email, codice accesso)
- Reset password per organizzazioni
- Eliminazione organizzazioni (con tutti gli assessment associati)

#### Gestione Assessment
- Elenco assessment per organizzazione con stato (in corso, completato)
- Label specifica per tipo: "Assessment 1/2" (DMA), "Audit 56002", "Assessment Governance"
- Righe assessment con sfondo colorato coordinato al programma
- Visualizzazione dettagliata di ogni assessment:
  - Punteggi per area tematica
  - Livello di maturità/conformità complessivo
  - Report completo in Markdown con rendering formattato
  - Scheda di audit
- Rigenerazione report su richiesta (program-aware)
- Eliminazione assessment

#### Visualizzazione Risposte Dettagliate
- Modal a schermo intero con tutte le risposte raggruppate per categoria
- Per ogni domanda: testo, tutte le opzioni disponibili, opzione selezionata evidenziata con punteggio
- Supporto domande da tutti i programmi (DMA dal DB, 56002 e Governance da file dati)
- Funzionalità di stampa professionale con layout formattato (Courier New)

#### Statistiche
- Totale organizzazioni registrate
- Totale assessment (completati, in corso)
- Media livello di maturità

#### Download Documentazione
- **Report DOCX**: Report in formato Microsoft Word
- **Scheda Audit**: Download scheda audit in Markdown
- **Doc. DIH**: Pacchetto documentazione completa (report + audit + profili)
- **CV**: Download CV separati delle figure professionali
- **Foglio Ore**: Generazione e download foglio ore specifico per assessment
- **Risposte**: Visualizzazione e stampa risposte dettagliate

---

### 4.9 Dashboard Utente

**URL:** `/dashboard` (richiede autenticazione)

**Descrizione:** Interfaccia per i beneficiari, automaticamente personalizzata in base al programma dell'organizzazione.

**Personalizzazione per programma:**

| Programma | Titolo Dashboard | Livello 2 |
|-----------|-----------------|-----------|
| DMA | "Assessment Maturità Digitale" | Sì (dopo completamento Livello 1) |
| ISO 56002 | "Audit UNI/PdR 56002 — Gestione dell'Innovazione" | No |
| Governance | "Assessment Governance Trasparente" | No |

**Funzionalità:**
- Panoramica assessment completati e in corso
- Accesso ai risultati con visualizzazione grafica:
  - Radar chart multidimensionale per aree tematiche
  - Barre comparative per punteggi di area
  - Indicatore livello di maturità/conformità complessivo
- Accesso all'assessment di Livello 2 (solo DMA, se idoneo)
- Download report in formato DOCX
- Logout con redirect al portale di appartenenza

---

## 5. API REST — ENDPOINTS

### 5.1 Autenticazione (`/api/auth`)

| Metodo | Endpoint | Descrizione |
|--------|----------|-------------|
| POST | `/api/auth/register` | Registrazione nuova organizzazione (con campo `program`) |
| POST | `/api/auth/login` | Login con codice di accesso e password |
| POST | `/api/auth/google` | Login/registrazione tramite Google OAuth (con campo `program`) |
| GET | `/api/auth/me` | Dati organizzazione corrente (autenticato) |
| PUT | `/api/auth/organization` | Aggiornamento dati organizzazione |

### 5.2 Questionari

#### DMA (Maturità Digitale)

| Metodo | Endpoint | Descrizione |
|--------|----------|-------------|
| GET | `/api/questions/` | Domande Livello 1 (18 domande, 6 aree) |
| GET | `/api/questions/categories` | Categorie disponibili |
| GET | `/api/questions-level2/` | Domande Livello 2 |
| GET | `/api/questions-level2/check-eligibility` | Verifica idoneità Livello 2 |

#### ISO 56002 (Gestione Innovazione)

| Metodo | Endpoint | Descrizione |
|--------|----------|-------------|
| GET | `/api/questions-iso56002/` | Domande audit 56002 (25 domande, 8 aree) |
| GET | `/api/questions-iso56002/categories` | Categorie 56002 |

#### Governance Trasparente

| Metodo | Endpoint | Descrizione |
|--------|----------|-------------|
| GET | `/api/questions-governance/` | Domande governance (21 domande, 7 aree) |
| GET | `/api/questions-governance/categories` | Categorie governance |

### 5.3 Assessment (`/api/assessments`)

| Metodo | Endpoint | Descrizione |
|--------|----------|-------------|
| POST | `/api/assessments/` | Creazione nuovo assessment (con parametro `level`) |
| GET | `/api/assessments/` | Elenco assessment dell'organizzazione |
| GET | `/api/assessments/{id}` | Dettaglio singolo assessment |
| PUT | `/api/assessments/{id}/save-progress` | Salvataggio progresso (bozza) |
| POST | `/api/assessments/{id}/submit` | Invio risposte, analisi e generazione report |
| GET | `/api/assessments/{id}/report` | Report dell'assessment |
| GET | `/api/assessments/{id}/audit-sheet` | Scheda audit dell'assessment |
| GET | `/api/assessments/{id}/full-documentation` | Documentazione DIH completa |
| GET | `/api/assessments/staff-profiles` | Profili figure professionali |

### 5.4 Assistente AI (`/api/assistant`)

| Metodo | Endpoint | Descrizione |
|--------|----------|-------------|
| POST | `/api/assistant/chat` | Invio messaggio all'assistente AI |

### 5.5 Amministrazione (`/api/admin`)

Tutti gli endpoint richiedono il parametro `admin_key`.

| Metodo | Endpoint | Descrizione |
|--------|----------|-------------|
| GET | `/api/admin/organizations` | Elenco organizzazioni (con campo `program`) |
| GET | `/api/admin/stats` | Statistiche generali |
| GET | `/api/admin/assessments/{id}` | Dettaglio assessment |
| GET | `/api/admin/assessments/{id}/responses` | Risposte dettagliate (program-aware) |
| GET | `/api/admin/assessments/{id}/timesheet` | Foglio ore assessment |
| POST | `/api/admin/assessments/{id}/regenerate` | Rigenerazione report (program-aware) |
| DELETE | `/api/admin/assessments/{id}` | Eliminazione assessment |
| POST | `/api/admin/reset-password` | Reset password organizzazione |
| DELETE | `/api/admin/organizations/{id}` | Eliminazione organizzazione |
| GET | `/api/admin/staff-profiles` | Profili figure professionali |
| GET | `/api/admin/staff-cvs` | CV figure professionali |

---

## 6. SICUREZZA

### 6.1 Crittografia
- Tutte le comunicazioni avvengono tramite **HTTPS** con certificati SSL/TLS
- Le password sono crittografate con algoritmo **bcrypt** (hashing irreversibile)
- La connessione al database è protetta da **SSL/TLS**

### 6.2 Autenticazione e autorizzazione
- Autenticazione utenti tramite **codice di accesso + password** oppure **Google OAuth 2.0**
- Autenticazione amministrativa tramite **chiave segreta** (ADMIN_SECRET)
- Token JWT con scadenza configurabile
- Separazione dei ruoli: utente (beneficiario) e amministratore
- Validazione di tutti gli input lato server (Pydantic)

### 6.3 Protezione dati
- Conformità al **Regolamento UE 2016/679 (GDPR)**
- Dati personali trattati esclusivamente per le finalità del programma DIH
- Backup giornaliero automatico del database
- Nessun dato sensibile esposto nelle API pubbliche
- Credenziali gestite esclusivamente tramite variabili d'ambiente

---

## 7. PERFORMANCE E SCALABILITÀ

| Parametro | Specifica |
|-----------|-----------|
| **Tempo di risposta API** | < 500ms (95° percentile) |
| **Tempo generazione report** | < 3 secondi |
| **Utenti concorrenti** | Fino a 100 simultanei |
| **Dimensione database** | Scalabile automaticamente (Neon serverless) |
| **Frontend** | CDN globale con edge caching (Vercel) |
| **Backend** | Container Docker con auto-restart |
| **Disponibilità target** | 99,5% su base mensile |
| **Portali supportati** | 3 (DMA, ISO 56002, Governance) |
| **Domande totali gestite** | 64 (18 DMA + 25 ISO 56002 + 21 Governance) |

---

## 8. MANUTENZIONE E AGGIORNAMENTI

### 8.1 Deploy continuo
- **Backend**: Deploy automatico su push al branch `main` (Render)
- **Frontend**: Deploy automatico su push al branch `main` (Vercel)
- Tempo di deploy: ~3-5 minuti per componente
- Repository: `https://github.com/percorsielmar/digital-maturity-assessment`

### 8.2 Migrazioni database
- Le migrazioni sono eseguite automaticamente all'avvio del backend
- Supporto PostgreSQL (produzione) e SQLite (sviluppo locale)
- Nuove colonne aggiunte con `ALTER TABLE` condizionale (verifica esistenza prima dell'aggiunta)

### 8.3 Monitoraggio
- Log applicativi in tempo reale (Render dashboard)
- Monitoraggio uptime e performance (provider-level)
- Alert automatici in caso di errori critici

### 8.4 Backup
- Database: backup automatico giornaliero con retention 30 giorni (Neon)
- Codice sorgente: versionato su repository Git privato (GitHub)

---

## 9. STRUTTURA DEL PROGETTO

```
digital-maturity-assessment/
├── backend/
│   ├── main.py                          # Entry point FastAPI, migrazioni, seed
│   ├── requirements.txt                 # Dipendenze Python
│   └── app/
│       ├── models.py                    # Modelli ORM (Organization, Assessment, Question)
│       ├── schemas.py                   # Schemi Pydantic (validazione I/O)
│       ├── database.py                  # Configurazione database async
│       ├── auth.py                      # Hashing, JWT, autenticazione
│       ├── config.py                    # Configurazione (variabili d'ambiente)
│       ├── crew_agents.py              # Generazione report (DMA, 56002, Governance)
│       ├── questions_data.py            # Domande DMA (18 domande)
│       ├── questions_level2_data.py     # Domande DMA Livello 2
│       ├── questions_iso56002_data.py   # Domande ISO 56002 (25 domande)
│       ├── questions_governance_data.py # Domande Governance (21 domande)
│       └── routers/
│           ├── auth.py                  # Endpoint autenticazione
│           ├── questions.py             # Endpoint domande DMA
│           ├── questions_level2.py      # Endpoint domande DMA Livello 2
│           ├── questions_iso56002.py    # Endpoint domande 56002
│           ├── questions_governance.py  # Endpoint domande Governance
│           ├── assessments.py           # Endpoint assessment
│           ├── admin.py                 # Endpoint amministrazione
│           └── assistant.py             # Endpoint assistente AI
├── frontend/
│   ├── package.json                     # Dipendenze Node.js
│   ├── vite.config.ts                   # Configurazione Vite
│   ├── tailwind.config.js               # Configurazione Tailwind CSS
│   └── src/
│       ├── App.tsx                      # Routing multi-portale
│       ├── api.ts                       # Client API (Axios)
│       ├── types.ts                     # Interfacce TypeScript
│       ├── context/
│       │   └── AuthContext.tsx           # Contesto autenticazione
│       └── components/
│           ├── LoginPage.tsx            # Login/registrazione (multi-programma)
│           ├── Dashboard.tsx            # Dashboard utente (program-aware)
│           ├── AssessmentPage.tsx        # Pagina assessment (program-aware)
│           ├── AssessmentLevel2Page.tsx  # Assessment Livello 2 (solo DMA)
│           ├── ReportPage.tsx           # Visualizzazione report
│           └── AdminPage.tsx            # Pannello amministrazione
└── docs/
    ├── allegato-a-descrizione-tecnica-piattaforma.md
    └── contratto-noleggio-piattaforma.md
```

---

## 10. REQUISITI DEL BENEFICIARIO

Per l'utilizzo della Piattaforma, il beneficiario necessita esclusivamente di:
- Browser web moderno (Chrome, Firefox, Safari, Edge — ultime 2 versioni)
- Connessione internet
- Nessuna installazione software richiesta

---

## 11. PROPRIETÀ E LICENZE

- Il codice sorgente della Piattaforma è di **proprietà esclusiva del Fornitore**
- Tutte le librerie e framework utilizzati sono rilasciati con **licenze open source** (MIT, Apache 2.0, BSD, ISC, PSF, PostgreSQL License) compatibili con l'uso commerciale
- L'unico componente con licenza commerciale è l'API OpenAI per l'assistente AI, il cui costo è incluso nel canone di noleggio

---

*Documento redatto come Allegato A al Contratto di Noleggio Piattaforma Software — Digital Maturity Assessment Platform*

*Rome Digital Innovation Hub in collaborazione con Il Borgo Urbano*

*Ultimo aggiornamento: 20 febbraio 2026*
