# ALLEGATO A — DESCRIZIONE TECNICA DELLA PIATTAFORMA

## "Digital Maturity Assessment Platform"

### Al Contratto di Noleggio Piattaforma Software

---

## 1. PANORAMICA GENERALE

La **Digital Maturity Assessment Platform** (di seguito "Piattaforma") è un sistema software web-based progettato per la somministrazione, analisi e reportistica di assessment di maturità digitale rivolti a Piccole e Medie Imprese (PMI) e Pubbliche Amministrazioni (PA), nell'ambito del programma European Digital Innovation Hub — Rome Digital Innovation Hub (R.O.M.E. DIH).

La Piattaforma consente di:
- Somministrare questionari strutturati di valutazione della maturità digitale
- Calcolare automaticamente punteggi multidimensionali di maturità
- Generare report professionali con gap analysis e raccomandazioni operative
- Gestire l'intero ciclo di vita degli assessment tramite pannello di amministrazione
- Produrre documentazione conforme ai requisiti di rendicontazione UE

---

## 2. ARCHITETTURA DEL SISTEMA

### 2.1 Architettura generale

La Piattaforma adotta un'architettura **client-server a tre livelli** (three-tier architecture):

```
┌─────────────────────────────────────────────────────┐
│                    LIVELLO 1                         │
│              FRONTEND (Presentazione)                │
│         React 18 + TypeScript + Vite                 │
│         Hosting: Vercel (CDN globale)                │
│         Protocollo: HTTPS (TLS 1.3)                  │
└──────────────────────┬──────────────────────────────┘
                       │ REST API (JSON)
┌──────────────────────▼──────────────────────────────┐
│                    LIVELLO 2                         │
│              BACKEND (Logica applicativa)             │
│         Python 3.11 + FastAPI (async)                │
│         Hosting: Render (container Docker)            │
│         Protocollo: HTTPS (TLS 1.3)                  │
└──────────────────────┬──────────────────────────────┘
                       │ SQL (async)
┌──────────────────────▼──────────────────────────────┐
│                    LIVELLO 3                         │
│              DATABASE (Persistenza dati)              │
│         PostgreSQL 15 (Neon — serverless)             │
│         Connessione: SSL/TLS encrypted               │
│         Backup: automatico giornaliero               │
└─────────────────────────────────────────────────────┘
```

### 2.2 Stack tecnologico

| Componente | Tecnologia | Versione | Licenza |
|------------|-----------|----------|---------|
| **Frontend framework** | React | 18.x | MIT |
| **Build tool** | Vite | 5.x | MIT |
| **Linguaggio frontend** | TypeScript | 5.x | Apache 2.0 |
| **Styling** | Tailwind CSS | 3.x | MIT |
| **Icone** | Lucide React | latest | ISC |
| **Generazione DOCX** | docx.js | latest | MIT |
| **Markdown rendering** | react-markdown | latest | MIT |
| **Backend framework** | FastAPI | 0.100+ | MIT |
| **Linguaggio backend** | Python | 3.11 | PSF |
| **ORM** | SQLAlchemy | 2.x (async) | MIT |
| **Database** | PostgreSQL | 15 | PostgreSQL License |
| **AI Assistant** | OpenAI API | GPT-3.5-turbo | Commerciale |
| **HTTP Client** | httpx | latest | BSD |

### 2.3 Infrastruttura cloud

| Servizio | Provider | Funzione | SLA Provider |
|----------|----------|----------|-------------|
| **Backend hosting** | Render | Container Docker, auto-scaling | 99.95% |
| **Frontend hosting** | Vercel | CDN globale, edge network | 99.99% |
| **Database** | Neon (PostgreSQL) | DB serverless, auto-scaling | 99.95% |
| **Certificati SSL** | Let's Encrypt (via provider) | Crittografia HTTPS | Automatico |
| **DNS** | Gestito dai provider | Risoluzione domini | 99.99% |

---

## 3. MODULI FUNZIONALI

### 3.1 Modulo di Registrazione e Autenticazione

**Descrizione:** Sistema di gestione delle identità dei beneficiari (organizzazioni) con registrazione, login e controllo degli accessi.

**Funzionalità:**
- Registrazione organizzazione con dati anagrafici completi (ragione sociale, tipologia, settore, dimensione, codice fiscale/P.IVA, email, telefono, responsabile)
- Autenticazione tramite codice di accesso e password con hashing sicuro (bcrypt)
- Generazione automatica di codici di accesso univoci
- Gestione sessioni con token JWT
- Differenziazione per tipologia: PMI (Impresa) e Pubblica Amministrazione
- Reset password da pannello amministrativo

**Modello dati — Organization:**

| Campo | Tipo | Descrizione |
|-------|------|-------------|
| id | Integer (PK) | Identificativo univoco |
| name | String(255) | Ragione sociale |
| type | String(50) | Tipologia: "azienda" o "pa" |
| sector | String(100) | Settore di attività |
| size | String(50) | Dimensione organizzazione |
| access_code | String(100) | Codice di accesso univoco |
| hashed_password | String(255) | Password crittografata |
| email | String(255) | Email di contatto |
| fiscal_code | String(50) | Codice Fiscale / Partita IVA |
| phone | String(50) | Numero di telefono |
| admin_name | String(255) | Nome e cognome responsabile |
| created_at | DateTime | Data di registrazione |

---

### 3.2 Modulo Assessment di Livello 1 (Base)

**Descrizione:** Questionario strutturato per la valutazione della maturità digitale di base, articolato in 6 aree tematiche con domande a risposta multipla pesata.

**Aree tematiche e struttura:**

| Area | Sottocategorie | N. Domande |
|------|---------------|------------|
| **Strategia Digitale** | Visione e Leadership, Budget e Investimenti | 3 |
| **Infrastruttura e Tecnologia** | Cloud e Infrastruttura, Sistemi e Integrazione, Cybersecurity | 3 |
| **Processi e Operazioni** | Automazione, Documentale, Collaborazione | 3 |
| **Dati e Analytics** | Gestione Dati, Business Intelligence, Data-Driven | 3 |
| **Competenze e Cultura** | Competenze Digitali, Formazione, Change Management | 3 |
| **Customer Experience** | Canali Digitali, Personalizzazione, Feedback | 3 |

**Caratteristiche delle domande:**
- Ogni domanda ha 5 opzioni di risposta con punteggio da 1 (minimo) a 5 (massimo)
- Ogni domanda ha un peso (weight) da 1.0 a 1.5 per riflettere l'importanza relativa
- Ogni domanda include un hint esplicativo con esempi pratici e definizioni
- Le domande possono essere specifiche per tipologia (azienda, PA) o comuni (both)
- Supporto per target_type: personalizzazione del questionario in base alla tipologia del beneficiario

**Scala di maturità (5 livelli):**

| Livello | Punteggio | Descrizione |
|---------|-----------|-------------|
| 1 | 1.0 - 1.4 | **Iniziale** — Processi ad hoc, nessuna strategia digitale |
| 2 | 1.5 - 2.4 | **Gestito** — Alcune iniziative digitali, gestione reattiva |
| 3 | 2.5 - 3.4 | **Definito** — Processi standardizzati, strategia parziale |
| 4 | 3.5 - 4.4 | **Quantitativamente Gestito** — Misurazione e ottimizzazione |
| 5 | 4.5 - 5.0 | **Ottimizzato** — Innovazione continua, eccellenza digitale |

---

### 3.3 Modulo Assessment di Livello 2 (Avanzato)

**Descrizione:** Questionario approfondito di secondo livello, accessibile solo dopo il completamento del Livello 1. Comprende domande a risposta aperta, selezione singola e selezione multipla.

**Prerequisito:** Almeno un assessment di Livello 1 completato.

**Aree tematiche:**

| Area | Descrizione |
|------|-------------|
| **Anagrafica** | Dati aziendali dettagliati (ragione sociale, forma societaria, P.IVA, ATECO, fatturato, dipendenti, sede) |
| **Contabilità e Finanza** | Sistemi contabili, gestione finanziaria, fatturazione elettronica, pagamenti digitali |
| **Clienti e Mercati** | CRM, canali di vendita, e-commerce, marketing digitale, presenza online |
| **Tecnologie** | Infrastruttura IT, software gestionale, cloud, cybersecurity, innovazione tecnologica |

**Tipologie di domanda:**
- **text**: Risposta aperta testuale
- **select**: Selezione singola da lista di opzioni
- **multiselect**: Selezione multipla da lista di opzioni

---

### 3.4 Motore di Analisi e Scoring

**Descrizione:** Algoritmo proprietario per il calcolo dei punteggi di maturità digitale, la gap analysis e la determinazione del livello complessivo.

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

**Gap Analysis automatizzata:**
Per ogni area tematica viene calcolato:
- **Current score**: Punteggio attuale normalizzato
- **Target score**: 5 (eccellenza)
- **Gap**: Differenza tra target e current
- **Priorità**: Alta (gap > 2), Media (gap > 1), Bassa (gap ≤ 1)

---

### 3.5 Modulo di Generazione Report

**Descrizione:** Sistema di generazione automatica di documentazione professionale in formato Markdown e DOCX.

**Documenti generati:**

#### a) Report di Maturità Digitale
- Intestazione istituzionale (Rome Digital Innovation Hub in collaborazione con Il Borgo Urbano)
- Dati del beneficiario (nome, tipologia, settore, dimensione)
- Punteggio complessivo e livello di maturità
- Punteggi per area tematica con analisi dettagliata
- Gap analysis con priorità di intervento
- Raccomandazioni operative personalizzate per tipologia (impresa/PA)
- Frase istituzionale contestualizzata
- Formato: Markdown + esportazione DOCX (font Courier New)

#### b) Scheda di Audit
- Formato sintetico per rendicontazione UE (max 1 pagina)
- Dati essenziali del beneficiario e dell'assessment
- Riepilogo punteggi e livello di maturità
- Metodologia applicata
- Frase istituzionale
- Intestazione Rome Digital Innovation Hub + Il Borgo Urbano

#### c) Documentazione DIH Completa
- Pacchetto unico scaricabile contenente:
  - Report di Maturità Digitale
  - Scheda di Audit
  - Profili professionali delle figure chiave
- Formato: Markdown (.md)

#### d) CV Figure Professionali
- CV sintetico di Alexander Schneider (Esperto Trasformazione Digitale)
- CV sintetico di Elmar Schneider (Analista Innovazione di Processo)
- Formato: Markdown (.md), documenti separati

#### e) Foglio Ore per Assessment
- Riepilogo ore per figura professionale (40 ore totali per assessment)
- Dettaglio attività svolte con ore per ciascuna
- Riepilogo complessivo con importi (tariffa 250 €/h)
- Spazio firme (responsabile progetto e beneficiario)
- Formato: Markdown (.md)

**Generazione DOCX (frontend):**
- Conversione automatica da Markdown a formato Microsoft Word (.docx)
- Font: Courier New (monospaced professionale)
- Intestazioni gerarchiche (H1, H2, H3)
- Paragrafi formattati con spaziatura professionale
- Elenchi puntati e grassetti
- Download diretto dal browser

---

### 3.6 Assistente AI Integrato

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

### 3.7 Pannello di Amministrazione

**Descrizione:** Dashboard di gestione completa per gli amministratori del programma DIH, protetta da chiave di accesso amministrativa.

**Funzionalità:**

#### Gestione Organizzazioni
- Elenco completo delle organizzazioni registrate con filtri e ricerca
- Visualizzazione dettagli anagrafici
- Reset password per organizzazioni
- Eliminazione organizzazioni

#### Gestione Assessment
- Elenco assessment per organizzazione con stato (in corso, completato)
- Visualizzazione dettagliata di ogni assessment:
  - Punteggi per area tematica
  - Livello di maturità complessivo
  - Report completo in Markdown con rendering formattato
  - Scheda di audit
- Rigenerazione report su richiesta
- Eliminazione assessment

#### Visualizzazione Risposte Dettagliate
- Modal a schermo intero con tutte le risposte raggruppate per categoria
- Per ogni domanda: testo, tutte le opzioni disponibili, opzione selezionata evidenziata con punteggio
- Funzionalità di stampa professionale con layout formattato (Courier New)

#### Download Documentazione
- **Report DOCX**: Report di maturità digitale in formato Microsoft Word
- **Scheda Audit**: Download scheda audit in Markdown
- **Doc. DIH**: Pacchetto documentazione completa (report + audit + profili)
- **CV**: Download CV separati delle figure professionali
- **Foglio Ore**: Generazione e download foglio ore specifico per assessment
- **Risposte**: Visualizzazione e stampa risposte dettagliate

#### Sicurezza
- Autenticazione tramite chiave amministrativa (ADMIN_SECRET)
- Tutte le operazioni richiedono validazione della chiave
- Chiave configurabile tramite variabile d'ambiente

---

### 3.8 Dashboard Utente

**Descrizione:** Interfaccia per i beneficiari che mostra lo stato degli assessment e i risultati ottenuti.

**Funzionalità:**
- Panoramica assessment completati e in corso
- Accesso ai risultati con visualizzazione grafica:
  - Radar chart multidimensionale per aree tematiche
  - Barre comparative per punteggi di area
  - Indicatore livello di maturità complessivo
- Accesso all'assessment di Livello 2 (se idoneo)
- Download report in formato DOCX

---

## 4. API REST — ENDPOINTS

### 4.1 Autenticazione

| Metodo | Endpoint | Descrizione |
|--------|----------|-------------|
| POST | `/api/auth/register` | Registrazione nuova organizzazione |
| POST | `/api/auth/login` | Login con codice di accesso e password |

### 4.2 Questionario

| Metodo | Endpoint | Descrizione |
|--------|----------|-------------|
| GET | `/api/questions/` | Elenco domande Livello 1 (filtrate per tipologia) |
| GET | `/api/questions/categories` | Elenco categorie disponibili |
| GET | `/api/questions-level2/` | Elenco domande Livello 2 |
| GET | `/api/questions-level2/check-eligibility` | Verifica idoneità Livello 2 |

### 4.3 Assessment

| Metodo | Endpoint | Descrizione |
|--------|----------|-------------|
| POST | `/api/assessments/` | Creazione nuovo assessment |
| POST | `/api/assessments/{id}/submit` | Invio risposte e analisi |
| GET | `/api/assessments/` | Elenco assessment dell'organizzazione |
| GET | `/api/assessments/{id}` | Dettaglio singolo assessment |

### 4.4 Assistente AI

| Metodo | Endpoint | Descrizione |
|--------|----------|-------------|
| POST | `/api/assistant/chat` | Invio messaggio all'assistente AI |

### 4.5 Amministrazione

| Metodo | Endpoint | Descrizione |
|--------|----------|-------------|
| GET | `/api/admin/organizations` | Elenco organizzazioni |
| GET | `/api/admin/organizations/{id}/assessments` | Assessment per organizzazione |
| GET | `/api/admin/assessments/{id}` | Dettaglio assessment |
| GET | `/api/admin/assessments/{id}/responses` | Risposte dettagliate assessment |
| GET | `/api/admin/assessments/{id}/timesheet` | Foglio ore assessment |
| POST | `/api/admin/assessments/{id}/regenerate` | Rigenerazione report |
| DELETE | `/api/admin/assessments/{id}` | Eliminazione assessment |
| POST | `/api/admin/reset-password` | Reset password organizzazione |
| DELETE | `/api/admin/organizations/{id}` | Eliminazione organizzazione |
| GET | `/api/admin/staff-profiles` | Profili figure professionali |
| GET | `/api/admin/staff-cvs` | CV figure professionali |

---

## 5. SICUREZZA

### 5.1 Crittografia
- Tutte le comunicazioni avvengono tramite **HTTPS** con certificati SSL/TLS
- Le password sono crittografate con algoritmo **bcrypt** (hashing irreversibile)
- La connessione al database è protetta da **SSL/TLS**

### 5.2 Autenticazione e autorizzazione
- Autenticazione utenti tramite **codice di accesso + password**
- Autenticazione amministrativa tramite **chiave segreta** (ADMIN_SECRET)
- Separazione dei ruoli: utente (beneficiario) e amministratore
- Validazione di tutti gli input lato server

### 5.3 Protezione dati
- Conformità al **Regolamento UE 2016/679 (GDPR)**
- Dati personali trattati esclusivamente per le finalità del programma DIH
- Backup giornaliero automatico del database
- Nessun dato sensibile esposto nelle API pubbliche

### 5.4 Variabili d'ambiente
Le credenziali e configurazioni sensibili sono gestite tramite variabili d'ambiente server-side, mai incluse nel codice sorgente:
- `DATABASE_URL` — Stringa di connessione al database
- `ADMIN_SECRET` — Chiave di accesso amministrativo
- `OPENAI_API_KEY` — Chiave API per assistente AI
- `VITE_API_URL` — URL del backend per il frontend

---

## 6. PERFORMANCE E SCALABILITÀ

| Parametro | Specifica |
|-----------|-----------|
| **Tempo di risposta API** | < 500ms (95° percentile) |
| **Tempo generazione report** | < 3 secondi |
| **Utenti concorrenti** | Fino a 100 simultanei |
| **Dimensione database** | Scalabile automaticamente (Neon serverless) |
| **Frontend** | CDN globale con edge caching (Vercel) |
| **Backend** | Container Docker con auto-restart |
| **Disponibilità target** | 99,5% su base mensile |

---

## 7. MANUTENZIONE E AGGIORNAMENTI

### 7.1 Deploy continuo
- **Backend**: Deploy automatico su push al repository Git (Render)
- **Frontend**: Deploy automatico su push al repository Git (Vercel)
- Tempo di deploy: ~3-5 minuti per componente

### 7.2 Monitoraggio
- Log applicativi in tempo reale (Render dashboard)
- Monitoraggio uptime e performance (provider-level)
- Alert automatici in caso di errori critici

### 7.3 Backup
- Database: backup automatico giornaliero con retention 30 giorni (Neon)
- Codice sorgente: versionato su repository Git privato (GitHub)

---

## 8. REQUISITI DEL BENEFICIARIO

Per l'utilizzo della Piattaforma, il beneficiario necessita esclusivamente di:
- Browser web moderno (Chrome, Firefox, Safari, Edge — ultime 2 versioni)
- Connessione internet
- Nessuna installazione software richiesta

---

## 9. PROPRIETÀ E LICENZE

- Il codice sorgente della Piattaforma è di **proprietà esclusiva del Fornitore**
- Tutte le librerie e framework utilizzati sono rilasciati con **licenze open source** (MIT, Apache 2.0, BSD, ISC, PSF, PostgreSQL License) compatibili con l'uso commerciale
- L'unico componente con licenza commerciale è l'API OpenAI per l'assistente AI, il cui costo è incluso nel canone di noleggio

---

*Documento redatto come Allegato A al Contratto di Noleggio Piattaforma Software — Digital Maturity Assessment Platform*

*Rome Digital Innovation Hub in collaborazione con Il Borgo Urbano*
