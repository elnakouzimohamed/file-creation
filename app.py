import streamlit as st
import google.generativeai as genai
from docx import Document
import json
from answers import formAnswer
from questions import form_data
import os
# Set your API Key
genai.configure(api_key="AIzaSyArlFxEb2FUqVIQEL_T6h7IeTu1C-2axu4")

# Function to get response from Gemini API
def get_gemini_response(prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text

# Streamlit UI
st.title("File Filler 🤖")

# User input



selected_form = st.selectbox("Select a Form:", list(form_data.keys()), index=0)

user_input = st.text_area("Enter your message:", height=150)
response = ""
if st.button("Generate Response"):
    if user_input.strip():
        with st.spinner("Thinking... 🤔"):
            query = "For the given prompt  "+user_input+ "Answer the questions of the following dictionary: " +json.dumps(form_data.get(selected_form)) + " and fill this dictionary with the correct answers: "+ json.dumps(formAnswer.get(selected_form)) + " and the answer of {{checks}} is either yes or no.Make sure to fill all the fields of the given sample. Give me the result directly in json format with nothing written before or after."
            response = get_gemini_response(query)
        st.write("**Gemini AI Response:**")
        st.write(response)
    else:
        st.warning("Please enter a valid prompt!")





# Load the existing Word form
#doc = Document("trial1.docx")
word_docs = {
    "Form1": "form1.docx",
    "Form2": "form2.docx",
    "Form3": "form3.docx",
    "Form4": "form4.docx",
    "Form5": "form5.docx",
    "Form6": "form6.docx",
}
print(response)
doc=Document(word_docs.get(selected_form))
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
                            if value == "No":
                               cell.text = cell.text.replace(key, " ☐") 
                            elif value == "Yes":
                                cell.text = cell.text.replace(key, " ☑") 
                            else:
                                cell.text = cell.text.replace(key, value)

        file_path = f"{selected_form}_filled.docx"
        filled = doc.save(file_path)
        print("✅ Form successfully filled!")
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

        print("✅ Form successfully filled and deleted after download!")

    except json.JSONDecodeError:
        st.error("Try Again")





