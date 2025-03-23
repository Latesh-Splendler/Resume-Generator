import streamlit as st
import google.generativeai as genai
from fpdf import FPDF

# Load API key from Streamlit secrets
GEMINI_API_KEY = st.secrets["gemini"]["api_key"]

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Define Gemini model
MODEL_NAME = "gemini-1.5-pro-001"  # Ensure this is available in your API list

# Function to generate a resume using Gemini API
def generate_resume(name, about, employment_history, education, skills, experience):
    prompt = f"""
    Generate a professional resume with the following details:

    **Personal Information:**
    Name: {name}

    **About Me:**
    {about}

    **Employment History:**
    {employment_history}

    **Education:**
    {education}

    **Skills:**
    {skills}

    **Experience:**
    {experience}

    Ensure the resume is well-structured, professional, and formatted neatly.
    """

    try:
        response = genai.GenerativeModel(MODEL_NAME).generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: Unable to generate resume. An error occurred with the Gemini API: {str(e)}"

# Function to generate a PDF resume
def generate_pdf(resume_text):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # ✅ FIX: Use a built-in font instead of DejaVuSans
    pdf.set_font("Arial", size=12)

    pdf.multi_cell(0, 10, resume_text)

    pdf_path = "generated_resume.pdf"
    pdf.output(pdf_path, "F")
    return pdf_path

# Streamlit UI
st.title("AI-Powered Resume Builder")
st.write("Generate a professional resume instantly using AI.")

# User Inputs
name = st.text_input("Enter your full name:")
about = st.text_area("About Me:", "Write a brief introduction about yourself...")
employment_history = st.text_area("Employment History:", "List your past job positions and companies...")
education = st.text_area("Education:", "List your degrees and institutions...")
skills = st.text_area("Skills:", "Mention your key skills and expertise areas...")
experience = st.text_area("Experience:", "Describe relevant work experience...")

# Generate Resume Button
if st.button("Generate Resume"):
    if name and about and employment_history and education and skills and experience:
        resume_output = generate_resume(name, about, employment_history, education, skills, experience)
        
        if not resume_output.startswith("Error:"):
            pdf_file = generate_pdf(resume_output)
            st.success("Resume generated successfully!")
            st.download_button("Download Resume", data=open(pdf_file, "rb"), file_name="Resume.pdf", mime="application/pdf")
        else:
            st.error(resume_output)
    else:
        st.warning("Please fill in all fields before generating the resume.")
