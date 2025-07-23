import streamlit as st
import pymupdf
import google.generativeai as genai
import os
from dotenv import load_dotenv
import re
import PyPDF2


load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.0-flash-lite")

def clean_text(text):
    return re.sub(r'\s+', ' ', text.strip().lower())

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    text = ""
    doc = pymupdf.open(stream=pdf_file.read(), filetype="pdf")  
    for page in doc:
        text += page.get_text("text")
    return clean_text(text)

def generate_answers(content, query):
    prompt = f'''
    Based on the following content:
    {content}
    
    Answer the following question:
    {query}
    
    Provide a concise and clear answer.
    '''

    
    try:
        response = model.generate_content(prompt)
        return response.candidates[0].content.parts[0].text if response.candidates else "No answer generated."
    except Exception as e:
        return f"Error: {str(e)}"

#st.set_page_config(page_title="Answer Generator from PDF")
#st.header("Generate Answers from PDF")
st.set_page_config(page_title="🔍 Ask PDF: Engineering Scope in Pakistan", page_icon="📘")
st.title("📘 PDF Question Answering Bot")
st.markdown("---")
st.subheader("📤 Ask anything about Engineering")



with open('imd.pdf', 'rb') as file:
    reader = PyPDF2.PdfReader(file)
    full_text = ""
    for page in reader.pages:
        full_text += page.extract_text()
    
    # Save to session state
    st.session_state['pdf_content'] = clean_text(full_text)
    
    # Get the number of pages
    num_pages = len(reader.pages)
    
    # Read text from the first page
    page = reader.pages[0]
    text = page.extract_text()

    
if 'pdf_content' not in st.session_state or not st.session_state['pdf_content']:
    full_text = ""
    for page in reader.pages:
        full_text += page.extract_text()
    st.session_state['pdf_content'] = clean_text(full_text)



    if 'pdf_content' not in st.session_state:
     st.session_state['pdf_content'] = ""

st.write("🎯If you just passed Inter or just want to know about engineering you can search anything about engineering.")
user_query = st.text_input("💬 What would you like to know about engineering?")



if st.button("Generate Answer") and st.session_state['pdf_content']:
    content = st.session_state['pdf_content']
    answer = generate_answers(content, user_query)

    st.subheader("Generated Answer:")
    st.text(answer)
    
st.markdown("---")
st.markdown("📌 **Tip:** The quality of answers improves with specific, clear questions.")
st.markdown("🔄 You can ask anything about engineering!")
