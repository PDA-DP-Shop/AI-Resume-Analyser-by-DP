import streamlit as st
import pdfplumber
from groq import Groq

st.set_page_config(page_title="AI Resume Analyzer")

st.title("AI Resume Analyzer")

uploaded_file = st.file_uploader(
    "Upload Resume",
    type=["pdf", "txt"]
)

job_role = st.text_input("Target Job Role")


def extract_text(file):

    text = ""

    if file.type == "text/plain":
        text = file.read().decode()

    elif file.type == "application/pdf":

        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""

    return text


if st.button("Analyze"):

    if uploaded_file is None:
        st.warning("Please upload a resume")
        st.stop()

    resume_text = extract_text(uploaded_file)

    if resume_text.strip() == "":
        st.error("Could not read resume text. Please upload a text-based PDF.")
        st.stop()

    client = Groq(api_key=st.secrets["GROQ_API_KEY"])

    prompt = f"""
You are an expert resume reviewer.

Analyze this resume and provide:

1. Overall Summary
2. Strengths
3. Weaknesses
4. Suggestions
5. ATS Keywords
6. Resume Score out of 100

Target Job Role: {job_role}

Resume:
{resume_text}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    st.subheader("Resume Analysis")
    st.write(response.choices[0].message.content)
