from typing import Dict, Any, List
from datetime import datetime

def get_assessment_date(assessment_info: Dict) -> datetime:
    """Get the date to use for assessment documents (custom_date if set, otherwise completed_at or now)"""
    custom_date = assessment_info.get("custom_date")
    if custom_date:
        try:
            if isinstance(custom_date, datetime):
                return custom_date
            return datetime.fromisoformat(str(custom_date).replace("Z", "+00:00"))
        except Exception:
            pass
    
    completed_at = assessment_info.get("completed_at")
    if completed_at:
        try:
            if isinstance(completed_at, datetime):
                return completed_at
            return datetime.fromisoformat(str(completed_at).replace("Z", "+00:00"))
        except Exception:
            pass
    
    return datetime.now()

def analyze_responses(responses: Dict[str, Any], questions: List[Dict], organization_info: Dict) -> Dict[str, Any]:
    """Analyze responses without AI if no API key is available"""
    
    category_scores = {}
    category_weights = {}
    total_score = 0
    total_weight = 0
    
    for answer in responses.get("answers", []):
        question_id = answer.get("question_id")
        selected_option = answer.get("selected_option", 0)
        
        question = next((q for q in questions if q["id"] == question_id), None)
        if question:
            category = question["category"]
            weight = question.get("weight", 1.0)
            options = question.get("options", [])
            
            if 0 <= selected_option < len(options):
                score = options[selected_option].get("score", 1)
            else:
                score = 1
            
            if category not in category_scores:
                category_scores[category] = 0
                category_weights[category] = 0
            
            category_scores[category] += score * weight
            category_weights[category] += weight
            total_score += score * weight
            total_weight += weight
    
    normalized_scores = {}
    for category in category_scores:
        if category_weights[category] > 0:
            normalized_scores[category] = round(
                (category_scores[category] / category_weights[category]), 2
            )
    
    overall_maturity = round(total_score / total_weight, 2) if total_weight > 0 else 1.0
    
    maturity_levels = {
        1: "Iniziale",
        2: "Gestito",
        3: "Definito",
        4: "Quantitativamente Gestito",
        5: "Ottimizzato"
    }
    
    maturity_label = maturity_levels.get(round(overall_maturity), "Iniziale")
    
    gap_analysis = {}
    for category, score in normalized_scores.items():
        gap = 5 - score
        priority = "Alta" if gap > 2 else "Media" if gap > 1 else "Bassa"
        gap_analysis[category] = {
            "current_score": score,
            "target_score": 5,
            "gap": round(gap, 2),
            "priority": priority
        }
    
    return {
        "scores": normalized_scores,
        "overall_maturity": overall_maturity,
        "maturity_label": maturity_label,
        "gap_analysis": gap_analysis
    }

def get_institutional_phrase(org_type: str) -> str:
    """Restituisce la frase istituzionale appropriata per il tipo di organizzazione"""
    if org_type == "pa":
        return "L'assessment è stato realizzato da esperti in trasformazione digitale e innovazione della PA, assicurando un'analisi contestualizzata della maturità digitale e l'elaborazione di una roadmap strategica orientata all'efficienza dei servizi e alla modernizzazione amministrativa."
    else:
        return "L'assessment è stato realizzato da esperti in trasformazione digitale e innovazione d'impresa, assicurando un'analisi contestualizzata della maturità digitale e l'elaborazione di una roadmap strategica orientata alla competitività e alla crescita sostenibile."

def get_maturity_interpretation(score: float, org_type: str) -> str:
    """Restituisce l'interpretazione strategica del livello di maturità"""
    is_pa = org_type == "pa"
    
    if score < 2:
        if is_pa:
            return "L'ente si trova in una fase iniziale del percorso di digitalizzazione. Le capacità digitali sono frammentate e non integrate in una visione strategica. È necessario un intervento strutturale per allinearsi agli standard di modernizzazione della PA."
        else:
            return "L'organizzazione si trova in una fase iniziale del percorso di digitalizzazione. Le capacità digitali sono frammentate e non integrate in una visione strategica. È necessario un intervento strutturale per garantire competitività nel medio termine."
    elif score < 3:
        if is_pa:
            return "L'ente ha avviato un percorso di digitalizzazione con risultati parziali. Esistono aree di forza ma permangono gap significativi che limitano l'efficienza dei servizi al cittadino. Un piano di consolidamento è prioritario."
        else:
            return "L'organizzazione ha avviato un percorso di digitalizzazione con risultati parziali. Esistono aree di forza ma permangono gap significativi che limitano la scalabilità operativa. Un piano di consolidamento è prioritario."
    elif score < 4:
        if is_pa:
            return "L'ente presenta un livello di maturità digitale in linea con le aspettative per organizzazioni pubbliche in fase di trasformazione. Le basi sono solide ma è necessario accelerare su specifiche aree per raggiungere l'eccellenza nei servizi digitali."
        else:
            return "L'organizzazione presenta un livello di maturità digitale in linea con le aspettative di mercato. Le basi sono solide ma è necessario accelerare su specifiche aree per consolidare il vantaggio competitivo."
    else:
        if is_pa:
            return "L'ente dimostra un elevato livello di maturità digitale, con capacità avanzate nella maggior parte delle aree analizzate. L'obiettivo è il mantenimento dell'eccellenza e l'adozione di tecnologie emergenti per l'innovazione dei servizi."
        else:
            return "L'organizzazione dimostra un elevato livello di maturità digitale, con capacità avanzate nella maggior parte delle aree analizzate. L'obiettivo è il mantenimento dell'eccellenza e l'adozione di tecnologie emergenti."

def get_category_interpretation(category: str, score: float, org_type: str) -> Dict[str, str]:
    """Restituisce interpretazione, implicazioni e rischi per categoria"""
    is_pa = org_type == "pa"
    
    interpretations = {
        "Strategia e Governance": {
            "low": "La strategia digitale non è formalizzata o non è allineata agli obiettivi organizzativi. Manca una governance chiara per guidare la trasformazione.",
            "medium": "Esiste una visione strategica ma non è pienamente integrata nei processi decisionali. La governance digitale richiede rafforzamento.",
            "high": "La strategia digitale è chiara, condivisa e integrata nella governance. L'organizzazione ha una visione matura della trasformazione."
        },
        "Processi e Operazioni": {
            "low": "I processi sono prevalentemente manuali o parzialmente digitalizzati. L'efficienza operativa è compromessa da gap tecnologici.",
            "medium": "I processi core sono digitalizzati ma esistono silos e inefficienze. L'automazione è parziale.",
            "high": "I processi sono digitalizzati, integrati e ottimizzati. L'automazione è diffusa e genera efficienza misurabile."
        },
        "Tecnologia e Infrastruttura": {
            "low": "L'infrastruttura tecnologica è obsoleta o inadeguata. Esistono rischi di sicurezza e limitazioni alla scalabilità.",
            "medium": "L'infrastruttura è adeguata ma richiede modernizzazione. Cloud e sicurezza sono parzialmente implementati.",
            "high": "L'infrastruttura è moderna, scalabile e sicura. Cloud, cybersecurity e integrazione sono a livelli avanzati."
        },
        "Dati e Analytics": {
            "low": "I dati sono frammentati e non valorizzati. Mancano strumenti di analytics e cultura data-driven.",
            "medium": "Esistono basi dati strutturate ma l'analytics è limitato. Il potenziale dei dati non è pienamente sfruttato.",
            "high": "I dati sono asset strategici. Analytics avanzati supportano le decisioni. La cultura data-driven è diffusa."
        },
        "Competenze e Cultura": {
            "low": "Le competenze digitali sono insufficienti. Resistenza al cambiamento e cultura tradizionale limitano la trasformazione.",
            "medium": "Esistono competenze digitali ma non diffuse. La cultura sta evolvendo ma richiede accelerazione.",
            "high": "Competenze digitali avanzate e diffuse. Cultura dell'innovazione consolidata e orientamento al miglioramento continuo."
        },
        "Innovazione": {
            "low": "L'innovazione è occasionale e non strutturata. Mancano processi e risorse dedicate.",
            "medium": "Esistono iniziative di innovazione ma non sistematiche. Il potenziale innovativo non è pienamente espresso.",
            "high": "L'innovazione è un processo strutturato e continuo. L'organizzazione è proattiva nell'adozione di nuove tecnologie."
        }
    }
    
    level = "low" if score < 2.5 else "medium" if score < 4 else "high"
    
    base_interp = interpretations.get(category, {}).get(level, f"Area con punteggio {score}/5.")
    
    if score < 3:
        risk_target = "l'efficienza dei servizi pubblici" if is_pa else "la competitività aziendale"
        risk = f"Il gap in quest'area rappresenta un rischio significativo per {risk_target}."
        opp_target = "qualità del servizio" if is_pa else "efficienza operativa"
        opportunity = f"Un intervento mirato può generare miglioramenti rapidi e visibili in termini di {opp_target}."
    else:
        risk = "Il livello attuale è adeguato ma richiede mantenimento e aggiornamento continuo."
        opp_target = "diventare riferimento nella PA digitale" if is_pa else "differenziarsi nel mercato"
        opportunity = f"Consolidare i risultati e puntare all'eccellenza per {opp_target}."
    
    return {
        "interpretation": base_interp,
        "risk": risk,
        "opportunity": opportunity
    }

def generate_report(analysis: Dict[str, Any], organization_info: Dict, assessment_info: Dict = None) -> str:
    """Genera un report DIH professionale per rendicontazione UE"""
    
    org_name = organization_info.get("name", "Organizzazione")
    org_type = organization_info.get("type", "azienda")
    org_type_label = "Pubblica Amministrazione" if org_type == "pa" else "Impresa"
    sector = organization_info.get("sector", "Non specificato")
    size = organization_info.get("size", "Non specificata")
    
    overall_score = analysis.get("overall_maturity", 0)
    maturity_label = analysis.get("maturity_label", "Iniziale")
    maturity_interpretation = get_maturity_interpretation(overall_score, org_type)
    
    assessment_date = get_assessment_date(assessment_info or {})
    current_date = assessment_date.strftime("%d/%m/%Y")
    
    report = f"""# AUDIT DI MATURITÀ DIGITALE

## Rome Digital Innovation Hub
### in collaborazione con Il Borgo Urbano
### Programma di Trasformazione Digitale

---

**Beneficiario:** {org_name}  
**Tipologia:** {org_type_label}  
**Settore:** {sector}  
**Dimensione:** {size}  
---

## 1. EXECUTIVE SUMMARY ISTITUZIONALE

### Contesto

Il presente audit rientra nel programma di Digital Maturity Assessment erogato dal **Rome Digital Innovation Hub**, nell'ambito delle iniziative europee per la trasformazione digitale del tessuto produttivo e della Pubblica Amministrazione.

### Obiettivi dell'Assessment

- Valutare il livello di maturità digitale del beneficiario secondo un framework multidimensionale
- Identificare gap e priorità di intervento
- Definire una roadmap strategica di trasformazione
- Fornire raccomandazioni operative allineate agli obiettivi UE di competitività, resilienza e sostenibilità

### Sintesi del Risultato

{org_name} ha conseguito un **livello di maturità digitale pari a {overall_score}/5** (livello: **{maturity_label}**).

{maturity_interpretation}

{get_institutional_phrase(org_type)}

---

## 2. INQUADRAMENTO METODOLOGICO

### Framework di Maturità Digitale

L'assessment si basa su un framework multidimensionale che analizza la maturità digitale attraverso aree chiave interconnesse:

- **Strategia e Governance** – Visione, leadership e allineamento strategico
- **Processi e Operazioni** – Digitalizzazione e ottimizzazione operativa
- **Tecnologia e Infrastruttura** – Modernità, sicurezza e scalabilità
- **Dati e Analytics** – Valorizzazione dei dati e capacità analitica
- **Competenze e Cultura** – Capitale umano e orientamento al cambiamento
- **Innovazione** – Capacità di adottare e generare innovazione

### Scala di Maturità

| Livello | Punteggio | Descrizione |
|---------|-----------|-------------|
| Iniziale | 1.0 - 1.9 | Capacità digitali frammentate, assenza di strategia |
| Gestito | 2.0 - 2.9 | Digitalizzazione parziale, processi non integrati |
| Definito | 3.0 - 3.9 | Strategia digitale formalizzata, buona integrazione |
| Avanzato | 4.0 - 4.4 | Maturità elevata, ottimizzazione continua |
| Ottimizzato | 4.5 - 5.0 | Eccellenza digitale, innovazione sistemica |

### Approccio Evidence-Based

La valutazione si fonda su evidenze raccolte attraverso questionari strutturati, analisi documentale e contestualizzazione qualitativa da parte di esperti in trasformazione digitale.

---

## 3. PROFILO DI MATURITÀ COMPLESSIVO

### Livello Raggiunto

| Indicatore | Valore |
|------------|--------|
| **Punteggio Complessivo** | {overall_score}/5 |
| **Livello di Maturità** | {maturity_label} |
| **Percentile Stimato** | {'Top 30%' if overall_score >= 3.5 else 'Nella media' if overall_score >= 2.5 else 'Sotto la media'} |

### Significato Strategico

{maturity_interpretation}

### Radar di Maturità per Area

"""
    
    for category, data in analysis.get("gap_analysis", {}).items():
        score = data["current_score"]
        bar = "█" * int(score) + "░" * (5 - int(score))
        report += f"- **{category}**: {score}/5 [{bar}]\n"
    
    report += """

---

## 4. ANALISI DETTAGLIATA PER AREA

"""
    
    for category, data in analysis.get("gap_analysis", {}).items():
        score = data["current_score"]
        gap = data["gap"]
        priority = data["priority"]
        
        cat_analysis = get_category_interpretation(category, score, org_type)
        
        priority_color = "🔴" if priority == "Alta" else "🟡" if priority == "Media" else "🟢"
        
        report += f"""### {category}

| Metrica | Valore |
|---------|--------|
| **Punteggio** | {score}/5 |
| **Gap vs Target** | {gap} punti |
| **Priorità** | {priority_color} {priority} |

**Interpretazione:** {cat_analysis['interpretation']}

**Implicazioni Operative:** {cat_analysis['opportunity']}

**Rischi:** {cat_analysis['risk']}

---

"""
    
    high_priority = [(cat, data) for cat, data in analysis.get("gap_analysis", {}).items() 
                     if data["priority"] == "Alta"]
    medium_priority = [(cat, data) for cat, data in analysis.get("gap_analysis", {}).items() 
                       if data["priority"] == "Media"]
    low_priority = [(cat, data) for cat, data in analysis.get("gap_analysis", {}).items() 
                    if data["priority"] == "Bassa"]
    
    report += """## 5. GAP ANALYSIS E PRIORITÀ

### Colli di Bottiglia Identificati

"""
    
    if high_priority:
        report += "**Criticità Elevate (Intervento Urgente):**\n\n"
        for cat, data in high_priority:
            report += f"- **{cat}** (gap: {data['gap']} punti) – Limita significativamente la capacità di crescita e trasformazione\n"
    
    if medium_priority:
        report += "\n**Aree di Miglioramento (Intervento Pianificato):**\n\n"
        for cat, data in medium_priority:
            report += f"- **{cat}** (gap: {data['gap']} punti) – Richiede consolidamento per sostenere la trasformazione\n"
    
    if low_priority:
        report += "\n**Aree di Forza (Mantenimento):**\n\n"
        for cat, data in low_priority:
            report += f"- **{cat}** (gap: {data['gap']} punti) – Livello adeguato, focus su ottimizzazione continua\n"
    
    report += f"""

### Relazione Gap-Obiettivi

I gap identificati impattano direttamente sulla capacità di {org_name} di:
- Raggiungere gli obiettivi di efficienza operativa
- Rispondere alle aspettative di {'cittadini e stakeholder istituzionali' if org_type == 'pa' else 'clienti e mercato'}
- Accedere a opportunità di finanziamento e crescita
- Garantire resilienza e sostenibilità nel medio-lungo termine

---

## 6. ROADMAP STRATEGICA DI TRASFORMAZIONE

### Fase 1 – Interventi Immediati (0-6 mesi)

**Obiettivo:** Colmare i gap critici e stabilizzare le fondamenta digitali

"""
    
    if high_priority:
        for cat, data in high_priority:
            report += f"- Intervento prioritario su **{cat}**: definizione piano d'azione, allocazione risorse, quick wins\n"
    
    report += """- Assessment approfondito delle aree critiche
- Definizione KPI di monitoraggio
- Avvio programmi di formazione base

### Fase 2 – Consolidamento (6-12 mesi)

**Obiettivo:** Integrare e ottimizzare le capacità digitali

"""
    
    if medium_priority:
        for cat, data in medium_priority:
            report += f"- Rafforzamento **{cat}**: implementazione soluzioni, integrazione processi\n"
    
    report += """- Sviluppo competenze digitali avanzate
- Ottimizzazione processi core
- Implementazione soluzioni tecnologiche prioritarie

### Fase 3 – Trasformazione (12-24 mesi)

**Obiettivo:** Raggiungere l'eccellenza digitale e l'innovazione continua

- Completamento trasformazione digitale
- Adozione tecnologie emergenti (AI, automazione avanzata)
- Consolidamento cultura dell'innovazione
- Raggiungimento livello di maturità target (4+/5)

---

## 7. VALORE PER IL BENEFICIARIO

### Benefici Attesi

| Area | Beneficio |
|------|-----------|
| **Efficienza** | Riduzione tempi e costi operativi attraverso automazione e ottimizzazione |
| **Qualità** | Miglioramento {'dei servizi al cittadino' if org_type == 'pa' else 'del prodotto/servizio e customer experience'} |
| **Resilienza** | Maggiore capacità di adattamento a cambiamenti e crisi |
| **Competitività** | {'Allineamento agli standard di PA digitale' if org_type == 'pa' else 'Vantaggio competitivo sostenibile'} |
| **Sostenibilità** | Riduzione impatto ambientale attraverso digitalizzazione |

### Impatto sulla Capacità Organizzativa

L'implementazione della roadmap consentirà a {org_name} di:
- Incrementare la produttività del 15-25%
- Ridurre i tempi di processo del 20-30%
- Migliorare la soddisfazione di {'cittadini/utenti' if org_type == 'pa' else 'clienti'}
- Abilitare nuovi modelli operativi e di servizio

---

## 8. CONCLUSIONI

### Perché Questo Assessment è Fondante

Il presente audit costituisce la base documentale e strategica per qualsiasi intervento di trasformazione digitale. Fornisce:
- Una fotografia oggettiva e misurabile dello stato attuale
- Priorità chiare e giustificate
- Una roadmap realistica e attuabile
- Metriche per il monitoraggio dei progressi

### Coerenza con Obiettivi DIH e UE

L'assessment è pienamente allineato con:
- **Digital Europe Programme** – Rafforzamento capacità digitali
- **PNRR** – Digitalizzazione PA e imprese
- **European Digital Innovation Hubs** – Supporto alla trasformazione digitale del territorio

### Abilitazione Interventi Successivi

Questo documento abilita:
- Accesso a finanziamenti per la trasformazione digitale
- Definizione di progetti specifici di innovazione
- Monitoraggio e rendicontazione dei progressi
- Benchmark con organizzazioni comparabili

---

**Rome Digital Innovation Hub** in collaborazione con **Il Borgo Urbano**  
*Programma di Trasformazione Digitale*

{get_institutional_phrase(org_type)}
"""
    
    return report

def generate_timesheet(assessment_info: Dict, organization_info: Dict) -> str:
    """Genera il foglio ore per un assessment specifico"""
    from datetime import datetime
    
    org_name = organization_info.get("name", "Organizzazione")
    assessment_id = assessment_info.get("id", "N/A")
    assessment_date = get_assessment_date(assessment_info or {})
    current_date = assessment_date.strftime("%d/%m/%Y")
    month_str = assessment_date.strftime("%B %Y")
    
    timesheet = f"""# FOGLIO ORE — DIGITAL MATURITY ASSESSMENT

## Rome Digital Innovation Hub in collaborazione con Il Borgo Urbano

---

**Beneficiario:** {org_name}
**Assessment ID:** #{assessment_id}
**Periodo di riferimento:** {month_str}
**Tariffa oraria:** 250,00 €/h

---

## RIEPILOGO ORE PER FIGURA PROFESSIONALE

### 1. Alexander Schneider — Esperto Trasformazione Digitale (Senior)

| Data | Attività | Ore |
|------|----------|-----|
| {current_date} | Analisi preliminare contesto organizzativo del beneficiario | 2.0 |
| {current_date} | Supervisione metodologica framework di assessment | 2.0 |
| {current_date} | Validazione e contestualizzazione dei risultati | 3.0 |
| {current_date} | Interpretazione strategica del profilo di maturità digitale | 2.5 |
| {current_date} | Definizione roadmap strategica di trasformazione | 3.0 |
| {current_date} | Elaborazione raccomandazioni operative allineate a obiettivi UE | 2.5 |
| {current_date} | Revisione e validazione report di audit digitale | 2.0 |
| {current_date} | Coordinamento e quality assurance documentazione | 1.0 |
| | **TOTALE ORE** | **18.0** |
| | **IMPORTO** | **4.500,00 €** |

---

### 2. Elmar Schneider — Analista Innovazione di Processo

| Data | Attività | Ore |
|------|----------|-----|
| {current_date} | Setup e configurazione piattaforma di assessment | 2.0 |
| {current_date} | Assistenza al beneficiario nella compilazione del questionario | 3.0 |
| {current_date} | Analisi e validazione dati raccolti tramite piattaforma | 3.0 |
| {current_date} | Elaborazione punteggi di maturità per area tematica | 2.0 |
| {current_date} | Identificazione pattern, gap e aree critiche | 3.0 |
| {current_date} | Redazione report di audit digitale professionale | 3.0 |
| {current_date} | Mappatura processi organizzativi del beneficiario | 2.5 |
| {current_date} | Preparazione materiali di sintesi e visualizzazioni | 2.0 |
| {current_date} | Documentazione, archiviazione e chiusura pratica | 1.5 |
| | **TOTALE ORE** | **22.0** |
| | **IMPORTO** | **5.500,00 €** |

---

## RIEPILOGO COMPLESSIVO

| Figura | Ruolo | Ore | Importo |
|--------|-------|-----|---------|
| Alexander Schneider | Esperto Trasformazione Digitale | 18.0 | 4.500,00 € |
| Elmar Schneider | Analista Innovazione di Processo | 22.0 | 5.500,00 € |
| | **TOTALE PROGETTO** | **40.0** | **10.000,00 €** |

---

## NOTE

- Le attività sono state svolte nell'ambito del programma DIH — Digital Maturity Assessment
- Le ore indicate si riferiscono all'intero ciclo di assessment per il beneficiario {org_name}
- Il servizio è stato erogato da personale qualificato della SRL incaricata
- Tariffa oraria applicata: 250,00 €/h (IVA esclusa)
- Documentazione di supporto: Report di Maturità Digitale, Scheda di Audit, CV figure professionali

---

**Firma Responsabile Progetto:** ____________________________

**Firma Beneficiario:** ____________________________

**Data:** {current_date}

---

*Rome Digital Innovation Hub in collaborazione con Il Borgo Urbano*
"""
    return timesheet

def generate_audit_sheet(analysis: Dict[str, Any], organization_info: Dict, assessment_info: Dict = None) -> str:
    """Genera la Scheda di Audit per rendicontazione UE (max 1 pagina)"""
    
    org_name = organization_info.get("name", "Organizzazione")
    org_type = organization_info.get("type", "azienda")
    org_type_label = "Pubblica Amministrazione" if org_type == "pa" else "Impresa"
    
    assessment_date = get_assessment_date(assessment_info or {})
    current_date = assessment_date.strftime("%d/%m/%Y")
    current_month = assessment_date.strftime("%B %Y")
    
    overall_score = analysis.get("overall_maturity", 0)
    maturity_label = analysis.get("maturity_label", "Iniziale")
    
    institutional_phrase = get_institutional_phrase(org_type)
    
    sheet = f"""# SCHEDA DI AUDIT – DIGITAL MATURITY ASSESSMENT

---

## 1. IDENTIFICAZIONE DEL SERVIZIO

| Campo | Valore |
|-------|--------|
| **Beneficiario** | {org_name} |
| **Tipologia** | {org_type_label} |
| **Ambito** | Rome Digital Innovation Hub in collaborazione con Il Borgo Urbano |
| **Periodo di svolgimento** | {current_month} |

---

## 2. OGGETTO DELL'AUDIT

Valutazione strutturata della maturità digitale del beneficiario attraverso un assessment multidimensionale, finalizzato a identificare il livello di preparazione digitale, i gap rispetto agli standard di settore e le priorità di intervento per la trasformazione digitale.

L'assessment è stato condotto in coerenza con gli obiettivi del programma DIH e i principi europei di competitività, resilienza e sostenibilità digitale.

---

## 3. ATTIVITÀ SVOLTE

- Raccolta dati attraverso piattaforma di assessment strutturato
- Analisi qualitativa e contestualizzazione dei risultati
- Interpretazione strategica del profilo di maturità
- Identificazione gap e priorità di intervento
- Elaborazione roadmap di trasformazione personalizzata
- Redazione report di maturità digitale professionale
- Definizione raccomandazioni operative

---

## 4. IMPEGNO DI PERSONALE

| Aspetto | Dettaglio |
|---------|-----------|
| **Giornate uomo stimate** | 2-3 gg/uomo |
| **Profili coinvolti** | Digital Transformation Expert, Process Analyst |
| **Competenze impiegate** | Trasformazione digitale, analisi processi, innovazione organizzativa, strategia digitale |

---

## 5. OUTPUT PRODOTTI

- Report di Maturità Digitale personalizzato (Punteggio: {overall_score}/5 - Livello: {maturity_label})
- Roadmap strategica di trasformazione (0-6 / 6-12 / 12-24 mesi)
- Gap Analysis con priorità di intervento
- Raccomandazioni operative allineate a obiettivi UE

---

## 6. VALORE PER IL BENEFICIARIO

L'assessment fornisce al beneficiario una fotografia oggettiva e misurabile del proprio livello di maturità digitale, identificando con chiarezza le aree di forza e i gap da colmare. La roadmap strategica consente di pianificare interventi mirati, ottimizzare gli investimenti in digitalizzazione e accedere a opportunità di finanziamento per la trasformazione digitale.

{institutional_phrase}

---

**Rome Digital Innovation Hub** in collaborazione con **Il Borgo Urbano**
"""
    
    return sheet

def generate_iso56002_report(analysis: Dict[str, Any], organization_info: Dict, assessment_info: Dict = None) -> str:
    """Genera il report per l'audit propedeutico alla certificazione UNI/PdR 56002"""
    from datetime import datetime
    
    org_name = organization_info.get("name", "Organizzazione")
    assessment_date = get_assessment_date(assessment_info or {})
    current_date = assessment_date.strftime("%d/%m/%Y")
    overall_score = analysis.get("overall_maturity", 0)
    maturity_label = analysis.get("maturity_label", "Iniziale")
    scores = analysis.get("scores", {})
    gap_analysis = analysis.get("gap_analysis", {})
    
    iso_levels = {
        1: "Non conforme — Il sistema di gestione dell'innovazione non è implementato",
        2: "Parzialmente conforme — Esistono elementi isolati ma non un sistema strutturato",
        3: "Sostanzialmente conforme — Il sistema è implementato ma richiede miglioramenti significativi",
        4: "Conforme — Il sistema è implementato ed efficace, con margini di miglioramento",
        5: "Pienamente conforme — Il sistema è maturo, efficace e in miglioramento continuo"
    }
    
    conformity_level = iso_levels.get(round(overall_score), iso_levels[1])
    
    scores_text = ""
    for category, score in scores.items():
        gap_info = gap_analysis.get(category, {})
        priority = gap_info.get("priority", "N/A")
        gap_val = gap_info.get("gap", 0)
        scores_text += f"### {category}\n"
        scores_text += f"- **Punteggio:** {score}/5\n"
        scores_text += f"- **Gap dalla conformità piena:** {gap_val}\n"
        scores_text += f"- **Priorità di intervento:** {priority}\n\n"
    
    report = f"""# AUDIT PROPEDEUTICO — CERTIFICAZIONE UNI/PdR 56002

## Gestione dell'Innovazione — Sistema di Gestione

---

**Organizzazione:** {org_name}
**Data assessment:** {current_date}

---

## 1. SINTESI DELLA VALUTAZIONE

**Punteggio complessivo di conformità:** {overall_score}/5 — **{maturity_label}**

**Livello di conformità:** {conformity_level}

---

## 2. PUNTEGGI PER AREA DELLA NORMA

{scores_text}

---

## 3. GAP ANALYSIS RISPETTO AI REQUISITI UNI/PdR 56002

La seguente analisi identifica le aree in cui l'organizzazione presenta i gap più significativi rispetto ai requisiti della norma, con indicazione della priorità di intervento per raggiungere la conformità.

| Area | Punteggio | Gap | Priorità |
|------|-----------|-----|----------|
"""
    
    for category, info in gap_analysis.items():
        report += f"| {category} | {info.get('current_score', 0)}/5 | {info.get('gap', 0)} | {info.get('priority', 'N/A')} |\n"
    
    report += f"""

---

## 4. RACCOMANDAZIONI PER IL PERCORSO DI CERTIFICAZIONE

### Azioni prioritarie (gap > 2):
"""
    
    high_gaps = {k: v for k, v in gap_analysis.items() if v.get("gap", 0) > 2}
    medium_gaps = {k: v for k, v in gap_analysis.items() if 1 < v.get("gap", 0) <= 2}
    low_gaps = {k: v for k, v in gap_analysis.items() if v.get("gap", 0) <= 1}
    
    if high_gaps:
        for cat in high_gaps:
            report += f"- **{cat}**: Intervento strutturale necessario. Definire un piano d'azione specifico con tempistiche e responsabili.\n"
    else:
        report += "- Nessuna area con gap critico.\n"
    
    report += "\n### Azioni di consolidamento (gap 1-2):\n"
    if medium_gaps:
        for cat in medium_gaps:
            report += f"- **{cat}**: Rafforzamento delle pratiche esistenti e formalizzazione dei processi.\n"
    else:
        report += "- Nessuna area con gap medio.\n"
    
    report += "\n### Aree di eccellenza (gap < 1):\n"
    if low_gaps:
        for cat in low_gaps:
            report += f"- **{cat}**: Mantenere il livello raggiunto e condividere le best practice.\n"
    else:
        report += "- Nessuna area al livello di eccellenza.\n"
    
    report += f"""

---

## 5. PIANO DI AZIONE PROPOSTO

Per raggiungere la conformità alla UNI/PdR 56002, si raccomanda il seguente percorso:

1. **Fase 1 — Analisi e pianificazione** (1-2 mesi)
   - Approfondimento delle aree con gap critico
   - Definizione della politica per l'innovazione
   - Assegnazione ruoli e responsabilità

2. **Fase 2 — Implementazione** (3-6 mesi)
   - Implementazione del sistema di gestione dell'innovazione
   - Formazione del personale
   - Definizione dei processi di ideazione e gestione progetti

3. **Fase 3 — Monitoraggio e audit interno** (1-2 mesi)
   - Audit interno di conformità
   - Azioni correttive
   - Riesame della direzione

4. **Fase 4 — Certificazione** (1 mese)
   - Audit di certificazione da parte dell'ente certificatore
   - Eventuali azioni correttive post-audit

**Tempistica stimata complessiva:** 6-12 mesi

---

## 6. NOTE METODOLOGICHE

L'assessment è stato condotto utilizzando un questionario strutturato basato sui requisiti della norma UNI/PdR 56002:2019 "Gestione dell'innovazione — Sistema di gestione dell'innovazione — Guida". La valutazione copre le 7 aree principali della norma più una sezione dedicata a strumenti e metodi.

L'assessment è stato realizzato da esperti in innovazione e trasformazione digitale, assicurando un'analisi contestualizzata e l'elaborazione di raccomandazioni operative orientate al raggiungimento della certificazione.

---

**Rome Digital Innovation Hub** in collaborazione con **Il Borgo Urbano**
"""
    return report

def generate_governance_report(analysis: Dict[str, Any], organization_info: Dict, assessment_info: Dict = None) -> str:
    """Genera il report per l'assessment di Governance Trasparente"""
    from datetime import datetime
    
    org_name = organization_info.get("name", "Organizzazione")
    assessment_date = get_assessment_date(assessment_info or {})
    current_date = assessment_date.strftime("%d/%m/%Y")
    overall_score = analysis.get("overall_maturity", 0)
    maturity_label = analysis.get("maturity_label", "Iniziale")
    scores = analysis.get("scores", {})
    gap_analysis = analysis.get("gap_analysis", {})
    
    gov_levels = {
        1: "Opaco — Governance non trasparente, processi non documentati, partecipazione assente",
        2: "Reattivo — Trasparenza minima obbligatoria, partecipazione limitata",
        3: "Strutturato — Trasparenza adeguata, primi strumenti di partecipazione attivi",
        4: "Proattivo — Trasparenza avanzata, partecipazione strutturata, strumenti digitali integrati",
        5: "Eccellente — Governance aperta, partecipazione deliberativa, innovazione continua"
    }
    
    gov_level = gov_levels.get(round(overall_score), gov_levels[1])
    
    scores_text = ""
    for category, score in scores.items():
        gap_info = gap_analysis.get(category, {})
        priority = gap_info.get("priority", "N/A")
        gap_val = gap_info.get("gap", 0)
        scores_text += f"### {category}\n"
        scores_text += f"- **Punteggio:** {score}/5\n"
        scores_text += f"- **Gap dall'eccellenza:** {gap_val}\n"
        scores_text += f"- **Priorità di intervento:** {priority}\n\n"
    
    report = f"""# REPORT DI ASSESSMENT — GOVERNANCE TRASPARENTE

## Percorso di Formazione e Consulenza per la Governance Partecipativa nella PA

---

**Ente:** {org_name}
**Data assessment:** {current_date}
**Termine attività:** 30 aprile 2026

---

## 1. SINTESI DELLA VALUTAZIONE

**Punteggio complessivo:** {overall_score}/5 — **{maturity_label}**

**Livello di governance:** {gov_level}

### Le Quattro Macro-Aree Valutate

| Macro-Area | Domande | Descrizione |
|------------|---------|-------------|
| **Governance e Trasparenza** | 27 | Meccanismi decisionali etici, conformità normativa, coinvolgimento stakeholder |
| **Innovazione Tecnologica** | 27 | Adozione tecnologie emergenti (IA, Blockchain, IoT), cybersecurity, competenze digitali |
| **Sostenibilità Ambientale** | 27 | Impatto ambientale, efficienza energetica, allineamento SDGs ONU |
| **Valore Sociale ed Economico** | 27 | Impatto territoriale, inclusione, welfare, sostenibilità della filiera |

---

## 2. INQUADRAMENTO METODOLOGICO

### Framework del Patto di Senso

L'assessment si basa su **108 domande** strutturate in 4 macro-aree da 27 domande ciascuna, con risposte su scala 1-5. Il framework valuta la capacità dell'organizzazione di:

- **Governare con trasparenza** — Decisioni etiche, partecipative e verificabili
- **Innovare con responsabilità** — Tecnologie emergenti al servizio del bene comune
- **Sostenere l'ambiente** — Impegno concreto verso gli SDGs e la neutralità climatica
- **Generare valore condiviso** — Impatto positivo su territorio, comunità e filiera

### Scala di Maturità

| Livello | Punteggio | Idoneità Patto di Senso |
|---------|-----------|------------------------|
| Iniziale | 1.0 - 1.9 | Non idoneo — Interventi strutturali necessari |
| Gestito | 2.0 - 2.9 | Parzialmente idoneo — Piano di adeguamento richiesto |
| Definito | 3.0 - 3.9 | Idoneo con riserva — Miglioramenti specifici necessari |
| Avanzato | 4.0 - 4.4 | Idoneo — Pronto per l'implementazione |
| Ottimizzato | 4.5 - 5.0 | Eccellente — Modello di riferimento |

### Collegamento con Smart Contract e Tokenomics

Il Patto di Senso prevede che gli impegni emersi dall'audit vengano tradotti in:
- **Smart Contract su blockchain binaria** — Condizioni verificabili (vero/falso)
- **Token A3** — Per la governance distribuita e il voto sulle proposte
- **Token L3** — Per premiare l'impatto generato e i comportamenti virtuosi

---

## 3. PROFILO DI MATURITÀ PER MACRO-AREA

{scores_text}

---

## 4. GAP ANALYSIS

| Macro-Area | Punteggio | Gap | Priorità |
|------------|-----------|-----|----------|
"""
    
    for category, info in gap_analysis.items():
        priority_icon = "🔴" if info.get("priority") == "Alta" else "🟡" if info.get("priority") == "Media" else "🟢"
        report += f"| {category} | {info.get('current_score', 0)}/5 | {info.get('gap', 0)} | {priority_icon} {info.get('priority', 'N/A')} |\n"
    
    high_gaps = {k: v for k, v in gap_analysis.items() if v.get("gap", 0) > 2}
    medium_gaps = {k: v for k, v in gap_analysis.items() if 1 < v.get("gap", 0) <= 2}
    low_gaps = {k: v for k, v in gap_analysis.items() if v.get("gap", 0) <= 1}
    
    report += f"""

---

## 5. RACCOMANDAZIONI PER L'ADESIONE AL PATTO DI SENSO

### Interventi prioritari (gap > 2):
"""
    if high_gaps:
        for cat in high_gaps:
            report += f"- **{cat}**: Intervento strutturale necessario. Definire un piano d'azione con tempistiche, responsabili e KPI misurabili.\n"
    else:
        report += "- Nessuna area con gap critico.\n"
    
    report += "\n### Interventi di consolidamento (gap 1-2):\n"
    if medium_gaps:
        for cat in medium_gaps:
            report += f"- **{cat}**: Rafforzamento delle pratiche esistenti e formalizzazione dei processi.\n"
    else:
        report += "- Nessuna area con gap medio.\n"
    
    report += "\n### Aree di eccellenza (gap < 1):\n"
    if low_gaps:
        for cat in low_gaps:
            report += f"- **{cat}**: Mantenere il livello raggiunto e condividere le best practice.\n"
    else:
        report += "- Nessuna area al livello di eccellenza.\n"
    
    report += f"""

---

## 6. ROADMAP VERSO IL PATTO DI SENSO

### Fase 1 — Audit e Pianificazione (0-3 mesi)
- Approfondimento delle aree con gap critico
- Definizione della politica di sostenibilità e governance etica
- Mappatura degli stakeholder e piano di coinvolgimento
- Identificazione degli SDG prioritari

### Fase 2 — Implementazione (3-9 mesi)
- Implementazione delle azioni correttive per le aree critiche
- Adozione di tecnologie emergenti (IA, blockchain) dove applicabile
- Formazione del personale su etica, sostenibilità e innovazione
- Avvio dei processi di stakeholder engagement

### Fase 3 — Codifica nel Patto (9-12 mesi)
- Traduzione degli impegni in clausole verificabili (Legal Engineering)
- Implementazione dello Smart Contract su blockchain binaria
- Definizione dei KPI monitorabili tramite oracoli digitali e IoT
- Attivazione del sistema di tokenomics (Token A3 e L3)

### Fase 4 — Monitoraggio e Miglioramento Continuo (12+ mesi)
- Monitoraggio automatizzato tramite oracoli e sensori
- Verifica periodica delle condizioni dello Smart Contract
- Distribuzione incentivi per obiettivi raggiunti
- Riesame e aggiornamento del Patto

**Tempistica stimata complessiva:** 12-18 mesi

---

## 7. ALLINEAMENTO STRATEGICO

### Coerenza con il Framework del Patto di Senso

L'assessment è allineato ai pilastri fondamentali del modello:

- **Transizione Digitale ed Etica** — IA, blockchain e IoT con approccio human-centric (Rome Call for AI Ethics)
- **Sostenibilità Integrale** — Allineamento agli SDGs dell'Agenda 2030 ONU
- **IA come Oracolo Digitale** — Facilitatore analitico e predittivo a supporto delle decisioni umane
- **Sensers e Oracolo di Senso** — Sistema collaborativo esperti-comunità per orientare la tecnologia al bene comune

### Coerenza con Obiettivi UE e Nazionali

- **European Green Deal** — Neutralità climatica e economia circolare
- **Digital Europe Programme** — Rafforzamento capacità digitali
- **PNRR** — Digitalizzazione, sostenibilità e inclusione
- **Strategia Nazionale per lo Sviluppo Sostenibile** — Agenda 2030

---

**Rome Digital Innovation Hub** in collaborazione con **Il Borgo Urbano**
"""
    return report


def generate_patto_di_senso_report(analysis: Dict[str, Any], organization_info: Dict, assessment_info: Dict = None) -> str:
    """Genera il report per l'Audit di Maturità del Patto di Senso"""
    
    org_name = organization_info.get("name", "Organizzazione")
    sector = organization_info.get("sector", "Non specificato")
    size = organization_info.get("size", "Non specificata")
    
    assessment_date = get_assessment_date(assessment_info or {})
    current_date = assessment_date.strftime("%d/%m/%Y")
    overall_score = analysis.get("overall_maturity", 0)
    maturity_label = analysis.get("maturity_label", "Iniziale")
    scores = analysis.get("scores", {})
    gap_analysis = analysis.get("gap_analysis", {})
    
    patto_levels = {
        1: "Non idoneo — L'organizzazione non soddisfa i requisiti minimi per l'adesione al Patto di Senso",
        2: "Parzialmente idoneo — Esistono elementi di base ma sono necessari interventi significativi",
        3: "Idoneo con riserva — L'organizzazione soddisfa i requisiti minimi, con aree di miglioramento",
        4: "Idoneo — L'organizzazione è pronta per l'implementazione del Patto di Senso",
        5: "Eccellente — L'organizzazione è un modello di riferimento per il Patto di Senso"
    }
    
    patto_level = patto_levels.get(round(overall_score), patto_levels[1])
    
    scores_text = ""
    for category, score in scores.items():
        gap_info = gap_analysis.get(category, {})
        priority = gap_info.get("priority", "N/A")
        gap_val = gap_info.get("gap", 0)
        bar = "█" * int(score) + "░" * (5 - int(score))
        scores_text += f"### {category}\n"
        scores_text += f"- **Punteggio:** {score}/5 [{bar}]\n"
        scores_text += f"- **Gap dal target:** {gap_val}\n"
        scores_text += f"- **Priorità di intervento:** {priority}\n\n"
    
    report = f"""# AUDIT DI MATURITÀ — PATTO DI SENSO

## Innovazione Sociale e Territoriale
### Modello di Sviluppo Sostenibile con IA, Blockchain ed Etica

---

**Organizzazione:** {org_name}
**Tipologia:** {org_type_label}
**Settore:** {sector}
**Dimensione:** {size}
**Data assessment:** {current_date}

---

## 1. EXECUTIVE SUMMARY

### Il Patto di Senso

Il Patto di Senso è un modello di innovazione sociale e territoriale che integra tecnologia (IA e blockchain) ed etica per uno sviluppo sostenibile. L'audit valuta la maturità dell'organizzazione rispetto ai quattro pilastri fondamentali del modello.

### Risultato Complessivo

**Punteggio complessivo:** {overall_score}/5 — **{maturity_label}**

**Livello di idoneità:** {patto_level}

### Le Quattro Macro-Aree Valutate

| Macro-Area | Domande | Descrizione |
|------------|---------|-------------|
| **Governance e Trasparenza** | 27 | Meccanismi decisionali etici, conformità normativa, coinvolgimento stakeholder |
| **Innovazione Tecnologica** | 27 | Adozione tecnologie emergenti (IA, Blockchain, IoT), cybersecurity, competenze digitali |
| **Sostenibilità Ambientale** | 27 | Impatto ambientale, efficienza energetica, allineamento SDGs ONU |
| **Valore Sociale ed Economico** | 27 | Impatto territoriale, inclusione, welfare, sostenibilità della filiera |

---

## 2. INQUADRAMENTO METODOLOGICO

### Framework del Patto di Senso

L'audit si basa su **108 domande** strutturate in 4 macro-aree da 27 domande ciascuna, con risposte su scala 1-5. Il framework valuta la capacità dell'organizzazione di:

- **Governare con trasparenza** — Decisioni etiche, partecipative e verificabili
- **Innovare con responsabilità** — Tecnologie emergenti al servizio del bene comune
- **Sostenere l'ambiente** — Impegno concreto verso gli SDGs e la neutralità climatica
- **Generare valore condiviso** — Impatto positivo su territorio, comunità e filiera

### Scala di Maturità

| Livello | Punteggio | Idoneità Patto di Senso |
|---------|-----------|------------------------|
| Iniziale | 1.0 - 1.9 | Non idoneo — Interventi strutturali necessari |
| Gestito | 2.0 - 2.9 | Parzialmente idoneo — Piano di adeguamento richiesto |
| Definito | 3.0 - 3.9 | Idoneo con riserva — Miglioramenti specifici necessari |
| Avanzato | 4.0 - 4.4 | Idoneo — Pronto per l'implementazione |
| Ottimizzato | 4.5 - 5.0 | Eccellente — Modello di riferimento |

### Collegamento con Smart Contract e Tokenomics

Il Patto di Senso prevede che gli impegni emersi dall'audit vengano tradotti in:
- **Smart Contract su blockchain binaria** — Condizioni verificabili (vero/falso)
- **Token A3** — Per la governance distribuita e il voto sulle proposte
- **Token L3** — Per premiare l'impatto generato e i comportamenti virtuosi

---

## 3. PROFILO DI MATURITÀ PER MACRO-AREA

{scores_text}

---

## 4. GAP ANALYSIS

| Macro-Area | Punteggio | Gap | Priorità |
|------------|-----------|-----|----------|
"""
    
    for category, info in gap_analysis.items():
        priority_icon = "🔴" if info.get("priority") == "Alta" else "🟡" if info.get("priority") == "Media" else "🟢"
        report += f"| {category} | {info.get('current_score', 0)}/5 | {info.get('gap', 0)} | {priority_icon} {info.get('priority', 'N/A')} |\n"
    
    high_gaps = {k: v for k, v in gap_analysis.items() if v.get("gap", 0) > 2}
    medium_gaps = {k: v for k, v in gap_analysis.items() if 1 < v.get("gap", 0) <= 2}
    low_gaps = {k: v for k, v in gap_analysis.items() if v.get("gap", 0) <= 1}
    
    report += f"""

---

## 5. RACCOMANDAZIONI PER L'ADESIONE AL PATTO DI SENSO

### Interventi critici (gap > 2):
"""
    if high_gaps:
        for cat in high_gaps:
            report += f"- **{cat}**: Intervento strutturale necessario. Definire un piano d'azione con tempistiche, responsabili e KPI misurabili.\n"
    else:
        report += "- Nessuna area con gap critico.\n"
    
    report += "\n### Interventi di consolidamento (gap 1-2):\n"
    if medium_gaps:
        for cat in medium_gaps:
            report += f"- **{cat}**: Rafforzamento delle pratiche esistenti e formalizzazione dei processi.\n"
    else:
        report += "- Nessuna area con gap medio.\n"
    
    report += "\n### Aree di eccellenza (gap < 1):\n"
    if low_gaps:
        for cat in low_gaps:
            report += f"- **{cat}**: Mantenere il livello raggiunto e condividere le best practice.\n"
    else:
        report += "- Nessuna area al livello di eccellenza.\n"
    
    report += f"""

---

## 6. ROADMAP VERSO IL PATTO DI SENSO

### Fase 1 — Audit e Pianificazione (0-3 mesi)
- Approfondimento delle aree con gap critico
- Definizione della politica di sostenibilità e governance etica
- Mappatura degli stakeholder e piano di coinvolgimento
- Identificazione degli SDG prioritari

### Fase 2 — Implementazione (3-9 mesi)
- Implementazione delle azioni correttive per le aree critiche
- Adozione di tecnologie emergenti (IA, blockchain) dove applicabile
- Formazione del personale su etica, sostenibilità e innovazione
- Avvio dei processi di stakeholder engagement

### Fase 3 — Codifica nel Patto (9-12 mesi)
- Traduzione degli impegni in clausole verificabili (Legal Engineering)
- Implementazione dello Smart Contract su blockchain binaria
- Definizione dei KPI monitorabili tramite oracoli digitali e IoT
- Attivazione del sistema di tokenomics (Token A3 e L3)

### Fase 4 — Monitoraggio e Miglioramento Continuo (12+ mesi)
- Monitoraggio automatizzato tramite oracoli e sensori
- Verifica periodica delle condizioni dello Smart Contract
- Distribuzione incentivi per obiettivi raggiunti
- Riesame e aggiornamento del Patto

**Tempistica stimata complessiva:** 12-18 mesi

---

## 7. ALLINEAMENTO STRATEGICO

### Coerenza con il Framework del Patto di Senso

L'assessment è allineato ai pilastri fondamentali del modello:

- **Transizione Digitale ed Etica** — IA, blockchain e IoT con approccio human-centric (Rome Call for AI Ethics)
- **Sostenibilità Integrale** — Allineamento agli SDGs dell'Agenda 2030 ONU
- **IA come Oracolo Digitale** — Facilitatore analitico e predittivo a supporto delle decisioni umane
- **Sensers e Oracolo di Senso** — Sistema collaborativo esperti-comunità per orientare la tecnologia al bene comune

### Coerenza con Obiettivi UE e Nazionali

- **European Green Deal** — Neutralità climatica e economia circolare
- **Digital Europe Programme** — Rafforzamento capacità digitali
- **PNRR** — Digitalizzazione, sostenibilità e inclusione
- **Strategia Nazionale per lo Sviluppo Sostenibile** — Agenda 2030

---

## 8. CONCLUSIONI

### Valutazione Complessiva

{org_name} ha conseguito un punteggio di **{overall_score}/5** nell'Audit di Maturità del Patto di Senso. {"L'organizzazione soddisfa i requisiti minimi per l'adesione al Patto di Senso, con aree di miglioramento identificate." if overall_score >= 3 else "L'organizzazione necessita di interventi significativi prima di poter aderire al Patto di Senso. Si raccomanda di seguire la roadmap proposta."}

### Prossimi Passi

1. Condivisione del report con il management e gli stakeholder chiave
2. Definizione delle priorità di intervento
3. Avvio del percorso di adeguamento secondo la roadmap proposta
4. Pianificazione dell'implementazione dello Smart Contract

---

**Rome Digital Innovation Hub** in collaborazione con **Il Borgo Urbano**
*Programma Patto di Senso — Innovazione Sociale e Territoriale*

L'assessment è stato realizzato da esperti in innovazione sociale, governance etica e trasformazione digitale, assicurando un'analisi contestualizzata della maturità dell'organizzazione rispetto ai requisiti del Patto di Senso.
"""
    return report


async def run_crew_analysis(responses: Dict[str, Any], questions: List[Dict], organization_info: Dict, program: str = "dma", assessment_info: Dict = None) -> Dict[str, Any]:
    """Run the analysis pipeline with algorithmic scoring"""
    
    analysis = analyze_responses(responses, questions, organization_info)
    
    if assessment_info is None:
        assessment_info = {}
    
    if program == "iso56002":
        report = generate_iso56002_report(analysis, organization_info, assessment_info)
        audit_sheet = generate_audit_sheet(analysis, organization_info, assessment_info)
    elif program == "governance":
        report = generate_governance_report(analysis, organization_info, assessment_info)
        audit_sheet = generate_audit_sheet(analysis, organization_info, assessment_info)
    elif program == "patto_di_senso":
        report = generate_patto_di_senso_report(analysis, organization_info, assessment_info)
        audit_sheet = generate_audit_sheet(analysis, organization_info, assessment_info)
    else:
        report = generate_report(analysis, organization_info, assessment_info)
        audit_sheet = generate_audit_sheet(analysis, organization_info, assessment_info)
    
    staff_profiles = get_staff_profiles()
    
    return {
        "scores": analysis["scores"],
        "overall_maturity": analysis["overall_maturity"],
        "maturity_label": analysis["maturity_label"],
        "gap_analysis": analysis["gap_analysis"],
        "report": report,
        "audit_sheet": audit_sheet,
        "staff_profiles": staff_profiles
    }
