"""
AI-Based Resume Analyzer
Author: Gaurav Sharma
Roll No: 23BDA70050
College: Chandigarh University
Year: 2025

Description:
    This tool parses resumes (PDF/DOCX/TXT), extracts key sections,
    and scores them against a Job Description (JD) for ATS compatibility.
"""

import re
import os
import json
import string
from datetime import datetime

# --- Optional imports (install via requirements.txt) ---
try:
    import nltk
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
    from nltk.stem import PorterStemmer
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('punkt_tab', quiet=True)
    NLP_AVAILABLE = True
except ImportError:
    NLP_AVAILABLE = False

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False

try:
    import pdfplumber
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

try:
    from docx import Document as DocxDocument
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False


# =====================================================================
# CONFIGURATION
# =====================================================================

# Common tech skills to look for in resumes
TECH_SKILLS = [
    "python", "java", "javascript", "c++", "c#", "sql", "r",
    "machine learning", "deep learning", "nlp", "data science",
    "pandas", "numpy", "scikit-learn", "tensorflow", "keras", "pytorch",
    "flask", "django", "fastapi", "react", "nodejs",
    "html", "css", "git", "github", "docker", "kubernetes",
    "aws", "azure", "gcp", "linux", "bash",
    "mysql", "postgresql", "mongodb", "sqlite",
    "tableau", "power bi", "excel", "spark", "hadoop",
    "rest api", "api", "agile", "scrum"
]

# Soft skills
SOFT_SKILLS = [
    "leadership", "communication", "teamwork", "problem solving",
    "analytical", "creative", "management", "collaboration",
    "adaptability", "time management", "critical thinking"
]

# Section headers to detect
SECTION_HEADERS = {
    "education":    ["education", "academic", "qualification", "degree", "university", "college"],
    "experience":   ["experience", "work history", "employment", "internship", "intern"],
    "skills":       ["skills", "technical skills", "technologies", "tools", "expertise"],
    "projects":     ["projects", "project work", "academic projects", "personal projects"],
    "certifications": ["certification", "certificate", "certified", "course", "training"],
    "contact":      ["contact", "email", "phone", "linkedin", "github", "address"]
}


# =====================================================================
# TEXT EXTRACTION
# =====================================================================

def extract_text_from_pdf(filepath):
    """Extract text from a PDF file using pdfplumber."""
    if not PDF_AVAILABLE:
        print("  [!] pdfplumber not installed. Run: pip install pdfplumber")
        return ""
    text = ""
    try:
        with pdfplumber.open(filepath) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        print(f"  [OK] Extracted {len(text)} characters from PDF")
    except Exception as e:
        print(f"  [ERROR] Could not read PDF: {e}")
    return text


def extract_text_from_docx(filepath):
    """Extract text from a DOCX file using python-docx."""
    if not DOCX_AVAILABLE:
        print("  [!] python-docx not installed. Run: pip install python-docx")
        return ""
    text = ""
    try:
        doc = DocxDocument(filepath)
        for para in doc.paragraphs:
            text += para.text + "\n"
        print(f"  [OK] Extracted {len(text)} characters from DOCX")
    except Exception as e:
        print(f"  [ERROR] Could not read DOCX: {e}")
    return text


def extract_text_from_txt(filepath):
    """Read plain text file."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
        print(f"  [OK] Read {len(text)} characters from TXT")
        return text
    except Exception as e:
        print(f"  [ERROR] Could not read TXT: {e}")
        return ""


def load_resume(filepath):
    """Auto-detect file type and extract text."""
    ext = os.path.splitext(filepath)[1].lower()
    print(f"\n  Loading resume: {os.path.basename(filepath)}")

    if ext == ".pdf":
        return extract_text_from_pdf(filepath)
    elif ext == ".docx":
        return extract_text_from_docx(filepath)
    elif ext == ".txt":
        return extract_text_from_txt(filepath)
    else:
        print(f"  [ERROR] Unsupported format: {ext}. Use PDF, DOCX, or TXT.")
        return ""


# =====================================================================
# TEXT CLEANING & NLP
# =====================================================================

def clean_text(text):
    """Basic text cleaning."""
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)           # multiple spaces to single
    text = re.sub(r'[^\w\s]', ' ', text)       # remove punctuation
    text = text.strip()
    return text


def tokenize_and_clean(text):
    """Tokenize and remove stopwords using NLTK if available."""
    text = clean_text(text)
    if NLP_AVAILABLE:
        tokens = word_tokenize(text)
        stop_words = set(stopwords.words('english'))
        stemmer = PorterStemmer()
        tokens = [stemmer.stem(t) for t in tokens
                  if t not in stop_words and len(t) > 2]
    else:
        # fallback: simple split + remove short words
        tokens = [w for w in text.split() if len(w) > 2]
    return tokens


# =====================================================================
# RESUME PARSING
# =====================================================================

def extract_email(text):
    """Find email address in text."""
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    matches = re.findall(pattern, text)
    return matches[0] if matches else "Not found"


def extract_phone(text):
    """Find phone number in text."""
    pattern = r'(\+?\d[\d\s\-().]{8,14}\d)'
    matches = re.findall(pattern, text)
    return matches[0].strip() if matches else "Not found"


def extract_name(text):
    """Try to extract candidate name from top of resume."""
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    # First non-empty line that's not too long and has no special chars is likely the name
    for line in lines[:5]:
        if 5 < len(line) < 50 and re.match(r'^[A-Za-z\s.]+$', line):
            return line.strip()
    return "Not detected"


def detect_sections(text):
    """Identify which sections are present in the resume."""
    text_lower = text.lower()
    found = {}
    for section, keywords in SECTION_HEADERS.items():
        found[section] = any(kw in text_lower for kw in keywords)
    return found


def extract_skills(text):
    """Find matching tech and soft skills from resume text."""
    text_lower = text.lower()
    found_tech  = [s for s in TECH_SKILLS  if s in text_lower]
    found_soft  = [s for s in SOFT_SKILLS  if s in text_lower]
    return found_tech, found_soft


def extract_education(text):
    """Try to detect education level mentioned."""
    text_lower = text.lower()
    levels = {
        "PhD / Doctorate": ["phd", "ph.d", "doctorate", "doctor of"],
        "Master's":        ["master", "m.tech", "mca", "msc", "m.sc", "mba", "m.e"],
        "Bachelor's":      ["bachelor", "b.tech", "bca", "bsc", "b.sc", "b.e", "be "],
        "Diploma":         ["diploma", "polytechnic"]
    }
    for level, keywords in levels.items():
        if any(kw in text_lower for kw in keywords):
            return level
    return "Not detected"


def count_experience_years(text):
    """Rough estimate of years of experience mentioned."""
    pattern = r'(\d+)\+?\s*year'
    matches = re.findall(pattern, text.lower())
    if matches:
        return max(int(m) for m in matches)
    return 0


def parse_resume(text):
    """Full resume parsing — returns structured dict."""
    result = {
        "name":          extract_name(text),
        "email":         extract_email(text),
        "phone":         extract_phone(text),
        "education":     extract_education(text),
        "experience_yrs": count_experience_years(text),
        "sections":      detect_sections(text),
        "tech_skills":   [],
        "soft_skills":   [],
        "word_count":    len(text.split()),
        "char_count":    len(text)
    }
    result["tech_skills"], result["soft_skills"] = extract_skills(text)
    return result


# =====================================================================
# ATS SCORING
# =====================================================================

def compute_similarity(resume_text, jd_text):
    """
    Compute TF-IDF cosine similarity between resume and JD.
    Falls back to keyword overlap if sklearn is not available.
    """
    if ML_AVAILABLE:
        vectorizer = TfidfVectorizer(stop_words='english')
        try:
            tfidf = vectorizer.fit_transform([resume_text, jd_text])
            score = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
            return round(score * 100, 2)
        except Exception:
            pass

    # Fallback: simple Jaccard similarity
    r_words = set(clean_text(resume_text).split())
    j_words = set(clean_text(jd_text).split())
    if not j_words:
        return 0.0
    intersection = r_words & j_words
    union = r_words | j_words
    return round(len(intersection) / len(union) * 100, 2)


def compute_keyword_score(resume_text, jd_text):
    """How many JD keywords appear in the resume."""
    jd_tokens   = set(tokenize_and_clean(jd_text))
    res_tokens  = set(tokenize_and_clean(resume_text))
    if not jd_tokens:
        return 0.0, [], []
    matched   = jd_tokens & res_tokens
    missing   = jd_tokens - res_tokens
    score     = round(len(matched) / len(jd_tokens) * 100, 2)
    # convert back to readable words (just first 10)
    matched_readable = sorted(list(matched))[:10]
    missing_readable = sorted(list(missing))[:10]
    return score, matched_readable, missing_readable


def score_resume_sections(sections):
    """Give points for each important section that is present."""
    weights = {
        "contact":        10,
        "education":      15,
        "experience":     25,
        "skills":         20,
        "projects":       20,
        "certifications": 10
    }
    score = sum(weights[s] for s, present in sections.items() if present and s in weights)
    return score


def compute_ats_score(resume_text, jd_text, parsed):
    """
    Final ATS score = weighted combination of:
    - TF-IDF similarity with JD (40%)
    - Keyword match score (35%)
    - Section completeness (25%)
    """
    sim_score     = compute_similarity(resume_text, jd_text)
    kw_score, matched, missing = compute_keyword_score(resume_text, jd_text)
    section_score = score_resume_sections(parsed["sections"])

    ats = round(0.40 * sim_score + 0.35 * kw_score + 0.25 * section_score, 2)
    ats = min(ats, 100.0)

    return {
        "ats_score":       ats,
        "similarity":      sim_score,
        "keyword_score":   kw_score,
        "section_score":   section_score,
        "matched_keywords": matched,
        "missing_keywords": missing
    }


def get_rating(score):
    if score >= 80: return "Excellent"
    if score >= 60: return "Good"
    if score >= 40: return "Average"
    return "Needs Improvement"


# =====================================================================
# DISPLAY & REPORT
# =====================================================================

def print_separator(char="=", width=58):
    print(char * width)


def display_results(parsed, scores, jd_provided=True):
    """Print results in a clean terminal format."""

    print("\n")
    print_separator()
    print("   AI-BASED RESUME ANALYZER — RESULTS")
    print_separator()

    print("\n  CANDIDATE INFORMATION")
    print(f"  Name        : {parsed['name']}")
    print(f"  Email       : {parsed['email']}")
    print(f"  Phone       : {parsed['phone']}")
    print(f"  Education   : {parsed['education']}")
    print(f"  Experience  : {parsed['experience_yrs']} year(s) detected")
    print(f"  Word Count  : {parsed['word_count']} words")

    print("\n  SECTIONS DETECTED")
    for sec, found in parsed["sections"].items():
        status = "YES" if found else "NO"
        mark   = "[+]" if found else "[ ]"
        print(f"  {mark} {sec.capitalize():<18} {status}")

    print(f"\n  TECH SKILLS FOUND ({len(parsed['tech_skills'])})")
    if parsed["tech_skills"]:
        for i in range(0, len(parsed["tech_skills"]), 4):
            row = parsed["tech_skills"][i:i+4]
            print("  " + "  |  ".join(f"{s:<18}" for s in row))
    else:
        print("  None detected")

    print(f"\n  SOFT SKILLS FOUND ({len(parsed['soft_skills'])})")
    if parsed["soft_skills"]:
        print("  " + ", ".join(parsed["soft_skills"]))
    else:
        print("  None detected")

    if jd_provided:
        print("\n  ATS COMPATIBILITY SCORES")
        print_separator("-")
        print(f"  TF-IDF Similarity   : {scores['similarity']:.1f}%")
        print(f"  Keyword Match       : {scores['keyword_score']:.1f}%")
        print(f"  Section Score       : {scores['section_score']}/100")
        print_separator("-")
        print(f"  OVERALL ATS SCORE   : {scores['ats_score']:.1f}%")
        print(f"  RATING              : {get_rating(scores['ats_score'])}")
        print_separator("-")

        if scores["matched_keywords"]:
            print(f"\n  MATCHED KEYWORDS (top {len(scores['matched_keywords'])})")
            print("  " + ", ".join(scores["matched_keywords"]))

        if scores["missing_keywords"]:
            print(f"\n  MISSING KEYWORDS (top {len(scores['missing_keywords'])})")
            print("  " + ", ".join(scores["missing_keywords"]))
            print("  TIP: Add these keywords to improve your ATS score!")

    print("\n  SUGGESTIONS")
    suggestions = generate_suggestions(parsed, scores if jd_provided else None)
    for s in suggestions:
        print(f"  -> {s}")

    print("\n" + "=" * 58)


def generate_suggestions(parsed, scores=None):
    """Give practical improvement suggestions."""
    tips = []
    if not parsed["sections"].get("skills"):
        tips.append("Add a dedicated 'Skills' section")
    if not parsed["sections"].get("projects"):
        tips.append("Add a 'Projects' section with 2-3 projects")
    if not parsed["sections"].get("certifications"):
        tips.append("Add certifications to improve credibility")
    if len(parsed["tech_skills"]) < 5:
        tips.append("List more technical skills (tools, languages, frameworks)")
    if parsed["word_count"] < 300:
        tips.append("Resume seems too short — add more detail")
    if parsed["word_count"] > 1000:
        tips.append("Resume might be too long — try to keep it to 1-2 pages")
    if scores:
        if scores["ats_score"] < 60:
            tips.append("Low ATS score — try to mirror the JD keywords more")
        if scores["keyword_score"] < 50:
            tips.append("Many JD keywords are missing — add them naturally")
    if not tips:
        tips.append("Resume looks good! Keep it updated regularly.")
    return tips


def save_report(parsed, scores, output_path="resume_report.json"):
    """Save analysis results to a JSON file."""
    report = {
        "timestamp":   datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "candidate":   parsed,
        "ats_scores":  scores
    }
    with open(output_path, "w") as f:
        json.dump(report, f, indent=4)
    print(f"\n  [OK] Report saved to: {output_path}")


# =====================================================================
# DEMO MODE (when no real resume file is provided)
# =====================================================================

SAMPLE_RESUME = """
Gaurav Sharma
gaurav.sharma@email.com | +91-9876543210 | LinkedIn: linkedin.com/in/gaurav

EDUCATION
B.Tech in Data Science
Chandigarh University, 2021-2025 | CGPA: 8.2

SKILLS
Technical: Python, Machine Learning, NLP, NLTK, Scikit-learn, Pandas, NumPy,
           Flask, SQL, Git, GitHub, HTML, CSS, REST API
Soft Skills: Communication, Teamwork, Problem Solving, Leadership

EXPERIENCE
Data Science Intern — XYZ Analytics, June 2024 - August 2024
- Built an NLP model to classify customer feedback with 89% accuracy
- Automated data cleaning pipeline reducing processing time by 60%
- Created dashboards in Python using matplotlib and seaborn

PROJECTS
1. Resume Analyzer (2025)
   - Built using Python, NLTK, scikit-learn to parse resumes and score ATS fit
   - Parsed 100+ resume formats; reduced manual screening time by 70%

2. Sentiment Analysis on Twitter Data (2024)
   - Used BERT + scikit-learn to classify tweets as positive/negative/neutral
   - Achieved 92% accuracy on test set

CERTIFICATIONS
- Machine Learning by Andrew Ng (Coursera) — 2023
- Python for Data Science (IBM) — 2022

CONTACT
Email: gaurav.sharma@email.com
Phone: +91-9876543210
GitHub: github.com/gaurav-sharma
"""

SAMPLE_JD = """
Job Title: Data Scientist / ML Engineer

We are looking for a Data Scientist with strong Python skills.

Requirements:
- Proficiency in Python, Pandas, NumPy
- Experience with Machine Learning and NLP
- Knowledge of scikit-learn, TensorFlow or PyTorch
- Experience with REST APIs and Flask
- Familiarity with SQL databases
- Git and version control
- Good communication and problem solving skills
- Experience with data preprocessing and feature engineering
- Knowledge of Agile methodology preferred
"""


# =====================================================================
# MAIN MENU
# =====================================================================

def main():
    print("\n" + "=" * 58)
    print("     AI-BASED RESUME ANALYZER")
    print("     Author: Gaurav Sharma | Chandigarh University")
    print("=" * 58)

    while True:
        print("\n  OPTIONS:")
        print("  1. Analyze a resume file (PDF / DOCX / TXT)")
        print("  2. Run demo with sample resume")
        print("  3. Batch analyze multiple resumes")
        print("  4. Exit")

        choice = input("\n  Enter choice (1-4): ").strip()

        if choice == "4":
            print("\n  Goodbye! — Gaurav Sharma\n")
            break

        elif choice == "2":
            print("\n  Running demo with sample resume...")
            parsed = parse_resume(SAMPLE_RESUME)
            scores = compute_ats_score(SAMPLE_RESUME, SAMPLE_JD, parsed)
            display_results(parsed, scores, jd_provided=True)
            save = input("\n  Save report to JSON? (y/n): ").strip().lower()
            if save == 'y':
                save_report(parsed, scores, "sample_report.json")

        elif choice == "1":
            path = input("\n  Enter resume file path: ").strip().strip('"')
            if not os.path.exists(path):
                print(f"  [ERROR] File not found: {path}")
                continue
            text = load_resume(path)
            if not text:
                continue
            parsed = parse_resume(text)

            use_jd = input("\n  Do you have a Job Description to compare? (y/n): ").strip().lower()
            if use_jd == 'y':
                jd_path = input("  Enter JD file path (or press Enter to type it): ").strip()
                if jd_path and os.path.exists(jd_path):
                    jd_text = extract_text_from_txt(jd_path)
                else:
                    print("  Paste the Job Description below (press Enter twice when done):")
                    lines, prev_empty = [], False
                    while True:
                        line = input()
                        if line == "" and prev_empty:
                            break
                        lines.append(line)
                        prev_empty = (line == "")
                    jd_text = "\n".join(lines)
                scores = compute_ats_score(text, jd_text, parsed)
                display_results(parsed, scores, jd_provided=True)
            else:
                display_results(parsed, {}, jd_provided=False)
                scores = {}

            save = input("\n  Save report to JSON? (y/n): ").strip().lower()
            if save == 'y':
                save_report(parsed, scores)

        elif choice == "3":
            folder = input("\n  Enter folder path with resumes: ").strip().strip('"')
            jd_text = SAMPLE_JD
            use_jd = input("  Use sample JD for scoring? (y/n): ").strip().lower()
            if use_jd != 'y':
                jd_path = input("  Enter JD file path: ").strip()
                if os.path.exists(jd_path):
                    jd_text = extract_text_from_txt(jd_path)

            results = []
            if os.path.isdir(folder):
                files = [f for f in os.listdir(folder) if f.endswith(('.pdf', '.docx', '.txt'))]
                if not files:
                    print("  No PDF/DOCX/TXT files found in folder.")
                    continue
                print(f"\n  Found {len(files)} resume(s). Processing...")
                for fname in files:
                    fpath = os.path.join(folder, fname)
                    text  = load_resume(fpath)
                    if text:
                        parsed = parse_resume(text)
                        scores = compute_ats_score(text, jd_text, parsed)
                        results.append({
                            "file":      fname,
                            "name":      parsed["name"],
                            "ats_score": scores["ats_score"],
                            "rating":    get_rating(scores["ats_score"])
                        })

                # Sort by ATS score descending
                results.sort(key=lambda x: x["ats_score"], reverse=True)
                print("\n  BATCH RESULTS (sorted by ATS score)")
                print("  " + "-" * 54)
                print(f"  {'File':<25} {'Name':<20} {'Score':>6}  Rating")
                print("  " + "-" * 54)
                for r in results:
                    print(f"  {r['file']:<25} {r['name']:<20} {r['ats_score']:>5}%  {r['rating']}")
                print("  " + "-" * 54)
            else:
                print("  [ERROR] Folder not found.")

        else:
            print("  Invalid choice. Enter 1, 2, 3, or 4.")

        input("\n  Press Enter to continue...")


if __name__ == "__main__":
    main()
