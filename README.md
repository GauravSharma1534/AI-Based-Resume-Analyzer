      #  AI-Based Resume Analyzer


#  Project Overview

The **AI-Based Resume Analyzer** is an intelligent recruitment assistance system that evaluates resumes and measures their compatibility with a Job Description (JD) using Natural Language Processing (NLP) and Machine Learning techniques.

Modern companies receive hundreds or even thousands of resumes for a single job opening. Reviewing every resume manually is time-consuming and inefficient. Most organizations use Applicant Tracking Systems (ATS) to automatically filter resumes before they reach recruiters.

This project simulates a real ATS system by analyzing resumes, extracting candidate information, identifying important skills, comparing resumes against job descriptions, and generating ATS compatibility scores with improvement suggestions.

The system helps both recruiters and job seekers by providing a fast, automated, and data-driven resume evaluation process.

---

#  Project Objectives

The main objectives of this project are:

* Automate resume screening.
* Extract candidate information automatically.
* Analyze resume quality and completeness.
* Calculate ATS compatibility scores.
* Compare resumes with job descriptions.
* Identify missing keywords and skills.
* Generate recruiter-friendly reports.
* Improve candidate resume optimization.

---

#  Problem Statement

Recruiters often spend significant time reviewing resumes manually.

Common challenges include:

* Large number of applications.
* Inconsistent resume formats.
* Missing skills and keywords.
* Difficulty identifying suitable candidates quickly.
* Manual screening errors.

The AI-Based Resume Analyzer addresses these challenges through automated resume parsing, NLP-based keyword extraction, and ATS scoring.

---

#  Key Features

##  Resume Parsing

Supports multiple file formats:

* PDF
* DOCX
* TXT

Automatically extracts:

* Candidate Name
* Email Address
* Phone Number
* Skills
* Education
* Experience
* Projects
* Certifications

---

##  ATS Compatibility Scoring

The system calculates:

* TF-IDF Similarity Score
* Keyword Match Score
* Section Completeness Score
* Overall ATS Score

Candidate ratings:

| Score Range | Rating            |
| ----------- | ----------------- |
| 90-100      | Excellent         |
| 75-89       | Very Good         |
| 60-74       | Good              |
| 40-59       | Average           |
| Below 40    | Needs Improvement |

---

##  Keyword Matching

Compares:

* Resume Keywords
* Job Description Keywords

Detects:

* Missing Skills
* Missing Technologies
* Missing Certifications
* Missing Keywords

Provides recommendations to improve ATS compatibility.

---

##  Batch Resume Analysis

Allows recruiters to:

* Analyze multiple resumes.
* Compare candidates.
* Save reports automatically.
* Speed up recruitment workflows.

---

##  Report Generation

Generates structured reports including:

* Candidate Information
* ATS Score
* Missing Keywords
* Resume Statistics
* Suggestions

Reports can be exported as JSON.

---

#  System Architecture

```text
Resume File
      │
      ▼
Text Extraction
      │
      ▼
Information Parsing
      │
      ▼
NLP Processing
      │
      ▼
Keyword Extraction
      │
      ▼
TF-IDF Vectorization
      │
      ▼
Cosine Similarity
      │
      ▼
ATS Score Generation
      │
      ▼
Recommendations & Reports
```

---

#  Technologies Used

| Technology   | Purpose                |
| ------------ | ---------------------- |
| Python       | Core Development       |
| NLTK         | NLP Processing         |
| Scikit-Learn | Machine Learning       |
| pdfplumber   | PDF Parsing            |
| python-docx  | DOCX Parsing           |
| JSON         | Report Storage         |
| Regex        | Information Extraction |
| HTML         | Report Visualization   |

---

#  Machine Learning & NLP Concepts Used

### TF-IDF Vectorization

Converts text into numerical vectors and measures the importance of keywords.

### Cosine Similarity

Measures similarity between:

* Resume Content
* Job Description

Higher similarity indicates better ATS compatibility.

### NLP Processing

Includes:

* Tokenization
* Stopword Removal
* Text Cleaning
* Keyword Extraction

---

#  Repository Structure

```text
AI-Based-Resume-Analyzer/
│
├── app.py
│
├── code/
│   ├── resume_analyzer.py
│   └── requirements.txt
│
├── screenshots/
│   ├── 01_main_menu.png
│   ├── 02_candidate_info.png
│   ├── 03_ats_scores.png
│   ├── 04_suggestions_save.png
│   ├── 05_batch_mode.png
│   ├── web_01_home.png
│   ├── web_02_analyzing.png
│   ├── web_03_results_score.png
│   └── web_04_skills_keywords.png
│
├── Chrome_Demo_Video.mp4
├── Gaurav_Resume_Analysis.mp4
├── output_demo.mp4
│
├── report web.html
├── Project_Report_Gaurav.pdf
├── Resume_Analyzer_PPT_Gaurav.pptx
│
└── README.md
```

---

#  Demo Resources

##  Project Demo Videos

The repository includes:

* Full System Demonstration
* Resume Analysis Workflow
* ATS Score Calculation Demo
* Browser-Based Demonstration

Files:

```text
Chrome_Demo_Video.mp4
Gaurav_Resume_Analysis.mp4
output_demo.mp4
```

---

##  Interactive HTML Report

Open:

```text
report web.html
```

This provides a browser-based demonstration of the generated analysis report.

---

# 📸 Screenshots

The repository contains screenshots demonstrating:

### Main Menu

* Resume Upload
* Analysis Options
* Batch Mode

### Candidate Information

Displays:

* Name
* Email
* Phone
* Education
* Experience

### ATS Score Dashboard

Displays:

* TF-IDF Similarity
* Keyword Match
* Overall Score

### Suggestions Panel

Provides recommendations to improve ATS compatibility.

### Batch Analysis

Analyzes multiple resumes simultaneously.

---

#  Installation

## Step 1: Clone Repository

```bash
git clone https://github.com/GauravSharma1534/AI-Based-Resume-Analyzer.git
cd AI-Based-Resume-Analyzer
```

## Step 2: Install Dependencies

```bash
pip install -r code/requirements.txt
```

## Step 3: Run Application

```bash
python app.py
```

or

```bash
python code/resume_analyzer.py
```

---

#  Menu Options

```text
1. Analyze Resume
2. Run Demo Analysis
3. Batch Analyze Resumes
4. Exit
```

---

#  Sample Output

```text
==========================================================
AI-BASED RESUME ANALYZER — RESULTS
==========================================================

Candidate Information

Name         : Gaurav Sharma
Email        : gaurav@email.com
Phone        : +91-9876543210

ATS Compatibility Scores

TF-IDF Similarity : 62.4%
Keyword Match     : 71.2%
Section Score     : 100/100

Overall ATS Score : 74.3%

Rating            : Good
```

---

# Demo link-** file:///C:/Users/gaura/Downloads/Resume_Analyzer_FINAL%20(1)/resume_project/report%20web.html **

#  Performance Highlights

✅ Fast Resume Parsing

✅ Multi-format Support

✅ ATS Compatibility Scoring

✅ Keyword Gap Analysis

✅ Batch Processing

✅ Structured Report Generation

✅ Real-World Recruitment Workflow

✅ Recruiter-Friendly Output

---

#  Learning Outcomes

Through this project, I gained practical experience in:

* Natural Language Processing (NLP)
* Information Extraction
* Resume Parsing
* ATS Systems
* TF-IDF Vectorization
* Cosine Similarity
* Python Application Development
* Data Processing
* JSON Report Generation
* Recruitment Technology

---

#  Real-World Applications

This project can be used for:

### Students

* Resume Improvement
* Placement Preparation
* Internship Applications

### Recruiters

* Resume Screening
* Candidate Shortlisting
* ATS Filtering

### Organizations

* Recruitment Automation
* Talent Acquisition
* Hiring Analytics

---

#  Future Enhancements

Planned improvements:

* Streamlit Web Dashboard
* Flask Deployment
* AI-Based Resume Ranking
* BERT Semantic Matching
* Interview Question Generator
* Career Recommendation System
* LinkedIn Profile Analysis
* Skill Gap Detection
* Resume Builder Integration
* Cloud Deployment

---

#  Conclusion

The AI-Based Resume Analyzer successfully demonstrates how Artificial Intelligence, Natural Language Processing, and Machine Learning can improve modern recruitment workflows.

The system automatically parses resumes, extracts candidate information, evaluates ATS compatibility, identifies missing keywords, and generates useful recommendations. This reduces manual effort for recruiters while helping candidates optimize their resumes for better job opportunities.

The project showcases practical applications of NLP and Information Retrieval techniques and serves as a strong foundation for developing advanced AI-powered recruitment platforms in the future.

---




