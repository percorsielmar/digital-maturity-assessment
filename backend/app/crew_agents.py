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

def generate_report(analysis: Dict[str, Any], organization_info: Dict) -> str:
    """Generate a professional report"""
    
    org_name = organization_info.get("name", "Organizzazione")
    org_type = "Pubblica Amministrazione" if organization_info.get("type") == "pa" else "Azienda"
    
    report = f"""
# REPORT DI MATURITÀ DIGITALE

## Organizzazione: {org_name}
### Tipologia: {org_type}

---

## EXECUTIVE SUMMARY

L'assessment di maturità digitale ha evidenziato un livello complessivo di **{analysis['maturity_label']}** 
con un punteggio medio di **{analysis['overall_maturity']}/5**.

---

## ANALISI PER AREA

"""
    
    for category, data in analysis.get("gap_analysis", {}).items():
        score = data["current_score"]
        gap = data["gap"]
        priority = data["priority"]
        
        stars = "★" * int(score) + "☆" * (5 - int(score))
        
        report += f"""
### {category}
- **Punteggio attuale:** {score}/5 {stars}
- **Gap rispetto al target:** {gap}
- **Priorità di intervento:** {priority}

"""
    
    report += """
---

## RACCOMANDAZIONI PRIORITARIE

"""
    
    high_priority = [(cat, data) for cat, data in analysis.get("gap_analysis", {}).items() 
                     if data["priority"] == "Alta"]
    medium_priority = [(cat, data) for cat, data in analysis.get("gap_analysis", {}).items() 
                       if data["priority"] == "Media"]
    
    if high_priority:
        report += "### Interventi Urgenti (Priorità Alta)\n\n"
        for cat, data in high_priority:
            report += f"1. **{cat}**: Necessario un piano di azione immediato per colmare il gap di {data['gap']} punti.\n"
    
    if medium_priority:
        report += "\n### Interventi a Medio Termine (Priorità Media)\n\n"
        for cat, data in medium_priority:
            report += f"1. **{cat}**: Pianificare interventi di miglioramento nel prossimo anno.\n"
    
    report += f"""
---

## ROADMAP SUGGERITA

### Fase 1 - Quick Wins (0-3 mesi)
- Identificare e implementare miglioramenti rapidi nelle aree critiche
- Avviare programmi di formazione digitale base
- Definire KPI di monitoraggio

### Fase 2 - Consolidamento (3-12 mesi)
- Implementare soluzioni tecnologiche per le aree prioritarie
- Sviluppare competenze digitali avanzate
- Ottimizzare i processi chiave

### Fase 3 - Trasformazione (12-24 mesi)
- Completare la trasformazione digitale delle aree core
- Implementare tecnologie emergenti
- Raggiungere l'eccellenza operativa

---

## CONCLUSIONI

{org_name} si trova in una fase di **{analysis['maturity_label']}** nel proprio percorso di trasformazione digitale.
Con un approccio strutturato e investimenti mirati, è possibile raggiungere livelli superiori di maturità 
e ottenere significativi benefici in termini di efficienza, qualità del servizio e competitività.

---

*Report generato automaticamente dal sistema di Digital Maturity Assessment*
"""
    
    return report

async def run_crew_analysis(responses: Dict[str, Any], questions: List[Dict], organization_info: Dict) -> Dict[str, Any]:
    """Run the analysis pipeline with algorithmic scoring"""
    
    analysis = analyze_responses(responses, questions, organization_info)
    report = generate_report(analysis, organization_info)
    
    return {
        "scores": analysis["scores"],
        "overall_maturity": analysis["overall_maturity"],
        "maturity_label": analysis["maturity_label"],
        "gap_analysis": analysis["gap_analysis"],
        "report": report
    }
