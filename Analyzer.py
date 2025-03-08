import os
import streamlit as st
import google.generativeai as genai
import PyPDF2
import streamlit as st


def set_custom_font():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Anton&family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap');
        body {
        font-family: 'Poppins', sans-serif;
        }

        h1 {
        color: #4CAF50;
        text-align: center;
        }
        html, body, .stApp {
            font-family: 'Poppins', sans-serif;
        }

        .stTextInput, .stButton, .stTitle, .stHeader, .stSubheader {
            font-family: 'Poppins', sans-serif;
        }
        .poppins-bold {
        font-family: "Poppins", sans-serif;
        font-weight: 700;
        font-style: normal;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

set_custom_font()

def add_bg_image():
    st.markdown(
        """
        <style>
        .stApp {
            background-image: url("https://wallpapercave.com/wp/VmZHnTO.jpg");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def remove_streamlit_header():
    st.markdown(
        """
        <style>
        header {visibility: hidden;}
        .block-container {
            padding-top: 0;  /* Adjust content spacing after header removal */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

add_bg_image()  
remove_streamlit_header()  

st.write(" ")
st.write("  ")
st.title("Job Recommendation AI")
st.markdown("<h5 style='text-align: center;'>Upload your resume (PDF) and get personalized job recommendations!</h5>", unsafe_allow_html=True)


api_key = "AIzaSyCfbKDOKMGa41MYQfaYvWsdyZIitRzLcA0"

if not api_key:
    st.warning("Please enter your Google AI API key to proceed.")
    st.stop()

genai.configure(api_key=api_key)


if 'response' not in st.session_state:
    st.session_state.response = None

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
    st.session_state.response = response.text  


if st.session_state.response:
    st.subheader("Your Job Recommendations")
    st.write(st.session_state.response)