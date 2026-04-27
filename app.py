import streamlit as st
import time
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(
    page_title="MediAI - Medical Symptom Analyzer",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* { font-family: 'Inter', sans-serif; }

.stApp { background: #f0f4f8 !important; }
.main .block-container { padding: 1.5rem 2rem; max-width: 1300px; }

/* HERO */
.hero {
    background: linear-gradient(135deg, #1a56db 0%, #1e429f 100%);
    border-radius: 20px; padding: 2rem 2.5rem; margin-bottom: 1.5rem;
    box-shadow: 0 10px 40px rgba(26,86,219,0.3);
}
.hero h1 { color: white; font-size: 2rem; font-weight: 700; margin: 0; }
.hero p { color: rgba(255,255,255,0.8); margin-top: 6px; font-size: 1rem; }
.hero-badge {
    display: inline-flex; align-items: center; gap: 5px;
    background: rgba(255,255,255,0.15); border: 1px solid rgba(255,255,255,0.3);
    border-radius: 50px; padding: 4px 14px; font-size: 0.72rem;
    color: white; margin-top: 12px; margin-right: 6px;
    text-transform: uppercase; letter-spacing: 0.06em; font-weight: 600;
}

/* CARDS */
.white-card {
    background: white; border-radius: 16px; padding: 1.4rem 1.6rem;
    margin-bottom: 1rem; box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    border: 1px solid #e5e7eb;
}
.section-title {
    font-size: 1rem; font-weight: 600; color: #111827; margin-bottom: 1rem;
}

/* CONDITION CARDS */
.cond-card {
    background: white; border-radius: 14px; padding: 1rem 1.3rem;
    margin-bottom: 0.75rem; border-left: 5px solid #1a56db;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    transition: box-shadow 0.2s, transform 0.2s;
}
.cond-card:hover { box-shadow: 0 6px 20px rgba(0,0,0,0.1); transform: translateY(-2px); }
.cond-name { font-size: 1rem; font-weight: 600; color: #111827; }
.cond-meta { font-size: 0.75rem; color: #6b7280; margin-top: 3px; }
.conf-bar-bg { background: #f3f4f6; border-radius: 50px; height: 6px; margin-top: 8px; }
.conf-bar-fill { height: 6px; border-radius: 50px; background: linear-gradient(90deg, #1a56db, #3b82f6); }

/* BADGES */
.badge-em { background: #fee2e2; color: #dc2626; border: 1px solid #fca5a5; border-radius: 20px; padding: 3px 10px; font-size: 0.7rem; font-weight: 600; }
.badge-hi { background: #ffedd5; color: #ea580c; border: 1px solid #fdba74; border-radius: 20px; padding: 3px 10px; font-size: 0.7rem; font-weight: 600; }
.badge-mo { background: #fef9c3; color: #ca8a04; border: 1px solid #fde047; border-radius: 20px; padding: 3px 10px; font-size: 0.7rem; font-weight: 600; }
.badge-lo { background: #dcfce7; color: #16a34a; border: 1px solid #86efac; border-radius: 20px; padding: 3px 10px; font-size: 0.7rem; font-weight: 600; }

/* ENTITY TAGS */
.entity-tag {
    display: inline-block; background: #eff6ff; border: 1px solid #bfdbfe;
    border-radius: 6px; padding: 2px 10px; font-size: 0.76rem;
    color: #1d4ed8; margin: 2px;
}

/* SEVERITY BANNER */
.sev-banner {
    border-radius: 14px; padding: 1rem 1.4rem; margin-bottom: 1rem;
    display: flex; justify-content: space-between; align-items: center;
}

/* CHAT */
.chat-user {
    background: #1a56db; border-radius: 18px 18px 4px 18px;
    padding: 0.9rem 1.1rem; margin: 0.5rem 0 0.5rem 3rem; color: white;
}
.chat-ai {
    background: white; border: 1px solid #e5e7eb;
    border-radius: 18px 18px 18px 4px;
    padding: 0.9rem 1.1rem; margin: 0.5rem 3rem 0.5rem 0; color: #111827;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}
.chat-lbl { font-size: 0.7rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 5px; }

/* DISCLAIMER */
.disclaimer {
    background: #fffbeb; border: 1px solid #fde68a;
    border-radius: 12px; padding: 0.9rem 1.1rem; margin: 0.8rem 0;
}

/* STREAMLIT OVERRIDES */
[data-testid="stSidebar"] {
    background: white !important;
    border-right: 1px solid #e5e7eb !important;
}
.stTextArea textarea {
    background: white !important; border: 1.5px solid #d1d5db !important;
    border-radius: 12px !important; color: #111827 !important;
    font-size: 0.95rem !important;
}
.stTextArea textarea:focus { border-color: #1a56db !important; box-shadow: 0 0 0 3px rgba(26,86,219,0.1) !important; }
.stTextInput input {
    background: white !important; border: 1.5px solid #d1d5db !important;
    border-radius: 10px !important; color: #111827 !important;
}
.stTextInput input:focus { border-color: #1a56db !important; }
.stButton > button {
    background: linear-gradient(135deg, #1a56db, #3b82f6) !important;
    color: white !important; border: none !important; border-radius: 10px !important;
    font-weight: 600 !important; box-shadow: 0 4px 12px rgba(26,86,219,0.3) !important;
    transition: all 0.2s !important;
}
.stButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 6px 20px rgba(26,86,219,0.4) !important; }
.stTabs [data-baseweb="tab-list"] {
    background: #f9fafb !important; border-radius: 12px !important;
    border: 1px solid #e5e7eb !important; padding: 4px !important;
}
.stTabs [data-baseweb="tab"] { color: #6b7280 !important; border-radius: 8px !important; font-weight: 500 !important; }
.stTabs [aria-selected="true"] { background: white !important; color: #1a56db !important; box-shadow: 0 1px 4px rgba(0,0,0,0.1) !important; }
[data-testid="metric-container"] {
    background: white !important; border: 1px solid #e5e7eb !important;
    border-radius: 14px !important; box-shadow: 0 2px 8px rgba(0,0,0,0.04) !important;
}
[data-testid="metric-container"] label { color: #6b7280 !important; }
[data-testid="metric-container"] [data-testid="stMetricValue"] { color: #111827 !important; }
.stSelectbox > div > div { background: white !important; border-color: #d1d5db !important; color: #111827 !important; }
hr { border-color: #e5e7eb !important; }
.streamlit-expanderHeader { background: #f9fafb !important; border: 1px solid #e5e7eb !important; border-radius: 10px !important; color: #374151 !important; }
</style>
""", unsafe_allow_html=True)

# ══ MEDICAL DATABASE ════════════════════════════════════════════════
CONDITIONS_DB = {
    "Common Cold": {
        "keywords": ["runny nose","sneezing","sore throat","mild fever","congestion","cough","cold"],
        "category":"Respiratory","icd":"J00","urgency":"low","color":"#16a34a",
        "desc":"Viral upper respiratory tract infection",
        "duration":"7-10 days",
        "doctor":"If fever >39°C or symptoms worsen after 10 days",
        "remedies":["Rest","Hydration","Honey-lemon tea","Steam inhalation"],
        "flags":["High fever","Difficulty breathing","Chest pain"],
    },
    "Influenza (Flu)": {
        "keywords":["high fever","body aches","fatigue","headache","chills","flu","influenza","muscle pain","shivering"],
        "category":"Respiratory","icd":"J10","urgency":"moderate","color":"#ca8a04",
        "desc":"Highly contagious viral respiratory illness",
        "duration":"1-2 weeks",
        "doctor":"Immediately if breathing difficulty or persistent high fever",
        "remedies":["Bed rest","Plenty of fluids","Paracetamol for fever"],
        "flags":["Difficulty breathing","Persistent chest pain","Confusion"],
    },
    "COVID-19": {
        "keywords":["fever","dry cough","loss of smell","loss of taste","covid","corona","shortness of breath","fatigue","oxygen"],
        "category":"Respiratory/Viral","icd":"U07.1","urgency":"moderate-high","color":"#ea580c",
        "desc":"SARS-CoV-2 viral infection",
        "duration":"2-6 weeks",
        "doctor":"If oxygen saturation drops or breathing becomes difficult",
        "remedies":["Isolation","Rest","Hydration","Monitor O2 levels"],
        "flags":["Difficulty breathing","Persistent chest pain","Bluish lips"],
    },
    "Pneumonia": {
        "keywords":["productive cough","chest pain","shortness of breath","high fever","chills","pneumonia","lung infection"],
        "category":"Respiratory","icd":"J18","urgency":"high","color":"#dc2626",
        "desc":"Lung infection causing air sac inflammation",
        "duration":"2-4 weeks with treatment",
        "doctor":"IMMEDIATELY — requires medical treatment",
        "remedies":["Antibiotics (prescribed)","Rest","Fluids"],
        "flags":["Blue lips","Confusion","Severe breathing difficulty"],
    },
    "Dengue Fever": {
        "keywords":["dengue","high fever","severe headache","eye pain","joint pain","rash","bleeding gums","platelet","mosquito bite"],
        "category":"Infectious Disease","icd":"A90","urgency":"high","color":"#dc2626",
        "desc":"Mosquito-borne viral infection — very common in Pakistan",
        "duration":"7-14 days",
        "doctor":"IMMEDIATELY — requires platelet monitoring",
        "remedies":["Rest","Hydration","Paracetamol ONLY (NOT aspirin)","Papaya leaf extract"],
        "flags":["Bleeding","Severe abdominal pain","Rapid breathing","Platelet drop"],
    },
    "Malaria": {
        "keywords":["malaria","cyclic fever","chills","sweating","shivering","mosquito","antimalarial","recurring fever"],
        "category":"Infectious Disease","icd":"B54","urgency":"high","color":"#dc2626",
        "desc":"Parasitic infection transmitted by mosquitoes",
        "duration":"Requires antimalarial treatment",
        "doctor":"IMMEDIATELY for blood smear test",
        "remedies":["Prescribed antimalarials","Rest","Hydration"],
        "flags":["Altered consciousness","Seizures","Severe anemia"],
    },
    "Typhoid Fever": {
        "keywords":["typhoid","sustained fever","weakness","abdominal pain","loss of appetite","rose spots","enteric fever"],
        "category":"Infectious Disease","icd":"A01.0","urgency":"high","color":"#dc2626",
        "desc":"Bacterial infection from Salmonella typhi — common in Pakistan",
        "duration":"3-4 weeks with treatment",
        "doctor":"IMMEDIATELY for blood culture test",
        "remedies":["Antibiotics (prescribed)","Rest","Soft diet","Hydration"],
        "flags":["Intestinal bleeding","Perforation signs","Severe confusion"],
    },
    "Gastroenteritis": {
        "keywords":["nausea","vomiting","diarrhea","stomach cramps","stomach ache","food poisoning","loose motion"],
        "category":"Gastrointestinal","icd":"K59.1","urgency":"moderate","color":"#ca8a04",
        "desc":"Inflammation of stomach and intestines",
        "duration":"1-3 days",
        "doctor":"If unable to keep fluids down for 24 hours",
        "remedies":["ORS/electrolyte solution","BRAT diet","Rest"],
        "flags":["Blood in stool","Severe dehydration","High fever"],
    },
    "Appendicitis": {
        "keywords":["severe abdominal pain","right side pain","navel pain","appendix","appendicitis","lower right pain"],
        "category":"Gastrointestinal","icd":"K37","urgency":"EMERGENCY","color":"#dc2626",
        "desc":"Inflammation of the appendix — SURGICAL EMERGENCY",
        "duration":"Requires immediate surgery",
        "doctor":"GO TO ER IMMEDIATELY",
        "remedies":["NO home treatment — EMERGENCY"],
        "flags":["Severe abdominal pain","Rigid abdomen","Pain worsening"],
    },
    "GERD / Acid Reflux": {
        "keywords":["heartburn","acid reflux","chest burning","regurgitation","sour taste","acidity","gerd","indigestion"],
        "category":"Gastrointestinal","icd":"K21","urgency":"low","color":"#16a34a",
        "desc":"Stomach acid flows back into esophagus",
        "duration":"Chronic if untreated",
        "doctor":"If symptoms occur more than twice weekly",
        "remedies":["Avoid spicy foods","Don't lie down after eating","Antacids"],
        "flags":["Difficulty swallowing","Blood in vomit","Unexplained weight loss"],
    },
    "Migraine": {
        "keywords":["severe headache","throbbing","nausea","light sensitivity","aura","migraine","one side head","pulsating"],
        "category":"Neurological","icd":"G43","urgency":"moderate","color":"#ca8a04",
        "desc":"Severe recurring headache disorder",
        "duration":"4-72 hours per episode",
        "doctor":"For diagnosis and preventive treatment",
        "remedies":["Dark quiet room","Cold compress","Hydration","Rest"],
        "flags":["Worst headache of life","Sudden severe onset","Vision changes"],
    },
    "Hypertension": {
        "keywords":["high blood pressure","hypertension","dizziness","blurred vision","headache","bp high","nosebleed"],
        "category":"Cardiovascular","icd":"I10","urgency":"moderate","color":"#ca8a04",
        "desc":"High blood pressure condition",
        "duration":"Chronic — requires ongoing management",
        "doctor":"Regularly for BP monitoring",
        "remedies":["Low-sodium diet","Regular exercise","Stress reduction"],
        "flags":["Severe headache","Vision changes","Chest pain"],
    },
    "Type 2 Diabetes": {
        "keywords":["frequent urination","excessive thirst","fatigue","blurred vision","slow healing","diabetes","sugar","sweet urine"],
        "category":"Endocrine","icd":"E11","urgency":"moderate","color":"#ca8a04",
        "desc":"Impaired blood sugar regulation",
        "duration":"Chronic condition requiring management",
        "doctor":"Regularly for blood sugar monitoring",
        "remedies":["Low-sugar diet","Regular exercise","Weight management"],
        "flags":["Very high blood sugar","Fruity breath","Confusion"],
    },
    "Urinary Tract Infection": {
        "keywords":["painful urination","burning urination","frequent urination","cloudy urine","uti","bladder pain","pelvic pain"],
        "category":"Urological","icd":"N39.0","urgency":"moderate","color":"#ca8a04",
        "desc":"Bacterial infection in the urinary system",
        "duration":"3-7 days with antibiotics",
        "doctor":"For antibiotic prescription",
        "remedies":["Increase water intake","Cranberry juice","Avoid bladder irritants"],
        "flags":["Fever","Back pain","Shaking chills — may indicate kidney infection"],
    },
    "Arthritis": {
        "keywords":["joint pain","joint stiffness","swelling joints","arthritis","knee pain","morning stiffness","joint inflammation"],
        "category":"Musculoskeletal","icd":"M19","urgency":"low","color":"#16a34a",
        "desc":"Joint inflammation causing pain and stiffness",
        "duration":"Chronic condition",
        "doctor":"For diagnosis and treatment plan",
        "remedies":["Low-impact exercise","Anti-inflammatory diet","Heat/cold therapy"],
        "flags":["Sudden severe joint pain","Fever with joint pain"],
    },
    "Anxiety Disorder": {
        "keywords":["anxiety","excessive worry","restlessness","panic","heart palpitations","nervousness","stress","racing heart"],
        "category":"Mental Health","icd":"F41","urgency":"moderate","color":"#ca8a04",
        "desc":"Excessive and persistent worry affecting daily life",
        "duration":"Requires therapy and/or medication",
        "doctor":"For proper diagnosis and treatment",
        "remedies":["Deep breathing exercises","Regular exercise","Meditation","Limit caffeine"],
        "flags":["Panic attacks","Unable to function","Suicidal thoughts"],
    },
    "Asthma": {
        "keywords":["wheezing","shortness of breath","chest tightness","difficulty breathing","asthma","inhaler","breathless"],
        "category":"Respiratory","icd":"J45","urgency":"moderate-high","color":"#ea580c",
        "desc":"Chronic airway inflammation causing breathing difficulty",
        "duration":"Chronic condition",
        "doctor":"Immediately during severe attack",
        "remedies":["Avoid triggers","Use inhaler as prescribed","Breathing exercises"],
        "flags":["Cannot speak full sentences","Blue lips","Inhaler not helping"],
    },
    "Hypothyroidism": {
        "keywords":["fatigue","weight gain","cold sensitivity","constipation","dry skin","thyroid","slow metabolism","hair loss"],
        "category":"Endocrine","icd":"E03","urgency":"low","color":"#16a34a",
        "desc":"Underactive thyroid gland",
        "duration":"Chronic — requires hormone replacement",
        "doctor":"For TSH blood test and diagnosis",
        "remedies":["Iodine-rich diet","Thyroid medication (prescribed)"],
        "flags":["Severe fatigue","Confusion","Irregular heartbeat"],
    },
}

EMERGENCY_KW = ["chest pain","can't breathe","cannot breathe","unconscious","severe bleeding",
                 "heart attack","stroke","paralysis","seizure","overdose","poisoning","anaphylaxis"]

# ══ ENGINE ══════════════════════════════════════════════════════════
def analyze(text):
    tl = text.lower()
    for kw in EMERGENCY_KW:
        if kw in tl:
            return {"emergency":True,"severity":{"level":"EMERGENCY","color":"#dc2626",
                    "action":"🚨 Call 115 / 1122 IMMEDIATELY!"},"conditions":[],"entities":[]}

    scores = []
    for name, d in CONDITIONS_DB.items():
        matched = [k for k in d["keywords"] if k in tl]
        if matched:
            sc = min(len(matched)/max(len(d["keywords"])*0.4,1), 1.0)
            scores.append({"condition":name,"confidence":round(sc*100,1),
                           "matched":matched, **{k:d[k] for k in ["category","icd","urgency","color","desc","duration","doctor","remedies","flags"]}})
    scores.sort(key=lambda x:x["confidence"],reverse=True)
    top = scores[:5]

    sym_words = ["fever","pain","cough","nausea","vomiting","headache","fatigue","rash",
                 "dizziness","swelling","bleeding","ache","chills","weakness","burning","itch"]
    entities = [w for w in sym_words if w in tl]

    if top:
        u = top[0]["urgency"]
        sev_map = {
            "EMERGENCY":("#dc2626","🚨 Go to ER immediately!"),
            "high":("#ea580c","⚠️ See a doctor within 2-4 hours"),
            "moderate-high":("#f97316","⚡ See a doctor today"),
            "moderate":("#ca8a04","📅 Schedule appointment in 24-48 hrs"),
            "low":("#16a34a","✅ Rest, hydrate, monitor symptoms"),
        }
        color, action = sev_map.get(u,("#ca8a04","Consult a doctor"))
        sev = {"level":u.upper(),"color":color,"action":action}
    else:
        sev = {"level":"UNKNOWN","color":"#6b7280","action":"Please describe symptoms in more detail"}

    return {"emergency":False,"severity":sev,"conditions":top,"entities":entities}


def badge(u):
    ul = u.lower()
    if "emergency" in ul: return f'<span class="badge-em">🚨 {u}</span>'
    if "high" in ul:      return f'<span class="badge-hi">⚠️ {u}</span>'
    if "moderate" in ul:  return f'<span class="badge-mo">⚡ {u}</span>'
    return f'<span class="badge-lo">✅ {u}</span>'


def ai_reply(sym, res):
    if res["emergency"]:
        return "🚨 **EMERGENCY!** Please call **115 or 1122** immediately. Do not delay."
    c = res["conditions"]
    if not c:
        return "I couldn't find a strong match. Please describe your symptoms in more detail — include location, duration, and severity. If you feel unwell, please consult a doctor."
    t = c[0]
    return (f"Based on your symptoms, the closest match is **{t['condition']}** (confidence: {t['confidence']:.1f}%).\n\n"
            f"**Severity:** {t['urgency'].upper()} — {res['severity']['action']}\n\n"
            f"**About:** {t['desc']}\n\n"
            f"**When to see doctor:** {t['doctor']}\n\n"
            f"⚠️ This is AI analysis for informational purposes only — always consult a qualified healthcare professional.")


# ══ SESSION STATE ════════════════════════════════════════════════════
for k,v in [("chat",[]),("history",[]),("result",None)]:
    if k not in st.session_state: st.session_state[k]=v

# ══ SIDEBAR ══════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:1rem 0 0.5rem">
        <div style="font-size:2.5rem">🏥</div>
        <div style="font-size:1.2rem;font-weight:700;color:#1a56db">MediAI</div>
        <div style="font-size:0.72rem;color:#9ca3af;text-transform:uppercase;letter-spacing:.08em">Symptom Analyzer</div>
    </div>""", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("**📊 Session Stats**")
    c1,c2 = st.columns(2)
    c1.metric("Analyses", len(st.session_state.history))
    c2.metric("Conditions DB", "18+")
    st.markdown("---")
    st.markdown("""
    <div class="disclaimer">
        <div style="color:#92400e;font-weight:700;font-size:.8rem;text-transform:uppercase">⚕️ Disclaimer</div>
        <div style="color:#92400e;font-size:.78rem;margin-top:4px;line-height:1.5">
            For <strong>educational purposes ONLY</strong>. Not a substitute for professional medical advice.
            <br><br><strong>Emergency (Pakistan):</strong><br>Rescue: 115 &nbsp;|&nbsp; Punjab: 1122
        </div>
    </div>""", unsafe_allow_html=True)
    st.markdown("---")
    if st.button("🗑️ Clear All", use_container_width=True):
        st.session_state.chat=[]
        st.session_state.history=[]
        st.session_state.result=None
        st.rerun()

# ══ HERO ══════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero">
    <div style="display:flex;align-items:center;justify-content:space-between">
        <div>
            <h1>🏥 MediAI Symptom Analyzer</h1>
            <p>Advanced AI-powered medical symptom analysis</p>
            <span class="hero-badge">🤖 AI Powered</span>
            <span class="hero-badge">📊 18+ Conditions</span>
            <span class="hero-badge">⚡ Instant Analysis</span>
        </div>
        <div style="font-size:5rem;opacity:0.3">🧬</div>
    </div>
</div>""", unsafe_allow_html=True)

# ══ TABS ══════════════════════════════════════════════════════════════
tab1,tab2,tab3,tab4 = st.tabs(["🔍 Symptom Analysis","💬 Chat Interface","📈 History","📚 Conditions DB"])

# ─── TAB 1 ────────────────────────────────────────────────────────────
with tab1:
    left,right = st.columns([1,1.2],gap="large")

    with left:
        st.markdown('<div class="white-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">🩺 Enter Your Symptoms</div>', unsafe_allow_html=True)

        st.markdown("**Quick Examples:**")
        e1,e2 = st.columns(2)
        examples=[
            ("🤒 Flu","High fever, body aches, severe headache, fatigue and chills for 2 days"),
            ("🤧 Cold","Runny nose, sneezing, sore throat, mild fever and congestion"),
            ("🤢 Stomach","Nausea, vomiting, diarrhea and stomach cramps since morning"),
            ("🧠 Migraine","Throbbing headache on one side, nausea and light sensitivity"),
        ]
        for i,(lbl,txt) in enumerate(examples):
            with (e1 if i%2==0 else e2):
                if st.button(lbl, key=f"e{i}", use_container_width=True):
                    st.session_state["_ex"]=txt

        sym = st.text_area("Symptoms", value=st.session_state.get("_ex",""), height=130,
            placeholder="Describe your symptoms in detail...\nE.g: High fever 39°C, body aches, dry cough, lost smell 2 days ago",
            label_visibility="collapsed")

        a1,a2=st.columns(2)
        age=a1.selectbox("Age Group",["Child (0-12)","Teen (13-17)","Adult (18-60)","Senior (60+)"])
        gender=a2.selectbox("Gender",["Male","Female","Prefer not to say"])
        dur=st.select_slider("Duration",["<24 hrs","1-3 days","4-7 days","1-2 weeks",">2 weeks"],value="1-3 days")
        go=st.button("🔬 Analyze Symptoms", use_container_width=True, type="primary")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("""
        <div class="disclaimer">
            <div style="color:#92400e;font-weight:700;font-size:.8rem">⚠️ Medical Disclaimer</div>
            <div style="color:#92400e;font-size:.78rem;margin-top:4px">
                AI analysis for <strong>educational purposes ONLY</strong>. Always consult a qualified healthcare professional.
                Emergency: <strong>115 / 1122</strong>
            </div>
        </div>""", unsafe_allow_html=True)

    with right:
        if go and sym.strip():
            with st.spinner("🧠 Analyzing symptoms..."):
                time.sleep(0.4)
                ctx=f"{age}, {gender}, duration:{dur}. Symptoms: {sym}"
                res=analyze(ctx)
                st.session_state.result=res
                st.session_state.history.append({
                    "time":datetime.now().strftime("%H:%M"),
                    "symptoms":sym[:60]+("..." if len(sym)>60 else ""),
                    "top":res["conditions"][0]["condition"] if res["conditions"] else "No match",
                    "severity":res["severity"]["level"],
                })
                r=ai_reply(sym,res)
                st.session_state.chat.append({"role":"user","content":sym})
                st.session_state.chat.append({"role":"ai","content":r})

        res=st.session_state.result
        if res:
            sev=res["severity"]
            # Severity banner
            st.markdown(f"""
            <div class="sev-banner" style="background:{sev['color']}15;border:1.5px solid {sev['color']}40">
                <div>
                    <div style="font-size:.7rem;text-transform:uppercase;letter-spacing:.08em;color:{sev['color']}99">Urgency Level</div>
                    <div style="font-size:1.5rem;font-weight:700;color:{sev['color']}">{sev['level']}</div>
                </div>
                <div style="font-size:.88rem;color:{sev['color']};text-align:right;max-width:55%">{sev['action']}</div>
            </div>""", unsafe_allow_html=True)

            if res["entities"]:
                st.markdown("**🏷️ Detected Symptoms:**")
                st.markdown(" ".join(f'<span class="entity-tag">{e}</span>' for e in res["entities"]), unsafe_allow_html=True)
                st.markdown("")

            if res["conditions"]:
                st.markdown(f"**🔍 Top {len(res['conditions'])} Possible Conditions:**")
                for i,c in enumerate(res["conditions"],1):
                    st.markdown(f"""
                    <div class="cond-card" style="border-left-color:{c['color']}">
                        <div style="display:flex;justify-content:space-between;align-items:flex-start">
                            <div style="flex:1">
                                <span style="font-size:1.2rem;font-weight:800;color:#d1d5db">#{i}</span>
                                <span class="cond-name"> {c['condition']}</span>
                                <div class="cond-meta">📁 {c['category']} &nbsp;|&nbsp; ICD: {c['icd']} &nbsp;|&nbsp; ⏱️ {c['duration']}</div>
                                <div style="font-size:.75rem;color:#9ca3af;margin-top:3px">Matched: {', '.join(c['matched'][:3])}</div>
                            </div>
                            <div style="text-align:right;margin-left:10px">
                                {badge(c['urgency'])}
                                <div style="font-size:1.4rem;font-weight:700;color:{c['color']};margin-top:4px">{c['confidence']:.1f}%</div>
                            </div>
                        </div>
                        <div class="conf-bar-bg"><div class="conf-bar-fill" style="width:{c['confidence']}%;background:linear-gradient(90deg,{c['color']},{c['color']}88)"></div></div>
                        <div style="font-size:.8rem;color:#6b7280;margin-top:6px;font-style:italic">{c['desc']}</div>
                    </div>""", unsafe_allow_html=True)
                    with st.expander(f"📋 Details: {c['condition']}"):
                        d1,d2=st.columns(2)
                        with d1:
                            st.markdown("**🩺 When to See Doctor:**")
                            st.markdown(f"<span style='color:#ca8a04;font-size:.88rem'>{c['doctor']}</span>",unsafe_allow_html=True)
                            st.markdown("**🏠 Home Remedies:**")
                            for r in c["remedies"]:
                                st.markdown(f"<div style='color:#16a34a;font-size:.85rem;padding:2px 0'>✅ {r}</div>",unsafe_allow_html=True)
                        with d2:
                            st.markdown("**🚨 Red Flags:**")
                            for f in c["flags"]:
                                st.markdown(f"<div style='color:#dc2626;font-size:.85rem;padding:2px 0'>⚠️ {f}</div>",unsafe_allow_html=True)
            else:
                st.info("No strong match found. Please add more details about your symptoms.")
        elif not go:
            st.markdown("""
            <div style="text-align:center;padding:3rem 1rem;opacity:.35">
                <div style="font-size:4rem">🩺</div>
                <div style="font-size:1.1rem;color:#6b7280;margin-top:1rem;font-weight:500">
                    Enter symptoms to begin analysis
                </div>
                <div style="font-size:.85rem;color:#9ca3af;margin-top:6px">AI-powered medical symptom checker</div>
            </div>""", unsafe_allow_html=True)

# ─── TAB 2 ────────────────────────────────────────────────────────────
with tab2:
    st.markdown('<div class="section-title" style="margin-top:.5rem">💬 Medical AI Chat</div>',unsafe_allow_html=True)

    if not st.session_state.chat:
        st.markdown("""
        <div class="chat-ai">
            <div class="chat-lbl" style="color:#7c3aed">🤖 MediAI</div>
            Hello! I'm MediAI, your medical symptom analyzer. Describe your symptoms and I'll analyze them instantly.<br><br>
            I can help identify possible conditions, assess severity, and suggest when to see a doctor.<br><br>
            <em>⚠️ For educational purposes only — always consult a real doctor.</em>
        </div>""", unsafe_allow_html=True)

    for msg in st.session_state.chat:
        if msg["role"]=="user":
            st.markdown(f"""
            <div class="chat-user">
                <div class="chat-lbl" style="color:rgba(255,255,255,0.7)">👤 You</div>
                {msg['content']}
            </div>""", unsafe_allow_html=True)
        else:
            content=msg["content"].replace("\n","<br>").replace("**","<strong>",1)
            st.markdown(f"""
            <div class="chat-ai">
                <div class="chat-lbl" style="color:#7c3aed">🤖 MediAI</div>
                {msg['content']}
            </div>""", unsafe_allow_html=True)

    ci1,ci2=st.columns([5,1])
    with ci1:
        chat_in=st.text_input("msg",placeholder="E.g: I have fever and joint pain...",label_visibility="collapsed")
    with ci2:
        send=st.button("Send →",use_container_width=True)

    if send and chat_in.strip():
        r=analyze(chat_in)
        rep=ai_reply(chat_in,r)
        st.session_state.chat.append({"role":"user","content":chat_in})
        st.session_state.chat.append({"role":"ai","content":rep})
        st.rerun()

# ─── TAB 3 ────────────────────────────────────────────────────────────
with tab3:
    st.markdown('<div class="section-title" style="margin-top:.5rem">📈 Analysis History</div>',unsafe_allow_html=True)
    if not st.session_state.history:
        st.info("No analyses yet. Go to Symptom Analysis tab to start!")
    else:
        m1,m2,m3=st.columns(3)
        m1.metric("Total Analyses",len(st.session_state.history))
        m2.metric("Last Condition",st.session_state.history[-1]["top"])
        m3.metric("Last Severity",st.session_state.history[-1]["severity"])
        st.markdown("---")
        for h in reversed(st.session_state.history):
            st.markdown(f"""
            <div class="white-card" style="display:flex;justify-content:space-between;align-items:center;padding:0.9rem 1.3rem">
                <div>
                    <div style="font-size:.72rem;color:#9ca3af">🕐 {h['time']}</div>
                    <div style="color:#111827;font-size:.9rem;margin-top:2px;font-weight:500">{h['symptoms']}</div>
                    <div style="color:#6b7280;font-size:.8rem;margin-top:2px">→ {h['top']}</div>
                </div>
                <div>{badge(h['severity'])}</div>
            </div>""", unsafe_allow_html=True)

# ─── TAB 4 ────────────────────────────────────────────────────────────
with tab4:
    st.markdown('<div class="section-title" style="margin-top:.5rem">📚 Medical Conditions Database</div>',unsafe_allow_html=True)
    srch=st.text_input("🔍 Search conditions or symptoms...",placeholder="e.g. fever, diabetes, chest pain")

    systems={
        "🫁 Respiratory":["Common Cold","Influenza (Flu)","COVID-19","Pneumonia","Asthma"],
        "🦠 Infectious Disease":["Dengue Fever","Malaria","Typhoid Fever"],
        "🫃 Gastrointestinal":["Gastroenteritis","Appendicitis","GERD / Acid Reflux"],
        "🧠 Neurological":["Migraine"],
        "❤️ Cardiovascular":["Hypertension"],
        "🩸 Endocrine":["Type 2 Diabetes","Hypothyroidism"],
        "🚽 Urological":["Urinary Tract Infection"],
        "🧘 Mental Health":["Anxiety Disorder"],
        "🦴 Musculoskeletal":["Arthritis"],
    }
    for sys_name,clist in systems.items():
        filtered=[c for c in clist if not srch or
                  srch.lower() in c.lower() or
                  any(srch.lower() in kw for kw in CONDITIONS_DB.get(c,{}).get("keywords",[]))]
        if filtered:
            with st.expander(f"{sys_name} — {len(filtered)} condition(s)", expanded=bool(srch)):
                for cn in filtered:
                    cd=CONDITIONS_DB.get(cn,{})
                    kws=" ".join(f'<span class="entity-tag">{k}</span>' for k in cd.get("keywords",[])[:5])
                    st.markdown(f"""
                    <div class="white-card" style="margin-bottom:0.6rem">
                        <div style="display:flex;justify-content:space-between;align-items:center">
                            <div>
                                <strong style="color:#111827">{cn}</strong>
                                <span style="color:#9ca3af;font-size:.75rem;margin-left:8px">ICD: {cd.get('icd','')}</span>
                            </div>
                            {badge(cd.get('urgency','moderate'))}
                        </div>
                        <div style="font-size:.82rem;color:#6b7280;margin-top:5px">{cd.get('desc','')}</div>
                        <div style="margin-top:8px">{kws}</div>
                    </div>""", unsafe_allow_html=True)
