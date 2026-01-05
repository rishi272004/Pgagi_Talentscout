"""
Prompt Engineering Module
Contains all system prompts and dynamic prompt generation
"""

from typing import Dict, List


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
        
        return f"""Based on the candidate's technical stack: {tech_list}
And their experience level: {years_exp} years (difficulty: {difficulty})

Generate exactly 3-5 technical questions that:
1. Are appropriate for their experience level
2. Test practical knowledge and problem-solving skills
3. Are clear and concise
4. Can be answered verbally
5. Cover different technologies from their stack when possible

Format each question on a new line with a number (1., 2., etc.)
Include a brief explanation of what you're testing with each question."""

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
        return f"""Evaluate this candidate's technical response:

Technology: {tech}
Experience: {years_exp} years
Question: {question}
Answer: {answer}

Provide:
1. A brief assessment (1-2 sentences) of their understanding
2. Whether the answer demonstrates the expected level for their experience
3. One constructive suggestion for improvement (if applicable)

Be encouraging and professional in your feedback."""

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
        user_input_lower = user_input.lower().strip()
        for keyword in ConversationFlow.EXIT_KEYWORDS:
            if keyword in user_input_lower:
                return True
        return False
