# Testing Guide & Quality Assurance

## 🧪 Testing Strategy

### Test Categories
1. **Unit Tests** - Individual functions
2. **Integration Tests** - Component interactions
3. **End-to-End Tests** - Complete user flows
4. **Manual Testing** - User experience validation

---

## ✅ Manual Testing Checklist

### 1. Greeting & Initialization
- [ ] Application starts without errors
- [ ] Initial greeting message displays
- [ ] Progress bar shows at 10%
- [ ] Sidebar displays properly
- [ ] Chat history is empty

### 2. Information Gathering

#### Name
- [ ] Prompt asks for name
- [ ] Input is accepted
- [ ] Name is collected correctly
- [ ] Progress moves to email stage
- [ ] Name displays in sidebar

#### Email
- [ ] Prompt asks for email
- [ ] Email is masked in sidebar (a***@***.com)
- [ ] Progress updates to 30%
- [ ] Phone prompt appears

#### Phone
- [ ] Prompt asks for phone
- [ ] Phone is masked in sidebar (***-***-XXXX)
- [ ] Progress updates to 40%
- [ ] Experience prompt appears

#### Experience
- [ ] Prompt asks for years of experience
- [ ] Accepts numeric input
- [ ] Clarifies if input is invalid
- [ ] Progress updates to 50%
- [ ] Position prompt appears

#### Position
- [ ] Prompt asks for desired positions
- [ ] Accepts multiple positions (comma-separated)
- [ ] Parses positions correctly
- [ ] Progress updates to 60%
- [ ] Location prompt appears

#### Location
- [ ] Prompt asks for location
- [ ] Accepts city and country
- [ ] Progress updates to 70%
- [ ] Tech stack prompt appears

#### Tech Stack
- [ ] Prompt asks for technologies
- [ ] Accepts multiple technologies (comma-separated)
- [ ] Lists various types (languages, frameworks, databases)
- [ ] Tech stack displays in sidebar
- [ ] Progress updates to 80%

### 3. Technical Question Generation
- [ ] Questions are generated after tech stack submission
- [ ] Correct number of questions (3-5)
- [ ] Questions are relevant to tech stack
- [ ] Questions match experience level
- [ ] Progress updates to 85%

### 4. Question Answering & Evaluation
- [ ] First question displays clearly
- [ ] User answer is accepted
- [ ] Evaluation/feedback is provided
- [ ] Next question appears
- [ ] All questions are presented

### 5. Conversation Conclusion
- [ ] Summary message displays
- [ ] Interview details are accurate
- [ ] Download button appears
- [ ] Reset button works
- [ ] Progress updates to 100%

### 6. Special Features

#### Sentiment Analysis
- [ ] Sentiment score appears in sidebar
- [ ] Score updates with each message
- [ ] Sentiment indicator is displayed
- [ ] Score range is -1 to 1

#### Language Detection
- [ ] Language selector in sidebar
- [ ] Detects user's language correctly
- [ ] Displays supported languages
- [ ] Works with different languages

#### Data Privacy
- [ ] Privacy notice can be expanded
- [ ] Notice contains GDPR information
- [ ] Notice is comprehensive and clear
- [ ] Data is anonymized in storage

#### Download Functionality
- [ ] Download button generates JSON file
- [ ] JSON contains interview transcript
- [ ] Sensitive data is not in downloaded file
- [ ] File downloads successfully

### 7. Edge Cases

#### Invalid Inputs
- [ ] Non-numeric experience input shows clarification
- [ ] Empty inputs are handled gracefully
- [ ] Special characters are sanitized
- [ ] Very long inputs are truncated appropriately

#### Exit Keywords
- [ ] "exit" ends conversation
- [ ] "quit" ends conversation
- [ ] "bye" ends conversation
- [ ] "goodbye" ends conversation
- [ ] "done" ends conversation

#### Conversation Reset
- [ ] Reset button clears all data
- [ ] Chat history is empty
- [ ] Progress resets to 10%
- [ ] Sidebar info is cleared
- [ ] New interview can start

---

## 🧪 Test Scenarios

### Scenario 1: Complete Interview (Junior Developer)
```
Name: Alice Johnson
Email: alice@example.com
Phone: 555-1234
Experience: 2 years
Position: Junior Developer, Frontend Engineer
Location: San Francisco, USA
Tech Stack: JavaScript, React, HTML, CSS, Git

Expected: 3-4 beginner-friendly questions on React/JavaScript
```

### Scenario 2: Complete Interview (Senior Developer)
```
Name: Bob Smith
Email: bob@example.com
Phone: 555-5678
Experience: 7 years
Position: Senior Backend Engineer, Tech Lead
Location: New York, USA
Tech Stack: Python, Django, PostgreSQL, Docker, Kubernetes, AWS

Expected: 4-5 advanced questions on system design, architecture
```

### Scenario 3: Multi-Technology Stack
```
Name: Carol White
Email: carol@example.com
Phone: 555-9012
Experience: 4 years
Position: Full Stack Developer
Location: London, UK
Tech Stack: Python, JavaScript, React, Node.js, PostgreSQL, MongoDB, Docker, Redis

Expected: Questions covering both frontend and backend technologies
```

### Scenario 4: Early Exit
```
Start interview → At phone stage → Type "exit"
Expected: Graceful conclusion with summary
```

### Scenario 5: Invalid Inputs
```
Experience: "about five years" → Clarification prompt
Experience: "5" → Accepted and proceeds
```

### Scenario 6: Special Characters
```
Name: "John O'Brien & Co."
Tech Stack: "C++, C#, Java, JavaScript, TypeScript"
Expected: All sanitized and processed correctly
```

---

## 🔍 Performance Testing

### Load Testing
```bash
# Simulate multiple concurrent users
# Expected: Streamlit handles 10-20 concurrent sessions

# Measure:
# - Response time per message
# - Memory usage
# - CPU usage
# - LLM API response time
```

### Response Time Benchmarks
- **Greeting**: <500ms
- **Info gathering clarification**: <500ms
- **Tech question generation**: 2-5s (depends on LLM)
- **Question evaluation**: 3-8s (depends on LLM)
- **Conclusion**: <1s

### Memory Usage
- **Idle**: ~200MB
- **Active conversation**: ~300-400MB
- **With 100 messages**: ~500MB

---

## 🛡️ Security Testing

### Input Validation
- [ ] Test SQL injection attempts
- [ ] Test script injection attempts
- [ ] Test path traversal attempts
- [ ] Test buffer overflow with very long inputs

### Data Privacy
- [ ] Verify anonymization works correctly
- [ ] Check no raw email/phone in storage
- [ ] Verify GDPR notice displays
- [ ] Test data download excludes sensitive info

### Session Security
- [ ] Session data isolated per user
- [ ] No data leakage between sessions
- [ ] Session clears on browser close

---

## 🎯 LLM-Specific Tests

### OpenAI Provider
- [ ] API key validation
- [ ] Rate limiting handling
- [ ] Token counting
- [ ] Cost estimation

### Ollama Provider
- [ ] Connection to localhost:11434
- [ ] Model availability
- [ ] Response quality
- [ ] Timeout handling

### Fallback Mechanism
- [ ] If primary provider fails, shows error
- [ ] User can reset and retry
- [ ] No crash on provider unavailability

---

## 📱 UI/UX Testing

### Responsiveness
- [ ] Works on desktop (1920x1080)
- [ ] Works on tablet (1024x768)
- [ ] Mobile experience adequate

### Accessibility
- [ ] Text is readable (font size, contrast)
- [ ] Chat history is scrollable
- [ ] Buttons are clickable
- [ ] Error messages are clear

### User Experience
- [ ] Navigation is intuitive
- [ ] Progress is clear
- [ ] Feedback is timely
- [ ] Error messages are helpful

---

## 📝 Regression Testing Checklist

After making code changes:

- [ ] Run full interview flow
- [ ] Test with different tech stacks
- [ ] Verify sentiment analysis
- [ ] Check language detection
- [ ] Test data storage
- [ ] Verify download functionality
- [ ] Check conversation reset
- [ ] Test exit keywords

---

## 🐛 Bug Tracking Template

```
Bug Report #X
Title: [Brief description]
Severity: Critical/High/Medium/Low
Status: New/In Progress/Fixed/Verified

Steps to Reproduce:
1. [Step 1]
2. [Step 2]
3. [Step 3]

Expected Result:
[What should happen]

Actual Result:
[What actually happens]

Environment:
- OS: [Windows/Mac/Linux]
- Python Version: [X.X]
- Streamlit Version: [X.X]
- LLM Provider: [openai/ollama]

Screenshots/Logs:
[Attach error messages or logs]

Notes:
[Additional information]
```

---

## ✨ Test Results Summary Template

```markdown
# Test Results - [Date]

## Overall Status: PASS/FAIL

### Test Coverage
- Unit Tests: X/X passed
- Integration Tests: X/X passed
- E2E Tests: X/X passed
- Manual Tests: X/X passed

### Issues Found
- [ ] Critical Issues: 0
- [ ] High Priority: 0
- [ ] Medium Priority: 0
- [ ] Low Priority: 0

### Performance
- Average Response Time: Xms
- Memory Usage: XXXMb
- Concurrent Users Tested: X

### Sign-off
- QA Lead: [Name]
- Date: [Date]
- Status: Ready for Deployment/Needs Fixes
```

---

## 🚀 Continuous Testing

### Automated Testing (Future)
```python
# tests/test_llm_client.py
def test_llm_response_generation():
    client = LLMClient()
    response = client.generate_response("Test prompt")
    assert len(response) > 0
    assert isinstance(response, str)

# tests/test_data_manager.py
def test_anonymization():
    manager = CandidateDataManager()
    data = {"email": "test@example.com", "phone": "123456"}
    anonymized = manager._anonymize_data(data, "test_id")
    assert "email" not in anonymized
    assert "phone" not in anonymized

# tests/test_conversation_flow.py
def test_conversation_stages():
    assert ConversationFlow.get_next_stage('greeting') == 'name'
    assert ConversationFlow.get_next_stage('name') == 'email'
```

---

**Version**: 1.0.0  
**Last Updated**: January 2026
