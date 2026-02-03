# Digital Maturity Assessment

Applicazione web per la valutazione della maturità digitale di aziende e Pubbliche Amministrazioni.

## Caratteristiche

- **Accesso riservato**: Ogni organizzazione ha un codice di accesso univoco
- **Questionario strutturato**: 20 domande su 7 aree di maturità digitale
- **Analisi automatica**: Scoring e gap analysis con CrewAI
- **Report professionale**: Output dettagliato con raccomandazioni
- **Modalità Kiosk**: Ottimizzato per tablet dedicati

## Architettura

```
digital-maturity-assessment/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── routers/        # API endpoints
│   │   ├── models.py       # Database models
│   │   ├── schemas.py      # Pydantic schemas
│   │   ├── auth.py         # Authentication
│   │   ├── crew_agents.py  # CrewAI agents
│   │   └── questions_data.py
│   ├── main.py
│   └── requirements.txt
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/
│   │   ├── context/
│   │   └── api.ts
│   └── package.json
└── data/                   # SQLite database
```

## Installazione

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

Crea un file `.env` nella cartella backend:
```env
SECRET_KEY=your-secret-key-min-32-characters-long
OPENAI_API_KEY=your-openai-api-key  # Opzionale, per CrewAI
```

Avvia il server:
```bash
python main.py
# oppure
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Utilizzo

1. **Registrazione**: L'organizzazione si registra e riceve un codice di accesso univoco
2. **Login**: Accesso con codice e password dal tablet kiosk
3. **Assessment**: Compilazione del questionario (20 domande)
4. **Analisi**: Il sistema elabora le risposte con CrewAI
5. **Report**: Visualizzazione e download del report di maturità

## Aree di Valutazione

1. **Strategia Digitale** - Visione, leadership, investimenti
2. **Infrastruttura e Tecnologia** - Cloud, integrazione, cybersecurity
3. **Processi e Operazioni** - Automazione, documentale, collaborazione
4. **Dati e Analytics** - Governance, BI, data-driven
5. **Competenze e Cultura** - Skills, formazione, change management
6. **Customer Experience** - Canali digitali, servizi online, feedback
7. **Innovazione** - Tecnologie emergenti, ecosistema

## CrewAI Agents

L'applicazione utilizza 3 agenti AI:

1. **Intervistatore**: Raccoglie e organizza le risposte
2. **Analista**: Calcola score e identifica gap
3. **Redattore**: Genera il report professionale

> Nota: Se `OPENAI_API_KEY` non è configurata, il sistema usa un algoritmo di scoring locale.

## Configurazione Kiosk

Per bloccare il tablet sulla pagina di accesso:

### Android (Chrome)
1. Impostazioni > App > Chrome > Imposta come app predefinita
2. Usa un'app di kiosk mode (es. Kiosk Browser)
3. Configura l'URL: `http://[server-ip]:3000`

### iOS (Safari)
1. Impostazioni > Generali > Accessibilità > Accesso Guidato
2. Apri Safari all'URL dell'app
3. Attiva Accesso Guidato

### Windows
1. Usa la modalità kiosk di Windows
2. Configura Edge/Chrome in modalità app

## API Endpoints

| Metodo | Endpoint | Descrizione |
|--------|----------|-------------|
| POST | `/api/auth/register` | Registra organizzazione |
| POST | `/api/auth/login` | Login |
| GET | `/api/auth/me` | Info organizzazione corrente |
| GET | `/api/questions/` | Lista domande |
| POST | `/api/assessments/` | Crea assessment |
| GET | `/api/assessments/` | Lista assessment |
| POST | `/api/assessments/{id}/submit` | Invia risposte |
| GET | `/api/assessments/{id}/report` | Ottieni report |

## Licenza

MIT License
