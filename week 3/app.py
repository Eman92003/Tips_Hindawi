import streamlit as st
import requests
import base64

st.title("📄 PDF Question Answering")

# رفع الملف
uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
question = st.text_input("Enter your question")

if st.button("Get Answer") and uploaded_file and question:
    with st.spinner("Generating answer..."):
        # اقرأ المحتوى كـ bytes
        pdf_bytes = uploaded_file.read()
        
        # حوّل الـ bytes لـ base64 string
        pdf_base64 = base64.b64encode(pdf_bytes).decode("utf-8")

        # إعداد payload
        payload = {
            "question": question,
            "pdf_file": pdf_base64
        }

        # NGROK / API URL
        URL = "https://pennie-sabulous-rheba.ngrok-free.dev/RAG"
        headers = {"Authorization": "Bearer secret123"}

        # إرسال الطلب
        res = requests.post(URL, headers=headers, json=payload)
        res.raise_for_status()
        answer = res.json()["response"]

    # عرض النتيجة
    st.subheader("📝 Answer")
    st.write(answer)
