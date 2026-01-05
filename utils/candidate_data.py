"""
Candidate Data Management Module
Handles storage, retrieval, and privacy of candidate information
"""

import json
import os
from datetime import datetime
from typing import Dict, Optional, List
import hashlib


class CandidateDataManager:
    """Manages candidate data storage and privacy"""

    def __init__(self, data_dir: str = "data"):
        """
        Initialize Candidate Data Manager
        
        Args:
            data_dir: Directory for storing candidate data
        """
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)

    def save_candidate(self, candidate_data: Dict) -> str:
        """
        Save candidate information securely
        
        Args:
            candidate_data: Dictionary containing candidate information
            
        Returns:
            Candidate ID (anonymized hash)
        """
        # Generate anonymized ID
        candidate_id = self._generate_candidate_id(candidate_data.get('email', ''))
        
        # Anonymize sensitive data
        anonymized_data = self._anonymize_data(candidate_data, candidate_id)
        
        # Save to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"candidates_{timestamp}.json"
        filepath = os.path.join(self.data_dir, filename)
        
        try:
            with open(filepath, 'w') as f:
                json.dump(anonymized_data, f, indent=2)
            return candidate_id
        except Exception as e:
            print(f"Error saving candidate data: {str(e)}")
            return None

    def save_interview_transcript(self, candidate_id: str, transcript: List[Dict]) -> bool:
        """
        Save interview transcript
        
        Args:
            candidate_id: Anonymized candidate ID
            transcript: Interview conversation transcript
            
        Returns:
            Success status
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"interview_{candidate_id}_{timestamp}.json"
        filepath = os.path.join(self.data_dir, filename)
        
        try:
            with open(filepath, 'w') as f:
                json.dump(transcript, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving interview transcript: {str(e)}")
            return False

    def _generate_candidate_id(self, email: str) -> str:
        """
        Generate anonymized candidate ID using hashing
        
        Args:
            email: Candidate email
            
        Returns:
            Anonymized ID
        """
        hash_object = hashlib.sha256(email.encode())
        return hash_object.hexdigest()[:16].upper()

    def _anonymize_data(self, candidate_data: Dict, candidate_id: str) -> Dict:
        """
        Anonymize sensitive candidate information
        
        Args:
            candidate_data: Original candidate data
            candidate_id: Anonymized ID
            
        Returns:
            Anonymized data dictionary
        """
        anonymized = {
            "candidate_id": candidate_id,
            "timestamp": datetime.now().isoformat(),
            "years_of_experience": candidate_data.get('years_of_experience'),
            "desired_positions": candidate_data.get('desired_positions', []),
            "tech_stack": candidate_data.get('tech_stack', []),
            "location": candidate_data.get('location'),
            # Note: Email, phone, and full name are NOT stored for privacy
        }
        return anonymized

    def get_data_privacy_notice(self) -> str:
        """Return GDPR-compliant data privacy notice"""
        return """
🔒 **Data Privacy Notice (GDPR Compliant)**

Your personal data is processed in accordance with GDPR regulations:
- **Data Collection**: We collect name, email, phone, experience, and tech stack
- **Purpose**: Initial screening and candidate assessment
- **Storage**: Data is anonymized and stored securely
- **Retention**: Data is retained for 90 days unless you request deletion
- **Rights**: You have the right to access, correct, or delete your data
- **Contact**: For privacy concerns, contact privacy@talentscout.com

By proceeding, you consent to the collection and processing of your data.
        """


class SensitiveDataHandler:
    """Handles sensitive information masking and security"""

    @staticmethod
    def mask_email(email: str) -> str:
        """Mask email address for display"""
        if not email or '@' not in email:
            return "***@***.com"
        
        parts = email.split('@')
        username = parts[0]
        
        if len(username) <= 2:
            masked_username = f"{username[0]}***"
        else:
            masked_username = f"{username[0]}***{username[-1]}"
        
        return f"{masked_username}@***"

    @staticmethod
    def mask_phone(phone: str) -> str:
        """Mask phone number for display"""
        if not phone or len(phone) < 4:
            return "***-***-****"
        
        return f"***-***-{phone[-4:]}"

    @staticmethod
    def sanitize_input(user_input: str) -> str:
        """Sanitize user input to prevent injection attacks"""
        # Remove potentially harmful characters
        forbidden_chars = ['<', '>', '"', "'", ';', '--', '/*', '*/']
        sanitized = user_input
        
        for char in forbidden_chars:
            sanitized = sanitized.replace(char, '')
        
        return sanitized.strip()
