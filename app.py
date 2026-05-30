from flask import Flask, render_template, request, jsonify
import os, re, json
from werkzeug.utils import secure_filename

try:
    import pdfplumber
    PDF_OK = True
except: PDF_OK = False

try:
    from docx import Document as DocxDoc
    DOCX_OK = True
except: DOCX_OK = False

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    ML_OK = True
except: ML_OK = False

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

TECH_SKILLS = [
    "python","java","javascript","c++","sql","r","machine learning","deep learning",
    "nlp","data science","pandas","numpy","scikit-learn","tensorflow","keras","pytorch",
    "flask","django","react","nodejs","html","css","git","github","docker","kubernetes",
    "aws","azure","mongodb","mysql","postgresql","spark","hadoop","power bi","tableau",
    "rest api","agile","scrum","selenium","opencv","nltk","spacy","bert","transformer"
]
SOFT_SKILLS = ["leadership","communication","teamwork","problem solving",
               "analytical","management","collaboration","adaptability","critical thinking"]

SAMPLE_JD = """
We are looking for a Data Scientist / ML Engineer with:
- Strong Python, Pandas, NumPy skills
- Machine Learning, NLP, scikit-learn experience
- REST API and Flask knowledge
- SQL and MongoDB databases
- Git, Docker, cloud (AWS/GCP)
- Good communication and problem solving skills
- Data preprocessing and feature engineering
- Experience with data visualization tools
"""

def extract_text(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    text = ""
    if ext == ".pdf" and PDF_OK:
        with pdfplumber.open(filepath) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t: text += t + "\n"
    elif ext == ".docx" and DOCX_OK:
        doc = DocxDoc(filepath)
        text = "\n".join([p.text for p in doc.paragraphs])
    elif ext == ".txt":
        with open(filepath, 'r', errors='ignore') as f:
            text = f.read()
    return text

def clean(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    return re.sub(r'\s+', ' ', text).strip()

def get_skills(text):
    tl = text.lower()
    tech = [s for s in TECH_SKILLS if s in tl]
    soft = [s for s in SOFT_SKILLS if s in tl]
    return tech, soft

def get_sections(text):
    tl = text.lower()
    return {
        "Contact":        any(x in tl for x in ["email","phone","linkedin","github","@"]),
        "Education":      any(x in tl for x in ["education","university","college","degree","b.e","b.tech","bca"]),
        "Experience":     any(x in tl for x in ["experience","internship","intern","work"]),
        "Skills":         any(x in tl for x in ["skills","technologies","tools"]),
        "Projects":       any(x in tl for x in ["project","built","developed","implemented"]),
        "Certifications": any(x in tl for x in ["certification","certificate","certified","course"]),
    }

def get_name(text):
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    for line in lines[:5]:
        if 4 < len(line) < 50 and re.match(r'^[A-Za-z\s.]+$', line):
            return line
    return "Not detected"

def get_email(text):
    m = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
    return m[0] if m else "Not found"

def get_phone(text):
    m = re.findall(r'(\+?\d[\d\s\-().]{8,14}\d)', text)
    return m[0].strip() if m else "Not found"

def get_education(text):
    tl = text.lower()
    if any(x in tl for x in ["b.e","b.tech","bca","bsc","bachelor"]): return "Bachelor's"
    if any(x in tl for x in ["m.tech","mca","msc","master"]):         return "Master's"
    if any(x in tl for x in ["phd","ph.d","doctorate"]):              return "PhD"
    return "Not detected"

def similarity_score(r, jd):
    if ML_OK:
        try:
            v = TfidfVectorizer(stop_words='english')
            m = v.fit_transform([r, jd])
            return round(cosine_similarity(m[0:1], m[1:2])[0][0] * 100, 1)
        except: pass
    rw = set(clean(r).split())
    jw = set(clean(jd).split())
    if not jw: return 0
    return round(len(rw & jw) / len(jw) * 100, 1)

def keyword_score(r, jd):
    rw = set(clean(r).split())
    jw = set(clean(jd).split())
    if not jw: return 0, [], []
    matched = sorted(rw & jw)[:12]
    missing = sorted(jw - rw)[:10]
    return round(len(rw & jw) / len(jw) * 100, 1), matched, missing

def section_score(sections):
    w = {"Contact":10,"Education":15,"Experience":25,"Skills":20,"Projects":20,"Certifications":10}
    return sum(v for k,v in w.items() if sections.get(k))

def analyze(text, jd_text):
    name  = get_name(text)
    email = get_email(text)
    phone = get_phone(text)
    edu   = get_education(text)
    secs  = get_sections(text)
    tech, soft = get_skills(text)
    exp_yrs = 0
    m = re.findall(r'(\d+)\+?\s*year', text.lower())
    if m: exp_yrs = max(int(x) for x in m)

    sim  = similarity_score(text, jd_text)
    kw, matched, missing = keyword_score(text, jd_text)
    sec  = section_score(secs)
    ats  = round(min(0.40*sim + 0.35*kw + 0.25*sec, 100), 1)

    rating = "Excellent" if ats>=80 else "Good" if ats>=60 else "Average" if ats>=40 else "Needs Improvement"
    rating_color = "#27ae60" if ats>=80 else "#2980b9" if ats>=60 else "#e67e22" if ats>=40 else "#e74c3c"

    tips = []
    if not secs.get("Projects"): tips.append("Add a Projects section with 2-3 projects")
    if not secs.get("Certifications"): tips.append("Add certifications to improve credibility")
    if len(tech) < 5: tips.append("List more technical skills")
    if len(text.split()) < 200: tips.append("Resume seems short — add more detail")
    if ats < 60: tips.append("Low ATS score — mirror JD keywords more")
    if missing: tips.append(f"Missing keywords: {', '.join(missing[:5])}")
    if not tips: tips.append("Great resume! Well structured and keyword-rich.")

    return {
        "name": name, "email": email, "phone": phone,
        "education": edu, "exp_yrs": exp_yrs,
        "word_count": len(text.split()),
        "sections": secs,
        "tech_skills": tech, "soft_skills": soft,
        "similarity": sim, "keyword_score": kw,
        "section_score": sec, "ats_score": ats,
        "rating": rating, "rating_color": rating_color,
        "matched_keywords": matched, "missing_keywords": missing,
        "tips": tips
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_route():
    if 'resume' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    f = request.files['resume']
    jd = request.form.get('jd', SAMPLE_JD)
    if not jd.strip(): jd = SAMPLE_JD
    if f.filename == '':
        return jsonify({"error": "No file selected"}), 400
    fname = secure_filename(f.filename)
    path  = os.path.join(app.config['UPLOAD_FOLDER'], fname)
    f.save(path)
    text = extract_text(path)
    if not text:
        return jsonify({"error": "Could not extract text from file"}), 400
    result = analyze(text, jd)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5055)
