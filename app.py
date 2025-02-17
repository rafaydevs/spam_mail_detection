

import pickle
import string
from nltk.corpus import stopwords
import nltk
from nltk.stem.porter import PorterStemmer

# Download nltk resources if not already present
nltk.download('punkt')
nltk.download('stopwords')

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

# Load pre-trained model and vectorizer
tfidf = pickle.load(open('vectorizer.pkl', 'rb'))
model = pickle.load(open('model.pkl', 'rb'))

# Enhanced UI
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
# Input box with placeholder (using text_area for larger input field)
st.text_area("Email/Text", placeholder="Type your message here...", key="input_sms", height=200)

# Predict button
if st.button("🔍 Analyze"):
    input_sms = st.session_state.input_sms
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


