import streamlit as st
import PyPDF2
import io
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="AI Resume Critiquer", page_icon="📃", layout="centered")

st.title("AI Resume Critiquer")
st.markdown("Upload your resume and get AI-powered feedback tailored to your needs!")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

uploaded_file = st.file_uploader("Upload your resume (PDF of TXT)", type=["pdf", "txt"])
job_role = st.text_input("Enter the job role you're taregtting (optional)")

analyze = st.button("Analyze Resume")

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

def extract_text_from_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        return extract_text_from_pdf(io.BytesIO(uploaded_file.read()))
    return uploaded_file.read().decode("utf-8")

if analyze and uploaded_file:
    try:
        file_content = extract_text_from_file(uploaded_file)
        
        if not file_content.strip():
            st.error("File does not have any contnet...")
            st.stop()
        
        prompt = f"""You are an expert AI Resume Critiquer and career coach specializing in IT and software roles.
                Your job is to carefully analyze a candidate’s resume (and, if provided, the job description) and give clear, practical feedback that will help them improve their chances of getting interviews.
                When you respond, always be honest, specific, and encouraging. Avoid generic advice like “improve your skills” or “make it better.” Point to exact lines, phrases, or sections that can be improved and suggest concrete rewrites.
                For each resume you receive, follow this structure in your reply:
                Overall Summary (2–4 sentences)
                Briefly describe the candidate’s profile (experience level, main tech skills, impression).
                Strengths
                Bullet points listing what the resume does well (e.g., clear tech stack, good projects, measurable achievements, etc.).
                Issues / Weaknesses
                Bullet points of problems: formatting issues, grammar, missing details, vague bullet points, lack of metrics, poor ordering, etc.
                Specific Line-by-Line Suggestions
                Quote or reference weak bullet points or sections from the resume.
                For each one, provide an improved version.
                Focus on using strong action verbs, quantifying impact (numbers, %, time saved), and highlighting relevant tools/technologies.
                ATS & Keywords Check (for IT roles)
                Suggest important keywords and technologies that might be missing based on the candidate’s field (e.g., Python, Django, REST API, React, AWS, Docker, CI/CD, SQL, etc.).
                Mention if the resume is likely to pass an Applicant Tracking System (ATS) and how to improve that.
                Score
                Give a score out of 100 for this resume for the target role.
                Example: “Resume Score: 78/100 for Junior Python Developer role.”
                If a job description is provided, heavily align your feedback and suggestions to that job description (required skills, responsibilities, keywords).
                If a job description is not provided, assume the target role is a general Software / IT Developer position.
                Always answer in clear, simple English, using headings and bullet points so it’s easy to read.
                4. Specific improvements for {job_role if job_role else 'general job applications'}
        
                Resume content:
                {file_content}
        
                Please provide your analysis in a clear, structured format with specific recommendations.
            """
        
        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert resume reviewer with years of experience in HR and recruitment."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        st.markdown("### Analysis Results")
        st.markdown(response.choices[0].message.content)
    
    except Exception as e:
        st.error(f"An error occured: {str(e)}")