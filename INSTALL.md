# Digital Maturity Assessment Platform — Guida all'Installazione

## Contenuto dell'Archivio

Questo archivio contiene il codice sorgente completo della piattaforma **Digital Maturity Assessment**, comprensiva di:

- **Backend** (Python/FastAPI) — API REST, motore di analisi AI, generazione report
- **Frontend** (React/TypeScript/Vite) — Interfaccia utente con landing page, portali di accesso, dashboard
- **Documentazione** — Specifiche tecniche e contratti

## Requisiti di Sistema

- **Python** 3.10+ (consigliato 3.11)
- **Node.js** 18+ (consigliato 20 LTS)
- **npm** 9+
- **Git** (opzionale, per aggiornamenti)

## Installazione

### 1. Backend

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

Creare un file `.env` nella cartella `backend/`:

```env
DATABASE_URL=sqlite+aiosqlite:///./data/maturity.db
SECRET_KEY=your-secret-key-here
OPENAI_API_KEY=your-openai-api-key
```

Avviare il server:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Il backend sarà disponibile su `http://localhost:8000`

### 2. Frontend

```bash
cd frontend
npm install
```

Creare un file `.env` nella cartella `frontend/`:

```env
VITE_API_URL=http://localhost:8000/api
```

Avviare il server di sviluppo:

```bash
npm run dev
```

Il frontend sarà disponibile su `http://localhost:3000`

### 3. Build di Produzione (Frontend)

```bash
cd frontend
npm run build
```

I file compilati saranno nella cartella `frontend/dist/`.

## Struttura del Progetto

```
digital-maturity-assessment/
├── backend/
│   ├── main.py                          # Entry point FastAPI
│   ├── requirements.txt                 # Dipendenze Python
│   └── app/
│       ├── models.py                    # Modelli SQLAlchemy
│       ├── schemas.py                   # Schemi Pydantic
│       ├── crew_agents.py               # Motore AI e generazione report
│       ├── questions_data.py            # Domande DMA
│       ├── questions_iso56002_data.py   # Domande ISO 56002
│       ├── questions_governance_data.py # Domande Governance
│       ├── questions_patto_di_senso_data.py # Domande Patto di Senso
│       └── routers/
│           ├── auth.py                  # Autenticazione
│           ├── assessments.py           # Assessment CRUD
│           ├── questions.py             # API domande DMA
│           ├── questions_iso56002.py    # API domande ISO 56002
│           ├── questions_governance.py  # API domande Governance
│           └── questions_patto_di_senso.py # API domande Patto di Senso
├── frontend/
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   └── src/
│       ├── App.tsx                      # Routing principale
│       ├── api.ts                       # Client API
│       └── components/
│           ├── LandingPage.tsx          # Landing page AI-powered
│           ├── LoginPage.tsx            # Pagina di login
│           ├── Dashboard.tsx            # Dashboard utente
│           ├── AssessmentPage.tsx        # Pagina assessment
│           ├── ReportPage.tsx           # Visualizzazione report
│           └── AdminPage.tsx            # Pannello amministrativo
└── docs/                                # Documentazione tecnica
```

## Portali Disponibili

| Portale | Route | Programma |
|---------|-------|-----------|
| Landing Page | `/` | Hub principale |
| Maturità Digitale | `/maturita-digitale` | `dma` |
| ISO 56002 | `/iso56002` | `iso56002` |
| Governance Trasparente | `/governance` | `governance` |
| Patto di Senso | `/patto-di-senso` | `patto_di_senso` |
| Admin | `/admin` | — |

## Credenziali Admin

- **URL:** `/admin`
- **Password:** configurata nel backend

## Licenza e Proprietà

Software proprietario — Rome Digital Innovation Hub / Il Borgo Urbano.
Tutti i diritti riservati. Vietata la riproduzione non autorizzata.

## Versione

- **Data:** Febbraio 2026
- **Commit:** vedi file `.git/` o eseguire `git log -1`
