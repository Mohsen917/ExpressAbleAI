import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure the Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Set up the model
model = genai.GenerativeModel('gemini-pro')

def translate_text(text, target_language):
    # Constructs a prompt to translate the given text into the target language
    prompt = f"Translate the following text into {target_language}:\n\n{text}"
    response = model.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(
            temperature=0.7,
            max_output_tokens=512,
        )
    )
    return response.text

def enhance_text(text, enhancement_type):
    # Constructs a prompt to enhance the text based on the selected enhancement type
    prompt = f"Enhance the following text to make it more {enhancement_type.lower()}:\n\n{text}"
    response = model.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(
            temperature=0.7,
            max_output_tokens=512,
        )
    )
    return response.text

st.title("Gemini AI Text Processing App")

# Task selection now includes Text Translation and Text Enhancement
task_type = st.radio("Select Task", ["Text Translation", "Text Enhancement"])

if task_type == "Text Translation":
    st.header("Text Translation")
    text_input = st.text_area("Enter text to translate:")
    language = st.selectbox("Select language to translate into:", 
                            ["Spanish", "French", "English", "Arabic"])
    
    if st.button("Translate"):
        if text_input:
            with st.spinner("Translating text..."):
                result = translate_text(text_input, language)
            st.success("Translated Text:")
            st.write(result)
        else:
            st.error("Please enter text to translate.")

elif task_type == "Text Enhancement":
    st.header("Text Enhancement")
    text_input = st.text_area("Enter text to enhance:")
    enhancement_type = st.selectbox("Select enhancement type:", 
                                    ["Formal", "Friendly", "Concise", "Detailed"])
    
    if st.button("Enhance"):
        if text_input:
            with st.spinner("Enhancing text..."):
                result = enhance_text(text_input, enhancement_type)
            st.success("Enhanced Text:")
            st.write(result)
        else:
            st.error("Please enter text to enhance.")

# Advanced Options
st.sidebar.header("Advanced Options")
temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.7, 0.1, 
                                help="Controls randomness in output. Lower values make the output more deterministic.")
max_tokens = st.sidebar.number_input("Max Tokens", 50, 1024, 256, 50, 
                                     help="Maximum number of tokens in the output.")

st.sidebar.header("About")
st.sidebar.info("""
This Gemini AI Text Processing App allows you to:
1. Translate text into different languages.
2. Enhance text based on selected style (formal, friendly, concise, or detailed).

The app uses Google's free Gemini Pro model to process your input.
""")
