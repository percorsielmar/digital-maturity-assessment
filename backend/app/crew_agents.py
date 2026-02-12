from typing import Dict, Any, List

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

def generate_report(analysis: Dict[str, Any], organization_info: Dict) -> str:
    """Genera un report DIH professionale per rendicontazione UE"""
    
    org_name = organization_info.get("name", "Organizzazione")
    org_type = organization_info.get("type", "azienda")
    org_type_label = "Pubblica Amministrazione" if org_type == "pa" else "Impresa"
    sector = organization_info.get("sector", "Non specificato")
    size = organization_info.get("size", "Non specificata")
    
    overall_score = analysis.get("overall_maturity", 0)
    maturity_label = analysis.get("maturity_label", "Iniziale")
    institutional_phrase = get_institutional_phrase(org_type)
    maturity_interpretation = get_maturity_interpretation(overall_score, org_type)
    
    from datetime import datetime
    current_date = datetime.now().strftime("%d/%m/%Y")
    
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

{institutional_phrase}

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

{institutional_phrase}
"""
    
    return report

def get_staff_profiles() -> Dict[str, str]:
    """Restituisce le schede profilo del personale DIH"""
    
    digital_expert = """## DIGITAL TRANSFORMATION EXPERT (SENIOR)

**Nome e Cognome:** Alexander Schneider
**Ruolo:** Esperto in Trasformazione Digitale — Senior AI Engineer & Product Manager

**Formazione Accademica:**
- Laurea in Ingegneria — Università degli Studi Roma Tre

**Esperienza Professionale:**
- Senior AI Engineer & Product Manager presso Deloitte, specializzato in soluzioni GenAI e AI Agents
- Esperienza consolidata nella progettazione e implementazione di soluzioni di intelligenza artificiale per la trasformazione digitale di imprese e PA
- Competenze avanzate in architetture AI, machine learning, NLP e sistemi di automazione intelligente

**Ruolo nel progetto DIH:**
Figura senior responsabile della supervisione metodologica e della qualità degli assessment di maturità digitale. Opera come referente tecnico-strategico per la valutazione delle capacità digitali dei beneficiari.

**Principali attività nel progetto:**
- Supervisione metodologica del framework di Digital Maturity Assessment
- Validazione e contestualizzazione dei risultati degli assessment
- Interpretazione strategica dei profili di maturità digitale
- Definizione delle roadmap di trasformazione
- Elaborazione di raccomandazioni operative allineate a obiettivi UE
- Revisione e validazione dei report di audit digitale

**Competenze chiave:** Intelligenza artificiale, GenAI, AI Agents, strategia digitale, framework di maturità (CMMI, EFQM), analisi organizzativa, tecnologie digitali avanzate, programmi europei.

**Valore aggiunto:** Visione tecnico-strategica di alto livello, competenze AI all'avanguardia, capacità di tradurre innovazione tecnologica in raccomandazioni operative concrete."""

    process_analyst = """## PROCESS & INNOVATION ANALYST

**Nome e Cognome:** Elmar Schneider
**Ruolo:** Analista Innovazione di Processo — Innovation Manager & Digital Expert

**Formazione e Certificazioni:**
- Innovation Manager — Esperienza pluriennale nella gestione di progetti europei e bandi pubblici
- Sviluppatore software e sistemi digitali dal 1996
- Autore del software registrato "DAE-O" (Modulo per la creazione ed ottimizzazione di Deep Autoencoder)

**Esperienza Professionale:**
- Coordinatore e Presidente di Rete Il Borgo Urbano — partner del Tecnopolo, capoprogetto nell'ATI
- Manager di Reti di Impresa — promozione attiva della collaborazione tra imprese per azioni win-win
- Programmatore e sviluppatore web dalla prima ora (dal 1996): sviluppo siti internet (tra cui Malesia.it, Guadalupa.it), applicazioni mobile, e-commerce, sistemi di pagamento online, logistica integrata
- Competenze complete in ambito digitale: programmazione DOS, HTML, sviluppo web, sistemi informatici, gestione e implementazione reti LAN, blog WordPress, suite Microsoft, Google Cloud, sviluppo con AI
- Energy Manager — Vicepresidente di una ESCo, ha partecipato alla strutturazione del progetto Officinae Verdi (Unicredit) per la realizzazione degli Audit Energetici CFD di edifici di rilievo tra cui il Grattacielo di Milano, la sede storica di Roma (Via Tupini) e il Palazzo del Banco di Sicilia di Palermo
- Coordinatore di un team di esperti sulle energie rinnovabili e le comunità energetiche
- Esperienza consolidata in bandi europei e pubblici: progetti di risparmio energetico, agricoltura sostenibile, Agrisolare, PSR agricoli

**Software Registrato — DAE-O:**
Modulo per la creazione ed ottimizzazione di Deep Autoencoder (rete neurale). Il software semplifica, ottimizza e automatizza il processo di creazione di un Deep Autoencoder in grado di acquisire e comprimere dati da dataset specifici, trasformandoli in uno spazio latente a dimensionalità ridotta. Sviluppato in Python con ottimizzazione semi-Montecarlo degli iperparametri. Applicazioni: energie rinnovabili (profili pale aerogeneratori), reti elettriche, comunità energetiche, problematiche biologiche, organizzative e finanziarie.

**Ruolo nel progetto DIH:**
Figura operativa responsabile dell'analisi dettagliata dei dati raccolti e della loro elaborazione in insight strategici. Collabora con il Digital Transformation Expert per trasformare i risultati quantitativi in valutazioni qualitative.

**Principali attività nel progetto:**
- Analisi e validazione dei dati raccolti tramite piattaforma
- Elaborazione dei punteggi di maturità per area
- Identificazione di pattern, gap e aree critiche
- Supporto alla redazione dei report di audit digitale
- Mappatura dei processi organizzativi del beneficiario
- Preparazione di materiali di sintesi e visualizzazioni

**Competenze chiave:** Innovation management, data analysis, process management, sviluppo software, AI e reti neurali, energy management, gestione bandi europei, reti di impresa, e-commerce, sistemi digitali integrati.

**Valore aggiunto:** Visione trasversale dall'innovazione tecnologica all'efficienza energetica, esperienza trentennale nel digitale, capacità di gestione di progetti complessi e reti collaborative."""

    return {
        "digital_transformation_expert": digital_expert,
        "process_innovation_analyst": process_analyst
    }


def get_staff_cvs() -> Dict[str, str]:
    """Restituisce i CV sintetici delle figure chiave per documentazione separata"""
    
    cv_alexander = """# CURRICULUM VITAE SINTETICO

## Alexander Schneider
### Esperto in Trasformazione Digitale

---

**DATI PERSONALI**
- **Nome e Cognome:** Alexander Schneider
- **Sede:** Roma
- **Ruolo attuale:** Senior AI Engineer & Product Manager — Deloitte

---

**FORMAZIONE ACCADEMICA**
- Laurea in Ingegneria — Università degli Studi Roma Tre, Roma

---

**ESPERIENZA PROFESSIONALE**

**Deloitte** — Senior AI Engineer & Product Manager
- Progettazione e sviluppo di soluzioni GenAI (Generative AI) e AI Agents
- Product management di piattaforme di intelligenza artificiale
- Consulenza strategica per la trasformazione digitale di imprese e PA

---

**COMPETENZE TECNICHE**
- Intelligenza Artificiale: GenAI, AI Agents, Machine Learning, NLP
- Architetture software e cloud computing
- Framework di maturità digitale (CMMI, EFQM)
- Analisi dati e business intelligence
- Strategia digitale e innovazione tecnologica

---

**RUOLO NEL PROGETTO DIH**
Esperto in Trasformazione Digitale (Senior) — Responsabile della supervisione metodologica e della qualità degli assessment di maturità digitale nell'ambito del programma Rome Digital Innovation Hub in collaborazione con Il Borgo Urbano.

---

*Documento redatto ai fini della rendicontazione del progetto DIH — Digital Maturity Assessment*
"""

    cv_elmar = """# CURRICULUM VITAE SINTETICO

## Elmar Schneider
### Analista Innovazione di Processo — Innovation Manager

---

**DATI PERSONALI**
- **Nome e Cognome:** Elmar Schneider
- **Sede:** Roma
- **Ruolo attuale:** Coordinatore e Presidente di Rete Il Borgo Urbano

---

**FORMAZIONE E CERTIFICAZIONI**
- Innovation Manager — Competenze certificate nella gestione di progetti innovativi
- Sviluppatore software e sistemi digitali dal 1996
- Energy Manager — Vicepresidente ESCo
- Autore software registrato "DAE-O" (Deep Autoencoder Optimization)

---

**ESPERIENZA PROFESSIONALE**

**Il Borgo Urbano** — Coordinatore e Presidente di Rete
- Partner del Tecnopolo, capoprogetto nell'ATI
- Coordinamento reti di impresa e promozione collaborazione inter-aziendale
- Gestione progetti europei e bandi pubblici

**Sviluppo Digitale** (dal 1996)
- Programmazione: DOS, HTML, sviluppo web, applicazioni mobile
- Siti internet: Malesia.it, Guadalupa.it e altri progetti web
- E-commerce: sistemi di pagamento online, logistica integrata
- Sistemi informatici: gestione e implementazione reti LAN
- CMS e blog: WordPress, suite Microsoft, Google Cloud
- Sviluppo con AI: progetti di intelligenza artificiale applicata

**Energy Management**
- Vicepresidente ESCo — gestione efficienza energetica
- Progetto Officinae Verdi (Unicredit): Audit Energetici CFD
  - Grattacielo di Milano (sede storica)
  - Sede Roma — Via Tupini
  - Palazzo del Banco di Sicilia — Palermo
- Coordinamento team esperti energie rinnovabili e comunità energetiche

**Bandi e Progetti Pubblici**
- Progetti europei di innovazione e trasformazione digitale
- Bandi risparmio energetico e agricoltura sostenibile
- Agrisolare, PSR agricoli e altri bandi pubblici

---

**SOFTWARE REGISTRATO**

**DAE-O — Deep Autoencoder Optimization**
Modulo Python per la creazione ed ottimizzazione di Deep Autoencoder (rete neurale). Il software semplifica e automatizza la creazione di reti neurali per la compressione e generazione sintetica di dati. Utilizza ottimizzazione semi-Montecarlo degli iperparametri (layer, nodi, patience) con funzione obiettivo MSE.

Applicazioni: profili pale aerogeneratori, reti elettriche e comunità energetiche, problematiche biologiche, organizzative e finanziarie.

---

**COMPETENZE CHIAVE**
- Innovation management e gestione progetti complessi
- Sviluppo software e sistemi digitali (30+ anni)
- AI e reti neurali (Deep Autoencoder)
- Energy management e audit energetici
- E-commerce e pagamenti digitali
- Gestione bandi europei e pubblici
- Reti di impresa e collaborazione inter-aziendale

---

**RUOLO NEL PROGETTO DIH**
Analista Innovazione di Processo — Responsabile dell'analisi dei dati e dell'elaborazione di insight strategici nell'ambito del programma Rome Digital Innovation Hub in collaborazione con Il Borgo Urbano.

---

*Documento redatto ai fini della rendicontazione del progetto DIH — Digital Maturity Assessment*
"""

    return {
        "alexander_schneider": cv_alexander,
        "elmar_schneider": cv_elmar
    }


def generate_timesheet(assessment_info: Dict, organization_info: Dict) -> str:
    """Genera il foglio ore per un assessment specifico"""
    from datetime import datetime
    
    org_name = organization_info.get("name", "Organizzazione")
    assessment_id = assessment_info.get("id", "N/A")
    completed_at = assessment_info.get("completed_at", "")
    
    if completed_at:
        try:
            dt = datetime.fromisoformat(completed_at.replace("Z", "+00:00"))
            date_str = dt.strftime("%d/%m/%Y")
            month_str = dt.strftime("%B %Y")
        except Exception:
            date_str = completed_at
            month_str = ""
    else:
        date_str = datetime.now().strftime("%d/%m/%Y")
        month_str = datetime.now().strftime("%B %Y")
    
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
| {date_str} | Analisi preliminare contesto organizzativo del beneficiario | 2.0 |
| {date_str} | Supervisione metodologica framework di assessment | 2.0 |
| {date_str} | Validazione e contestualizzazione dei risultati | 3.0 |
| {date_str} | Interpretazione strategica del profilo di maturità digitale | 2.5 |
| {date_str} | Definizione roadmap strategica di trasformazione | 3.0 |
| {date_str} | Elaborazione raccomandazioni operative allineate a obiettivi UE | 2.5 |
| {date_str} | Revisione e validazione report di audit digitale | 2.0 |
| {date_str} | Coordinamento e quality assurance documentazione | 1.0 |
| | **TOTALE ORE** | **18.0** |
| | **IMPORTO** | **4.500,00 €** |

---

### 2. Elmar Schneider — Analista Innovazione di Processo

| Data | Attività | Ore |
|------|----------|-----|
| {date_str} | Setup e configurazione piattaforma di assessment | 2.0 |
| {date_str} | Assistenza al beneficiario nella compilazione del questionario | 3.0 |
| {date_str} | Analisi e validazione dati raccolti tramite piattaforma | 3.0 |
| {date_str} | Elaborazione punteggi di maturità per area tematica | 2.0 |
| {date_str} | Identificazione pattern, gap e aree critiche | 3.0 |
| {date_str} | Redazione report di audit digitale professionale | 3.0 |
| {date_str} | Mappatura processi organizzativi del beneficiario | 2.5 |
| {date_str} | Preparazione materiali di sintesi e visualizzazioni | 2.0 |
| {date_str} | Documentazione, archiviazione e chiusura pratica | 1.5 |
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

**Data:** {date_str}

---

*Rome Digital Innovation Hub in collaborazione con Il Borgo Urbano*
"""
    return timesheet


def generate_audit_sheet(analysis: Dict[str, Any], organization_info: Dict) -> str:
    """Genera la Scheda di Audit per rendicontazione UE (max 1 pagina)"""
    
    from datetime import datetime
    
    org_name = organization_info.get("name", "Organizzazione")
    org_type = organization_info.get("type", "azienda")
    org_type_label = "Pubblica Amministrazione" if org_type == "pa" else "Impresa"
    
    current_date = datetime.now().strftime("%d/%m/%Y")
    current_month = datetime.now().strftime("%B %Y")
    
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


async def run_crew_analysis(responses: Dict[str, Any], questions: List[Dict], organization_info: Dict) -> Dict[str, Any]:
    """Run the analysis pipeline with algorithmic scoring"""
    
    analysis = analyze_responses(responses, questions, organization_info)
    report = generate_report(analysis, organization_info)
    audit_sheet = generate_audit_sheet(analysis, organization_info)
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
