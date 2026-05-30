# AI-Based Resume Analyzer

A Python tool that parses resumes and scores them against a Job Description (JD) for ATS compatibility.

---

## Features

- Parse PDF, DOCX, and TXT resume formats
- Extract: Name, Email, Phone, Skills, Education, Experience
- Score resume against a Job Description using TF-IDF + Cosine Similarity
- Keyword match analysis — shows what's missing from your resume
- Batch analyze multiple resumes at once
- Save results to JSON report

---

## Tech Stack

| Technology    | Purpose                          |
|---------------|----------------------------------|
| Python 3.x    | Core language                    |
| NLTK          | Tokenization, stopwords, stemming |
| Scikit-learn  | TF-IDF vectorizer, cosine similarity |
| pdfplumber    | PDF text extraction              |
| python-docx   | DOCX text extraction             |
| re / json     | Regex parsing, report saving     |

---

## How to Run

### Step 1 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 2 — Run the tool
```bash
python resume_analyzer.py
```

### Step 3 — Choose an option
```
1. Analyze a resume file (PDF / DOCX / TXT)
2. Run demo with sample resume
3. Batch analyze multiple resumes
4. Exit
```

---

## Sample Output

```
==========================================================
   AI-BASED RESUME ANALYZER — RESULTS
==========================================================

  CANDIDATE INFORMATION
  Name        : Gaurav Sharma
  Email       : gaurav.sharma@email.com
  Phone       : +91-9876543210
  Education   : Bachelor's
  Experience  : 1 year(s) detected
  Word Count  : 312 words

  SECTIONS DETECTED
  [+] Contact            YES
  [+] Education          YES
  [+] Experience         YES
  [+] Skills             YES
  [+] Projects           YES
  [+] Certifications     YES

  ATS COMPATIBILITY SCORES
  ----------------------------------------------------------
  TF-IDF Similarity   : 62.4%
  Keyword Match       : 71.2%
  Section Score       : 100/100
  ----------------------------------------------------------
  OVERALL ATS SCORE   : 74.3%
  RATING              : Good
```

---

## Project Structure

```
resume-analyzer/
├── resume_analyzer.py     # Main application
├── requirements.txt       # Dependencies
└── README.md              # This file
```

---

## Author

**Gaurav Sharma**
Roll No: 23BDA70050
B.Tech Data Science — Chandigarh University — 2025
