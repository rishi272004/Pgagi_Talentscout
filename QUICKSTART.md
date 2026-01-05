# TalentScout - Quick Start Guide

## ⚡ 5-Minute Setup

### Option 1: Using Ollama (Recommended - Free & Local)

#### 1. Install Ollama
- Visit: https://ollama.ai
- Download and install for your OS
- Run the installer

#### 2. Start Ollama
```bash
ollama serve
```
This will start Ollama on `localhost:11434`

#### 3. Pull a Model
In a new terminal:
```bash
ollama pull mistral
```
(Alternative models: `ollama pull llama2`, `ollama pull neural-chat`)

#### 4. Install TalentScout
```bash
cd talentscout-hiring-assistant
pip install -r requirements.txt
```

#### 5. Run the App
```bash
streamlit run app.py
```
The app opens at: `http://localhost:8501`

### Option 2: Using OpenAI API

#### 1. Get API Key
- Go to: https://platform.openai.com/api-keys
- Create new secret key
- Copy the key

#### 2. Configure
Edit `.env`:
```
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-actual-key-here
```

#### 3. Install & Run
```bash
pip install -r requirements.txt
streamlit run app.py
```

## 🎯 Testing the Chatbot

### Sample Interview
1. **Name**: "John Smith"
2. **Email**: "john.smith@email.com"
3. **Phone**: "555-123-4567"
4. **Experience**: "5 years"
5. **Position**: "Full Stack Developer, Backend Engineer"
6. **Location**: "New York, USA"
7. **Tech Stack**: "Python, Django, PostgreSQL, Docker, React, JavaScript"
8. **Answer technical questions** - the bot will evaluate your responses
9. **Type "exit"** to end the interview

## 🔧 Configuration Files

### .env File
```env
# Choose provider: openai or ollama
LLM_PROVIDER=ollama
OLLAMA_MODEL=mistral

# Only if using OpenAI
OPENAI_API_KEY=your_api_key_here

# Debug mode
APP_DEBUG=False
```

### requirements.txt
All dependencies are pre-configured. Install with:
```bash
pip install -r requirements.txt
```

## 📁 Project Structure
```
talentscout-hiring-assistant/
├── app.py                    # Main application
├── requirements.txt          # Dependencies
├── .env                      # Configuration (create from .env.example)
├── README.md                 # Full documentation
├── QUICKSTART.md             # This file
├── utils/                    # Utility modules
│   ├── llm_client.py        # LLM integration
│   ├── candidate_data.py    # Data management
│   ├── sentiment_analyzer.py
│   └── language_detector.py
├── prompts/                  # Prompt templates
│   └── prompt_templates.py
└── data/                     # Candidate data (auto-created)
```

## 🐛 Troubleshooting

### "Cannot connect to Ollama"
- Make sure Ollama is running: `ollama serve`
- Check it's accessible: `curl http://localhost:11434`

### "Module not found"
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### "Port 8501 already in use"
```bash
# Use different port
streamlit run app.py --server.port 8502
```

### "OpenAI API key invalid"
- Check `.env` file has correct key
- Key should start with `sk-`
- Regenerate key at: https://platform.openai.com/api-keys

## 🚀 Next Steps

1. **Run the application** - follow setup steps above
2. **Test with different tech stacks** - see how questions adapt
3. **Explore the code** - check `prompts/prompt_templates.py` for prompt engineering
4. **Download conversation** - test the export functionality
5. **Deploy to cloud** - see README.md for Streamlit Cloud deployment

## 📖 More Information

- Full documentation: See [README.md](README.md)
- Prompt engineering details: Check `prompts/prompt_templates.py`
- Architecture: Review `utils/` modules
- Privacy & Data: See Data Privacy section in README.md

## 💡 Tips

- **Best Experience**: Use Ollama with Mistral for fast, free responses
- **Production**: Switch to OpenAI for higher quality responses
- **Customization**: Edit prompts in `prompts/prompt_templates.py`
- **Data Privacy**: All sensitive data is automatically anonymized

---

**Ready to go?** Run: `streamlit run app.py` 🚀
