import streamlit as st
from extractive import extractive_summary
from abstractive import abstractive_summary
import base64
import fitz  # PyMuPDF
import requests
from bs4 import BeautifulSoup

# Set background with enhanced text color
def add_bg_from_local(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            color: #f1f1f1;
        }}

        .stTextInput > div > div > input,
        .stTextArea > div > textarea,
        .stSelectbox > div > div,
        .stRadio > div,
        .stButton > button,
        .stDownloadButton > button,
        .stMarkdown,
        .stSubheader,
        .stHeader {{
            background-color: rgba(0, 0, 0, 0.6) !important;
            color: #f1f1f1 !important;
            border-radius: 10px;
        }}

        label, .css-10trblm, .css-1d391kg, .css-1cpxqw2 {{
            color: #fffae6 !important;
            font-weight: bold;
        }}

        .stButton > button {{
            padding: 0.5em 2em;
            font-weight: bold;
            border: none;
            border-radius: 8px;
            background-color: #00b894;
            color: white;
        }}

        .stButton > button:hover {{
            background-color: #00cec9;
            transform: scale(1.02);
            transition: all 0.3s ease-in-out;
        }}

        .stDownloadButton > button {{
            background-color: #0984e3;
            color: white;
            font-weight: bold;
            border-radius: 8px;
            padding: 0.5em 2em;
        }}

        .stDownloadButton > button:hover {{
            background-color: #74b9ff;
            transform: scale(1.02);
            transition: all 0.3s ease-in-out;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Page config
st.set_page_config(page_title="Text Summarizer", layout="centered")
add_bg_from_local("text3.jpg")  # Ensure the image is in the same folder

# Title
st.title("📝 Text Summarization App")

# Input type selector
input_type = st.radio("Choose input type:", ["Text Box", "PDF File", "Web URL"])

text = ""

# Handle each input method
if input_type == "Text Box":
    text = st.text_area("Enter your text here:", height=300)

elif input_type == "PDF File":
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
    if uploaded_file:
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        text = "\n".join([page.get_text() for page in doc])

elif input_type == "Web URL":
    url = st.text_input("Enter the webpage URL:")
    if url:
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            paragraphs = soup.find_all('p')
            text = ' '.join([p.get_text() for p in paragraphs])
        except Exception as e:
            st.error("Failed to fetch content from URL.")

# Summary type selector
summary_type = st.selectbox("Choose summarization type:", ["Extractive", "Abstractive"])

# Controls for each summarizer
if summary_type == "Extractive":
    num_sentences = st.slider("Number of sentences:", 1, 10, 3)
else:
    min_len = st.slider("Minimum summary length:", 10, 100, 30)
    max_len = st.slider("Maximum summary length:", 50, 300, 130)

# Summarize button
if st.button("Summarize"):
    if text.strip() == "":
        st.warning("Please provide content for summarization.")
    else:
        with st.spinner("Summarizing..."):
            if summary_type == "Extractive":
                summary = extractive_summary(text, num_sentences)
            else:
                summary = abstractive_summary(text, min_len, max_len)
        st.subheader("Summary:")
        st.write(summary)

        # Download summary
        st.download_button(
            label="📥 Download Summary",
            data=summary,
            file_name="summary.txt",
            mime="text/plain"
        )
