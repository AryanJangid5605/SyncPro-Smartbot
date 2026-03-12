from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash-lite")

def my_output(query):
    response = model.generate_content(query)
    return response.text

#### UI Development using streamlit

# Page configuration
st.set_page_config(
    page_title="SyncPro Smart Bot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
    <style>
    /* Import modern font */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Animated gradient background */
    .main {
        background: linear-gradient(-45deg, #667eea, #764ba2, #f093fb, #4facfe);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Enhanced sidebar styling with gradient background and proper text colors */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: white !important;
    }
    
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h4,
    [data-testid="stSidebar"] h5,
    [data-testid="stSidebar"] h6 {
        color: white !important;
    }
    
    [data-testid="stSidebar"] p {
        color: rgba(255, 255, 255, 0.9) !important;
    }
    
    [data-testid="stSidebar"] .stMetric {
        background: rgba(255, 255, 255, 0.15);
        padding: 1rem;
        border-radius: 10px;
        backdrop-filter: blur(10px);
    }
    
    [data-testid="stSidebar"] .stMetric label {
        color: rgba(255, 255, 255, 0.9) !important;
        font-weight: 500;
    }
    
    [data-testid="stSidebar"] .stMetric [data-testid="stMetricValue"] {
        color: white !important;
        font-weight: 700;
        font-size: 1.5rem;
    }
    
    [data-testid="stSidebar"] hr {
        border-color: rgba(255, 255, 255, 0.2) !important;
    }
    
    [data-testid="stSidebar"] .stAlert {
        background: rgba(255, 255, 255, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: white !important;
        backdrop-filter: blur(10px);
    }
    
    [data-testid="stSidebar"] .stAlert p {
        color: white !important;
    }
    
    [data-testid="stSidebar"] .stButton > button {
        background: rgba(255, 255, 255, 0.2) !important;
        color: white !important;
        border: 2px solid rgba(255, 255, 255, 0.3);
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    [data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(255, 255, 255, 0.3) !important;
        border-color: rgba(255, 255, 255, 0.5);
        transform: translateY(-2px);
    }
    
    /* Message styling */
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 5px 20px;
        margin: 1rem 0 1rem 20%;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    
    .bot-message {
        background: white;
        color: #1e293b;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 20px 5px;
        margin: 1rem 20% 1rem 0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    
    .message-label {
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        opacity: 0.8;
        margin-bottom: 0.5rem;
    }
    
    /* <CHANGE> Fixed input text color to be dark and visible */
    .stTextInput > div > div > input {
        border-radius: 15px;
        border: 2px solid rgba(255, 255, 255, 0.3);
        padding: 1rem 1.5rem;
        font-size: 1rem;
        background: rgba(255, 255, 255, 0.95);
        color: #1e293b !important;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #94a3b8 !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
        transform: translateY(-2px);
        color: #1e293b !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 15px;
        padding: 1rem 2rem;
        font-size: 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'query_count' not in st.session_state:
    st.session_state.query_count = 0

# Sidebar
with st.sidebar:
    st.title("📊 Statistics")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Queries", st.session_state.query_count)
    with col2:
        st.metric("Messages", len(st.session_state.messages) // 2)
    
    st.divider()
    
    st.markdown("### About")
    st.info("Smart Bot uses Google's Gemini 2.5 Flash Lite AI model for intelligent conversations.")
    
    st.divider()
    
    if st.button("🗑️ Clear History", use_container_width=True):
        st.session_state.messages = []
        st.session_state.query_count = 0
        st.rerun()

# Header
st.title("🤖 Smart Bot")
st.caption("Powered by Google Gemini AI - Your intelligent assistant")
st.divider()

# Chat display area
chat_container = st.container()

with chat_container:
    if st.session_state.messages:
        # Display chat history
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f"""
                    <div class="user-message">
                        <div class="message-label">You</div>
                        <div>{message["content"]}</div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div class="bot-message">
                        <div class="message-label">Smart Bot</div>
                        <div>{message["content"]}</div>
                    </div>
                """, unsafe_allow_html=True)
    else:
        # Welcome screen using native Streamlit components
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Center content
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("<h1 style='text-align: center; font-size: 4rem;'>🤖</h1>", unsafe_allow_html=True)
            st.markdown("<h2 style='text-align: center; color: white;'>Welcome to Smart Bot</h2>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: rgba(255,255,255,0.9); font-size: 1.1rem;'>I'm powered by Google Gemini AI and ready to help you with any questions. Ask me anything from general knowledge to complex problem-solving!</p>", unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Suggestion cards
            col_a, col_b = st.columns(2)
            
            with col_a:
                with st.container():
                    st.markdown("### 💡")
                    st.markdown("*Explain complex concepts*")
                    st.caption("Get clear, simple explanations")
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                with st.container():
                    st.markdown("### ✍️")
                    st.markdown("*Writing assistance*")
                    st.caption("Help with content creation")
            
            with col_b:
                with st.container():
                    st.markdown("### 🔍")
                    st.markdown("*Research & analysis*")
                    st.caption("Analyze information deeply")
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                with st.container():
                    st.markdown("### 🧮")
                    st.markdown("*Problem solving*")
                    st.caption("Solve math and logic puzzles")
            
            st.markdown("<br><br>", unsafe_allow_html=True)
            
            # Features
            feat_col1, feat_col2, feat_col3 = st.columns(3)
            with feat_col1:
                st.markdown("<p style='text-align: center; color: white;'>⚡ Fast Responses</p>", unsafe_allow_html=True)
            with feat_col2:
                st.markdown("<p style='text-align: center; color: white;'>🎯 Accurate Info</p>", unsafe_allow_html=True)
            with feat_col3:
                st.markdown("<p style='text-align: center; color: white;'>🌟 AI Powered</p>", unsafe_allow_html=True)

st.divider()

# Input section at bottom
col1, col2 = st.columns([5, 1])

with col1:
    input = st.text_input(
        "Input",
        key="input",
        placeholder="Type your question here...",
        label_visibility="collapsed"
    )

with col2:
    submit = st.button("Send", use_container_width=True)

# Handle submission
if submit and input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": input})
    st.session_state.query_count += 1
    
    # Get bot response
    with st.spinner("🤔 Smart Bot is thinking..."):
        response = my_output(input)
        st.session_state.messages.append({"role": "bot", "content": response})
    
    st.rerun()