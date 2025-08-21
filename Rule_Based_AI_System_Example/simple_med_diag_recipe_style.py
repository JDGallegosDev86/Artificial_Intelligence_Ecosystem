# simple_med_diag_recipe_style.py
# -----------------------------------------
# Simple Medical Diagnostic Tool (Rule-Based) — Recipe-style pattern
# Educational demo only — NOT medical advice.

# --------- Dataset of conditions (like recipes) ---------

conditions = {
    "Common Cold": ["runny nose", "congestion", "sneezing", "sore throat"],
    "Influenza (Flu)": ["sudden onset", "high fever", "body aches", "headache", "cough"],
    "COVID-like Illness": ["loss of smell", "fever", "cough or sore throat", "recent exposure"],
    "Strep Throat": ["sore throat", "fever", "no cough"],
    "Gastroenteritis": ["nausea or vomiting", "diarrhea", "abdominal pain"],
    "Food Poisoning": ["after meal", "others sick", "abdominal pain"],
    "Seasonal Allergies": ["sneezing", "itchy eyes or itchy nose", "runny nose", "no fever"],
    "Urinary Tract Infection (UTI)": ["painful urination", "urinary frequency or urgency", "lower abdominal pain"],
    "Dehydration": ["very low urine or dark urine", "dizziness or dry mouth", "vomiting or diarrhea"]
}

# Optional simple advice for matched conditions
advice = {
    "Common Cold": "Rest, fluids, OTC symptom relief as labeled.",
    "Influenza (Flu)": "Rest, fluids, fever control as labeled. Consider early care if high risk.",
    "COVID-like Illness": "Consider testing and isolation; rest and fluids.",
    "Strep Throat": "Testing recommended; if confirmed, antibiotics per clinician.",
    "Gastroenteritis": "Small sips of fluids; advance diet slowly. Seek care if severe.",
    "Food Poisoning": "Hydration and rest. Seek care if high fever or persistent vomiting.",
    "Seasonal Allergies": "Avoid triggers; saline rinse; OTC antihistamines as labeled.",
    "Urinary Tract Infection (UTI)": "Seek testing/clinical care; increase fluids.",
    "Dehydration": "Increase fluids (oral rehydration if available). Seek care if unable to keep fluids."
}

# --------- Triage (red flags) ---------

emergency_flags = {"chest pain", "bluish lips", "confusion"}
meningitis_bundle = {"stiff neck", "fever", "severe headache"}  # all three → emergency
urgent_flags = {"persistent high fever", "severe dehydration", "blood in stool"}

# --------- Synonyms / normalization ---------

synonyms = {
    "stuffy nose": "congestion",
    "blocked nose": "congestion",
    "loss of taste": "loss of smell",
    "short of breath": "shortness of breath",
    "breathless": "shortness of breath",
    "blue lips": "bluish lips",
    "after eating": "after meal",
    # keep exact phrases we use in rules:
    "no cough": "no cough",
    "no fever": "no fever",
}

def normalize(symptom):
    """Lowercase + trim + map simple synonyms to canonical tokens."""
    s = symptom.strip().lower()
    return synonyms.get(s, s)

# --------- Utility functions ---------

def has_any(user_set, options):
    """True if user_set contains ANY item in options."""
    for opt in options:
        if opt in user_set:
            return True
    return False

def triage_check(user_set):
    """IF/ELIF triage checks; returns ('EMERGENCY'|'URGENT'|'OK', message)."""
    if has_any(user_set, list(emergency_flags)):
        return "EMERGENCY", "Emergency signs (chest pain / bluish lips / confusion). Seek immediate care."
    if all(x in user_set for x in meningitis_bundle):
        return "EMERGENCY", "Fever + stiff neck + severe headache — seek immediate care."
    if has_any(user_set, list(urgent_flags)):
        return "URGENT", "Concerning signs (persistent high fever / severe dehydration / blood in stool). See a clinician soon."
    return "OK", ""

def condition_match_score(user_set, req_list):
    """
    Compute matches per condition.
    Requirement grammar supports:
      - single: "fever"
      - 'X or Y'
      - 'X and Y'
    Returns (matched_count, total_requirements, missing_list).
    """
    matched = 0
    missing = []

    for req in req_list:
        text = req.strip()

        if " or " in text:
            options = [t.strip() for t in text.split(" or ")]
            if has_any(user_set, options):
                matched += 1
            else:
                missing.append(f"one of ({' / '.join(options)})")

        elif " and " in text:
            parts = [t.strip() for t in text.split(" and ")]
            have_all = all(p in user_set for p in parts)
            if have_all:
                matched += 1
            else:
                missing_parts = [p for p in parts if p not in user_set]
                missing.append(" + ".join(missing_parts))

        else:
            if text in user_set:
                matched += 1
            else:
                missing.append(text)

    total = len(req_list)
    return matched, total, missing

def _compute_suggestions(user_set, partial_threshold=0.70):
    """
    Build messages for exact and partial matches.
    Exact: matched == total
    Partial: matched/total >= threshold → include missing items.
    """
    outputs = []
    for condition, reqs in conditions.items():
        matched, total, missing = condition_match_score(user_set, reqs)

        if total == 0:
            continue

        if matched == total:
            outputs.append(f"You may have: {condition}! (All key features matched)\nAdvice: {advice.get(condition, '')}")
        else:
            ratio = matched / total
            if ratio >= partial_threshold:
                outputs.append(
                    f"You are showing many features of: {condition}. "
                    f"Missing: {', '.join(missing)}.\nAdvice: {advice.get(condition, '')}"
                )

    if not outputs:
        return ["No strong rule-based matches. Consider rest, fluids, and monitoring.\n"
                "Seek care if symptoms worsen, high fever lasts >3 days, breathing trouble, or red flags appear."]
    return outputs

def recommend_diagnoses(user_symptoms):
    """
    Main recommender: mirrors the recipe example.
    1) Normalize user inputs
    2) TRIAGE check (emergency/urgent)
    3) If OK/URGENT, compute exact/partial matches
    """
    normalized = [normalize(s) for s in user_symptoms if s.strip() != ""]
    user_set = set(normalized)

    # Low Symptom Rule
    if len(user_set) < 3:
        return ["Please add more symptoms (at least three) for better suggestions."]

    # TRIAGE first
    level, msg = triage_check(user_set)
    if level == "EMERGENCY":
        return [msg]
    elif level == "URGENT":
        # Show urgent note + suggested matches
        suggestions = _compute_suggestions(user_set)
        return [msg, "-"*50] + suggestions

    # Normal path
    return _compute_suggestions(user_set)

# --------- Interactive loop ---------

print("Welcome to the Simple Medical Diagnostic Tool! (Demo)")
print("Type 'exit' to quit.")
print("Enter symptoms comma-separated (e.g., fever, cough, sore throat, sudden onset)")
print("Tip: try phrases like 'no cough', 'no fever', 'after meal', 'others sick', 'loss of smell'.")

while True:
    user_input = input("\nEnter your symptoms (comma-separated): ").strip()
    if user_input.lower() == "exit":
        print("Goodbye! Stay well.")
        break

    user_symptoms = [s.strip() for s in user_input.split(",")]
    results = recommend_diagnoses(user_symptoms)
    for line in results:
        print(line)