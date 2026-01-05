"""
Main Streamlit Application - TalentScout Hiring Assistant Chatbot
"""

import streamlit as st
import json
from typing import Dict, List
from datetime import datetime
import sys
import os

# Add utils to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.llm_client import LLMClient, ConversationManager
from utils.candidate_data import CandidateDataManager, SensitiveDataHandler
from utils.sentiment_analyzer import SentimentAnalyzer
from utils.language_detector import LanguageHandler
from prompts.prompt_templates import PromptTemplates, ConversationFlow


# Configure Streamlit page
st.set_page_config(
    page_title="TalentScout - Hiring Assistant",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
st.markdown("""
    <style>
    /* Main theme colors - Modern Light Theme */
    :root {
        --primary-color: #0066cc;
        --secondary-color: #7c3aed;
        --accent-color: #00bcd4;
        --success-color: #10b981;
        --warning-color: #f59e0b;
        --light-bg: #f8fafc;
        --card-bg: #ffffff;
        --hover-bg: #f1f5f9;
        --text-primary: #1a202c;
        --text-secondary: #4a5568;
    }
    
    /* Keyframe Animations */
    @keyframes slideInDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-40px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(40px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }
    
    @keyframes pulse {
        0%, 100% {
            opacity: 1;
        }
        50% {
            opacity: 0.7;
        }
    }
    
    @keyframes glow {
        0%, 100% {
            box-shadow: 0 0 5px rgba(0, 102, 204, 0.3);
        }
        50% {
            box-shadow: 0 0 20px rgba(0, 102, 204, 0.5);
        }
    }
    
    @keyframes shimmer {
        0% {
            background-position: -1000px 0;
        }
        100% {
            background-position: 1000px 0;
        }
    }
    
    @keyframes bounce {
        0%, 100% {
            transform: translateY(0);
        }
        50% {
            transform: translateY(-5px);
        }
    }
    
    @keyframes scaleIn {
        from {
            opacity: 0;
            transform: scale(0.95);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    @keyframes floatUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Body and main background */
    body {
        background: linear-gradient(135deg, #f8fafc 0%, #e0f4f8 50%, #f0ebf8 100%);
        color: var(--text-primary);
    }
    
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #f8fafc 0%, #e0f4f8 50%, #f0ebf8 100%);
        animation: fadeIn 0.8s ease-in;
    }
    
    [data-testid="stVerticalBlock"] {
        background: transparent;
    }
    
    /* Main container */
    .main {
        background: linear-gradient(135deg, #f8fafc 0%, #e0f4f8 50%, #f0ebf8 100%);
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #ffffff 0%, #f0f4f9 50%, #e8eef5 100%);
        padding: 45px;
        border-radius: 25px;
        color: #1a202c;
        text-align: center;
        margin-bottom: 35px;
        box-shadow: 0 12px 40px rgba(0, 102, 204, 0.15), 0 0 60px rgba(124, 58, 237, 0.08);
        border: 2px solid rgba(0, 102, 204, 0.2);
        position: relative;
        overflow: hidden;
        animation: slideInDown 0.8s ease-out;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, transparent, #0066cc, #7c3aed, transparent);
        box-shadow: 0 0 20px rgba(0, 102, 204, 0.4);
        animation: shimmer 3s infinite;
    }
    
    .main-header::after {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 100%;
        height: 100%;
        background: radial-gradient(circle, rgba(0, 102, 204, 0.1) 0%, transparent 70%);
        animation: floatUp 2s ease-in-out infinite;
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 3.2em;
        font-weight: 900;
        background: linear-gradient(135deg, #0066cc, #7c3aed);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: 2px;
        animation: slideInUp 0.8s ease-out 0.2s both;
    }
    
    .main-header p {
        margin: 18px 0 0 0;
        font-size: 1.4em;
        background: linear-gradient(135deg, #0066cc, #7c3aed);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        opacity: 1;
        font-weight: 600;
        animation: slideInUp 0.8s ease-out 0.4s both;
    }
    
    /* Chat messages styling */
    .chat-message {
        padding: 20px 24px;
        border-radius: 18px;
        margin: 18px 0;
        word-wrap: break-word;
        animation: slideInUp 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
        backdrop-filter: blur(12px);
        transition: all 0.3s ease;
    }
    
    .chat-message:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.1);
    }
    
    .user-message {
        background: linear-gradient(135deg, #e3f2fd 0%, #f3e5f5 100%);
        color: #1a202c;
        border-left: 6px solid #0066cc;
        border-right: 2px solid rgba(0, 102, 204, 0.3);
        border-top: 1px solid rgba(0, 102, 204, 0.2);
        margin-left: 40px;
        box-shadow: 0 6px 25px rgba(0, 102, 204, 0.12);
        animation: slideInLeft 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    
    .user-message:hover {
        box-shadow: 0 12px 35px rgba(0, 102, 204, 0.2);
    }
    
    .assistant-message {
        background: linear-gradient(135deg, #f3e5f5 0%, #e8d5f2 100%);
        color: #1a202c;
        border-left: 6px solid #7c3aed;
        border-right: 2px solid rgba(124, 58, 237, 0.3);
        border-top: 1px solid rgba(124, 58, 237, 0.2);
        margin-right: 40px;
        box-shadow: 0 6px 25px rgba(124, 58, 237, 0.12);
        animation: slideInRight 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    
    .assistant-message:hover {
        box-shadow: 0 12px 35px rgba(124, 58, 237, 0.2);
    }
    
    /* Question card styling */
    .question-card {
        background: linear-gradient(135deg, #f0f4f9 0%, #e8eef5 100%);
        padding: 28px;
        border-radius: 18px;
        border-left: 6px solid #0066cc;
        border-top: 2px solid rgba(0, 102, 204, 0.3);
        border-right: 1px solid rgba(0, 102, 204, 0.15);
        margin: 22px 0;
        box-shadow: 0 10px 35px rgba(0, 102, 204, 0.1);
        color: #1a202c;
        line-height: 1.7;
        font-size: 1.05em;
        animation: scaleIn 0.5s ease-out;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .question-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(0, 102, 204, 0.1), transparent);
        animation: shimmer 2s infinite;
    }
    
    .question-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 50px rgba(0, 102, 204, 0.2);
        border-left-color: #7c3aed;
    }
    
    /* Form styling */
    .form-container {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        padding: 45px;
        border-radius: 22px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08);
        border: 2px solid rgba(0, 102, 204, 0.15);
        border-top: 3px solid rgba(0, 102, 204, 0.3);
        animation: slideInUp 0.8s ease-out;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #0066cc 0%, #7c3aed 100%);
        color: #ffffff;
        border-radius: 12px;
        padding: 16px 36px;
        font-weight: 800;
        border: none;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 10px 30px rgba(0, 102, 204, 0.3);
        font-size: 1.08em;
        letter-spacing: 0.5px;
        position: relative;
        overflow: hidden;
        animation: scaleIn 0.5s ease-out;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: translate(-50%, -50%);
    }
    
    .stButton > button:hover {
        transform: translateY(-4px);
        box-shadow: 0 15px 45px rgba(0, 102, 204, 0.4), 0 0 30px rgba(124, 58, 237, 0.3);
        animation: bounce 0.6s ease-in-out;
    }
    
    .stButton > button:active {
        transform: translateY(-1px);
        box-shadow: 0 5px 15px rgba(0, 102, 204, 0.3);
    }
    
    /* Progress bar styling */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #0066cc 0%, #7c3aed 100%);
        border-radius: 10px;
        box-shadow: 0 0 25px rgba(0, 102, 204, 0.3);
        animation: slideInLeft 1s ease-out;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
        border-right: 2px solid rgba(0, 102, 204, 0.1);
        animation: slideInLeft 0.8s ease-out;
    }
    
    [data-testid="stSidebarNav"] {
        background: transparent;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #f0f4f9 0%, #e8eef5 100%);
        border-radius: 12px;
        border-left: 5px solid #0066cc;
        border: 2px solid rgba(0, 102, 204, 0.2);
        color: #1a202c;
        transition: all 0.3s ease;
        animation: slideInUp 0.5s ease-out;
    }
    
    .streamlit-expanderHeader:hover {
        background: linear-gradient(135deg, #e3f2fd 0%, #f3e5f5 100%);
        border: 2px solid rgba(0, 102, 204, 0.35);
        transform: translateX(5px);
        box-shadow: 0 8px 20px rgba(0, 102, 204, 0.15);
    }
    
    /* Info box styling */
    .stInfo, [data-testid="stAlert"] {
        background: linear-gradient(135deg, rgba(0, 102, 204, 0.08) 0%, rgba(124, 58, 237, 0.05) 100%);
        border-radius: 14px;
        border-left: 6px solid #0066cc;
        border: 2px solid rgba(0, 102, 204, 0.2);
        color: #1a202c;
        box-shadow: 0 6px 20px rgba(0, 102, 204, 0.08);
        animation: slideInUp 0.5s ease-out;
        transition: all 0.3s ease;
    }
    
    .stInfo:hover {
        box-shadow: 0 10px 30px rgba(0, 102, 204, 0.15);
        transform: translateY(-3px);
    }
    
    /* Success message styling */
    .stSuccess {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.08) 0%, rgba(5, 150, 105, 0.05) 100%);
        border-radius: 14px;
        border-left: 6px solid #10b981;
        border: 2px solid rgba(16, 185, 129, 0.2);
        color: #065f46;
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.08);
        animation: slideInUp 0.5s ease-out;
        transition: all 0.3s ease;
    }
    
    .stSuccess:hover {
        box-shadow: 0 10px 30px rgba(16, 185, 129, 0.15);
        transform: translateY(-3px);
    }
    
    /* Warning message styling */
    .stWarning {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.08) 0%, rgba(217, 119, 6, 0.05) 100%);
        border-radius: 14px;
        border-left: 6px solid #f59e0b;
        border: 2px solid rgba(245, 158, 11, 0.2);
        color: #92400e;
        box-shadow: 0 6px 20px rgba(245, 158, 11, 0.08);
        animation: slideInUp 0.5s ease-out;
        transition: all 0.3s ease;
    }
    
    .stWarning:hover {
        box-shadow: 0 10px 30px rgba(245, 158, 11, 0.15);
        transform: translateY(-3px);
    }
    
    /* Text input styling */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stNumberInput > div > div > input {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border-radius: 12px;
        border: 2px solid rgba(0, 102, 204, 0.2);
        padding: 14px 16px;
        font-size: 1.02em;
        color: #1a202c;
        transition: all 0.3s ease;
        animation: scaleIn 0.4s ease-out;
    }
    
    .stTextInput > div > div > input::placeholder,
    .stTextArea > div > div > textarea::placeholder {
        color: #a0aec0;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stNumberInput > div > div > input:focus {
        border-color: #0066cc;
        box-shadow: 0 0 0 5px rgba(0, 102, 204, 0.15), inset 0 0 0 1px rgba(0, 102, 204, 0.1);
        background: linear-gradient(135deg, #f8fafc 0%, #e8eef5 100%);
        transform: scale(1.01);
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        border-radius: 12px;
        animation: scaleIn 0.4s ease-out;
    }
    
    /* Metric styling */
    .metric-card {
        background: linear-gradient(135deg, #f3e5f5 0%, #e8d5f2 100%);
        padding: 22px;
        border-radius: 14px;
        border-left: 5px solid #7c3aed;
        border: 2px solid rgba(124, 58, 237, 0.2);
        margin: 15px 0;
        box-shadow: 0 6px 20px rgba(124, 58, 237, 0.1);
        color: #1a202c;
        animation: slideInUp 0.5s ease-out;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 30px rgba(124, 58, 237, 0.2);
    }
    
    /* Divider styling */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(0, 102, 204, 0.25), transparent);
        margin: 28px 0;
        box-shadow: 0 0 15px rgba(0, 102, 204, 0.1);
        animation: slideInLeft 0.8s ease-out;
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: linear-gradient(180deg, #f8fafc 0%, #e0f4f8 100%);
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #0066cc, #7c3aed);
        border-radius: 5px;
        box-shadow: 0 0 10px rgba(0, 102, 204, 0.2);
        animation: glow 2s infinite;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #7c3aed, #0066cc);
        box-shadow: 0 0 15px rgba(0, 102, 204, 0.35);
    }
    
    /* Text styling */
    h1, h2, h3, h4, h5, h6 {
        color: #1a202c;
        animation: slideInUp 0.6s ease-out;
    }
    
    p, span, div {
        color: var(--text-secondary);
    }
    
    /* Markdown links */
    a {
        color: #0066cc;
        text-decoration: none;
        transition: all 0.3s ease;
        position: relative;
    }
    
    a::after {
        content: '';
        position: absolute;
        width: 0;
        height: 2px;
        bottom: -3px;
        left: 0;
        background: #7c3aed;
        transition: width 0.3s ease;
    }
    
    a:hover {
        color: #7c3aed;
        text-shadow: 0 0 10px rgba(0, 102, 204, 0.2);
    }
    
    a:hover::after {
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)


class TalentScoutApp:
    """Main TalentScout Application Class"""
    
    def __init__(self):
        """Initialize the application"""
        self.data_manager = CandidateDataManager()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.language_handler = LanguageHandler()
        self._initialize_session_state()

    def _initialize_session_state(self):
        """Initialize Streamlit session state variables"""
        if 'initialized' not in st.session_state:
            st.session_state.initialized = True
            st.session_state.conversation_stage = 'greeting'
            st.session_state.llm_client = LLMClient()
            st.session_state.conversation_manager = ConversationManager(
                st.session_state.llm_client,
                PromptTemplates.SYSTEM_PROMPT
            )
            st.session_state.candidate_data = {}
            st.session_state.chat_history = []
            st.session_state.interview_transcript = []
            st.session_state.conversation_active = True
            st.session_state.technical_questions = []
            st.session_state.question_index = 0
            st.session_state.detected_language = 'en'
            st.session_state.sentiment_scores = []

    def display_header(self):
        """Display application header"""
        st.markdown("""
            <div class='main-header'>
                <h1>🎯 TalentScout</h1>
                <p>Intelligent Hiring Assistant</p>
            </div>
        """, unsafe_allow_html=True)

    def display_privacy_notice(self):
        """Display GDPR-compliant privacy notice"""
        with st.expander("🔒 Data Privacy & GDPR Compliance"):
            st.info(self.data_manager.get_data_privacy_notice())

    def display_sidebar_info(self):
        """Display sidebar information and controls"""
        with st.sidebar:
            st.markdown("### 📋 Interview Progress")
            
            # Progress tracker
            progress_stages = {
                'greeting': 10,
                'name': 20,
                'email': 30,
                'phone': 40,
                'experience': 50,
                'position': 60,
                'location': 70,
                'tech_stack': 80,
                'questions': 85,
                'conclusion': 100
            }
            
            current_progress = progress_stages.get(st.session_state.conversation_stage, 0)
            st.progress(current_progress / 100)
            st.caption(f"Stage: {st.session_state.conversation_stage.replace('_', ' ').title()}")
            
            st.divider()
            
            # Collected information in form style
            if st.session_state.candidate_data:
                st.markdown("### 📝 Candidate Information")
                
                # Create a form-like display
                info_items = []
                
                if 'name' in st.session_state.candidate_data:
                    info_items.append(('Full Name', st.session_state.candidate_data['name']))
                
                if 'email' in st.session_state.candidate_data:
                    masked_email = SensitiveDataHandler.mask_email(st.session_state.candidate_data['email'])
                    info_items.append(('Email', masked_email))
                
                if 'phone' in st.session_state.candidate_data:
                    masked_phone = SensitiveDataHandler.mask_phone(st.session_state.candidate_data['phone'])
                    info_items.append(('Phone', masked_phone))
                
                if 'years_of_experience' in st.session_state.candidate_data:
                    info_items.append(('Experience', f"{st.session_state.candidate_data['years_of_experience']} years"))
                
                if 'desired_positions' in st.session_state.candidate_data:
                    positions = ', '.join(st.session_state.candidate_data['desired_positions'])
                    info_items.append(('Target Positions', positions))
                
                if 'location' in st.session_state.candidate_data:
                    info_items.append(('Location', st.session_state.candidate_data['location']))
                
                if 'tech_stack' in st.session_state.candidate_data:
                    tech = ', '.join(st.session_state.candidate_data['tech_stack'])
                    info_items.append(('Tech Stack', tech))
                
                # Display as key-value pairs in form style
                for label, value in info_items:
                    st.markdown(f"**{label}:**")
                    st.markdown(f"> {value}")
                
                st.divider()
                
                # Question progress
                if st.session_state.conversation_stage == 'questions':
                    st.markdown("### ❓ Questions Progress")
                    total_q = len(st.session_state.technical_questions)
                    current_q = min(st.session_state.question_index + 1, total_q)
                    st.caption(f"Question {current_q} of {total_q}")
                    st.progress(current_q / total_q if total_q > 0 else 0)
            
            st.divider()
            
            # Language selection
            st.markdown("### 🌐 Language")
            selected_lang = st.selectbox(
                "Select language:",
                options=list(self.language_handler.SUPPORTED_LANGUAGES.keys()),
                format_func=lambda x: self.language_handler.SUPPORTED_LANGUAGES[x],
                index=0
            )
            st.session_state.detected_language = selected_lang
            
            st.divider()
            
            # Sentiment analysis (if available)
            if st.session_state.sentiment_scores:
                st.markdown("### 😊 Conversation Sentiment")
                avg_sentiment = sum(st.session_state.sentiment_scores) / len(st.session_state.sentiment_scores)
                sentiment_label = "Positive" if avg_sentiment > 0.1 else "Negative" if avg_sentiment < -0.1 else "Neutral"
                st.metric("Overall Sentiment", sentiment_label, f"{avg_sentiment:.2f}")
            
            st.divider()
            
            # Controls
            st.markdown("### ⚙️ Controls")
            if st.button("🔄 Reset Conversation"):
                st.session_state.clear()
                self._initialize_session_state()
                st.rerun()
            
            if st.button("📥 Download Conversation"):
                self._download_conversation()

    def display_chat_history(self):
        """Display chat history"""
        for message in st.session_state.chat_history:
            if message['role'] == 'user':
                st.markdown(
                    f"<div class='chat-message user-message'><b>👤 You:</b><br/>{message['content'].replace(chr(10),'<br>')}</div>",
                    unsafe_allow_html=True
                )
            elif message['role'] == 'assistant':
                st.markdown(
                    f"<div class='chat-message assistant-message'><b>🤖 TalentScout:</b><br/>{message['content'].replace(chr(10),'<br>')}</div>",
                    unsafe_allow_html=True
                )

    def process_greeting(self):
        """Process greeting stage"""
        if not st.session_state.chat_history:
            # First message
            greeting = PromptTemplates.INITIAL_GREETING
            st.session_state.chat_history.append({'role': 'assistant', 'content': greeting})
            st.session_state.conversation_manager.add_message('assistant', greeting)
            st.session_state.conversation_stage = 'name'
            # Add the next question immediately
            self._get_next_input('name')

    def process_user_input(self, user_input: str):
        """Process user input based on conversation stage"""
        if not user_input:
            return

        # Sanitize input
        user_input = SensitiveDataHandler.sanitize_input(user_input)
        
        # Check for exit keywords
        if ConversationFlow.should_exit(user_input):
            self._end_conversation()
            return

        # Add to history
        st.session_state.chat_history.append({'role': 'user', 'content': user_input})
        st.session_state.interview_transcript.append({'role': 'user', 'content': user_input})

        # Detect language
        detected_lang = self.language_handler.detect_language(user_input)
        st.session_state.detected_language = detected_lang

        # Analyze sentiment
        sentiment = self.sentiment_analyzer.analyze_sentiment(user_input)
        if 'polarity' in sentiment:
            st.session_state.sentiment_scores.append(sentiment['polarity'])

        # Process based on stage
        current_stage = st.session_state.conversation_stage

        if current_stage == 'name':
            st.session_state.candidate_data['name'] = user_input
            self._get_next_input("email")

        elif current_stage == 'email':
            st.session_state.candidate_data['email'] = user_input
            self._get_next_input("phone")

        elif current_stage == 'phone':
            st.session_state.candidate_data['phone'] = user_input
            self._get_next_input("experience")

        elif current_stage == 'experience':
            try:
                years = float(user_input.split()[0])
                st.session_state.candidate_data['years_of_experience'] = years
                self._get_next_input("position")
            except (ValueError, IndexError):
                self._ask_for_clarification("years of experience", "experience")

        elif current_stage == 'position':
            positions = [p.strip() for p in user_input.split(',')]
            st.session_state.candidate_data['desired_positions'] = positions
            self._get_next_input("location")

        elif current_stage == 'location':
            st.session_state.candidate_data['location'] = user_input
            self._get_next_input("tech_stack")

        elif current_stage == 'tech_stack':
            tech_stack = [t.strip() for t in user_input.split(',')]
            st.session_state.candidate_data['tech_stack'] = tech_stack
            self._generate_technical_questions()

        elif current_stage == 'questions':
            self._process_question_answer(user_input)

    def _get_next_input(self, field: str):
        """Get next input from candidate"""
        prompts = PromptTemplates.INFORMATION_GATHERING_PROMPTS
        if field in prompts:
            prompt = prompts[field]
            st.session_state.chat_history.append({'role': 'assistant', 'content': prompt})
            st.session_state.interview_transcript.append({'role': 'assistant', 'content': prompt})
            st.session_state.conversation_stage = field

    def _ask_for_clarification(self, field: str, stage: str):
        """Ask for clarification on invalid input"""
        clarification = f"I didn't quite understand. Could you please provide your {field}? (e.g., for experience: '5 years' or just '5')"
        st.session_state.chat_history.append({'role': 'assistant', 'content': clarification})
        st.session_state.interview_transcript.append({'role': 'assistant', 'content': clarification})
        st.session_state.conversation_stage = stage

    def _generate_technical_questions(self):
        """Generate technical questions based on tech stack"""
        st.session_state.conversation_stage = 'questions'
        
        prompt = PromptTemplates.create_tech_question_prompt(
            st.session_state.candidate_data.get('tech_stack', []),
            int(st.session_state.candidate_data.get('years_of_experience', 0))
        )
        
        # Use LLM client directly without conversation history to avoid confusion
        response = st.session_state.llm_client.generate_response(
            prompt, 
            system_message="You are a technical interviewer. Generate ONLY the numbered questions, nothing else.",
            temperature=0.7,
            max_tokens=800
        )
        
        # Parse questions - look for numbered questions
        questions = []
        lines = response.split('\n')
        
        for i, line in enumerate(lines):
            line_stripped = line.strip()
            
            # Check if line starts with a number (1., 2., 1), 2), etc.)
            if line_stripped and line_stripped[0].isdigit():
                # Extract the question number and content
                if '.' in line_stripped[:3]:
                    # Format: "1. Question text"
                    question = line_stripped
                elif ')' in line_stripped[:3]:
                    # Format: "1) Question text"
                    question = line_stripped
                else:
                    continue
                
                # Check if there are continuation lines (next line doesn't start with a number)
                j = i + 1
                while j < len(lines):
                    next_line = lines[j].strip()
                    if next_line and next_line[0].isdigit() and ('.' in next_line[:3] or ')' in next_line[:3]):
                        # Next numbered question found
                        break
                    if next_line:
                        question += " " + next_line
                    j += 1
                
                if len(question) > 10:  # Only add substantial questions
                    questions.append(question)
        
        # Fallback: if no questions extracted, split by newline and clean
        if not questions:
            questions = [q.strip() for q in lines if q.strip() and len(q.strip()) > 15]
        
        st.session_state.technical_questions = questions[:5]  # Limit to 5 questions
        st.session_state.question_index = 0
        
        # Format the message with the questions
        if st.session_state.technical_questions:
            questions_text = "\n\n".join(st.session_state.technical_questions)
            message = f"Great! Based on your tech stack ({', '.join(st.session_state.candidate_data.get('tech_stack', []))}), here are your technical questions:\n\n{questions_text}\n\nLet's start with question 1:"
        else:
            message = "Let me generate some technical questions for you based on your experience with " + ", ".join(st.session_state.candidate_data.get('tech_stack', [])) + "."
        
        st.session_state.chat_history.append({'role': 'assistant', 'content': message})
        st.session_state.interview_transcript.append({'role': 'assistant', 'content': message})

    def _process_question_answer(self, answer: str):
        """Process technical question answer"""
        # Make sure we have valid questions
        if not st.session_state.technical_questions or st.session_state.question_index >= len(st.session_state.technical_questions):
            self._end_conversation()
            return
        
        current_question = st.session_state.technical_questions[st.session_state.question_index]
        
        # Get evaluation using LLM client directly
        evaluation_prompt = PromptTemplates.create_response_evaluation_prompt(
            current_question,
            answer,
            st.session_state.candidate_data.get('tech_stack', ['Technology'])[0],
            int(st.session_state.candidate_data.get('years_of_experience', 0))
        )
        
        with st.spinner("Evaluating your answer..."):
            evaluation = st.session_state.llm_client.generate_response(
                evaluation_prompt,
                system_message="You are a technical interviewer. Respond ONLY with the 3 bullet points. No other text.",
                temperature=0.6,
                max_tokens=250
            )
        
        # Extract only the bullet points - remove everything before first bullet
        lines = evaluation.split('\n')
        feedback_lines = []
        
        for line in lines:
            line_stripped = line.strip()
            # Look for lines starting with bullet point or containing "Assessment", "Experience", "Suggestion"
            if line_stripped.startswith('•') or line_stripped.startswith('-') or line_stripped.startswith('*'):
                feedback_lines.append(line_stripped)
            elif any(keyword in line_stripped for keyword in ['Assessment:', 'Experience:', 'Suggestion:', 'Experience Match:', 'Improvement:']):
                feedback_lines.append(line_stripped)
            # Stop if we hit unwanted content
            elif any(keyword in line_stripped for keyword in ['Thank you', 'Interview Summary', 'Good luck', 'Next Steps', 'Name:', 'Years']):
                break
        
        # Reconstruct feedback
        if feedback_lines:
            evaluation = '\n'.join(feedback_lines)
        else:
            # Fallback: take first 3-4 lines
            evaluation = '\n'.join(lines[:min(4, len(lines))])
        
        evaluation = evaluation.strip()
        
        # Only add if we have meaningful feedback
        if evaluation and len(evaluation) > 10:
            st.session_state.chat_history.append({'role': 'assistant', 'content': evaluation})
            st.session_state.interview_transcript.append({'role': 'assistant', 'content': evaluation})
        
        st.session_state.question_index += 1
        
        # Move to next question or end
        if st.session_state.question_index < len(st.session_state.technical_questions):
            next_q = st.session_state.technical_questions[st.session_state.question_index]
            next_msg = f"Let's move on to question {st.session_state.question_index + 1}:\n\n{next_q}"
            st.session_state.chat_history.append({'role': 'assistant', 'content': next_msg})
            st.session_state.interview_transcript.append({'role': 'assistant', 'content': next_msg})
        else:
            # All questions answered
            self._end_conversation()
        
        # Rerun to immediately show the response
        st.rerun()

    def _end_conversation(self):
        """End conversation and provide summary"""
        st.session_state.conversation_active = False
        st.session_state.conversation_stage = 'conclusion'
        
        conclusion_message = f"""
Thank you for your interest in TalentScout! 🎉

**Interview Summary:**
- Name: {st.session_state.candidate_data.get('name', 'N/A')}
- Years of Experience: {st.session_state.candidate_data.get('years_of_experience', 'N/A')}
- Desired Positions: {', '.join(st.session_state.candidate_data.get('desired_positions', []))}
- Tech Stack: {', '.join(st.session_state.candidate_data.get('tech_stack', []))}

**Next Steps:**
Our team will review your responses and contact you within 48 hours with feedback and information about the next interview round.

Good luck! 🚀
"""
        
        st.session_state.chat_history.append({'role': 'assistant', 'content': conclusion_message})
        st.session_state.interview_transcript.append({'role': 'assistant', 'content': conclusion_message})
        
        # Save candidate data
        self.data_manager.save_candidate(st.session_state.candidate_data)
        self.data_manager.save_interview_transcript(
            self.data_manager._generate_candidate_id(st.session_state.candidate_data.get('email', '')),
            st.session_state.interview_transcript
        )

    def _download_conversation(self):
        """Prepare conversation for download"""
        data = {
            'timestamp': datetime.now().isoformat(),
            'candidate_data': {k: v for k, v in st.session_state.candidate_data.items() if k not in ['email', 'phone']},
            'conversation': st.session_state.interview_transcript
        }
        
        json_str = json.dumps(data, indent=2)
        st.download_button(
            label="Download Interview Transcript (JSON)",
            data=json_str,
            file_name=f"interview_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )

    def display_form(self):
        """Display candidate information form"""
        st.markdown("""
            <div style='text-align: center; margin-bottom: 30px;'>
                <h2 style='color: #1a237e; margin-bottom: 10px;'>📋 Candidate Information Form</h2>
                <p style='color: #666; font-size: 1.1em;'>Let's get to know you better. Please fill in the details below to begin your interview.</p>
            </div>
        """, unsafe_allow_html=True)
        st.divider()
        
        with st.form("candidate_form", clear_on_submit=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Personal Information**", help="Enter your personal details")
                name = st.text_input("👤 Full Name *", placeholder="e.g., John Doe")
                email = st.text_input("📧 Email Address *", placeholder="e.g., john@example.com")
                phone = st.text_input("📱 Phone Number *", placeholder="e.g., 9876543210")
            
            with col2:
                st.markdown("**Professional Background**", help="Tell us about your experience")
                experience = st.number_input("💼 Years of Experience *", min_value=0, max_value=70, value=0, step=1)
                location = st.text_input("📍 Location (City, Country) *", placeholder="e.g., New York, USA")
            
            st.divider()
            
            st.markdown("**🎯 Target Role**")
            position = st.text_input(
                "Target Position(s) *", 
                placeholder="e.g., Software Engineer, AI/ML Engineer (comma separated)",
                label_visibility="collapsed"
            )
            
            st.markdown("**💻 Technical Skills**")
            st.caption("List technologies you're proficient in (comma separated)")
            tech_stack = st.text_area(
                "Tech Stack",
                placeholder="e.g., Python, LLM, Generative AI, React, PostgreSQL, Docker",
                height=80,
                label_visibility="collapsed"
            )
            
            st.divider()
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                submitted = st.form_submit_button("🚀 Start Interview", use_container_width=True)
            
            if submitted:
                # Validate form
                errors = []
                if not name.strip():
                    errors.append("• Full Name is required")
                if not email.strip():
                    errors.append("• Email is required")
                if not phone.strip():
                    errors.append("• Phone is required")
                if experience <= 0:
                    errors.append("• Experience is required")
                if not location.strip():
                    errors.append("• Location is required")
                if not position.strip():
                    errors.append("• Target Position is required")
                if not tech_stack.strip():
                    errors.append("• Tech Stack is required")
                
                if errors:
                    st.error("⚠️ Please fix the following errors:\n" + "\n".join(errors))
                else:
                    # Save form data
                    st.session_state.candidate_data = {
                        'name': name.strip(),
                        'email': email.strip(),
                        'phone': phone.strip(),
                        'years_of_experience': experience,
                        'location': location.strip(),
                        'desired_positions': [p.strip() for p in position.split(',')],
                        'tech_stack': [t.strip() for t in tech_stack.split(',')]
                    }
                    
                    # Transition to interview
                    st.session_state.conversation_stage = 'questions'
                    st.session_state.chat_history = []
                    st.session_state.interview_transcript = []
                    
                    # Generate greeting and technical questions
                    greeting = f"Hello {name.split()[0]}! 👋 Welcome to TalentScout Interview!\n\nThank you for completing the information form. We're excited to learn more about your experience with {', '.join(st.session_state.candidate_data['tech_stack'][:3])}.\n\nLet's proceed with the technical interview questions."
                    st.session_state.chat_history.append({'role': 'assistant', 'content': greeting})
                    st.session_state.interview_transcript.append({'role': 'assistant', 'content': greeting})
                    
                    # Generate technical questions
                    self._generate_technical_questions()
                    
                    st.rerun()

    def run(self):
        """Run the application"""
        self.display_header()
        self.display_privacy_notice()
        
        # Show form or chat based on stage
        if st.session_state.conversation_stage == 'greeting':
            # Show form for initial data collection
            self.display_form()
        else:
            # Show interview chat
            self.display_sidebar_info()
            st.divider()
            
            # Display chat history at the top
            st.markdown("""
                <div style='margin-bottom: 20px;'>
                    <h3 style='color: #1a237e;'>💬 Interview Chat</h3>
                </div>
            """, unsafe_allow_html=True)
            chat_container = st.container()
            with chat_container:
                self.display_chat_history()
            
            st.divider()
            
            # Main question input area
            st.markdown("""
                <div style='margin-bottom: 20px;'>
                    <h3 style='color: #1a237e;'>❓ Answer Current Question</h3>
                </div>
            """, unsafe_allow_html=True)

            # Input area - present current question and a submit form per question
            if st.session_state.conversation_active:
                # Ensure we have questions
                total_q = len(st.session_state.technical_questions)
                qi = st.session_state.question_index if 'question_index' in st.session_state else 0

                if total_q == 0:
                    st.info("No technical questions available. Please restart the interview.")
                else:
                    # Display the current question explicitly
                    current_q = st.session_state.technical_questions[qi]
                    st.markdown(f"""
                        <div class='question-card'>
                            <strong>Question {qi+1} of {total_q}:</strong><br/><br/>
                            {current_q}
                        </div>
                    """, unsafe_allow_html=True)

                    # Provide a dedicated answer box and submit button
                    answer_key = f"answer_input_{qi}"
                    st.markdown("**Your Answer:**")
                    answer = st.text_area(
                        label="Your answer",
                        placeholder="Type your answer to this question here...",
                        key=answer_key,
                        height=150
                    )

                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col2:
                        if st.button("✅ Submit Answer", key=f"submit_{qi}", use_container_width=True):
                            user_input = (answer or "").strip()
                            if not user_input:
                                st.warning("⚠️ Please enter an answer before submitting.")
                            else:
                                # Append user answer and evaluate
                                st.session_state.chat_history.append({'role': 'user', 'content': user_input})
                                st.session_state.interview_transcript.append({'role': 'user', 'content': user_input})

                                # Check for explicit exit keywords
                            if ConversationFlow.should_exit(user_input):
                                self._end_conversation()
                            else:
                                self._process_question_answer(user_input)
            else:
                st.markdown("""
                    <div style='background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(6, 182, 212, 0.1) 100%); 
                                padding: 40px; border-radius: 20px; border-left: 5px solid #10b981;
                                border: 2px solid rgba(16, 185, 129, 0.3);
                                text-align: center; margin: 30px 0;
                                box-shadow: 0 8px 25px rgba(16, 185, 129, 0.1);'>
                        <h2 style='color: #10b981; margin: 0; font-size: 2em;'>✅ Interview Completed!</h2>
                        <p style='color: #86efac; margin-top: 15px; font-size: 1.15em; line-height: 1.6;'>
                            Thank you for participating in TalentScout Interview. Your responses have been recorded 
                            and will be reviewed shortly. Our team will contact you within 48 hours with feedback.
                        </p>
                    </div>
                """, unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns([1, 1, 1])
                with col1:
                    if st.button("🔄 Start New Interview", use_container_width=True):
                        st.session_state.clear()
                        self._initialize_session_state()
                        st.rerun()
                with col3:
                    if st.button("📥 Download Results", use_container_width=True):
                        self._download_conversation()


# Main execution
if __name__ == "__main__":
    app = TalentScoutApp()
    app.run()
