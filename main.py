import streamlit as st
import pdfplumber
import requests
import os
from dotenv import load_dotenv

# API Key لوڈ کرنا
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# صفحے کی سیٹنگ (Professional Look)
st.set_page_config(page_title="AI Sales Assistant", page_icon="📊")

st.title("📊 پروفیشنل سیلز ڈیش بورڈ")
st.markdown("اپنی پی ڈی ایف رپورٹ اپ لوڈ کریں اور سیلز سے متعلق سوالات پوچھیں۔")

# پی ڈی ایف سے ٹیکسٹ نکالنے کا فنکشن
def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

# گوگل AI سے بات کرنے کا فنکشن
def ask_gemini(context, question):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    headers = {'Content-Type': 'application/json'}
    prompt = f"آپ ایک ماہر سیلز اسسٹنٹ ہیں۔ اس رپورٹ کی بنیاد پر اردو میں جواب دیں:\n\nڈیٹا:\n{context}\n\nسوال: {question}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            return "گوگل سرور سے رابطہ نہیں ہو سکا۔ اپنی API Key چیک کریں۔"
    except Exception as e:
        return f"نیٹ ورک کا مسئلہ: {e}"

# سائیڈ بار میں فائل اپ لوڈر
with st.sidebar:
    st.header("رپورٹ اپ لوڈ کریں")
    uploaded_file = st.file_uploader("PDF فائل منتخب کریں", type="pdf")

if uploaded_file:
    # ڈیٹا لوڈ کرنا
    with st.spinner("رپورٹ پڑھی جا رہی ہے..."):
        report_text = extract_text_from_pdf(uploaded_file)
    st.success("رپورٹ کامیابی سے لوڈ ہو گئی!")

    # چیٹ انٹرفیس
    st.divider()
    user_query = st.text_input("اپنا سوال یہاں لکھیں (مثلاً: کل سیل کتنی ہے؟)")

    if user_query:
        with st.spinner("AI جواب تیار کر رہا ہے..."):
            answer = ask_gemini(report_text, user_query)
            st.info(f"AI کا جواب:\n\n{answer}")
else:
    st.warning("براہ کرم بائیں طرف موجود بٹن سے اپنی سیلز رپورٹ (PDF) اپ لوڈ کریں۔")