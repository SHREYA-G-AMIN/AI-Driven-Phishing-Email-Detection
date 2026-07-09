import streamlit as st
import re
import nltk
nltk.download('stopwords', quiet=True)
from nltk.corpus import stopwords
import joblib

st.set_page_config(
    page_title="Phishing Email Detector",
    page_icon="📧",
    layout="wide"
)

# ===== CUSTOM CSS =====
st.markdown("""
<style>
    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(90deg, #ff6b6b, #ffd93d);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 20px 0;
    }
    .hero-subtitle {
        text-align: center;
        color: #888;
        font-size: 1.1rem;
        margin-bottom: 30px;
    }
    .result-phishing {
        background: linear-gradient(135deg, #ff4444, #cc0000);
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        color: white;
        font-size: 1.8rem;
        font-weight: bold;
        margin: 20px 0;
        box-shadow: 0 4px 20px rgba(255, 68, 68, 0.4);
    }
    .result-safe {
        background: linear-gradient(135deg, #00b09b, #096551);
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        color: white;
        font-size: 1.8rem;
        font-weight: bold;
        margin: 20px 0;
        box-shadow: 0 4px 20px rgba(0, 176, 155, 0.4);
    }
    .info-card {
        background: #1e2130;
        padding: 20px;
        border-radius: 12px;
        border-left: 4px solid #ff6b6b;
        margin: 10px 0;
    }
    .footer {
        text-align: center;
        color: #555;
        padding: 20px;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# ===== HERO =====
st.markdown('<div class="hero-title">📧 Phishing Email Detector</div>',
            unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">AI-Powered Email Security using NLP & Machine Learning</div>',
            unsafe_allow_html=True)

# ===== STATS =====
col1, col2, col3, col4 = st.columns(4)
col1.metric("🎯 Model Accuracy", "96.68%")
col2.metric("📧 Emails Trained", "18,650")
col3.metric("🧠 Algorithm", "Logistic Regression")
col4.metric("📊 Features", "5,000 TF-IDF")

st.markdown("---")

# ===== LOAD MODEL =====
@st.cache_resource
def load_model():
    model = joblib.load("models/lr_model.pkl")
    tfidf = joblib.load("models/tfidf.pkl")
    return model, tfidf

with st.spinner("🔄 Loading AI Model..."):
    model, tfidf = load_model()

st.success("✅ Model Ready!")

# ===== INPUT =====
st.subheader("📝 Enter Email Content")

col1, col2 = st.columns([2, 1])

with col1:
    email_input = st.text_area(
        "Paste email content here:",
        height=250,
        placeholder="Paste the email text you want to analyze..."
    )
    analyze_btn = st.button("🔍 Analyze Email", use_container_width=True)

with col2:
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.markdown("### 💡 How It Works")
    st.markdown("""
    1. **Paste** email content
    2. **Click** Analyze Email
    3. **Get** instant AI verdict
    
    The model analyzes:
    - Word patterns
    - Writing style
    - Suspicious phrases
    - Language structure
    """)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.markdown("### 📊 Model Performance")
    st.markdown("""
    | Model | Accuracy |
    |-------|----------|
    | Neural Network | 96.94% |
    | Logistic Reg. | **96.68%** |
    | Random Forest | 95.76% |
    | Naive Bayes | 95.52% |
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# ===== RESULTS =====
if analyze_btn:
    if email_input.strip() == "":
        st.warning("⚠️ Please enter email content first!")
    else:
        with st.spinner("🧠 Analyzing email..."):
            stop_words = set(stopwords.words('english'))

            def preprocess(text):
                text = str(text).lower()
                text = re.sub(r'[^a-zA-Z\s]', '', text)
                words = text.split()
                words = [w for w in words if w not in stop_words]
                return ' '.join(words)

            cleaned = preprocess(email_input)
            input_tfidf = tfidf.transform([cleaned])
            prediction = model.predict(input_tfidf)[0]
            probability = model.predict_proba(input_tfidf)[0]

        st.markdown("---")
        st.subheader("🎯 Analysis Result")

        if prediction == 1:
            st.markdown(
                '<div class="result-phishing">🚨 PHISHING EMAIL DETECTED!</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                '<div class="result-safe">✅ EMAIL IS SAFE!</div>',
                unsafe_allow_html=True
            )

        col1, col2, col3 = st.columns(3)
        col1.metric("✅ Safe Probability",
                    f"{probability[0]*100:.2f}%")
        col2.metric("🚨 Phishing Probability",
                    f"{probability[1]*100:.2f}%")
        col3.metric("🎯 Confidence",
                    f"{max(probability)*100:.2f}%")

        st.markdown("### 📊 Confidence Breakdown")
        st.markdown("**Safe Probability:**")
        st.progress(float(probability[0]))
        st.markdown("**Phishing Probability:**")
        st.progress(float(probability[1]))

        if max(probability) < 0.70:
            st.warning("⚠️ Low confidence. Manual review recommended.")

# ===== FOOTER =====
st.markdown("---")
st.markdown(
    '<div class="footer">Built by <b>Shreya G Amin</b> | '
    'AI-Driven Phishing Email Detection | '
    'Powered by scikit-learn & Streamlit</div>',
    unsafe_allow_html=True
)