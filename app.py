import streamlit as st
import google.generativeai as genai
from docx import Document
import json
from answers import formAnswer
from questions import form_data
import os

def get_gemini_response(prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text

def find_missing_keys(form1, form2):
    return list(set(form1.keys()) - set(form2.keys()))

genai.configure(api_key="AIzaSyArlFxEb2FUqVIQEL_T6h7IeTu1C-2axu4")

APP_PASSWORD = "xyzabc#DRC"
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if not st.session_state.authenticated:
    st.title("🔒 Enter Password")
    password = st.text_input("Password:", type="password")
    if st.button("Login"):
        if password == APP_PASSWORD:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Incorrect password. Try again.")
    st.stop()


st.title("File Filler 🤖")
selected_form = st.selectbox("Select a Form:", list(form_data.keys()), index=0)
user_input = st.text_area("Enter The Prompt:", height=250)
response = ""
if st.button("Fill Form"):
    if user_input.strip():
        with st.spinner("Preparing your file..."):
            query = "For the given prompt:"+user_input+",analyze it very well and understand it and then answer the questions of the following dictionary:"+json.dumps(form_data.get(selected_form))+", and fill this dictionary with the correct answers:"+json.dumps(formAnswer.get(selected_form))+"and the answer of {{checks}} is either 'true' or 'false' only only as a string only, if you do not know if it is 'true' or 'false' then ignore it and don't include it in the answers json, and analyze carefully before answering. Make sure to fill ALL the fields of the given sample and NEVER put a null value, ignore instead if and only if when the answer can not be determined or concluded or interpreted or analyzed from the prompt. Give me the result directly in json format with nothing written before or after and DO NOT SKIP AN ENTRY IN THE ANSWERS file or the dictionary file especially {{check_33}}, and the answers must not exceed 40 words, no 'answer' having more than 40 words is acceptable. Try to elaborate your answers within those 40 words even if there is no enough data try to analyze them, do not write very brief answers. Give me the result directly in json format as a string with nothing written before or after!"
            response = get_gemini_response(query)
        st.write(response)
    else:
        st.warning("Please enter a valid prompt!")

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
        
        missing_keys = find_missing_keys(formAnswer.get(selected_form), data)
        for key in missing_keys:
            if str(key).startswith("{{Check"):
                data[key] = " ☐"
            else:
                data[key] = " "
                
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    for key, value in data.items():
                        if key in cell.text:
                            if str(value) == "false":
                                if(str(key).startswith("{{Check")):
                                    cell.text = cell.text.replace(key, " ☐")
                                else:
                                    cell.text = cell.text.replace(key, value)
                            elif str(value) == "true":
                                if(str(key).startswith("{{Check")):
                                    cell.text = cell.text.replace(key, " ☑")
                                else:
                                    cell.text = cell.text.replace(key, value)
                            elif value == "NA" or value=="answer":
                                if(str(key).startswith("{{Check")):
                                    cell.text = cell.text.replace(key, " ☐")
                                else:
                                    cell.text = cell.text.replace(key, " ")
                            else:
                                cell.text = cell.text.replace(str(key or ""), str(value or ""))

        file_path = f"{selected_form}_filled.docx"
        filled = doc.save(file_path)
        st.write("✅ The form is successfully filled!")
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





