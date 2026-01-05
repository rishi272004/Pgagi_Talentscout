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

# Custom CSS for better UI
st.markdown("""
<style>
    .stApp {
        background-color: #f5f7fa;
    }
    .chat-message {
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        font-size: 15px;
        line-height: 1.6;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196F3;
    }
    .assistant-message {
        background-color: #f3e5f5;
        border-left: 4px solid #9c27b0;
    }
    .system-message {
        background-color: #fff3e0;
        border-left: 4px solid #ff9800;
    }
    .header-title {
        color: #1a237e;
        text-align: center;
        margin-bottom: 20px;
    }
    .sidebar-info {
        background-color: #eceff1;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)


class TalentScoutApp:
    """Main application class for TalentScout Hiring Assistant"""

    def __init__(self):
        """Initialize the application"""
        self.data_manager = CandidateDataManager(data_dir="data")
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
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("<h1 style='text-align: center; color: #1a237e;'>🎯 TalentScout</h1>", 
                       unsafe_allow_html=True)
            st.markdown("<h3 style='text-align: center; color: #5e35b1;'>Intelligent Hiring Assistant</h3>", 
                       unsafe_allow_html=True)

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
            
            # Collected information
            if st.session_state.candidate_data:
                st.markdown("### 📝 Collected Information")
                
                if 'name' in st.session_state.candidate_data:
                    st.text(f"👤 Name: {st.session_state.candidate_data['name']}")
                
                if 'email' in st.session_state.candidate_data:
                    masked_email = SensitiveDataHandler.mask_email(st.session_state.candidate_data['email'])
                    st.text(f"📧 Email: {masked_email}")
                
                if 'phone' in st.session_state.candidate_data:
                    masked_phone = SensitiveDataHandler.mask_phone(st.session_state.candidate_data['phone'])
                    st.text(f"📞 Phone: {masked_phone}")
                
                if 'years_of_experience' in st.session_state.candidate_data:
                    st.text(f"⏱️ Experience: {st.session_state.candidate_data['years_of_experience']} years")
                
                if 'desired_positions' in st.session_state.candidate_data:
                    positions = ", ".join(st.session_state.candidate_data['desired_positions'])
                    st.text(f"💼 Positions: {positions}")
                
                if 'tech_stack' in st.session_state.candidate_data:
                    st.text(f"🛠️ Tech Stack: {len(st.session_state.candidate_data['tech_stack'])} technologies")
            
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
                    f"<div class='chat-message user-message'><b>You:</b> {message['content']}</div>",
                    unsafe_allow_html=True
                )
            elif message['role'] == 'assistant':
                st.markdown(
                    f"<div class='chat-message assistant-message'><b>TalentScout:</b> {message['content']}</div>",
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
        
        response = st.session_state.conversation_manager.get_response(prompt, temperature=0.8)
        
        # Parse questions
        st.session_state.technical_questions = [q.strip() for q in response.split('\n') if q.strip()]
        st.session_state.question_index = 0
        
        message = f"Great! Based on your tech stack, here are your technical questions:\n\n{response}\n\nLet's start with question 1:"
        st.session_state.chat_history.append({'role': 'assistant', 'content': message})
        st.session_state.interview_transcript.append({'role': 'assistant', 'content': message})

    def _process_question_answer(self, answer: str):
        """Process technical question answer"""
        if st.session_state.question_index < len(st.session_state.technical_questions):
            current_question = st.session_state.technical_questions[st.session_state.question_index]
            
            # Get evaluation
            evaluation_prompt = PromptTemplates.create_response_evaluation_prompt(
                current_question,
                answer,
                st.session_state.candidate_data.get('tech_stack', ['Technology'])[0],
                int(st.session_state.candidate_data.get('years_of_experience', 0))
            )
            
            evaluation = st.session_state.conversation_manager.get_response(evaluation_prompt, temperature=0.6)
            
            st.session_state.chat_history.append({'role': 'assistant', 'content': evaluation})
            st.session_state.interview_transcript.append({'role': 'assistant', 'content': evaluation})
            
            st.session_state.question_index += 1
            
            if st.session_state.question_index < len(st.session_state.technical_questions):
                next_q = f"\nLet's move on to question {st.session_state.question_index + 1}: {st.session_state.technical_questions[st.session_state.question_index]}"
                st.session_state.chat_history.append({'role': 'assistant', 'content': next_q})
                st.session_state.interview_transcript.append({'role': 'assistant', 'content': next_q})
            else:
                self._end_conversation()
        else:
            self._end_conversation()

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

    def run(self):
        """Run the application"""
        self.display_header()
        self.display_sidebar_info()
        self.display_privacy_notice()
        
        st.divider()
        
        # Main chat area
        st.markdown("### 💬 Interview Chat")
        
        # Display chat history
        chat_container = st.container()
        with chat_container:
            self.display_chat_history()
        
        st.divider()
        
        # Input area
        if st.session_state.conversation_active:
            user_input = st.text_input(
                "Your response:",
                placeholder="Type your answer here... (or type 'exit' to end)",
                key=f"input_{len(st.session_state.chat_history)}"
            )
            
            if user_input:
                self.process_user_input(user_input)
                st.rerun()
        else:
            st.info("Interview completed! Thank you for participating.")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔄 Start New Interview"):
                    st.session_state.clear()
                    self._initialize_session_state()
                    st.rerun()
            with col2:
                if st.button("📥 Download Results"):
                    self._download_conversation()
        
        # Process greeting if needed
        if st.session_state.conversation_stage == 'greeting' and not st.session_state.chat_history:
            self.process_greeting()
            st.rerun()


# Main execution
if __name__ == "__main__":
    app = TalentScoutApp()
    app.run()
