# AI/ML Tutor Bot

## Overview
AI/ML Tutor Bot is an intelligent web application built with Streamlit and LangChain. It acts as an expert tutor for Artificial Intelligence and Machine Learning concepts. The application provides clear explanations, interactive quizzes, document-based question answering (RAG), and integrated web search to ensure the latest information is used.

## Features
- Interactive Chat Interface: Ask questions about AI and ML and get concise or detailed explanations based on a selected response mode.
- Document Q&A (RAG): Placed study materials (PDFs) into the `data/` folder, and the bot will answer questions based strictly on your own documents.
- Web Search: Automatically searches the web for queries that require recent context or the latest information.
- Quiz Mode: Generate custom multiple-choice quizzes on any AI/ML topic to test your knowledge directly within the application.

## Project Structure
- `app.py`: The main Streamlit application script containing the frontend UI, session state management, and core logic.
- `config/`: Contains application configuration settings.
- `data/`: Directory where you should place your PDF study materials for the Document Q&A (RAG) feature.
- `models/`: Contains model initialization code for Large Language Models (`llm.py`) and vector embeddings (`embeddings.py`).
- `utils/`: Contains utility modules for various features:
  - `rag.py`: The Retrieval-Augmented Generation pipeline handling PDF ingestion, vector store creation, and chunk retrieval (using FAISS).
  - `search.py`: Web search integration using DuckDuckGo.
  - `quiz.py`: Quiz generation and structured parsing logic.
- `requirements.txt`: List of Python dependencies.

## Prerequisites
- Python 3.8 or higher.
- Necessary API keys for the configured models (e.g., Groq, OpenAI, or Google GenAI depending on your setup).

## Installation

1. Navigate to the project directory in your terminal.

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure your environment variables. Ensure your `.env` file is present in the root directory and contains your necessary API keys (for example, `GROQ_API_KEY`, `OPENAI_API_KEY`, etc.):
   ```env
   GROQ_API_KEY=your_api_key_here
   ```

## Usage

1. Start the Streamlit application:
   ```bash
   streamlit run app.py
   ```

2. Open your web browser and navigate to the local URL provided in the terminal (usually http://localhost:8501).

3. To use the Document Q&A feature, place your PDF files into the `data/` folder. Then, toggle "Enable Document Q&A" in the sidebar and click the "Load PDFs" button.

4. To take a quiz, use the Quiz section in the sidebar. Enter a topic, select the number of questions, and click "Generate Quiz".

## Note
Please ensure you do not commit your `.env` file or API keys to any public version control repository.
