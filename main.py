import streamlit as st
import PyPDF2
import io
import os
from groq import Groq

st.title("AI Resume Analyzer")

uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "txt"])
job_role = st.text_input("Target Job Role")

if st.button("Analyze"):

    if uploaded_file is None:
        st.warning("Please upload a resume")
        st.stop()

    def extract_text(file):

        if file.type == "application/pdf":

            pdf = PyPDF2.PdfReader(file)
            text = ""

            for page in pdf.pages:
                text += page.extract_text() or ""

            return text

        return file.read().decode()

    resume_text = extract_text(uploaded_file)

    client = Groq(api_key=st.secrets["GROQ_API_KEY"])

    prompt = f"""
Analyze this resume and give feedback.

Target Role: {job_role}

Resume:
{resume_text}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    st.write(response.choices[0].message.content)
