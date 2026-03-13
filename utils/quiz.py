import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from models.llm import get_chatgroq_model
from langchain_core.messages import HumanMessage, SystemMessage


def generate_quiz(topic, context="", num_questions=5):
    """Generate MCQ quiz on a given topic"""
    try:
        chat_model = get_chatgroq_model()

        system_prompt = """You are a quiz generator for AI/ML topics.
Generate exactly the number of MCQ questions requested.
Always follow this exact format for each question:

Q1. Question here?
A) Option 1
B) Option 2
C) Option 3
D) Option 4
Answer: A

Do not add any extra text or explanation outside this format."""

        if context:
            user_prompt = f"""Generate {num_questions} MCQ questions on the topic: {topic}
            
Use this context from the study material:
{context}

Follow the exact format specified."""
        else:
            user_prompt = f"""Generate {num_questions} MCQ questions on the topic: {topic}
Follow the exact format specified."""

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]

        response = chat_model.invoke(messages)
        return response.content

    except Exception as e:
        return f"Failed to generate quiz: {str(e)}"


def parse_quiz(quiz_text):
    """Parse raw quiz text into structured list of questions"""
    try:
        questions = []
        blocks = quiz_text.strip().split("\n\n")

        for block in blocks:
            lines = [l.strip() for l in block.strip().split("\n") if l.strip()]
            if len(lines) < 6:
                continue

            question = lines[0]
            options = {}
            answer = ""

            for line in lines[1:]:
                if line.startswith("A)"):
                    options["A"] = line[2:].strip()
                elif line.startswith("B)"):
                    options["B"] = line[2:].strip()
                elif line.startswith("C)"):
                    options["C"] = line[2:].strip()
                elif line.startswith("D)"):
                    options["D"] = line[2:].strip()
                elif line.startswith("Answer:"):
                    answer = line.replace("Answer:", "").strip()

            if question and options and answer:
                questions.append({
                    "question": question,
                    "options": options,
                    "answer": answer
                })

        return questions

    except Exception as e:
        return []