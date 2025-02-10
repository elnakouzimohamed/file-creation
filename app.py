import streamlit as st
import google.generativeai as genai
from docx import Document
import json
from answers import formAnswer
from questions import form_data
import os

# Gemini API Key
genai.configure(api_key="AIzaSyArlFxEb2FUqVIQEL_T6h7IeTu1C-2axu4")
APP_PASSWORD = "Trabolsi#DRC"

# Initialize authentication state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Authentication UI
if not st.session_state.authenticated:
    st.title("🔒 Enter Password")
    password = st.text_input("Password:", type="password")
    
    if st.button("Login"):
        if password == APP_PASSWORD:
            st.session_state.authenticated = True
            st.rerun()  # Use st.rerun() instead of st.experimental_rerun()
        else:
            st.error("Incorrect password. Try again.")
    
    st.stop()  # Stop execution if not authenticated


# Function to get response from Gemini API
def get_gemini_response(prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text

# Streamlit UI
st.title("File Filler 🤖")

# User input
selected_form = st.selectbox("Select a Form:", list(form_data.keys()), index=0)

user_input = st.text_area("Enter The Prompt:", height=150)
response = ""
if st.button("Fill Form"):
    if user_input.strip():
        with st.spinner("Preparing your file..."):
            query = "For the given prompt:"+user_input+ ", analyze then answer the questions of the following dictionary: " +json.dumps(form_data.get(selected_form)) + ", and fill this dictionary with the correct answers: "+ json.dumps(formAnswer.get(selected_form)) + " and the answer of {{checks}} is either 'true' or 'false', if you do not know if it is true or false then put 'false'. Make sure to fill all the fields of the given sample and never put a null value, put NA instead, however for {{checks}} like {{check_14}} put 'false' if you do not know or have an answer. Give me the result directly in json format with nothing written before or after and do not skip any entry in the answers file or the dictionary file, and be brief with the text answers but not too brief. Give me the result directly in json format as a string with nothing written before or after!"
            
            #  "For the given prompt  "+user_input+ "Answer the questions of the following dictionary: " +json.dumps(form_data.get(selected_form)) + " and fill this dictionary with the correct answers: "+ json.dumps(formAnswer.get(selected_form)) + ", and the answer of {{checks}} is either 'true' or 'false', and lowercase only. Make sure to fill all the fields of the given sample, if there exist a question that you can't answer just leave it as an 'empty string' and never null. Give me the result directly in json format with nothing written before or after."
            response = get_gemini_response(query)
        st.write("**Gemini AI Response:**")
        st.write(response)
    else:
        st.warning("Please enter a valid prompt!")


# Load the existing Word form
# doc = Document("trial1.docx")
word_docs = {
    "Form1": "form1.docx",
    "Form2": "form2.docx",
    "Form3": "form3.docx",
    "Form4": "form4.docx",
    "Form5": "form5.docx",
    "Form6": "form6.docx",
}
print(response)
doc = Document(word_docs.get(selected_form))

data = {}
# Dictionary of values to replace placeholders
if response != "":
    try:
        data = json.loads(response)
        print(data,type(data))
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    for key, value in data.items():
                        if key in cell.text:
                            if value == "false":
                               cell.text = cell.text.replace(key, " ☐") 
                            elif value == "true":
                                cell.text = cell.text.replace(key, " ☑") 
                            elif value == "NA":
                                cell.text = cell.text.replace(key, " ")
                            else:
                                cell.text = cell.text.replace(key, value)

        file_path = f"{selected_form}_filled.docx"
        filled = doc.save(file_path)
        print("✅ The form is successfully filled!")
        with open(file_path, "rb") as file:
            btn = st.download_button(
                label="📄 Download Filled Word Document",
                data=file,
                file_name=file_path,
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )

        # Delete file after download button is clicked
        if btn:
            os.remove(file_path)

        print("✅ The form is successfully filled and deleted after downloading!")

    except json.JSONDecodeError:
        st.error("Try Again")





