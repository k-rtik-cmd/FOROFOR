import os
import streamlit as st
import google.generativeai as genai
import PyPDF2

st.title("Job Recommendation AI")
st.write("Upload your resume (PDF) and get personalized job recommendations!")


api_key = "AIzaSyCfbKDOKMGa41MYQfaYvWsdyZIitRzLcA0"

if not api_key:
    st.warning("Please enter your Google AI API key to proceed.")
    st.stop()

genai.configure(api_key="AIzaSyCfbKDOKMGa41MYQfaYvWsdyZIitRzLcA0")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    file_path = os.path.join("uploads", uploaded_file.name)
    os.makedirs("uploads", exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        text = ""
        for page in reader.pages:
            text += page.extract_text()

    model = genai.GenerativeModel("gemini-2.0-pro-exp-02-05")
    prompt = f"""Youre a job suggesting AI that takes input as a pdf file from the user which is basically the user's resume and then based on his/her resume gives : 
1. A personalized character profile.
2. Job recommendations based on his skills and experience with direct links to the companies
3. Suggest skills that would help improve the resume and also tell what job opportunities it will open

You talk in a very short, friendly and clean manner 
Here is the resume text:
{text}
"""

    st.write("Generating recommendations...")
    response = model.generate_content(prompt)

    st.subheader("Your Job Recommendations")
    st.write(response.text)

    os.remove(file_path)