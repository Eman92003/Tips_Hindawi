import streamlit as st
import requests
import base64

st.title("CV Extractor")

# رفع الملف
uploaded_file = st.file_uploader("Upload CV PDF", type=["pdf"])

if uploaded_file:
    with st.spinner("Extracting data..."):
        # اقرأ الملف كـ bytes
        pdf_bytes = uploaded_file.read()
        
        # حوّل bytes لـ base64
        pdf_base64 = base64.b64encode(pdf_bytes).decode("utf-8")

        # إعداد payload
        payload = {"pdf_file": pdf_base64}

        # URL الخاص بـ FastAPI على Kaggle أو Ngrok
        URL = "https://pennie-sabulous-rheba.ngrok-free.dev/CV_Extractor"
        headers = {"Authorization": "Bearer secret123"}

        # إرسال الطلب
        try:
            res = requests.post(URL, headers=headers, json=payload)
            res.raise_for_status()
            output_data = res.json()["response"]

            # عرض كل جزء في Section مستقل
            st.subheader("Full Name")
            st.write(output_data.get("full_name", "Not found"))

            st.subheader("Email")
            st.write(output_data.get("email", "Not found"))

            st.subheader("Education")
            st.write(output_data.get("Education", "Not found"))

            st.subheader("Skills")
            st.write(output_data.get("Skills", "Not found"))

            st.subheader("Experience")
            st.write(output_data.get("Experience", "Not found"))

        except requests.HTTPError as e:
            st.error(f"Error: {e}")
