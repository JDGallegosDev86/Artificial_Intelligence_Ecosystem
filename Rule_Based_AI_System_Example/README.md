# Sample submission for the Building a Rule-Based AI System in Python project.

---

## Part 1: Initial Project Ideas  

### 1. Project Idea 1: Simple Medical Diagnostic Tool  
- **Description:** A system that suggests possible conditions based on symptoms the user reports. The user enters symptoms, and the system matches them to conditions using predefined rules.  
- **Rule-Based Approach:**  
  - The system checks for exact and partial matches between the user’s symptoms and each condition’s key features.  
  - For partial matches, it lists which symptoms are missing.  
  - Triage rules (red flags) override everything (e.g., “seek immediate care”).  

---

### 2. Project Idea 2: Troubleshooting Assistant  
- **Description:** A system that helps users diagnose problems with their devices, such as a computer that won’t start.  
- **Rule-Based Approach:**  
  - The system applies IF–THEN rules to guide the user through possible causes.  
  - For example:  
    - IF no power light → suggest checking the power cable.  
    - IF power light on but no display → suggest checking the monitor.  
    - IF strange beeping sound → suggest a possible hardware error.  
  - The rules can expand into a decision tree where each answer leads to the next step.  

---

### 3. Project Idea 3: Rule-Based Game AI  
- **Description:** A system that provides decision-making for a simple game opponent, such as Tic-Tac-Toe.  
- **Rule-Based Approach:**  
  - The system applies strategic IF–THEN rules to decide moves.  
  - For example:  
    - IF the AI can win in one move → take that move.  
    - ELSE IF the opponent can win next turn → block them.  
    - ELSE IF the center is free → take the center.  
    - ELSE → pick a random corner.  
  - Additional heuristics can be added to make the AI more challenging.  

---

### **Chosen Idea:** Simple Medical Diagnostic Tool  
**Justification:** I chose this project because it is directly related to healthcare, which makes it meaningful and engaging. It demonstrates how rule-based systems can simulate expert reasoning. This project also challenges me to think carefully about symptom-condition mapping and clear decision rules.  

---

## Part 2: Rules/Logic for the Chosen System  

The **Simple Medical Diagnostic Tool** system will follow these rules:  

1. **Exact Match Rule:**  
   - **IF** all key symptoms for a condition are present → **Suggest that condition.**  

2. **Partial Match Rule:**  
   - **IF** at least 50–75% of the symptoms for a condition are present →  
     - **Suggest the condition as a possibility.**  
     - **List the missing symptoms.**  

3. **Red Flag Rule (Triage):**  
   - **IF** the user reports severe symptoms (e.g., chest pain, difficulty breathing, high fever) →  
     - **Override everything and recommend immediate medical attention.**  

4. **No Match Rule:**  
   - **IF** no conditions match → **Suggest seeking general medical advice or adding more symptoms.**  

5. **Low Input Rule:**  
   - **IF** fewer than two symptoms are provided → **Notify the user** to enter more symptoms.

---

## Part 3: Rules/Logic for the Chosen System

Sample input and output: 

Enter your symptoms (comma-separated): cough, fever, fatigue
You may have the Flu. Missing: sore throat.

Enter your symptoms (comma-separated): chest pain, shortness of breath
⚠️ Severe symptoms detected! Seek immediate medical care.

Enter your symptoms (comma-separated): headache
Please enter at least two symptoms for better suggestions.

Enter your symptoms (comma-separated): runny nose, sneezing, sore throat
You may have the Common Cold.

---

## Part 4: Reflection  

### Project Overview:  
This project involved designing a practical, rule-based system to suggest possible conditions based on user inputs. The system uses logical conditions (e.g., exact matches, partial matches, and red flags) to evaluate symptoms against a set of known conditions.  

### Challenges:  
- **Balancing Matches:**  
  Deciding how many symptoms are required for a “partial match” was challenging. I set the threshold around 50–75% to balance flexibility with accuracy.  
- **Red Flag Handling:**  
  It was important to prioritize safety by creating rules that override normal matches when severe symptoms are detected.  















