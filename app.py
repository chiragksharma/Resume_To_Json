import streamlit as st
import requests
import json
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key from environment variables
api_key = os.getenv("API_KEY")

# Ensure the API key is loaded
if not api_key:
    st.error("API key not found. Please check your .env file.")
    st.stop()

# Configure the API key
genai.configure(api_key=api_key)


# Function to call the LLM API
def convert_resume_to_json(file_content, file_name):
    try:
        # Set the model to Gemini 1.5 Pro
        model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")

        prompt = (
            "Context: I am developing a Streamlit application that takes an input resume file and converts it into JSON format. "
            "AI’s Role: You are an expert in data extraction and transformation. "
            "Action: Convert the given resume file into a structured JSON format. "
            "Audience: The end-users of this application are HR professionals and recruiters who need a structured JSON representation of resumes for better data handling. "
            "Goal: The goal is to accurately extract all relevant information from the resume and convert it into a well-structured JSON format. "
            "Style & Tone: Your response should be technical, clear, and concise. "
            "Format: Format the response as a step-by-step process that includes handling the input file, extracting information, and outputting JSON."
        )

        # Prepare the file as expected by the API
        file = {
            'data': file_content,
            'mime_type': 'application/pdf' if file_name.endswith(
                '.pdf') else 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        }

        # Generate content using the model
        response = model.generate_content([prompt, file])

        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred: {e}")
        return None


# Streamlit app
st.title("Resume to JSON Converter")

st.write("Upload your resume file and convert it to JSON format.")

uploaded_file = st.file_uploader("Choose a resume file", type=["pdf", "docx"])

if uploaded_file is not None:
    st.write("File uploaded successfully.")

    # Read the file content
    file_content = uploaded_file.read()
    file_name = uploaded_file.name

    # Call the function to convert the resume
    with st.spinner("Converting..."):
        result = convert_resume_to_json(file_content, file_name)

    if result:
        st.write("Conversion successful!")
        # Display the JSON result
        st.json(result)
        # Option to download the JSON file
        json_file = json.dumps(result, indent=4)
        st.download_button(label="Download JSON", data=json_file, file_name="resume.json", mime="application/json")
    else:
        st.write("Conversion failed. Please try again.")
else:
    st.write("Please upload a file.")
