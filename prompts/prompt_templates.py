"""
Prompt Engineering Module
Contains all system prompts and dynamic prompt generation
"""

from typing import Dict, List
import re


class PromptTemplates:
    """System prompts for different conversation stages"""

    SYSTEM_PROMPT = """You are TalentScout's Intelligent Hiring Assistant - a professional, friendly, and knowledgeable recruiter helping candidates through an initial screening process.

Your responsibilities:
1. Greet candidates warmly and explain the screening process
2. Gather essential information: name, email, phone, experience, desired positions, location, and tech stack
3. Maintain a conversational, professional tone
4. Ask one piece of information at a time
5. Validate inputs and ask for clarification if needed
6. Once you have all information, generate 3-5 technical questions based on their tech stack
7. Evaluate their responses thoughtfully
8. End the conversation gracefully with next steps

Important Guidelines:
- Be encouraging and supportive
- Never deviate from your purpose as a hiring assistant
- If the candidate asks off-topic questions, politely redirect to the interview
- Provide meaningful feedback on technical responses
- Remember context from previous messages
- Use appropriate technical depth based on their experience level

Exit Conditions:
- Respond with "Thank you for your interest in TalentScout!" when you encounter:
  - "exit", "quit", "bye", "goodbye", "done", "thank you", "no more"
  - Or when the interview process is complete
"""

    INITIAL_GREETING = """Hello! 👋 Welcome to TalentScout - your gateway to exciting technology job opportunities!

I'm your Hiring Assistant, and I'm here to conduct an initial screening to understand your background and skills. This conversation should take about 10-15 minutes.

Let's get started! Could you please tell me your **full name**?"""

    INFORMATION_GATHERING_PROMPTS = {
        'email': "Great! Now, what's your **email address**? (We'll use this to contact you about next steps)",
        'phone': "Perfect! And your **phone number**? (We'll keep this for interview scheduling)",
        'experience': "Thanks! How many **years of experience** do you have in software development/technology? (e.g., 2, 5, 10)",
        'position': "Excellent! What **position(s)** are you interested in? (e.g., Software Engineer, Data Scientist, Full-Stack Developer)",
        'location': "And where are you currently located? (City and Country)",
        'tech_stack': """Wonderful! Now, let's talk about your **technical skills**. 

Please list the technologies you're proficient in. Include:
- **Programming Languages** (Python, Java, JavaScript, etc.)
- **Frameworks** (Django, React, Spring Boot, etc.)
- **Databases** (PostgreSQL, MongoDB, etc.)
- **Tools** (Git, Docker, Kubernetes, etc.)

You can list them separated by commas (e.g., "Python, Django, PostgreSQL, Docker")"""
    }

    @staticmethod
    def create_tech_question_prompt(tech_stack: List[str], years_exp: int) -> str:
        """
        Create dynamic prompt for generating technical questions
        
        Args:
            tech_stack: List of technologies
            years_exp: Years of experience
            
        Returns:
            Prompt for generating technical questions
        """
        difficulty = "beginner" if years_exp < 2 else "intermediate" if years_exp < 5 else "advanced"
        
        tech_list = ", ".join(tech_stack[:5])  # Limit to first 5 for clarity
        
        return f"""You are a technical interviewer. Generate exactly 5 technical interview questions for a candidate with the following profile:
- Technical Stack: {tech_list}
- Experience Level: {years_exp} years ({difficulty} level)

IMPORTANT: Format your response EXACTLY like this, with ONLY the questions and nothing else:

1. [FIRST FULL QUESTION HERE - Make it clear and detailed]

2. [SECOND FULL QUESTION HERE - Make it clear and detailed]

3. [THIRD FULL QUESTION HERE - Make it clear and detailed]

4. [FOURTH FULL QUESTION HERE - Make it clear and detailed]

5. [FIFTH FULL QUESTION HERE - Make it clear and detailed]

Rules:
- Each question MUST start with a number (1., 2., 3., etc.) 
- Questions should be appropriate for {difficulty} level
- Questions should test practical knowledge
- No extra text, explanations, or formatting - just the numbered questions
- Keep questions concise but complete (1-3 sentences each)"""

    @staticmethod
    def create_response_evaluation_prompt(question: str, answer: str, tech: str, years_exp: int) -> str:
        """
        Create prompt for evaluating candidate responses
        
        Args:
            question: The question asked
            answer: The candidate's answer
            tech: The technology being tested
            years_exp: Years of experience
            
        Returns:
            Evaluation prompt
        """
        return f"""Evaluate this technical response in BULLET format only.

Q: {question}
A: {answer}

Respond ONLY with these 3 bullets, nothing else:
• Assessment: [1-2 sentences on their understanding]
• Experience Match: [Is this appropriate for {years_exp} years experience?]
• Suggestion: [One improvement tip]

DO NOT add any other text, conclusions, or messages."""

    @staticmethod
    def create_conclusion_prompt(candidate_data: Dict, transcript: List[str]) -> str:
        """
        Create prompt for concluding the interview
        
        Args:
            candidate_data: Candidate information collected
            transcript: Interview transcript
            
        Returns:
            Conclusion prompt
        """
        position = candidate_data.get('desired_positions', ['the applied position'])[0]
        
        return f"""Based on this interview with a candidate for {position} position:
Candidate Experience: {candidate_data.get('years_of_experience')} years
Tech Stack: {', '.join(candidate_data.get('tech_stack', []))}

Provide a brief summary (2-3 sentences) of your initial impressions and 
recommend next steps in the interview process."""


class ConversationFlow:
    """Manages the flow of conversation through different stages"""

    STAGES = ['greeting', 'name', 'email', 'phone', 'experience', 'position', 'location', 'tech_stack', 'questions', 'conclusion']
    
    EXIT_KEYWORDS = ['exit', 'quit', 'bye', 'goodbye', 'done', 'thank you', 'no more', 'end']

    @staticmethod
    def get_next_stage(current_stage: str) -> str:
        """Get next conversation stage"""
        try:
            current_index = ConversationFlow.STAGES.index(current_stage)
            if current_index < len(ConversationFlow.STAGES) - 1:
                return ConversationFlow.STAGES[current_index + 1]
        except ValueError:
            pass
        return 'conclusion'

    @staticmethod
    def should_exit(user_input: str) -> bool:
        """Check if user input contains exit keywords"""
        # Normalize input by removing punctuation and extra whitespace
        user_input_lower = re.sub(r"[^\w\s]", "", user_input.lower()).strip()
        # Trigger exit only on exact matches (or exact phrase matches like 'no more')
        for keyword in ConversationFlow.EXIT_KEYWORDS:
            if user_input_lower == keyword:
                return True
        return False
