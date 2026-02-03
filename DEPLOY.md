# Guida al Deploy - Vercel + Render

## Prerequisiti
- Account GitHub
- Account Vercel (https://vercel.com)
- Account Render (https://render.com)

---

## 1. Carica su GitHub

```bash
cd C:\Users\Alex\CascadeProjects\digital-maturity-assessment
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/TUO-USERNAME/digital-maturity-assessment.git
git push -u origin main
```

---

## 2. Deploy Backend su Render

1. Vai su https://render.com e accedi con GitHub
2. Clicca **New > Web Service**
3. Connetti il repository GitHub
4. Configura:
   - **Name**: `digital-maturity-api`
   - **Root Directory**: `backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Aggiungi **Environment Variables**:
   - `SECRET_KEY` = (genera una stringa random di 32+ caratteri)
6. Clicca **Create Web Service**
7. Attendi il deploy (~3-5 minuti)
8. Copia l'URL (es. `https://digital-maturity-api.onrender.com`)

---

## 3. Deploy Frontend su Vercel

1. Vai su https://vercel.com e accedi con GitHub
2. Clicca **Add New > Project**
3. Importa il repository GitHub
4. Configura:
   - **Root Directory**: `frontend`
   - **Framework Preset**: `Vite`
5. Aggiungi **Environment Variables**:
   - `VITE_API_URL` = `https://digital-maturity-api.onrender.com/api`
   (usa l'URL del backend da Render)
6. Clicca **Deploy**
7. Attendi il deploy (~1-2 minuti)

---

## 4. Verifica

1. Apri l'URL Vercel (es. `https://digital-maturity-xxx.vercel.app`)
2. Registra un'organizzazione di test
3. Completa un assessment
4. Verifica il report

---

## Note importanti

### Cold Start (Render Free Tier)
Il backend su Render si spegne dopo 15 minuti di inattività. 
Il primo accesso dopo l'inattività richiede ~30 secondi.

### Database
SQLite viene ricreato ad ogni deploy su Render (piano gratuito).
Per persistenza, considera:
- Render PostgreSQL ($7/mese)
- Supabase (gratis)
- PlanetScale (gratis)

### Dominio personalizzato
Entrambi i servizi supportano domini personalizzati gratuitamente.

---

## Costi stimati (30 audit/mese)

| Servizio | Piano | Costo |
|----------|-------|-------|
| Vercel | Hobby | **Gratis** |
| Render | Free | **Gratis** |
| **Totale** | | **$0/mese** |
