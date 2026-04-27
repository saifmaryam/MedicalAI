"""
Advanced Symptom Analyzer - Medical Knowledge Base & Analysis Engine
Comprehensive medical conditions database with symptom mapping
"""

from typing import Dict, List, Tuple
import re


# ============================================================
# COMPREHENSIVE MEDICAL CONDITIONS DATABASE
# ============================================================
MEDICAL_CONDITIONS_DB = {
    # RESPIRATORY
    "Common Cold": {
        "symptoms": ["runny nose", "sneezing", "sore throat", "mild fever", "congestion", "cough"],
        "category": "Respiratory",
        "icd_code": "J00",
        "urgency": "low",
        "description": "Viral upper respiratory tract infection",
        "typical_duration": "7-10 days",
        "when_to_see_doctor": "If fever exceeds 39°C or symptoms worsen after 10 days",
        "home_remedies": ["Rest", "Hydration", "Honey-lemon tea", "Steam inhalation"],
        "red_flags": ["High fever", "Difficulty breathing", "Chest pain"],
    },
    "Influenza (Flu)": {
        "symptoms": ["high fever", "body aches", "fatigue", "headache", "cough", "chills"],
        "category": "Respiratory",
        "icd_code": "J10",
        "urgency": "moderate",
        "description": "Highly contagious viral respiratory illness",
        "typical_duration": "1-2 weeks",
        "when_to_see_doctor": "Immediately if breathing difficulty or persistent fever",
        "home_remedies": ["Bed rest", "Fluids", "Paracetamol for fever"],
        "red_flags": ["Difficulty breathing", "Persistent chest pain", "Confusion"],
    },
    "Pneumonia": {
        "symptoms": ["high fever", "productive cough", "chest pain", "shortness of breath", "chills", "fatigue"],
        "category": "Respiratory",
        "icd_code": "J18",
        "urgency": "high",
        "description": "Lung infection causing air sac inflammation",
        "typical_duration": "2-4 weeks with treatment",
        "when_to_see_doctor": "IMMEDIATELY - requires medical treatment",
        "home_remedies": ["Antibiotics (prescribed)", "Rest", "Fluids"],
        "red_flags": ["Blue lips", "Confusion", "Severe breathing difficulty"],
    },
    "Asthma": {
        "symptoms": ["wheezing", "shortness of breath", "chest tightness", "coughing", "difficulty breathing"],
        "category": "Respiratory",
        "icd_code": "J45",
        "urgency": "moderate-high",
        "description": "Chronic airway inflammation causing breathing difficulty",
        "typical_duration": "Chronic condition",
        "when_to_see_doctor": "Immediately during severe attack",
        "home_remedies": ["Avoid triggers", "Inhaler use", "Breathing exercises"],
        "red_flags": ["Cannot speak", "Blue lips", "Inhaler not helping"],
    },
    "COVID-19": {
        "symptoms": ["fever", "dry cough", "fatigue", "loss of smell", "loss of taste", "body aches", "headache"],
        "category": "Respiratory/Viral",
        "icd_code": "U07.1",
        "urgency": "moderate-high",
        "description": "SARS-CoV-2 viral infection",
        "typical_duration": "2-6 weeks",
        "when_to_see_doctor": "If oxygen saturation drops below 94%",
        "home_remedies": ["Isolation", "Rest", "Hydration", "Monitor O2 levels"],
        "red_flags": ["Difficulty breathing", "Persistent chest pain", "Confusion", "Bluish lips"],
    },
    # GASTROINTESTINAL
    "Gastroenteritis": {
        "symptoms": ["nausea", "vomiting", "diarrhea", "stomach cramps", "fever", "dehydration"],
        "category": "Gastrointestinal",
        "icd_code": "K59.1",
        "urgency": "moderate",
        "description": "Inflammation of stomach and intestines",
        "typical_duration": "1-3 days",
        "when_to_see_doctor": "If unable to keep fluids down for 24 hours",
        "home_remedies": ["ORS/electrolyte solutions", "BRAT diet", "Rest"],
        "red_flags": ["Blood in stool", "Severe dehydration", "High fever"],
    },
    "Appendicitis": {
        "symptoms": ["severe abdominal pain", "pain starting around navel", "nausea", "vomiting", "fever", "loss of appetite"],
        "category": "Gastrointestinal",
        "icd_code": "K37",
        "urgency": "EMERGENCY",
        "description": "Inflammation of the appendix - SURGICAL EMERGENCY",
        "typical_duration": "Requires immediate surgery",
        "when_to_see_doctor": "GO TO ER IMMEDIATELY",
        "home_remedies": ["NO home treatment - EMERGENCY"],
        "red_flags": ["Severe abdominal pain", "Rigid abdomen", "Pain moving to lower right"],
    },
    "GERD / Acid Reflux": {
        "symptoms": ["heartburn", "acid reflux", "chest burning", "regurgitation", "difficulty swallowing", "sour taste"],
        "category": "Gastrointestinal",
        "icd_code": "K21",
        "urgency": "low-moderate",
        "description": "Stomach acid flows back into esophagus",
        "typical_duration": "Chronic if untreated",
        "when_to_see_doctor": "If symptoms occur more than twice weekly",
        "home_remedies": ["Avoid spicy foods", "Don't lie down after eating", "Antacids"],
        "red_flags": ["Difficulty swallowing", "Blood in vomit", "Unexplained weight loss"],
    },
    "Irritable Bowel Syndrome (IBS)": {
        "symptoms": ["abdominal cramping", "bloating", "diarrhea", "constipation", "gas", "mucus in stool"],
        "category": "Gastrointestinal",
        "icd_code": "K58",
        "urgency": "low",
        "description": "Functional bowel disorder affecting large intestine",
        "typical_duration": "Chronic condition",
        "when_to_see_doctor": "For proper diagnosis and management",
        "home_remedies": ["High-fiber diet", "Stress management", "Regular exercise"],
        "red_flags": ["Blood in stool", "Unexplained weight loss", "Severe pain"],
    },
    # CARDIOVASCULAR
    "Hypertension": {
        "symptoms": ["headache", "dizziness", "blurred vision", "shortness of breath", "chest pain", "nosebleeds"],
        "category": "Cardiovascular",
        "icd_code": "I10",
        "urgency": "moderate-high",
        "description": "High blood pressure condition",
        "typical_duration": "Chronic - requires ongoing management",
        "when_to_see_doctor": "Regularly for monitoring",
        "home_remedies": ["Low-sodium diet", "Exercise", "Stress reduction"],
        "red_flags": ["Severe headache", "Vision changes", "Chest pain"],
    },
    "Angina": {
        "symptoms": ["chest pain", "chest pressure", "chest tightness", "pain radiating to arm", "shortness of breath"],
        "category": "Cardiovascular",
        "icd_code": "I20",
        "urgency": "high",
        "description": "Chest pain from reduced blood flow to heart",
        "typical_duration": "Usually few minutes",
        "when_to_see_doctor": "See doctor immediately",
        "home_remedies": ["Rest", "Nitroglycerin (if prescribed)"],
        "red_flags": ["Pain at rest", "Increasing frequency", "Not relieved by rest"],
    },
    # NEUROLOGICAL
    "Migraine": {
        "symptoms": ["severe headache", "throbbing pain", "nausea", "vomiting", "light sensitivity", "sound sensitivity", "aura"],
        "category": "Neurological",
        "icd_code": "G43",
        "urgency": "moderate",
        "description": "Severe recurring headache disorder",
        "typical_duration": "4-72 hours per episode",
        "when_to_see_doctor": "For diagnosis and preventive treatment",
        "home_remedies": ["Dark quiet room", "Cold compress", "Hydration", "Rest"],
        "red_flags": ["Worst headache of life", "Sudden severe onset", "Neurological symptoms"],
    },
    "Tension Headache": {
        "symptoms": ["dull headache", "pressure around head", "tenderness in scalp", "neck pain", "shoulder pain"],
        "category": "Neurological",
        "icd_code": "G44.2",
        "urgency": "low",
        "description": "Most common type of headache",
        "typical_duration": "30 minutes to several hours",
        "when_to_see_doctor": "If occurring frequently",
        "home_remedies": ["OTC pain relievers", "Rest", "Stress management", "Neck exercises"],
        "red_flags": ["Sudden severe headache", "Fever with headache", "Neck stiffness"],
    },
    # METABOLIC / ENDOCRINE
    "Type 2 Diabetes": {
        "symptoms": ["frequent urination", "excessive thirst", "fatigue", "blurred vision", "slow healing", "frequent infections"],
        "category": "Endocrine",
        "icd_code": "E11",
        "urgency": "moderate",
        "description": "Impaired blood sugar regulation",
        "typical_duration": "Chronic condition requiring management",
        "when_to_see_doctor": "Regularly for monitoring",
        "home_remedies": ["Low-sugar diet", "Exercise", "Weight management"],
        "red_flags": ["Very high blood sugar", "Fruity breath", "Confusion"],
    },
    "Hypothyroidism": {
        "symptoms": ["fatigue", "weight gain", "cold sensitivity", "constipation", "dry skin", "slow heart rate", "depression"],
        "category": "Endocrine",
        "icd_code": "E03",
        "urgency": "low-moderate",
        "description": "Underactive thyroid gland",
        "typical_duration": "Chronic - requires hormone replacement",
        "when_to_see_doctor": "For blood test and diagnosis",
        "home_remedies": ["Iodine-rich diet", "Thyroid medication (prescribed)"],
        "red_flags": ["Severe fatigue", "Confusion", "Irregular heartbeat"],
    },
    # MUSCULOSKELETAL
    "Arthritis": {
        "symptoms": ["joint pain", "joint stiffness", "swelling", "reduced range of motion", "joint warmth", "morning stiffness"],
        "category": "Musculoskeletal",
        "icd_code": "M19",
        "urgency": "low-moderate",
        "description": "Joint inflammation causing pain and stiffness",
        "typical_duration": "Chronic condition",
        "when_to_see_doctor": "For diagnosis and treatment plan",
        "home_remedies": ["Low-impact exercise", "Anti-inflammatory diet", "Heat/cold therapy"],
        "red_flags": ["Sudden severe joint pain", "Fever with joint pain", "Inability to move joint"],
    },
    # DERMATOLOGICAL
    "Eczema (Atopic Dermatitis)": {
        "symptoms": ["itchy skin", "dry skin", "rash", "red patches", "scaly skin", "skin inflammation"],
        "category": "Dermatological",
        "icd_code": "L20",
        "urgency": "low",
        "description": "Chronic inflammatory skin condition",
        "typical_duration": "Chronic with flare-ups",
        "when_to_see_doctor": "For prescription creams and management",
        "home_remedies": ["Moisturize regularly", "Avoid triggers", "Gentle soap"],
        "red_flags": ["Signs of infection", "Spreading rapidly", "Not responding to treatment"],
    },
    # MENTAL HEALTH
    "Anxiety Disorder": {
        "symptoms": ["excessive worry", "restlessness", "fatigue", "difficulty concentrating", "sleep problems", "muscle tension", "heart palpitations"],
        "category": "Mental Health",
        "icd_code": "F41",
        "urgency": "moderate",
        "description": "Excessive and persistent worry affecting daily life",
        "typical_duration": "Requires therapy and/or medication",
        "when_to_see_doctor": "For proper diagnosis and treatment",
        "home_remedies": ["Deep breathing", "Exercise", "Meditation", "Limit caffeine"],
        "red_flags": ["Panic attacks", "Unable to function", "Suicidal thoughts"],
    },
    "Urinary Tract Infection (UTI)": {
        "symptoms": ["painful urination", "burning urination", "frequent urination", "cloudy urine", "lower abdominal pain", "blood in urine"],
        "category": "Urological",
        "icd_code": "N39.0",
        "urgency": "moderate",
        "description": "Bacterial infection in the urinary system",
        "typical_duration": "3-7 days with antibiotics",
        "when_to_see_doctor": "For antibiotic prescription",
        "home_remedies": ["Increase water intake", "Cranberry juice", "Avoid irritants"],
        "red_flags": ["Fever", "Back pain", "Shaking chills - may indicate kidney infection"],
    },
    "Dengue Fever": {
        "symptoms": ["high fever", "severe headache", "eye pain", "joint pain", "muscle pain", "rash", "bleeding gums", "fatigue"],
        "category": "Infectious Disease",
        "icd_code": "A90",
        "urgency": "high",
        "description": "Mosquito-borne viral infection common in Pakistan",
        "typical_duration": "7-14 days",
        "when_to_see_doctor": "IMMEDIATELY - requires platelet monitoring",
        "home_remedies": ["Rest", "Hydration", "Paracetamol (NOT aspirin/ibuprofen)", "Papaya leaf extract"],
        "red_flags": ["Bleeding", "Severe abdominal pain", "Rapid breathing", "Platelet drop"],
    },
    "Malaria": {
        "symptoms": ["cyclic fever", "chills", "sweating", "headache", "nausea", "vomiting", "muscle pain", "fatigue"],
        "category": "Infectious Disease",
        "icd_code": "B54",
        "urgency": "high",
        "description": "Parasitic infection transmitted by mosquitoes",
        "typical_duration": "Requires antimalarial treatment",
        "when_to_see_doctor": "IMMEDIATELY for blood test",
        "home_remedies": ["Prescribed antimalarials", "Rest", "Hydration"],
        "red_flags": ["Altered consciousness", "Seizures", "Severe anemia"],
    },
    "Typhoid Fever": {
        "symptoms": ["sustained high fever", "weakness", "abdominal pain", "headache", "loss of appetite", "constipation or diarrhea", "rash"],
        "category": "Infectious Disease",
        "icd_code": "A01.0",
        "urgency": "high",
        "description": "Bacterial infection from Salmonella typhi",
        "typical_duration": "3-4 weeks with treatment",
        "when_to_see_doctor": "IMMEDIATELY for blood culture test",
        "home_remedies": ["Prescribed antibiotics", "Rest", "Soft diet", "Hydration"],
        "red_flags": ["Intestinal bleeding", "Perforation symptoms", "Severe confusion"],
    },
}

# All condition names for zero-shot classification
ALL_CONDITIONS = list(MEDICAL_CONDITIONS_DB.keys())

BODY_SYSTEMS = {
    "Respiratory": ["Common Cold", "Influenza (Flu)", "Pneumonia", "Asthma", "COVID-19"],
    "Gastrointestinal": ["Gastroenteritis", "Appendicitis", "GERD / Acid Reflux", "Irritable Bowel Syndrome (IBS)"],
    "Cardiovascular": ["Hypertension", "Angina"],
    "Neurological": ["Migraine", "Tension Headache"],
    "Endocrine": ["Type 2 Diabetes", "Hypothyroidism"],
    "Musculoskeletal": ["Arthritis"],
    "Dermatological": ["Eczema (Atopic Dermatitis)"],
    "Mental Health": ["Anxiety Disorder"],
    "Urological": ["Urinary Tract Infection (UTI)"],
    "Infectious Disease": ["Dengue Fever", "Malaria", "Typhoid Fever"],
}


class SymptomAnalyzer:
    """Advanced symptom analysis with medical knowledge base"""

    def __init__(self, nlp_pipeline=None):
        self.conditions_db = MEDICAL_CONDITIONS_DB
        self.nlp = nlp_pipeline

    def preprocess_symptoms(self, text: str) -> str:
        """Clean and normalize symptom text"""
        text = text.lower().strip()
        text = re.sub(r"[^\w\s,.-]", " ", text)
        text = re.sub(r"\s+", " ", text)
        return text

    def keyword_match_score(self, symptoms_text: str, condition: str) -> float:
        """Calculate keyword match score for a condition"""
        if condition not in self.conditions_db:
            return 0.0

        condition_symptoms = self.conditions_db[condition]["symptoms"]
        symptoms_lower = symptoms_text.lower()
        matches = sum(1 for s in condition_symptoms if s in symptoms_lower)
        return matches / len(condition_symptoms) if condition_symptoms else 0.0

    def get_top_keyword_matches(self, symptoms_text: str, top_n: int = 5) -> List[Dict]:
        """Get top conditions by keyword matching"""
        scores = []
        for condition in self.conditions_db:
            score = self.keyword_match_score(symptoms_text, condition)
            if score > 0:
                scores.append({"condition": condition, "keyword_score": score})

        return sorted(scores, key=lambda x: x["keyword_score"], reverse=True)[:top_n]

    def combine_scores(
        self, keyword_matches: List[Dict], nlp_results: List[Dict]
    ) -> List[Dict]:
        """
        Combine keyword matching + NLP model scores
        Weighted: 30% keyword + 70% NLP model
        """
        combined = {}

        for item in keyword_matches:
            cond = item["condition"]
            combined[cond] = {"keyword_score": item["keyword_score"], "nlp_score": 0.0}

        for item in nlp_results:
            cond = item["condition"]
            if cond not in combined:
                combined[cond] = {"keyword_score": 0.0, "nlp_score": 0.0}
            combined[cond]["nlp_score"] = item["confidence_raw"]

        final_results = []
        for cond, scores in combined.items():
            final_score = (0.3 * scores["keyword_score"]) + (0.7 * scores["nlp_score"])
            if final_score > 0.05:
                db_info = self.conditions_db.get(cond, {})
                final_results.append(
                    {
                        "condition": cond,
                        "confidence": round(final_score * 100, 1),
                        "urgency": db_info.get("urgency", "moderate"),
                        "category": db_info.get("category", "General"),
                        "icd_code": db_info.get("icd_code", ""),
                        "description": db_info.get("description", ""),
                        "when_to_see_doctor": db_info.get("when_to_see_doctor", ""),
                        "home_remedies": db_info.get("home_remedies", []),
                        "red_flags": db_info.get("red_flags", []),
                        "typical_duration": db_info.get("typical_duration", ""),
                    }
                )

        return sorted(final_results, key=lambda x: x["confidence"], reverse=True)[:5]

    def full_analysis(self, symptoms_text: str, nlp_results: List[Dict]) -> Dict:
        """Complete analysis combining all methods"""
        processed = self.preprocess_symptoms(symptoms_text)
        keyword_matches = self.get_top_keyword_matches(processed)
        final_conditions = self.combine_scores(keyword_matches, nlp_results)

        urgency_order = {"EMERGENCY": 5, "high": 4, "moderate-high": 3, "moderate": 2, "low-moderate": 1, "low": 0}
        max_urgency = max(
            (urgency_order.get(c["urgency"], 0) for c in final_conditions),
            default=0,
        )
        overall_urgency = [k for k, v in urgency_order.items() if v == max_urgency]
        overall_urgency = overall_urgency[0] if overall_urgency else "moderate"

        return {
            "conditions": final_conditions,
            "overall_urgency": overall_urgency,
            "analysis_method": "Hybrid (NLP + Keyword Matching)",
        }
