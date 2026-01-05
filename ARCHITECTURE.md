# Architecture & Technical Details

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  STREAMLIT FRONTEND                      │
│  (Interactive Web UI with Chat Interface)               │
└──────────────┬──────────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────────┐
│              TALENTSCOUT APPLICATION (app.py)           │
│  ┌─────────────────────────────────────────────────────┐│
│  │  - Conversation Flow Management                      ││
│  │  - User Input Processing                             ││
│  │  - Interview Stage Orchestration                     ││
│  └─────────────────────────────────────────────────────┘│
└──────────────┬──────────────────────────────────────────┘
               │
        ┌──────┴────────┬──────────────┬──────────────┐
        │               │              │              │
        ▼               ▼              ▼              ▼
  ┌──────────┐  ┌──────────────┐ ┌────────────┐ ┌──────────┐
  │ LLM      │  │ Prompt       │ │ Data       │ │ Sentiment│
  │ Client   │  │ Templates    │ │ Manager    │ │Analyzer  │
  │          │  │              │ │            │ │          │
  │- OpenAI │  │- System      │ │- Storage   │ │- Emotion │
  │- Ollama │  │  Prompts     │ │- Privacy   │ │- Tone    │
  │- Local  │  │- Q Generator │ │- Anonymize │ │ Analysis │
  └────┬─────┘  └──────────────┘ └────────────┘ └──────────┘
       │
  ┌────▼────────────────┐
  │  External LLM API    │
  │  (OpenAI/Ollama)    │
  └─────────────────────┘
```

## Data Flow

### Interview Process
```
User Input
    ↓
Sanitization (Injection Prevention)
    ↓
Language Detection
    ↓
Sentiment Analysis
    ↓
Context-Aware Processing (Based on Current Stage)
    ↓
LLM Processing with System Prompt
    ↓
Response Generation
    ↓
Conversation History Update
    ↓
Data Storage (Anonymized)
    ↓
Display to User
```

## Module Descriptions

### 1. `app.py` - Main Application
**Responsibilities**:
- UI rendering with Streamlit
- Conversation flow orchestration
- User session management
- Chat history display
- Sidebar information panel

**Key Classes**:
- `TalentScoutApp`: Main application class

**Key Methods**:
- `process_greeting()`: Initial greeting
- `process_user_input()`: Route input to stage handlers
- `_generate_technical_questions()`: Create tech questions
- `_process_question_answer()`: Evaluate responses
- `_end_conversation()`: Graceful conclusion

### 2. `utils/llm_client.py` - LLM Integration
**Responsibilities**:
- Multi-provider LLM support (OpenAI, Ollama, Local)
- API request handling
- Response parsing
- Error handling and fallbacks

**Key Classes**:
- `LLMClient`: Abstracts LLM provider differences
- `ConversationManager`: Manages multi-turn conversations with context

**Key Methods**:
- `generate_response()`: Get LLM response with context
- `get_response()`: Conversation-aware response generation

### 3. `utils/candidate_data.py` - Data Management
**Responsibilities**:
- Candidate information storage
- Data anonymization (GDPR compliance)
- Sensitive data masking
- Interview transcript saving

**Key Classes**:
- `CandidateDataManager`: Handles data persistence
- `SensitiveDataHandler`: Masking and sanitization

**Key Methods**:
- `save_candidate()`: Persist anonymized data
- `_anonymize_data()`: Remove sensitive information
- `mask_email()`: Email masking (a***@***.com)
- `mask_phone()`: Phone masking (***-***-1234)
- `sanitize_input()`: Input validation

### 4. `utils/sentiment_analyzer.py` - Sentiment Analysis (Bonus)
**Responsibilities**:
- Analyze emotional tone in responses
- Rate confidence and subjectivity
- Provide sentiment indicators

**Key Classes**:
- `SentimentAnalyzer`: TextBlob-based analysis

**Key Methods**:
- `analyze_sentiment()`: Get polarity and subjectivity
- `_classify_sentiment()`: Convert score to label

### 5. `utils/language_detector.py` - Multilingual Support (Bonus)
**Responsibilities**:
- Detect user language
- Provide multilingual greetings
- Track language preferences

**Key Classes**:
- `LanguageHandler`: Language detection and management

**Key Methods**:
- `detect_language()`: Identify language from text
- `create_multilingual_greeting()`: Localized greetings

### 6. `prompts/prompt_templates.py` - Prompt Engineering
**Responsibilities**:
- Store all system and user prompts
- Generate dynamic prompts based on context
- Manage conversation stages

**Key Classes**:
- `PromptTemplates`: Static prompt templates
- `ConversationFlow`: Stage management

**Key Methods**:
- `create_tech_question_prompt()`: Generate tech questions
- `create_response_evaluation_prompt()`: Evaluate answers
- `get_next_stage()`: Orchestrate conversation flow

## Conversation States

```
greeting (Start)
    ↓
name (Collect name)
    ↓
email (Collect email)
    ↓
phone (Collect phone)
    ↓
experience (Collect years of experience)
    ↓
position (Collect desired position)
    ↓
location (Collect location)
    ↓
tech_stack (Collect tech stack)
    ↓
questions (Ask technical questions - loop)
    ├─ Q1 ↔ Answer 1
    ├─ Q2 ↔ Answer 2
    ├─ Q3 ↔ Answer 3
    └─ Q4/5 ↔ Answer 4/5
    ↓
conclusion (End interview)
```

## Prompt Engineering Strategy

### 1. System Prompt
- Sets overall behavior and constraints
- Defines role as hiring assistant
- Establishes communication style
- Sets boundaries and exit conditions

### 2. Context Management
- Maintains conversation history
- Includes previous messages for coherence
- Adapts difficulty based on experience level

### 3. Dynamic Prompt Generation
```python
# Example: Tech Question Generation
difficulty = "beginner" if years < 2 else "intermediate" if years < 5 else "advanced"
prompt = f"""Generate {len(tech_stack)} questions for {difficulty} developer
with skills: {tech_stack}"""
```

### 4. Response Evaluation
- Contextual feedback based on experience
- Constructive suggestions
- Professional tone

## Security & Privacy

### Data Flow Security
```
User Input → Sanitization → Processing → Anonymization → Storage
```

### Privacy Measures
1. **Input Sanitization**
   - Remove SQL injection characters
   - Filter script tags
   - Escape special characters

2. **Data Anonymization**
   - Hash-based candidate ID (SHA-256)
   - Never store raw email/phone in main data
   - Separate sensitive data handling

3. **GDPR Compliance**
   - Data minimization
   - User rights (access, delete)
   - Privacy notice display
   - 90-day retention policy

### Masked Data Example
```python
Original: john.smith@gmail.com
Masked:   j***@***.com

Original: 555-123-4567
Masked:   ***-***-4567
```

## Performance Optimization

### 1. Context Caching
- Store conversation history in session
- Avoid reprocessing previous messages
- Limit context window for efficiency

### 2. Lazy Loading
- Initialize LLM client only when needed
- Load sentiment analyzer on demand
- Defer non-critical features

### 3. Response Optimization
```python
max_tokens=500  # Limit response length
temperature=0.7  # Balance creativity and consistency
```

## Error Handling Strategy

### 1. LLM Provider Fallback
- Try primary provider (OpenAI)
- Fall back to Ollama
- Provide helpful error message if both fail

### 2. Input Validation
- Sanitize all user inputs
- Ask for clarification on invalid data
- Provide examples

### 3. Connection Recovery
- Retry logic for network errors
- Graceful degradation
- User-friendly error messages

## Scalability Considerations

### 1. Multi-User Support
- Streamlit handles multiple sessions
- Each user has isolated session state
- Data saved independently

### 2. Data Storage
- JSON files for simplicity
- Can migrate to database (PostgreSQL, MongoDB)
- Anonymization ensures privacy at scale

### 3. LLM Provider Scaling
- Ollama: Limited by single machine resources
- OpenAI: Scales automatically with API

## Testing Strategy

### Unit Tests
```python
# Test data anonymization
test_anonymize_data()
test_mask_email()
test_mask_phone()

# Test prompt generation
test_tech_question_prompt()
test_response_evaluation_prompt()

# Test sentiment analysis
test_sentiment_analysis()

# Test language detection
test_language_detection()
```

### Integration Tests
- Full conversation flow
- Multi-turn interactions
- Data persistence
- Error scenarios

### User Acceptance Tests
- End-to-end interview
- Different tech stacks
- Edge cases (special characters, etc.)
- Privacy compliance

## Deployment Architecture

### Local Development
```
Developer Machine
    ↓
Ollama (localhost:11434)
    ↓
Streamlit Server (localhost:8501)
    ↓
Browser
```

### Cloud Deployment (AWS)
```
GitHub Repository
    ↓
AWS EC2 Instance
    ├─ Ollama Server
    └─ Streamlit Application
    ↓
AWS Elastic IP (Static URL)
    ↓
Internet Users
```

### Streamlit Cloud Deployment
```
GitHub Repository
    ↓
Streamlit Cloud
    ├─ Auto-deployed
    ├─ Environment variables set
    └─ Live URL generated
    ↓
Internet Users
```

## Future Enhancements

### 1. Database Integration
- Replace JSON with PostgreSQL
- Enable scalable data storage
- Add query capabilities

### 2. Advanced Analytics
- Candidate scoring algorithm
- Interview quality metrics
- Comparative analysis dashboard

### 3. Integration Features
- Resume parsing (PDF/DOCX)
- ATS system integration
- Email notifications
- Slack integration

### 4. Advanced AI Features
- Resume-based question generation
- Video interview support
- Behavioral assessment
- Skill scoring

### 5. Performance Optimizations
- Async processing
- Response caching
- Load balancing
- Rate limiting

---

**Version**: 1.0.0  
**Last Updated**: January 2026
