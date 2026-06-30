# ResumeIQ

### Analyze. Improve. Get Hired.

ResumeIQ is an AI-powered Resume Analyzer that compares a resume against a job description using **Google Gemini AI** and provides actionable insights to improve job applications.

---

## Features

- Upload PDF Resume
- AI Resume Match Score
- ATS Compatibility (AI Estimate)
- Hiring Readiness (AI Estimate)
- Missing Skills Detection
- Missing Keywords
- Personalized Recommendations
- Overall Resume Feedback
- Responsive UI
- Print Analysis Report

---

## Tech Stack

- Python
- Flask
- Tailwind CSS
- Google Gemini API
- pdfplumber
- HTML
- JavaScript

---

## Project Structure

```
ResumeIQ/
│
├── app.py
├── requirements.txt
├── README.md
├── Procfile
├── runtime.txt
├── LICENSE
├── .gitignore
│
├── templates/
│   ├── index.html
│   └── result.html
│
├── uploads/
│
└── static/
```

---

## Installation

Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/ResumeIQ.git
```

Go into the project

```bash
cd ResumeIQ
```

Create virtual environment

```bash
python -m venv venv
```

Activate it

Windows

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file

```env
GEMINI_API_KEY=YOUR_API_KEY
```

Run

```bash
python app.py
```

---

## Future Improvements

- Resume History
- Cover Letter Generator
- Interview Question Generator
- User Authentication
- Resume Download PDF
- Dark Mode

---

## Author

**Theekshitha Chevvakula**

B.Tech Artificial Intelligence & Data Science

---

## License

MIT License