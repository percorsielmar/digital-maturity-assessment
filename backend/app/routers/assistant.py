from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
import httpx

router = APIRouter(prefix="/assistant", tags=["assistant"])

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

class AssistantRequest(BaseModel):
    question_text: str
    question_hint: str = ""
    options: list[str] = []
    user_message: str
    organization_type: str = "azienda"
    organization_sector: str = ""

class AssistantResponse(BaseModel):
    response: str

SYSTEM_PROMPT = """Sei un assistente esperto in trasformazione digitale e maturità digitale delle organizzazioni.
Il tuo compito è aiutare gli utenti a rispondere correttamente alle domande di un questionario di valutazione della maturità digitale.

Quando l'utente ti chiede aiuto su una domanda:
1. Spiega in modo semplice cosa significa la domanda
2. Dai esempi pratici per ogni opzione di risposta
3. Aiuta l'utente a capire quale opzione descrive meglio la sua situazione
4. Se l'utente descrive la sua situazione, suggerisci quale opzione potrebbe essere più appropriata

Rispondi sempre in italiano, in modo chiaro e conciso. Non fare domande retoriche, vai dritto al punto.
Se non hai abbastanza informazioni per suggerire una risposta specifica, chiedi dettagli sulla situazione dell'organizzazione."""

@router.post("/chat", response_model=AssistantResponse)
async def chat_with_assistant(request: AssistantRequest):
    if not OPENAI_API_KEY:
        return AssistantResponse(
            response="⚠️ L'assistente AI non è configurato. Contatta l'amministratore per attivare questa funzionalità.\n\n"
                     f"**Suggerimento dalla guida:**\n{request.question_hint}" if request.question_hint else 
                     "⚠️ L'assistente AI non è configurato. Usa il pulsante '?' per vedere il suggerimento."
        )
    
    context = f"""
Domanda del questionario: {request.question_text}

Opzioni disponibili:
{chr(10).join([f"- {opt}" for opt in request.options])}

Suggerimento/Contesto: {request.question_hint}

Tipo organizzazione: {request.organization_type}
Settore: {request.organization_sector or 'Non specificato'}

Messaggio dell'utente: {request.user_message}
"""

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENAI_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "gpt-3.5-turbo",
                    "messages": [
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": context}
                    ],
                    "max_tokens": 500,
                    "temperature": 0.7
                },
                timeout=30.0
            )
            
            if response.status_code != 200:
                return AssistantResponse(
                    response=f"Errore nella comunicazione con l'AI. Usa il suggerimento: {request.question_hint}"
                )
            
            data = response.json()
            ai_response = data["choices"][0]["message"]["content"]
            return AssistantResponse(response=ai_response)
            
    except Exception as e:
        return AssistantResponse(
            response=f"Errore temporaneo. Usa il suggerimento: {request.question_hint}"
        )
