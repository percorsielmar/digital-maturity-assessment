# Setup Locale - Digital Maturity Assessment

## Prerequisiti
- **Python 3.9+** installato
- **Node.js 18+** e npm installati
- Nessun Docker necessario

---

## 1. Backend (FastAPI + SQLite)

```bash
cd backend

# Installa dipendenze
pip install -r requirements.txt

# Crea cartella dati (se non esiste)
mkdir data

# Avvia il server
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Il backend sarà disponibile su `http://localhost:8000`.
Il database SQLite viene creato automaticamente in `backend/data/maturity.db`.

### Variabili d'ambiente (opzionali)
Crea un file `backend/.env` se necessario:

```env
SECRET_KEY=una-chiave-segreta-di-almeno-32-caratteri
DATABASE_URL=sqlite+aiosqlite:///./data/maturity.db
OPENAI_API_KEY=sk-...  # Solo se vuoi l'assistente AI attivo
```

Se non viene creato il `.env`, il backend usa SQLite locale di default.

---

## 2. Frontend (React + Vite)

```bash
cd frontend

# Installa dipendenze
npm install

# Crea .env per puntare al backend locale
echo VITE_API_URL=http://localhost:8000/api > .env

# Avvia il dev server
npm run dev
```

Il frontend sarà disponibile su `http://localhost:3000` (o porta successiva se occupata).

---

## 3. Verifica

1. Apri `http://localhost:3000` nel browser
2. Registra un'organizzazione di test
3. Completa un assessment
4. Verifica il report

API docs disponibili su `http://localhost:8000/docs`.

---

## Note per agenti AI

### Compatibilità Python 3.9
- NON usare `str | None` → usare `Optional[str]` da `typing`
- NON usare `list[str]` → usare `List[str]` da `typing`
- Aggiungere sempre `from typing import Optional, List` dove necessario

### SQLite vs PostgreSQL
- In locale il default è **SQLite** (`sqlite+aiosqlite:///./data/maturity.db`)
- In produzione (Render/Neon) si usa **PostgreSQL** impostando `DATABASE_URL` nel `.env`
- SQLite NON supporta `ALTER TABLE ... ADD COLUMN IF NOT EXISTS` — le migration usano `PRAGMA table_info()` per verificare prima

### Struttura progetto
```
backend/
  main.py              # Entry point, lifespan, migrations, seed
  app/
    config.py           # Settings (DATABASE_URL, SECRET_KEY, ecc.)
    database.py         # Engine SQLAlchemy async
    models.py           # Modelli ORM (Organization, Assessment, Question)
    schemas.py          # Pydantic schemas
    auth.py             # Autenticazione JWT
    crew_agents.py      # Analisi e generazione report
    questions_data.py   # Domande livello 1
    questions_level2_data.py  # Domande livello 2
    routers/
      auth.py           # Login, registrazione, Google OAuth
      questions.py      # API domande
      assessments.py    # API assessment
      admin.py          # Dashboard admin
      assistant.py      # Chat AI assistente
      questions_level2.py  # API domande livello 2

frontend/
  src/
    api.ts              # Client API axios
    types.ts            # TypeScript types
    context/            # Auth context
    components/         # Pagine React
```

### Porte
| Servizio | Porta |
|----------|-------|
| Backend  | 8000  |
| Frontend | 3000  |
