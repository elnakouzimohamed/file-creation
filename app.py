import streamlit as st
from google import genai
from docx import Document
import json
from answers import formAnswer
from questions import form_data
import os

# =========================
# GEMINI 3 CLIENT (FREE)
# =========================
client = genai.Client(
    api_key="AIzaSyCKfQtaNLGNvRTazcDzetjUZ15MVRFZhKs"
)

def get_gemini_response(prompt):
    response = client.models.generate_content(
        model="gemini-3-flash",
        contents=prompt
    )
    return response.text.strip()

# =========================
# HELPERS
# =========================
def process_item(item):
    if isinstance(item, dict):
        temp_dict = {}
        for key, value in item.items():
            if key.startswith('{{'):
                temp_dict[key] = value
            elif isinstance(value, dict):
                processed = process_item(value)
                for k, v in processed.items():
                    temp_dict[k] = v
        return temp_dict
    return item

def find_missing_keys(form1, form2):
    return list(set(form1.keys()) - set(form2.keys()))

# =========================
# AUTH
# =========================
APP_PASSWORD = "mgt1988"

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

# =========================
# MAIN APP
# =========================
st.title("Form Filler")

selected_form = st.selectbox("Select a Form:", list(form_data.keys()), index=0)
user_input = st.text_area("Enter The Prompt:", height=250)

response = ""

if st.button("Fill Form"):
    if user_input.strip():
        with st.spinner("Preparing your file..."):

            if selected_form == "Form3":
                query1 = (
                    "For the given prompt:" + user_input +
                    ", analyze it carefully and fill this answers dictionary: " +
                    json.dumps(formAnswer.get("Form3_part1")) +
                    " based on these questions: " +
                    json.dumps(form_data.get(selected_form).get("Form3_part1")) +
                    ". Return ONLY valid JSON."
                )

                query2 = (
                    "For the given prompt:" + user_input +
                    ", analyze it carefully and fill this answers dictionary: " +
                    json.dumps(formAnswer.get("Form3_part2")) +
                    " based on these questions: " +
                    json.dumps(form_data.get(selected_form).get("Form3_part2")) +
                    ". Return ONLY valid JSON."
                )

                r1 = json.loads(get_gemini_response(query1))
                r2 = json.loads(get_gemini_response(query2))

                response = {**r1, **r2}
                response = process_item(response)

            elif selected_form == "Form2":
                query1 = (
                    "For the given prompt:" + user_input +
                    ", analyze it carefully and fill this answers dictionary: " +
                    json.dumps(formAnswer.get("Form2_part1")) +
                    " based on these questions: " +
                    json.dumps(form_data.get(selected_form).get("Form2_part1")) +
                    ". Return ONLY valid JSON."
                )

                query2 = (
                    "For the given prompt:" + user_input +
                    ", analyze it carefully and fill this answers dictionary: " +
                    json.dumps(formAnswer.get("Form2_part2")) +
                    " based on these questions: " +
                    json.dumps(form_data.get(selected_form).get("Form2_part2")) +
                    ". Return ONLY valid JSON."
                )

                r1 = json.loads(get_gemini_response(query1))
                r2 = json.loads(get_gemini_response(query2))

                response = {**r1, **r2}
                response = process_item(response)

            elif selected_form == "CFP":
                query = (
                    "For the given prompt:" + user_input +
                    ", analyze it carefully and fill this answers dictionary: " +
                    json.dumps(formAnswer.get(selected_form)) +
                    " based on these questions: " +
                    json.dumps(form_data.get(selected_form)) +
                    ". Return ONLY valid JSON."
                )

                response = json.loads(get_gemini_response(query))
                response = process_item(response)

    else:
        st.warning("Please enter a valid prompt!")

# =========================
# WORD FILE HANDLING
# =========================
word_docs = {
    "Form1": "form1.docx",
    "Form2": "form2.docx",
    "Form3": "form3.docx",
    "Form4": "form4.docx",
    "Form5": "form5.docx",
    "Form6": "form6.docx",
    "CFP": "CFP.docx"
}

if response:
    doc = Document(word_docs.get(selected_form))
    data = response

    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for key, value in data.items():
                    if key in cell.text:
                        if str(value).lower() in ["true", "yes"]:
                            cell.text = cell.text.replace(key, " ☑")
                        elif str(value).lower() in ["false", "no", "na", ""]:
                            cell.text = cell.text.replace(key, " ☐")
                        else:
                            cell.text = cell.text.replace(key, str(value))

    file_path = f"{selected_form}_filled.docx"
    doc.save(file_path)

    st.success("✅ The form is successfully filled!")

    with open(file_path, "rb") as file:
        btn = st.download_button(
            label="📄 Download Filled Word Document",
            data=file,
            file_name=file_path,
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )

    if btn:
        os.remove(file_path)

# =========================
# CASE NOTES (UNCHANGED LOGIC)
# =========================
st.write(" ")
st.write(" ")
st.title("Case Notes Filler")

caseNoteDict = {
    "{time1}": "answer",
    "{first}": "answer",
    "{time2}": "answer",
    "{second}": "answer",
    "{time3}": "answer",
    "{third}": "answer",
    "{time4}": "answer",
    "{fourth}": "answer",
    "{time5}": "answer",
    "{fifth}": "answer",
    "{time6}": "answer",
    "{sixth}": "answer",
    "{time7}": "answer",
    "{seventh}": "answer",
    "{time8}": "answer",
    "{eighth}": "answer",
    "{time9}": "answer",
    "{ninth}": "answer",
    "{time10}": "answer",
    "{tenth}": "answer"
}

user_input2 = st.text_area("Enter:", height=250)

if st.button("Fill Case Note") and user_input2.strip():
    caseQuery = (
        "For each timeline in: " + user_input2 +
        " fill this dictionary with extremely detailed explanations: " +
        json.dumps(caseNoteDict) +
        ". Return ONLY valid JSON."
    )

    caseData = json.loads(get_gemini_response(caseQuery))
    caseNote = Document("CaseNotes.docx")

    for table in caseNote.tables:
        for row in table.rows:
            for cell in row.cells:
                for key, value in caseData.items():
                    if key in cell.text:
                        cell.text = cell.text.replace(key, value or "")

    file_path2 = "CaseNotes_filled.docx"
    caseNote.save(file_path2)

    st.success("✅ Case notes filled!")

    with open(file_path2, "rb") as file:
        btn = st.download_button(
            label="📄 Download Filled Case Notes Document",
            data=file,
            file_name=file_path2,
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )

    if btn:
        os.remove(file_path2)








