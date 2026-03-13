# 🧠 AI/ML Tutor Bot

An intelligent chatbot built with Streamlit that teaches AI/ML concepts, answers questions from study materials, and generates quizzes — powered by Groq LLM.

---

## 🎯 Use Case

Students studying AI/ML often struggle to get quick, clear explanations of complex topics. This bot acts as a **personal tutor** that:
- Explains concepts in simple or detailed ways
- Answers questions directly from your study PDFs
- Tests your knowledge with auto-generated MCQ quizzes
- Searches the web for latest AI/ML news and updates

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 💬 Chat Interface | Conversational AI powered by Groq LLM |
| 📄 RAG (Document Q&A) | Answer questions from uploaded PDF study materials |
| 🌐 Web Search | Real-time search using DuckDuckGo |
| 📝 Quiz Generation | Auto-generate MCQ quizzes on any AI/ML topic |
| 🎯 Response Modes | Switch between Concise and Detailed answers |

---

## 🏗️ Project Structure
```
AI_UseCase/
├── config/
│   └── config.py          ← API keys and settings
├── models/
│   ├── llm.py             ← Groq LLM setup
│   └── embeddings.py      ← HuggingFace embedding model
├── utils/
│   ├── rag.py             ← PDF loading and vector search
│   ├── search.py          ← DuckDuckGo web search
│   └── quiz.py            ← MCQ quiz generation
├── data/
│   └── main_notes.pdf     ← CS229 Lecture Notes (Andrew Ng)
├── app.py                 ← Main Streamlit UI
├── requirements.txt       ← Dependencies
└── .env                   ← API keys (not committed)
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/YOURUSERNAME/aiml-tutor-bot.git
cd aiml-tutor-bot
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up API Keys
Create a `.env` file in the root folder:
```
GROQ_API_KEY=your_groq_api_key_here
```
Get your free Groq API key at: https://console.groq.com/keys

### 4. Run the App
```bash
streamlit run app.py
```

---

## 🚀 How to Use

### 💬 Chat Mode
- Type any AI/ML question in the chat box
- Example: *"Explain gradient descent"*

### 📄 Document Q&A (RAG)
- Toggle **Enable Document Q&A** in sidebar
- Click **Load PDFs from /data folder**
- Ask questions from your study material

### 🌐 Web Search
- Toggle **Enable Web Search** in sidebar
- Ask about latest AI/ML news
- Example: *"Latest LLM models 2025"*

### 📝 Quiz Mode
- Enter a topic in the Quiz section (sidebar)
- Choose number of questions (3-10)
- Click **Generate Quiz** and answer MCQs
- Get your final score!

---

## 📦 Dependencies
```
streamlit
langchain-groq
langchain-community
langchain-core
langchain-text-splitters
sentence-transformers
faiss-cpu
pypdf2
duckduckgo-search
requests
```

---

## 🤖 Models Used

| Model | Provider | Purpose |
|-------|----------|---------|
| `llama-3.3-70b-versatile` | Groq | Chat + Quiz Generation |
| `all-MiniLM-L6-v2` | HuggingFace | PDF Embeddings |

---

## ⚡ Challenges Faced

- **Model Deprecation** — `llama3-8b-8192` was decommissioned, migrated to `llama-3.3-70b-versatile`
- **LangChain Import Changes** — Updated imports to use `langchain_text_splitters`
- **Large PDF Handling** — Used chunk splitting + FAISS for efficient retrieval
- **Web Search API** — Serper required paid signup, switched to free DuckDuckGo

---

## 🌐 Live Demo

[Click here to try the live app](#) ← Replace with your Streamlit Cloud link

---

## 📌 Built For

NeoStats AI Engineer Case Study — *The Chatbot Blueprint: Imagine, Build, Solve*
