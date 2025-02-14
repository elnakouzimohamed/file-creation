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

data = json.loads("{ "{{response_1}}": "Protection Risk/Emergency Situation Briefing:

PA, a 33-year-old Syrian refugee with special needs, and his family of five are facing a critical situation. PA's war injury and his wife's mental illness render them unable to provide adequate care for their children. The family resides in a rented tent in Mineh Adawi, paying 
30
p
e
r
m
o
n
t
h
.
H
o
w
e
v
e
r
,
t
h
e
y
h
a
v
e
f
a
l
l
e
n
b
e
h
i
n
d
o
n
r
e
n
t
f
o
r
f
i
v
e
m
o
n
t
h
s
,
t
o
t
a
l
i
n
g
30permonth.However,theyhavefallenbehindonrentforfivemonths,totaling150. The landlord has threatened eviction, confiscation of belongings, and verbal abuse. PA lacks relatives in Lebanon for financial support, and the camp's residents are also facing severe financial constraints.

Purpose of CFP:

The purpose of the Child Focus Program (CFP) is to conduct a comprehensive assessment of PA's family's situation, provide immediate assistance, and develop a plan for long-term support.

Justification for Recommended Action/Assistance:

The family is facing an imminent risk of eviction due to their inability to pay rent. Eviction would expose them to further vulnerability and hardship. The landlord's threats and verbal abuse have created a hostile and unsafe environment for PA and his family. Additionally, the children are at risk of neglect and abuse due to their parents' health conditions. The CFP will provide financial assistance to cover the rent arrears and prevent eviction. It will also offer psychosocial support to the family and explore options for accessible healthcare and rehabilitation services for PA. The CFP will advocate on behalf of the family to ensure their rights and protection.", "{{response_2}}": "The protection risk for PA is clearly articulated as he and his family face the threat of eviction and loss of shelter due to their inability to pay rent and the owner's hostile behavior. The situation is exacerbated by PA's health issues and his wife's mental condition, making it challenging for them to adequately care for their children. The prompt indicates that this is a one-time emergency rather than a recurrent, chronic issue as it mentions that the family has been unable to pay rent for five months, suggesting a temporary financial crisis. However, the prompt does not provide specific details on the cause of the financial difficulty, which could provide further insight into the likelihood of the issue recurring.", "{{response_3}}": "Cash assistance can alleviate the protection risk faced by PA and his family in several ways. Firstly, it can help them pay their overdue rent, preventing their eviction and providing them with a safe and stable living environment. This will reduce the risk of family separation and exposure to violence or exploitation.

Secondly, cash assistance can provide PA with the financial means to access healthcare services for himself and his wife, improving their health and well-being. This will enable PA to better care for his children and reduce the burden on his wife, who suffers from a mental condition.

Thirdly, cash assistance can empower PA and his family by providing them with greater control over their lives and decision-making. This will enhance their resilience and ability to cope with future challenges.

To ensure the protection risk does not reappear once cash assistance ends, it is crucial to implement sustainable solutions alongside the provision of cash. This could include linking PA to vocational training programs, providing his wife with access to mental health services, and advocating for improved living conditions in the camp. By addressing the underlying causes of their vulnerability, PA and his family will be better equipped to navigate the challenges they face and maintain their well-being in the long term.", "{{response_4}}": "The panel has carefully assessed the risks and benefits of providing cash assistance to PA, acknowledging his complex vulnerabilities and the impact it will have on him, his household, and the community. The assistance aims to alleviate PA's financial burden, reduce the pressure on his family, and improve their overall well-being. By providing cash, PA will have greater flexibility and control over meeting his family's essential needs, such as shelter, food, and healthcare, while also promoting their dignity and self-reliance.

For PA as an individual, cash assistance will empower him to access necessary medical care for his war injury and mental health support for his wife, enabling him to better manage his health conditions and improve his quality of life. It will also alleviate the financial stress that has been weighing heavily on him, providing him with peace of mind and reducing his anxiety levels.

At the household level, cash assistance will strengthen family cohesion and improve their overall well-being. PA will be better able to provide for his wife and children, ensuring their basic needs are met and reducing their vulnerability to exploitation and abuse. The improved living conditions will contribute to a more stable and nurturing environment for the children, fostering their physical, emotional, and cognitive development.

Within the community, cash assistance can have ripple effects by stimulating local businesses and services. PA's increased spending power will support small-scale enterprises, creating employment opportunities and contributing to economic revitalization within the camp. By investing in one family, the assistance has the potential to create a positive impact on the entire community.

The panel has given careful consideration to PA's specific needs, age, and gender in determining the appropriate form and level of assistance. As an adult male with war injuries, PA has unique needs that require tailored support. The cash assistance will provide him with the flexibility to access specialized healthcare services and assistive devices that can enhance his mobility and well-being.

Through comprehensive case management, the protection outcomes for PA and his family will be closely monitored and addressed. Regular follow-ups will ensure that the cash assistance is used effectively, that their living conditions improve, and that their protection concerns are adequately addressed. By empowering PA and his family, the case management approach will foster their resilience and ability to cope with the challenges they face, while also advocating for their rights and promoting their well-being." }")
st.title("Form Filler 🤖")
selected_form = st.selectbox("Select a Form:", list(form_data.keys()), index=0)
user_input = st.text_area("Enter The Prompt:", height=250)
response = ""
if st.button("Fill Form"):
    if user_input.strip():
        with st.spinner("Preparing your file..."):
            if(selected_form=="Form3"):

                query1 = "For the given prompt:"+user_input+",analyze it very well and understand it and then answer the questions of the following dictionary:"+json.dumps(form_data.get(selected_form).get("Form3_part1"))+", and fill this dictionary with the correct answers:"+json.dumps(formAnswer.get("Form3_part1"))+"and the answer of {{checks}} is either 'true' or 'false' only, and as a string only, if you do not know if it is 'true' or 'false' then put 'false', and analyze the prompt carefully before answering. Make sure to fill ALL the fields of the given sample and NEVER put a null value, put NA if and only if the answer can not be determined or concluded or interpreted or analyzed from the prompt, but avoid putting NA as much as possible. Give me the result directly in json format with nothing written before or after and DO NOT SKIP ANY ENTRY IN THE ANSWERS file or the dictionary file especially {{check_33}}, and the answers must not exceed 20 words, no 'answer' having more than 20 words is acceptable. Try to elaborate your answers within those 20 words even if there is no enough data try to analyze them, do not write very brief answers. Give me the result directly in json format as a string with nothing written before or after!"
                query2= "For the given prompt:"+user_input+",analyze it very well and understand it and then answer the questions of the following dictionary:"+json.dumps(form_data.get(selected_form).get("Form3_part2"))+", and fill this dictionary with the correct answers:"+json.dumps(formAnswer.get("Form3_part2"))+". Analyze the prompt carefully before answering. Make sure to fill ALL the fields of the given sample and NEVER put a null value, put NA if and only if the answer can not be determined or concluded or interpreted or analyzed from the prompt, but avoid putting NA as much as possible. Give me the result directly in json format with nothing written before or after and DO NOT SKIP ANY ENTRY IN THE ANSWERS file or the dictionary file especially {{check_33}}, and the answers must not exceed 20 words, no 'answer' having more than 20 words is acceptable. Try to elaborate your answers within those 20 words even if there is no enough data try to analyze them, do not write very brief answers. Give me the result directly in json format as a string with nothing written before or after!"
                response1 = get_gemini_response(query1)
                if(response1[:3]=="\"{{"):
                    response1="{"+response1
                if(response1[-1]=='"'):
                    response1=response1+"}"
                response2=  get_gemini_response(query2)
                if(response2[:3]=="\"{{"):
                    response2="{"+response2
                if(response2[-1]=='"'):
                    response2=response2+"}"
                response = response1.rstrip('}') + ',' + response2.lstrip('{')
            elif(selected_form=="Form2"):
                query1 = "For the given prompt:"+user_input+",analyze it very well and understand it and then answer the questions of the following dictionary:"+json.dumps(form_data.get(selected_form).get("Form2_part1"))+", and fill this dictionary with the correct answers:"+json.dumps(formAnswer.get(selected_form))+"and the answer of {{checks}} is either 'true' or 'false' only, and as a string only, if you do not know if it is 'true' or 'false' then put 'false', and analyze the prompt carefully before answering. Make sure to fill ALL the fields of the given sample especially long questions and be strict to the word limit. Give me the result directly in json format with nothing written before or after and DO NOT SKIP ANY ENTRY IN THE ANSWERS file or the dictionary file especially {{check_33}}, and the answers must not exceed 100 words, no 'answer' having more than 100 words is acceptable, and answer directly without writing 'Person said that he/she'. Try to elaborate your answers within those 100 words even if there is no enough data try to analyze them and be reasonable, do not write brief answers. Give me the result directly in json format with nothing written before or after!"
                query2 = "For the given prompt:"+user_input+",analyze it very well and understand it and then answer the questions of the following dictionary:"+json.dumps(form_data.get(selected_form).get("Form2_part2"))+", and fill this dictionary with the correct answers:"+json.dumps(formAnswer.get("Form2_part2"))+"and the answer of {{checks}} is either 'true' or 'false' only, and as a string only, if you do not know if it is 'true' or 'false' then put 'false', and analyze the prompt carefully before answering. Make sure to fill ALL the fields of the given sample especially long questions and be strict to the word limit. Give me the result directly in json format with nothing written before or after and DO NOT SKIP ANY ENTRY IN THE ANSWERS file or the dictionary file especially {{check_33}}, and the answers must not exceed 100 words, no 'answer' having more than 100 words is acceptable, and answer directly without writing 'Person said that he/she'. Try to elaborate your answers within those 100 words even if there is no enough data try to analyze them and be reasonable, do not write brief answers. Give me the result directly in json format with nothing written before or after!"
                response1 = get_gemini_response(query1)
                response2=  get_gemini_response(query2)
                response = response1.rstrip('}') + ',' + response2.lstrip('{')
            # st.write(response)
            elif(selected_form=="CFP"):
                query1 = "For the given prompt:"+user_input+",analyze it very well and understand it and then answer the question: 'write the protection Risk/Emergency situation briefing, purpose of CFP and justification for recommended action/assistance for the corresponding case and write in details, answer as a paragraph not bullet points, be formal'.    Analyze the prompt carefully before answering. Give me the result directly with nothing written before or after, and answer directly without writing 'Person said that he/she', and do not add any text formatting like bold or italic or anything else just a pure text. Give me the answers in the shape of a paragraph without a title or a conclusion or extra stuff. Try to elaborate your answers within the word limit (not less than 300 words), even if there is no enough data try to analyze them and be reasonable, do not write brief answers. must be at least 350-400 words. be formal and add details as much as you can. Give me the result directly as a string with nothing written before or after!"
                response1 = get_gemini_response(query1)
                query2 = "For the given prompt:"+user_input+",analyze it very well and understand it and then answer the question: 'Is the protection risk clearly articulated? Is there good reason to assume it is a one-time emergency rather than a recurrent, chronic issue? answer as a paragraph not bullet points, be formal'.    Analyze the prompt carefully before answering. Give me the result directly with nothing written before or after, and answer directly without writing 'Person said that he/she', and do not add any text formatting like bold or italic or anything else just a pure text. Give me the answers in the shape of a paragraph without a title or a conclusion or extra stuff. Try to elaborate your answers within the word limit (not less than 300 words), even if there is no enough data try to analyze them and be reasonable, do not write brief answers. must be at least 350-400 words. be formal and add details as much as you can. Give me the result directly as a string with nothing written before or after!"
                response2 = get_gemini_response(query2)
                query3 = "For the given prompt:"+user_input+",analyze it very well and understand it and then answer the question: 'Describe how cash assistance can solve or mitigate the protection risk: What is the expected protection outcome? What specific output will cash provide? How does that output contribute to the expected protection outcome? What measures are or will be in place to ensure the protection risk doesn’t reappear once the cash assistance ends? answer as a paragraph not bullet points, be formal'.    Analyze the prompt carefully before answering. Give me the result directly with nothing written before or after, and answer directly without writing 'Person said that he/she', and do not add any text formatting like bold or italic or anything else just a pure text. Give me the answers in the shape of a paragraph without a title or a conclusion or extra stuff. Try to elaborate your answers within the word limit (not less than 300 words), even if there is no enough data try to analyze them and be reasonable, do not write brief answers. must be at least 350-400 words. be formal and add details as much as you can. Give me the result directly as a string with nothing written before or after!"
                response3 = get_gemini_response(query3)
                query4 = "For the given prompt:"+user_input+",analyze it very well and understand it and then answer the question: 'Cash Panel: Has the panel weighed risks vs. benefits of the assistance? What will the impact be on the individual? Household? Community? Has enough consideration been given to the impact of cash on the specific needs, age and gender of the PoC? How will the protection outcome be achieved through case management? answer as a paragraph not bullet points, be formal'.    Analyze the prompt carefully before answering. Give me the result directly with nothing written before or after, and answer directly without writing 'Person said that he/she', and do not add any text formatting like bold or italic or anything else just a pure text. Give me the answers in the shape of a paragraph without a title or a conclusion or extra stuff. Try to elaborate your answers within the word limit (not less than 300 words), even if there is no enough data try to analyze them and be reasonable, do not write brief answers. must be at least 350-400 words. be formal and add details as much as you can. Give me the result directly as a string with nothing written before or after!"
                response4 = get_gemini_response(query4)
                response="{ \"{{response_1}}\": \""+response1+"\", \"{{response_2}}\": \""+response2+"\", \"{{response_3}}\": \""+response3+"\", \"{{response_4}}\": \""+response4+"\" }" 
                st.write(response)
                # if(response[:3]=="\"{{"):
                #     response="{"+response
                # if(response[-1]=='"'):
                #     response=response+"}"
                # if(response[0]!='{' and response[-1]!='}'):
                #     response="{"+response+"}"
    else:
        st.warning("Please enter a valid prompt!")

word_docs = {
    "Form1": "form1.docx",
    "Form2": "form2.docx",
    "Form3": "form3.docx",
    "Form4": "form4.docx",
    "Form5": "form5.docx",
    "Form6": "form6.docx",
    "CFP": "CFP.docx"
}
print(response)
doc = Document(word_docs.get(selected_form))

data = {}
# Dictionary of values to replace placeholders
if response != "":
    try:
        st.write("loading")
        data = json.loads(response)
        st.write("Loaded")
        
        if(selected_form=="Form3"):
            all_key_values= formAnswer.get("Form3_part1")
            missing_keys = find_missing_keys(formAnswer.get("Form3_part1"), formAnswer.get("Form3_part2"))
            for key in missing_keys:
                if str(key).startswith("{{Check"):
                    all_key_values[key] = " ☐"
                else:
                    all_key_values[key] = " "
            missing_keys = find_missing_keys(all_key_values, data)
            for key in missing_keys:
                if str(key).startswith("{{Check"):
                    data[key] = " ☐"
                else:
                    data[key] = " "

        elif(selected_form=="Form2"):
            all_key_values= formAnswer.get("Form2")
            missing_keys = find_missing_keys(formAnswer.get("Form2"), formAnswer.get("Form2_part2"))
            for key in missing_keys:
                if str(key).startswith("{{Check"):
                    all_key_values[key] = " ☐"
                else:
                    all_key_values[key] = " "
            missing_keys = find_missing_keys(all_key_values, data)
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
                            if str(value) == "false" or str(value) == "False" or str(value) == "No" or str(value) == "no":
                                if(str(key).startswith("{{Check")):
                                    cell.text = cell.text.replace(key, " ☐")
                                else:
                                    cell.text = cell.text.replace(key, value)
                            elif str(value) == "true" or str(value) == "True" or str(value) == "Yes" or str(value) == "yes":
                                if(str(key).startswith("{{Check")):
                                    cell.text = cell.text.replace(key, " ☑")
                                else:
                                    cell.text = cell.text.replace(key, value)
                            elif value in {"NA", "answer", "N/A", "null", "Null"}:
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





