"""
Medical NLP Pipeline - Advanced HuggingFace Transformers Integration
Uses multiple pre-trained medical NLP models for comprehensive analysis
"""

import torch
import numpy as np
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    pipeline,
    AutoModelForTokenClassification,
)
from typing import Dict, List, Tuple, Optional
import re
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MedicalNLPPipeline:
    """
    Advanced Medical NLP Pipeline using HuggingFace pre-trained models.
    
    Models used:
    - ner: d4data/biomedical-ner-all (Biomedical Named Entity Recognition)
    - zero-shot: facebook/bart-large-mnli (Zero-shot classification for conditions)
    - sentiment: cardiffnlp/twitter-roberta-base-sentiment (Severity analysis)
    - text-classification: distilbert-base-uncased-finetuned-sst-2-english (Urgency detection)
    """

    def __init__(self):
        self.device = 0 if torch.cuda.is_available() else -1
        self.models_loaded = False
        self._initialize_models()

    def _initialize_models(self):
        """Load all HuggingFace models with error handling"""
        try:
            logger.info("Loading Biomedical NER model...")
            self.ner_pipeline = pipeline(
                "ner",
                model="d4data/biomedical-ner-all",
                tokenizer="d4data/biomedical-ner-all",
                aggregation_strategy="simple",
                device=self.device,
            )
            logger.info("✓ NER model loaded")

            logger.info("Loading Zero-shot classification model...")
            self.zero_shot_pipeline = pipeline(
                "zero-shot-classification",
                model="facebook/bart-large-mnli",
                device=self.device,
            )
            logger.info("✓ Zero-shot model loaded")

            logger.info("Loading symptom severity model...")
            self.severity_pipeline = pipeline(
                "text-classification",
                model="distilbert-base-uncased-finetuned-sst-2-english",
                device=self.device,
            )
            logger.info("✓ Severity model loaded")

            self.models_loaded = True
            logger.info("✅ All models loaded successfully!")

        except Exception as e:
            logger.error(f"Error loading models: {e}")
            self.models_loaded = False
            self._load_fallback_models()

    def _load_fallback_models(self):
        """Load lightweight fallback models if primary ones fail"""
        try:
            logger.info("Loading fallback models...")
            self.zero_shot_pipeline = pipeline(
                "zero-shot-classification",
                model="typeform/distilbert-base-uncased-mnli",
                device=self.device,
            )
            self.ner_pipeline = None
            self.severity_pipeline = pipeline(
                "text-classification",
                model="distilbert-base-uncased-finetuned-sst-2-english",
                device=self.device,
            )
            self.models_loaded = True
            logger.info("✓ Fallback models loaded")
        except Exception as e:
            logger.error(f"Fallback models also failed: {e}")
            self.models_loaded = False

    def extract_medical_entities(self, text: str) -> Dict:
        """
        Extract biomedical named entities from symptom text
        Returns diseases, symptoms, anatomical locations, etc.
        """
        if not self.models_loaded or self.ner_pipeline is None:
            return self._rule_based_extraction(text)

        try:
            entities = self.ner_pipeline(text)
            categorized = {
                "diseases": [],
                "symptoms": [],
                "anatomy": [],
                "chemicals": [],
                "other": [],
            }

            for entity in entities:
                label = entity.get("entity_group", "").upper()
                word = entity.get("word", "").strip()
                score = entity.get("score", 0)

                if score < 0.5:
                    continue

                if any(k in label for k in ["DISO", "DISEASE", "CHEM"]):
                    categorized["diseases"].append(
                        {"entity": word, "confidence": round(score, 3)}
                    )
                elif any(k in label for k in ["SIGN", "SYMPT", "FIND"]):
                    categorized["symptoms"].append(
                        {"entity": word, "confidence": round(score, 3)}
                    )
                elif any(k in label for k in ["ANAT", "BODY", "ORGAN"]):
                    categorized["anatomy"].append(
                        {"entity": word, "confidence": round(score, 3)}
                    )
                else:
                    categorized["other"].append(
                        {"entity": word, "confidence": round(score, 3)}
                    )

            return categorized

        except Exception as e:
            logger.error(f"NER extraction error: {e}")
            return self._rule_based_extraction(text)

    def _rule_based_extraction(self, text: str) -> Dict:
        """Rule-based fallback for entity extraction"""
        symptom_keywords = [
            "pain", "ache", "fever", "cough", "nausea", "vomiting", "dizziness",
            "fatigue", "headache", "rash", "swelling", "bleeding", "shortness",
            "chest", "abdomen", "back", "throat", "joint", "muscle", "skin",
        ]
        text_lower = text.lower()
        found = [kw for kw in symptom_keywords if kw in text_lower]
        return {
            "diseases": [],
            "symptoms": [{"entity": s, "confidence": 0.7} for s in found],
            "anatomy": [],
            "chemicals": [],
            "other": [],
        }

    def classify_medical_condition(
        self, symptoms_text: str, candidate_conditions: List[str]
    ) -> List[Dict]:
        """
        Zero-shot classify symptoms into medical conditions with confidence scores.
        Uses facebook/bart-large-mnli for robust classification.
        """
        if not self.models_loaded:
            return []

        try:
            prompt = f"Patient symptoms: {symptoms_text}. This describes a case of"
            result = self.zero_shot_pipeline(
                prompt,
                candidate_labels=candidate_conditions,
                hypothesis_template="This patient may have {}.",
                multi_label=True,
            )

            conditions = []
            for label, score in zip(result["labels"], result["scores"]):
                if score > 0.05:
                    conditions.append(
                        {
                            "condition": label,
                            "confidence": round(score * 100, 1),
                            "confidence_raw": score,
                        }
                    )

            return sorted(conditions, key=lambda x: x["confidence_raw"], reverse=True)

        except Exception as e:
            logger.error(f"Zero-shot classification error: {e}")
            return []

    def analyze_severity(self, text: str) -> Dict:
        """
        Analyze symptom severity and urgency using NLP model.
        Returns severity level and recommendation.
        """
        if not self.models_loaded or self.severity_pipeline is None:
            return {"severity": "moderate", "urgency_score": 0.5}

        try:
            # Check for emergency keywords
            emergency_keywords = [
                "chest pain", "can't breathe", "unconscious", "severe bleeding",
                "stroke", "heart attack", "paralysis", "seizure", "anaphylaxis",
                "suicidal", "overdose", "poisoning",
            ]

            high_keywords = [
                "high fever", "severe pain", "constant vomiting", "blood in urine",
                "difficulty swallowing", "sudden vision", "confusion",
            ]

            text_lower = text.lower()

            if any(kw in text_lower for kw in emergency_keywords):
                return {
                    "severity": "EMERGENCY",
                    "urgency_score": 1.0,
                    "color": "#FF0000",
                    "action": "Call emergency services (115/1122) IMMEDIATELY",
                }
            elif any(kw in text_lower for kw in high_keywords):
                return {
                    "severity": "HIGH",
                    "urgency_score": 0.8,
                    "color": "#FF6B00",
                    "action": "Visit ER or doctor within 2-4 hours",
                }

            result = self.severity_pipeline(text[:512])
            score = result[0]["score"]
            label = result[0]["label"]

            if label == "NEGATIVE" and score > 0.8:
                severity = "MODERATE"
                urgency = 0.6
                color = "#FFB700"
                action = "Schedule a doctor appointment within 24-48 hours"
            elif label == "NEGATIVE":
                severity = "MILD-MODERATE"
                urgency = 0.4
                color = "#7BC67E"
                action = "Monitor symptoms, see doctor if worsening"
            else:
                severity = "MILD"
                urgency = 0.2
                color = "#4CAF50"
                action = "Rest, hydrate, monitor symptoms"

            return {
                "severity": severity,
                "urgency_score": urgency,
                "color": color,
                "action": action,
            }

        except Exception as e:
            logger.error(f"Severity analysis error: {e}")
            return {
                "severity": "MODERATE",
                "urgency_score": 0.5,
                "color": "#FFB700",
                "action": "Consult a healthcare professional",
            }

    def analyze_symptoms_full(self, symptoms_text: str, conditions_db: List[str]) -> Dict:
        """
        Complete medical analysis pipeline:
        1. Extract entities (NER)
        2. Classify conditions (Zero-shot)
        3. Analyze severity
        4. Generate recommendations
        """
        logger.info(f"Analyzing: {symptoms_text[:100]}...")

        entities = self.extract_medical_entities(symptoms_text)
        conditions = self.classify_medical_condition(symptoms_text, conditions_db)
        severity = self.analyze_severity(symptoms_text)

        top_conditions = conditions[:5] if conditions else []

        return {
            "entities": entities,
            "possible_conditions": top_conditions,
            "severity_analysis": severity,
            "models_used": [
                "d4data/biomedical-ner-all (NER)",
                "facebook/bart-large-mnli (Zero-shot)",
                "distilbert-base-uncased-finetuned-sst-2-english (Severity)",
            ],
            "disclaimer": (
                "⚠️ This analysis is AI-generated for informational purposes ONLY. "
                "It is NOT a medical diagnosis. Always consult a qualified healthcare "
                "professional for proper diagnosis and treatment."
            ),
        }
