from flask import Flask, render_template, request
import os
import json
import uuid
import pdfplumber
import secrets

from dotenv import load_dotenv
from google import genai

# -----------------------------
# Load Environment Variables
# -----------------------------
load_dotenv()

# -----------------------------
# Flask App Configuration
# -----------------------------

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# -----------------------------
# Gemini Client
# -----------------------------
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# -----------------------------
# Helper Function
# -----------------------------
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# -----------------------------
# Home Page
# -----------------------------
@app.route("/")
def home():
    return render_template("index.html")


# -----------------------------
# Resume Analysis
# -----------------------------
@app.route("/analyze", methods=["POST"])
def analyze():

    # Check Resume Upload
    if "resume" not in request.files:
        return "No resume uploaded."

    resume = request.files["resume"]

    if resume.filename == "":
        return "Please select a PDF resume."

    if not allowed_file(resume.filename):
        return "Only PDF files are allowed."

    # Job Description
    job_description = request.form.get("job_description", "").strip()

    if job_description == "":
        return "Please paste a job description."

    # Save PDF
    unique_filename = f"{uuid.uuid4()}.pdf"

    resume_path = os.path.join(
        UPLOAD_FOLDER,
        unique_filename
    )

    resume.save(resume_path)

    # -----------------------------
    # Extract Resume Text
    # -----------------------------
    resume_text = ""

    try:

        with pdfplumber.open(resume_path) as pdf:

            for page in pdf.pages:

                text = page.extract_text()

                if text:
                    resume_text += text + "\n"

    except Exception:

        if os.path.exists(resume_path):
            os.remove(resume_path)

        return "Unable to read the uploaded PDF."

    # Delete uploaded file after extraction
    if os.path.exists(resume_path):
        os.remove(resume_path)

    # -----------------------------
    # Gemini Prompt
    # -----------------------------
    prompt = f"""
You are ResumeIQ.

Act as an experienced ATS Resume Reviewer and Technical Recruiter.

Compare the candidate's resume with the job description.

Evaluate:

1. Resume Match Score (0-100)
2. ATS Score (0-100)
3. Hiring Readiness (0-100)
4. Strengths
5. Missing Skills
6. Missing Keywords
7. Recommendations
8. Overall Feedback

Return ONLY valid JSON.

Example:

{{
    "match_score":85,
    "ats_score":90,
    "hiring_readiness":82,

    "strengths":[
        "Python",
        "SQL",
        "Machine Learning"
    ],

    "missing_skills":[
        "Docker",
        "AWS"
    ],

    "missing_keywords":[
        "CI/CD",
        "REST API"
    ],

    "recommendations":[
        "Add measurable achievements",
        "Mention GitHub projects",
        "Include certifications"
    ],

    "overall_feedback":"The resume aligns well with the job description but needs stronger cloud skills and quantified achievements."
}}

Resume:

{resume_text}

Job Description:

{job_description}
"""

    # -----------------------------
    # Gemini Response
    # -----------------------------
    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        response_text = response.text.strip()

        response_text = (
            response_text
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        data = json.loads(response_text)

    except Exception as e:

        data = {
            "match_score": "N/A",
            "ats_score": "N/A",
            "hiring_readiness": "N/A",
            "strengths": [],
            "missing_skills": [],
            "missing_keywords": [],
            "recommendations": [],
            "overall_feedback": f"Unable to analyze resume. {str(e)}"
        }

    # -----------------------------
    # Render Result
    # -----------------------------
    return render_template(
        "result.html",
        data=data
    )


# -----------------------------
# Run App
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)