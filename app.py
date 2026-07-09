import streamlit as st
import re
import nltk
nltk.download('stopwords', quiet=True)
from nltk.corpus import stopwords
import joblib

st.set_page_config(
    page_title="PhishGuard AI",
    page_icon="🛡️",
    layout="wide"
)

# ===== CUSTOM CSS =====
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0a0a0f 0%, #1a0a2e 50%, #0a0a0f 100%);
    }
    
    /* Hero title */
    .hero-title {
        font-size: 3.5rem;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(90deg, #ffd700, #ff8c00, #ffd700);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 10px 0;
        letter-spacing: 2px;
    }
    
    /* Subtitle */
    .hero-subtitle {
        text-align: center;
        color: #9d7fd4;
        font-size: 1.2rem;
        margin-bottom: 10px;
        letter-spacing: 1px;
    }

    /* Badge */
    .badge {
        text-align: center;
        margin-bottom: 30px;
    }

    /* Dashboard card */
    .dash-card {
        background: linear-gradient(135deg, #1e0a3c, #2d1458);
        border: 1px solid #ffd70033;
        border-radius: 16px;
        padding: 20px;
        margin: 8px 0;
        box-shadow: 0 4px 20px rgba(255, 215, 0, 0.1);
    }

    /* Result cards */
    .result-phishing {
        background: linear-gradient(135deg, #8b0000, #ff0000);
        border: 2px solid #ff6b6b;
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        color: white;
        font-size: 2rem;
        font-weight: 900;
        margin: 20px 0;
        box-shadow: 0 0 40px rgba(255, 0, 0, 0.5);
        letter-spacing: 2px;
        animation: pulse 1s infinite;
    }

    .result-safe {
        background: linear-gradient(135deg, #004d00, #00cc00);
        border: 2px solid #00ff00;
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        color: white;
        font-size: 2rem;
        font-weight: 900;
        margin: 20px 0;
        box-shadow: 0 0 40px rgba(0, 255, 0, 0.3);
        letter-spacing: 2px;
    }

    /* Section headers */
    .section-header {
        color: #ffd700;
        font-size: 1.3rem;
        font-weight: 700;
        border-bottom: 1px solid #ffd70033;
        padding-bottom: 8px;
        margin-bottom: 15px;
        letter-spacing: 1px;
    }

    /* Threat level */
    .threat-high {
        background: linear-gradient(90deg, #8b0000, #ff0000);
        color: white;
        padding: 8px 20px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
    }

    .threat-low {
        background: linear-gradient(90deg, #004d00, #00cc00);
        color: white;
        padding: 8px 20px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #9d7fd4;
        padding: 20px;
        font-size: 0.9rem;
        border-top: 1px solid #ffd70022;
        margin-top: 30px;
    }

    /* Input area styling */
    .stTextArea textarea {
        background: #1e0a3c !important;
        border: 1px solid #ffd70055 !important;
        color: white !important;
        border-radius: 12px !important;
    }

    /* Button styling */
    .stButton button {
        background: linear-gradient(90deg, #ffd700, #ff8c00) !important;
        color: black !important;
        font-weight: 900 !important;
        border: none !important;
        border-radius: 12px !important;
        font-size: 1.1rem !important;
        letter-spacing: 1px !important;
        padding: 15px !important;
    }
</style>
""", unsafe_allow_html=True)

# ===== HERO SECTION =====
st.markdown('<div class="hero-title">🛡️ PHISHGUARD AI</div>', 
            unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Advanced AI-Powered Phishing Email Detection System</div>', 
            unsafe_allow_html=True)
st.markdown('<div class="badge">⚡ Powered by NLP & Machine Learning • 96.68% Accuracy</div>',
            unsafe_allow_html=True)

st.markdown("---")

# ===== TOP DASHBOARD METRICS =====
st.markdown('<p class="section-header">📊 SYSTEM DASHBOARD</p>', 
            unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("🎯 Accuracy", "96.68%", "↑ High")
col2.metric("📧 Emails Trained", "18,650", "Real Data")
col3.metric("🧠 Algorithm", "Logistic Reg.", "Best Speed")
col4.metric("📊 NLP Features", "5,000", "TF-IDF")
col5.metric("⚡ Response", "< 1 sec", "Real-time")

st.markdown("---")

# ===== LOAD MODEL =====
@st.cache_resource
def load_model():
    model = joblib.load("models/lr_model.pkl")
    tfidf = joblib.load("models/tfidf.pkl")
    return model, tfidf

with st.spinner("🔄 Initializing PhishGuard AI..."):
    model, tfidf = load_model()

st.success("✅ PhishGuard AI System Online!")

st.markdown("---")

# ===== MAIN DASHBOARD =====
left, right = st.columns([3, 2])

with left:
    st.markdown('<p class="section-header">📧 EMAIL ANALYSIS CONSOLE</p>',
                unsafe_allow_html=True)
    
    email_input = st.text_area(
        "Paste suspicious email content below:",
        height=280,
        placeholder="Paste email content here for instant AI analysis...\n\nExample: Dear Customer, Your account has been suspended..."
    )
    
    analyze_btn = st.button("🔍 ANALYZE EMAIL NOW", use_container_width=True)

with right:
    st.markdown('<p class="section-header">🏆 MODEL COMPARISON</p>',
                unsafe_allow_html=True)
    
    st.markdown("""
    | Rank | Model | Accuracy |
    |------|-------|----------|
    | 🥇 | Neural Network | 96.94% |
    | 🥈 | **Logistic Reg.** | **96.68%** |
    | 🥉 | Random Forest | 95.76% |
    | 4th | Naive Bayes | 95.52% |
    """)

    st.markdown("---")
    
    st.markdown('<p class="section-header">🔬 HOW IT WORKS</p>',
                unsafe_allow_html=True)
    
    st.markdown("""
    **1.** 📝 Email text is cleaned & normalized  
    **2.** 🔢 TF-IDF converts text to 5,000 features  
    **3.** 🧠 AI model analyzes word patterns  
    **4.** 🎯 Instant phishing/safe verdict  
    **5.** 📊 Confidence score displayed  
    """)

    st.markdown("---")

    st.markdown('<p class="section-header">⚠️ COMMON PHISHING SIGNS</p>',
                unsafe_allow_html=True)
    
    st.markdown("""
    🔴 Urgent account warnings  
    🔴 "Click here immediately"  
    🔴 Suspicious URLs/links  
    🔴 Request for credentials  
    🔴 Too-good-to-be-true offers  
    """)

# ===== RESULTS =====
if analyze_btn:
    if email_input.strip() == "":
        st.warning("⚠️ Please paste email content before analyzing!")
    else:
        with st.spinner("🧠 PhishGuard AI analyzing email..."):
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
        st.markdown('<p class="section-header">🎯 ANALYSIS RESULTS</p>',
                    unsafe_allow_html=True)

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

        # Results dashboard
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("🛡️ Verdict", 
                    "PHISHING" if prediction == 1 else "SAFE")
        col2.metric("✅ Safe Score", 
                    f"{probability[0]*100:.1f}%")
        col3.metric("🚨 Threat Score", 
                    f"{probability[1]*100:.1f}%")
        col4.metric("🎯 Confidence", 
                    f"{max(probability)*100:.1f}%")

        # Threat level
        st.markdown("### 🌡️ Threat Level")
        threat = probability[1] * 100
        
        if threat >= 80:
            st.markdown('<span class="threat-high">🔴 HIGH THREAT</span>', 
                       unsafe_allow_html=True)
        elif threat >= 50:
            st.markdown('<span class="threat-high">🟡 MEDIUM THREAT</span>', 
                       unsafe_allow_html=True)
        else:
            st.markdown('<span class="threat-low">🟢 LOW THREAT</span>', 
                       unsafe_allow_html=True)

        # Progress bars
        st.markdown("### 📊 Probability Breakdown")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**✅ Safe Probability**")
            st.progress(float(probability[0]))
        with col2:
            st.markdown("**🚨 Phishing Probability**")
            st.progress(float(probability[1]))

        # Recommendation
        st.markdown("### 💡 Recommendation")
        if prediction == 1:
            st.error("""
            🚨 **DO NOT** click any links in this email  
            🚨 **DO NOT** provide any personal information  
            🚨 **REPORT** this email to your IT security team  
            🚨 **DELETE** this email immediately  
            """)
        else:
            st.success("""
            ✅ This email appears to be **legitimate**  
            ✅ Always stay cautious with unknown senders  
            ✅ Never share passwords via email  
            """)

        if max(probability) < 0.70:
            st.warning("⚠️ Low confidence prediction. Manual security review recommended.")

# ===== FOOTER =====
st.markdown(
    '<div class="footer">🛡️ PhishGuard AI | Built by <b>Shreya G Amin</b> | '
    'AI-Driven Phishing Detection | Powered by scikit-learn & Streamlit</div>',
    unsafe_allow_html=True
)