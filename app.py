import streamlit as st
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from models.llm import get_chatgroq_model
from utils.rag import build_rag_pipeline, retrieve_relevant_chunks
from utils.search import web_search, should_use_web_search
from utils.quiz import generate_quiz, parse_quiz


@st.cache_resource
def load_vector_store():
    """Load and cache vector store so it only builds once"""
    try:
        import os

        st.write("Current working directory:", os.getcwd())

        if os.path.exists("data"):
            st.write("Files inside data folder:", os.listdir("data"))
        else:
            st.write("❌ Data folder not found")

        vector_store = build_rag_pipeline("data")
        return vector_store

    except Exception as e:
        st.error(f"RAG error: {e}")
        return None──────────────────────
# HELPER: Get chat response
# ─────────────────────────────────────────────
def get_chat_response(chat_model, messages, system_prompt):
    """Get response from the chat model"""
    try:
        formatted_messages = [SystemMessage(content=system_prompt)]
        for msg in messages:
            if msg["role"] == "user":
                formatted_messages.append(HumanMessage(content=msg["content"]))
            else:
                formatted_messages.append(AIMessage(content=msg["content"]))
        response = chat_model.invoke(formatted_messages)
        return response.content
    except Exception as e:
        return f"Error getting response: {str(e)}"


# ─────────────────────────────────────────────
# HELPER: Build system prompt based on mode
# ─────────────────────────────────────────────
def get_system_prompt(mode, context="", web_results=""):
    """Build system prompt based on response mode and context"""
    try:
        base = """You are an expert AI/ML tutor. 
You teach concepts clearly with examples.
You are helpful, patient, and encouraging."""

        if mode == "Concise":
            base += "\nKeep your answers short and to the point. Maximum 3-4 sentences."
        else:
            base += "\nGive detailed, step-by-step explanations with examples."

        if context:
            base += f"\n\nUse this context from study materials to answer:\n{context}"

        if web_results:
            base += f"\n\nAlso use these latest web search results:\n{web_results}"

        return base
    except Exception as e:
        return "You are a helpful AI/ML tutor."


# ─────────────────────────────────────────────
# PAGE: Chat
# ─────────────────────────────────────────────
def chat_page():
    """Main chat interface"""
    st.title("🧠 AI/ML Tutor Bot")
    st.caption("Ask me anything about AI and Machine Learning!")

    chat_model = get_chatgroq_model()

    # ── Sidebar Controls ──
    with st.sidebar:
        st.header("⚙️ Settings")

        # Response Mode
        response_mode = st.radio(
            "Response Mode",
            ["Concise", "Detailed"],
            index=1
        )

        st.divider()

        # Web Search Toggle
        web_search_enabled = st.toggle("🌐 Enable Web Search", value=False)
        if web_search_enabled:
            st.caption("Bot will search the web for latest info")

        st.divider()

        # RAG Toggle
        rag_enabled = st.toggle("📄 Enable Document Q&A (RAG)", value=False)
        if rag_enabled:
            st.caption("Bot will answer from your study PDFs")
            if st.button("📚 Load PDFs from /data folder", use_container_width=True):
                with st.spinner("Loading and indexing PDFs..."):
                    try:
                        vector_store = load_vector_store()
                        if vector_store:
                            st.session_state.vector_store = vector_store
                            st.success("✅ PDFs loaded successfully!")
                        else:
                            st.error("No PDFs found in /data folder")
                    except Exception as e:
                        st.error(f"Failed to load PDFs: {str(e)}")


        st.divider()

        # Quiz Mode
        st.header("📝 Quiz Mode")
        quiz_topic = st.text_input("Enter topic for quiz", placeholder="e.g. Neural Networks")
        num_questions = st.slider("Number of questions", 3, 10, 5)

        if st.button("🎯 Generate Quiz", use_container_width=True):
            if quiz_topic:
                with st.spinner("Generating quiz..."):
                    try:
                        # Use RAG context if available
                        context = ""
                        if "vector_store" in st.session_state:
                            context = retrieve_relevant_chunks(
                                st.session_state.vector_store,
                                quiz_topic
                            )
                        quiz_text = generate_quiz(quiz_topic, context, num_questions)
                        st.session_state.quiz_questions = parse_quiz(quiz_text)
                        st.session_state.quiz_score = 0
                        st.session_state.quiz_index = 0
                        st.session_state.quiz_active = True
                        st.session_state.selected_answer = None
                        st.rerun()
                    except Exception as e:
                        st.error(f"Quiz generation failed: {str(e)}")
            else:
                st.warning("Please enter a topic first!")

        st.divider()

        # Clear Chat
        if st.button("🗑️ Clear Chat History", use_container_width=True):
            st.session_state.messages = []
            st.session_state.quiz_active = False
            st.rerun()

    # ── Quiz UI ──
    if st.session_state.get("quiz_active") and st.session_state.get("quiz_questions"):
        questions = st.session_state.quiz_questions
        idx = st.session_state.quiz_index

        if idx < len(questions):
            q = questions[idx]
            st.subheader(f"📝 Question {idx + 1} of {len(questions)}")
            st.markdown(f"**{q['question']}**")

            selected = st.radio(
                "Choose your answer:",
                list(q["options"].values()),
                key=f"q_{idx}"
            )

            if st.button("Submit Answer", key=f"submit_{idx}"):
                # Find selected letter
                selected_letter = ""
                for letter, text in q["options"].items():
                    if text == selected:
                        selected_letter = letter
                        break

                if selected_letter == q["answer"]:
                    st.success("✅ Correct!")
                    st.session_state.quiz_score += 1
                else:
                    correct_text = q["options"].get(q["answer"], "")
                    st.error(f"❌ Wrong! Correct answer: {q['answer']}) {correct_text}")

                st.session_state.quiz_index += 1

                if st.session_state.quiz_index >= len(questions):
                    st.session_state.quiz_active = False
                    score = st.session_state.quiz_score
                    total = len(questions)
                    st.balloons()
                    st.success(f"🎉 Quiz Complete! Your score: {score}/{total}")
                else:
                    st.rerun()
        return

    # ── Chat UI ──
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask me anything about AI/ML..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    # RAG context
                    context = ""
                    if rag_enabled and "vector_store" in st.session_state:
                        context = retrieve_relevant_chunks(
                            st.session_state.vector_store, prompt
                        )

                    # Web search
                    web_results = ""
                    if web_search_enabled:
                        if should_use_web_search(prompt):
                            web_results = web_search(prompt)

                    # Build system prompt
                    system_prompt = get_system_prompt(
                        response_mode, context, web_results
                    )

                    # Get response
                    response = get_chat_response(
                        chat_model,
                        st.session_state.messages,
                        system_prompt
                    )
                    st.markdown(response)

                except Exception as e:
                    response = f"Error: {str(e)}"
                    st.error(response)

        st.session_state.messages.append({"role": "assistant", "content": response})


# ─────────────────────────────────────────────
# PAGE: Instructions
# ─────────────────────────────────────────────
def instructions_page():
    """Instructions page"""
    st.title("📖 How to Use AI/ML Tutor Bot")
    st.markdown("""
    ## 🚀 Getting Started
    
    ### 1. Chat with the Bot
    - Just type any AI/ML question in the chat box
    - Example: *"Explain gradient descent"*
    
    ### 2. Response Modes
    - **Concise** — Short 3-4 sentence answers
    - **Detailed** — Full step-by-step explanations
    
    ### 3. Document Q&A (RAG)
    - Place your PDF study materials in the `/data` folder
    - Toggle **Enable Document Q&A**
    - Click **Load PDFs** button
    - Now the bot answers from your actual study material!
    
    ### 4. Web Search
    - Toggle **Enable Web Search**
    - Bot auto-detects queries needing latest info
    - Example: *"Latest developments in LLMs 2025"*
    
    ### 5. Quiz Mode
    - Enter any topic in the Quiz section (sidebar)
    - Choose number of questions
    - Click **Generate Quiz**
    - Answer MCQs and get your score!
    
    ## 💡 Example Questions to Try
    - *"Teach me about backpropagation"*
    - *"What is the difference between CNN and RNN?"*
    - *"Explain overfitting with an example"*
    - *"What are transformers in deep learning?"*
    
    ## 📁 Adding Study Materials
    Place these PDFs in your `/data` folder:
    - Deep Learning book (Goodfellow et al.)
    - CS229 Lecture Notes (Andrew Ng)
    """)


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
def main():
    st.set_page_config(
        page_title="AI/ML Tutor Bot",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    with st.sidebar:
        st.title("🧠 AI/ML Tutor Bot")
        st.divider()
        page = st.radio("Navigate", ["Chat", "Instructions"], index=0)

    if page == "Instructions":
        instructions_page()
    if page == "Chat":
        chat_page()


if __name__ == "__main__":
    main()