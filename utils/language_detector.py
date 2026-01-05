"""
Language Detection and Translation Module (Optional Enhancement)
Supports multilingual interactions
"""

from typing import Optional, Dict
from langdetect import detect, DetectorFactory

# Set seed for consistent results
DetectorFactory.seed = 0


class LanguageHandler:
    """Handles language detection and simple translation"""

    SUPPORTED_LANGUAGES = {
        'en': 'English',
        'es': 'Spanish',
        'fr': 'French',
        'de': 'German',
        'pt': 'Portuguese',
        'it': 'Italian',
        'ja': 'Japanese',
        'zh-cn': 'Chinese (Simplified)',
        'hi': 'Hindi'
    }

    @staticmethod
    def detect_language(text: str) -> Optional[str]:
        """
        Detect language of given text
        
        Args:
            text: Text to analyze
            
        Returns:
            Language code (e.g., 'en', 'es')
        """
        try:
            lang = detect(text)
            return lang if lang in LanguageHandler.SUPPORTED_LANGUAGES else 'en'
        except Exception:
            return 'en'  # Default to English on error

    @staticmethod
    def get_language_name(lang_code: str) -> str:
        """Get full language name from code"""
        return LanguageHandler.SUPPORTED_LANGUAGES.get(lang_code, 'Unknown')

    @staticmethod
    def get_supported_languages() -> Dict[str, str]:
        """Get all supported languages"""
        return LanguageHandler.SUPPORTED_LANGUAGES.copy()

    @staticmethod
    def create_multilingual_greeting(language: str = 'en') -> str:
        """Create greeting in specified language"""
        greetings = {
            'en': 'Hello! Welcome to TalentScout.',
            'es': '¡Hola! Bienvenido a TalentScout.',
            'fr': 'Bonjour! Bienvenue à TalentScout.',
            'de': 'Hallo! Willkommen bei TalentScout.',
            'pt': 'Olá! Bem-vindo ao TalentScout.',
            'it': 'Ciao! Benvenuto a TalentScout.',
            'ja': 'こんにちは！TalentScoutへようこそ。',
            'zh-cn': '你好！欢迎来到TalentScout。',
            'hi': 'नमस्ते! TalentScout में आपका स्वागत है।'
        }
        return greetings.get(language, greetings['en'])
