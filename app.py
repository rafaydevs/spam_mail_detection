import streamlit as st
import pickle
import string
import os
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from gmail_integration import fetch_email  

# Ensure NLTK resources are available before downloading
nltk_data_path = "/home/appuser/nltk_data"
if not os.path.exists(nltk_data_path + "/tokenizers/punkt"):
    nltk.download('punkt_tab', download_dir=nltk_data_path)

if not os.path.exists(nltk_data_path + "/corpora/stopwords"):
    nltk.download('stopwords', download_dir=nltk_data_path)

ps = PorterStemmer()

# Function to preprocess the text
def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)

    y = []
    for i in text:
        if i.isalnum():
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        y.append(ps.stem(i))

    return " ".join(y)

# ✅ Ensure model files exist before loading
try:
    with open("vectorizer.pkl", "rb") as f:
        tfidf = pickle.load(f)

    with open("model.pkl", "rb") as f:
        model = pickle.load(f)

except FileNotFoundError:
    st.error("❌ Model files not found! Ensure 'vectorizer.pkl' and 'model.pkl' are present in the working directory.")
    st.stop()

# Streamlit UI Configuration
st.set_page_config(page_title="Spam Detector", page_icon="📧", layout="centered")

# Header with description
st.markdown(
    """
    <div style="text-align: center; padding: 20px;">
        <h1 style="color: #4CAF50;">📧 Spam Detector</h1>
        <p style="font-size: 18px; color: #555;">
            The Spam Detector evaluates email or text messages to identify whether they are spam.
            Enter your message below, and let the AI determine its classification.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Input box with placeholder
input_sms = st.text_area("Email/Text", placeholder="Type your message here...", height=200)

# Predict button
if st.button("🔍 Analyze"):
    if input_sms:
        # Preprocess input
        transformed_sms = transform_text(input_sms)
        # Vectorize
        vector_input = tfidf.transform([transformed_sms])
        # Predict
        result = model.predict(vector_input)[0]
        # Display result
        if result == 1:
            st.success("🛑 This message is Spam!")
        else:
            st.info("✅ This message is Not Spam!")
    else:
        st.warning("⚠️ Please enter a message to analyze.")
