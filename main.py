import streamlit as st
import PyPDF2
import io
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="AI Resume Critiquer", page_icon="📃", layout="centered")

st.title("AI Resume Critiquer")
st.markdown("Upload your resume and get AI-powered feedback!")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

uploaded_file = st.file_uploader("Upload your resume (PDF or TXT)", type=["pdf", "txt"])
job_role = st.text_input("Enter the job role you're targeting (optional)")

analyze = st.button("Analyze Resume")


def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""

    for page in pdf_reader.pages:
        text += page.extract_text() or ""

    return text


def extract_text_from_file(uploaded_file):

    if uploaded_file.type == "application/pdf":
        return extract_text_from_pdf(io.BytesIO(uploaded_file.read()))

    return uploaded_file.read().decode("utf-8")


if analyze and uploaded_file:

    try:

        file_content = extract_text_from_file(uploaded_file)

        if not file_content.strip():
            st.error("File does not contain text")
            st.stop()

        prompt = f"""
You are an expert AI Resume Reviewer.

Analyze the following resume and give detailed feedback.

Structure:

1. Overall Summary
2. Strengths
3. Weaknesses
4. Suggestions for Improvement
5. ATS Keyword Suggestions
6. Resume Score out of 100

Target Job Role: {job_role if job_role else "General Software Developer"}

Resume:
{file_content}
"""

        client = Groq(api_key=GROQ_API_KEY)

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are an expert resume reviewer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )

        st.markdown("## Resume Analysis")
        st.write(response.choices[0].message.content)

    except Exception as e:
        st.error(f"Error: {str(e)}")
