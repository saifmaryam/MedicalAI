---
title: MediAI - Medical Symptom Analyzer
emoji: 🏥
colorFrom: blue
sdk: streamlit
sdk_version: 1.32.0
app_file: app.py
pinned: true
license: mit
short_description: Advanced AI-powered medical symptom analyzer using HuggingFace NLP
---

# 🏥 MediAI - Medical Symptom Analyzer

> **⚠️ DISCLAIMER:** This tool is for **educational and informational purposes ONLY**. It is NOT a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare professional.

---

## 🚀 Features

- **🧬 Biomedical NER** — Extracts symptoms, diseases, and anatomical entities using `d4data/biomedical-ner-all`
- **🎯 Zero-Shot Classification** — Maps symptoms to 22+ medical conditions using `facebook/bart-large-mnli`
- **⚡ Severity Analysis** — Detects urgency levels using `distilbert-base-uncased-finetuned-sst-2-english`
- **📊 Interactive Charts** — Plotly confidence bars & radar charts
- **💬 AI Chat Interface** — Conversational symptom discussion
- **📈 Analysis History** — Track all your analyses with analytics
- **📚 Conditions Database** — 22+ conditions across 10 body systems

---

## 🤖 HuggingFace Models Used

| Model | Task | Purpose |
|-------|------|---------|
| `d4data/biomedical-ner-all` | Named Entity Recognition | Extract medical entities from symptoms |
| `facebook/bart-large-mnli` | Zero-shot Classification | Map symptoms to medical conditions |
| `distilbert-base-uncased-finetuned-sst-2-english` | Text Classification | Severity & urgency detection |

---

## 🏗️ Architecture

```
User Input (Symptoms)
        ↓
┌─────────────────────────────────────────┐
│         Medical NLP Pipeline            │
│                                         │
│  1. Biomedical NER (d4data)             │
│     └─ Extract: diseases, symptoms,    │
│        anatomy, chemicals              │
│                                         │
│  2. Zero-Shot Classification (BART)    │
│     └─ Map to 22+ medical conditions  │
│        with confidence scores          │
│                                         │
│  3. Severity Analysis (DistilBERT)     │
│     └─ Detect urgency level            │
└─────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────┐
│       Hybrid Scoring Engine             │
│  70% NLP Model + 30% Keyword Match     │
└─────────────────────────────────────────┘
        ↓
   Ranked Results with:
   - Confidence scores
   - ICD codes
   - Red flags
   - Home remedies
   - Doctor visit timeline
```

---

## 📦 Tech Stack

- **Backend:** Python 3.10+
- **ML Framework:** HuggingFace Transformers + PyTorch
- **Frontend:** Streamlit (Advanced dark gradient UI)
- **Charts:** Plotly
- **Deployment:** HuggingFace Spaces

---

## 🗂️ Project Structure

```
medical-ai-chatbot/
├── app.py                  # Main Streamlit application
├── medical_nlp.py          # HuggingFace NLP pipeline
├── symptom_analyzer.py     # Medical knowledge base + analyzer
├── requirements.txt        # Python dependencies
├── README.md               # This file
└── .streamlit/
    └── config.toml         # Streamlit theme configuration
```

---

## 🌍 Emergency Contacts (Pakistan)

- **Rescue:** 115
- **Punjab Emergency:** 1122
- **Edhi Foundation:** 115

---

## 👩‍💻 Built With

- HuggingFace Transformers for medical NLP
- Streamlit for interactive web interface
- Plotly for data visualization
- Python for backend processing
