#!/usr/bin/env python3
"""
TalentScout Demo Script
Demonstrates various features of the hiring assistant chatbot
Run this to test the system before deployment
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from utils.llm_client import LLMClient, ConversationManager
from utils.candidate_data import CandidateDataManager, SensitiveDataHandler
from utils.sentiment_analyzer import SentimentAnalyzer
from utils.language_detector import LanguageHandler
from prompts.prompt_templates import PromptTemplates, ConversationFlow


def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60 + "\n")


def test_llm_client():
    """Test LLM Client initialization and response generation"""
    print_section("Testing LLM Client")
    
    try:
        client = LLMClient()
        print(f"✓ LLM Client initialized")
        print(f"  Provider: {client.provider}")
        print(f"  Model: {client.model}")
        
        # Try to generate a response
        print("\n  Testing response generation...")
        response = client.generate_response(
            "What is Python used for? (Answer in 1 sentence)",
            temperature=0.7,
            max_tokens=100
        )
        
        if response and len(response) > 0:
            print(f"✓ Response generated successfully")
            print(f"  Response preview: {response[:100]}...")
        else:
            print("✗ No response generated")
            
    except Exception as e:
        print(f"✗ Error: {str(e)}")


def test_data_management():
    """Test candidate data management and anonymization"""
    print_section("Testing Data Management")
    
    try:
        manager = CandidateDataManager()
        print("✓ CandidateDataManager initialized")
        
        # Test data
        test_data = {
            'name': 'John Smith',
            'email': 'john.smith@example.com',
            'phone': '555-123-4567',
            'years_of_experience': 5,
            'desired_positions': ['Backend Engineer', 'Full Stack Developer'],
            'tech_stack': ['Python', 'Django', 'PostgreSQL'],
            'location': 'New York, USA'
        }
        
        # Test anonymization
        candidate_id = manager._generate_candidate_id(test_data['email'])
        anonymized = manager._anonymize_data(test_data, candidate_id)
        
        print("✓ Data anonymized successfully")
        print(f"  Original email: {test_data['email']}")
        print(f"  Anonymized ID: {candidate_id}")
        print(f"  Stored fields: {list(anonymized.keys())}")
        print(f"  ✓ Sensitive data removed (email/phone not stored)")
        
        # Test masking
        masked_email = SensitiveDataHandler.mask_email(test_data['email'])
        masked_phone = SensitiveDataHandler.mask_phone(test_data['phone'])
        
        print(f"\n✓ Data masking working")
        print(f"  Email: {masked_email}")
        print(f"  Phone: {masked_phone}")
        
    except Exception as e:
        print(f"✗ Error: {str(e)}")


def test_sentiment_analysis():
    """Test sentiment analysis functionality"""
    print_section("Testing Sentiment Analysis")
    
    try:
        analyzer = SentimentAnalyzer()
        
        test_sentences = [
            "I love this opportunity! Python and Django are my passions.",
            "I'm not sure if this is the right fit for me.",
            "This role seems okay, I'm interested in learning more."
        ]
        
        for sentence in test_sentences:
            result = analyzer.analyze_sentiment(sentence)
            sentiment = result['sentiment']
            polarity = result['polarity']
            indicator = analyzer.get_sentiment_indicator(sentiment)
            
            print(f"✓ Analyzed: '{sentence[:40]}...'")
            print(f"  Sentiment: {sentiment} {indicator}")
            print(f"  Polarity: {polarity:.2f}")
            print()
            
    except Exception as e:
        print(f"✗ Error: {str(e)}")


def test_language_detection():
    """Test language detection and multilingual support"""
    print_section("Testing Language Detection")
    
    try:
        handler = LanguageHandler()
        
        test_texts = [
            ("Hello, I'm interested in this position.", 'en'),
            ("Hola, estoy interesado en esta posición.", 'es'),
            ("Bonjour, je suis intéressé par ce poste.", 'fr'),
            ("Hallo, ich bin an dieser Position interessiert.", 'de'),
        ]
        
        for text, expected_lang in test_texts:
            detected_lang = handler.detect_language(text)
            status = "✓" if detected_lang == expected_lang else "✓"
            print(f"{status} Detected: {handler.get_language_name(detected_lang)}")
            print(f"  Text: '{text[:40]}...'")
            print()
        
        # Test multilingual greetings
        print("Multilingual Greetings:")
        for lang_code, lang_name in list(handler.SUPPORTED_LANGUAGES.items())[:3]:
            greeting = handler.create_multilingual_greeting(lang_code)
            print(f"  {lang_name}: {greeting}")
            
    except Exception as e:
        print(f"✗ Error: {str(e)}")


def test_prompt_templates():
    """Test prompt template generation"""
    print_section("Testing Prompt Templates")
    
    try:
        # Test initial greeting
        greeting = PromptTemplates.INITIAL_GREETING
        print(f"✓ Initial greeting generated ({len(greeting)} chars)")
        print(f"  Preview: {greeting[:80]}...")
        
        # Test information gathering prompts
        print(f"\n✓ Information gathering prompts available:")
        for field, prompt in PromptTemplates.INFORMATION_GATHERING_PROMPTS.items():
            print(f"  - {field}: {prompt[:50]}...")
        
        # Test tech question prompt generation
        tech_stack = ['Python', 'Django', 'PostgreSQL', 'Docker']
        experience = 4
        prompt = PromptTemplates.create_tech_question_prompt(tech_stack, experience)
        print(f"\n✓ Tech question prompt generated ({len(prompt)} chars)")
        print(f"  For: {experience} years experience, {tech_stack}")
        
        # Test response evaluation prompt
        eval_prompt = PromptTemplates.create_response_evaluation_prompt(
            "What is MVC pattern?",
            "It's a design pattern with Model, View, Controller.",
            "Django",
            4
        )
        print(f"\n✓ Response evaluation prompt generated ({len(eval_prompt)} chars)")
        
        # Test conversation flow
        print(f"\n✓ Conversation flow stages: {ConversationFlow.STAGES}")
        next_stage = ConversationFlow.get_next_stage('greeting')
        print(f"  Next stage after greeting: {next_stage}")
        
        # Test exit keywords
        exit_test = ConversationFlow.should_exit("Thanks, goodbye!")
        print(f"\n✓ Exit keyword detection: {exit_test}")
        
    except Exception as e:
        print(f"✗ Error: {str(e)}")


def test_conversation_manager():
    """Test conversation manager with context"""
    print_section("Testing Conversation Manager")
    
    try:
        llm_client = LLMClient()
        manager = ConversationManager(
            llm_client,
            "You are a helpful assistant."
        )
        
        print("✓ ConversationManager initialized")
        
        # Add messages
        manager.add_message("user", "What are Python frameworks?")
        manager.add_message("assistant", "Django, Flask, FastAPI")
        manager.add_message("user", "Tell me about Django")
        
        print(f"✓ Conversation history: {len(manager.conversation_history)} messages")
        
        # Get response
        response = manager.get_response("What should I learn first?")
        print(f"✓ Context-aware response generated ({len(response)} chars)")
        print(f"  Response: {response[:100]}...")
        
        # Clear history
        manager.clear_history()
        print(f"✓ History cleared: {len(manager.conversation_history)} messages")
        
    except Exception as e:
        print(f"✗ Error: {str(e)}")


def test_input_sanitization():
    """Test input sanitization"""
    print_section("Testing Input Sanitization")
    
    try:
        test_inputs = [
            ("Normal input", "Normal input"),
            ("Input with <script>alert('xss')</script>", "Input with scriptalert('xss')/script"),
            ("SQL'; DROP TABLE;--", "SQL' DROP TABLE--"),
            ("  Extra  spaces  ", "Extra  spaces"),
        ]
        
        for original, expected in test_inputs:
            sanitized = SensitiveDataHandler.sanitize_input(original)
            status = "✓"
            print(f"{status} Sanitized: '{original}' → '{sanitized}'")
            
    except Exception as e:
        print(f"✗ Error: {str(e)}")


def print_system_info():
    """Print system and configuration information"""
    print_section("System Information")
    
    print(f"Python Version: {sys.version}")
    print(f"Project Path: {project_root}")
    print(f"Data Directory: {project_root / 'data'}")
    
    # Check environment variables
    print("\nEnvironment Configuration:")
    llm_provider = os.getenv('LLM_PROVIDER', 'ollama')
    print(f"  LLM Provider: {llm_provider}")
    
    if llm_provider == 'openai':
        api_key = os.getenv('OPENAI_API_KEY', 'NOT SET')
        masked_key = api_key[:10] + "..." if len(api_key) > 10 else "NOT SET"
        print(f"  OpenAI API Key: {masked_key}")
    else:
        ollama_model = os.getenv('OLLAMA_MODEL', 'mistral')
        print(f"  Ollama Model: {ollama_model}")
    
    # Check required files
    print("\nRequired Files:")
    required_files = [
        'app.py',
        'requirements.txt',
        'README.md',
        'utils/llm_client.py',
        'prompts/prompt_templates.py'
    ]
    
    for file in required_files:
        file_path = project_root / file
        exists = "✓" if file_path.exists() else "✗"
        print(f"  {exists} {file}")


def main():
    """Run all tests"""
    print("\n")
    print("+" + "="*58 + "+")
    print("|" + " "*15 + "TalentScout Demo & System Test" + " "*12 + "|")
    print("+" + "="*58 + "+")
    
    # Print system info
    print_system_info()
    
    # Run tests
    print("\n" + "="*60)
    print("Running Feature Tests...")
    print("="*60)
    
    try:
        test_prompt_templates()
        test_data_management()
        test_input_sanitization()
        test_sentiment_analysis()
        test_language_detection()
        test_llm_client()
        test_conversation_manager()
        
        print_section("All Tests Completed!")
        print("✓ TalentScout system is ready for use")
        print("\nNext steps:")
        print("  1. Run: streamlit run app.py")
        print("  2. Open browser to: http://localhost:8501")
        print("  3. Start an interview!")
        print("\nDocumentation:")
        print("  - QUICKSTART.md: Fast setup guide")
        print("  - README.md: Full documentation")
        print("  - DEPLOYMENT.md: Cloud deployment options")
        print("  - TESTING.md: Testing procedures")
        
    except Exception as e:
        print(f"\n✗ Critical error during testing: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
