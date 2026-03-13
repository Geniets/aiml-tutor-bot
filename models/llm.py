import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from langchain_groq import ChatGroq
import streamlit as st

GROQ_API_KEY = st.secrets["GROQ_API_KEY"]


def get_chatgroq_model():
    """Initialize and return the Groq chat model"""
    try:
        # Initialize the Groq chat model with the API key
        groq_model = ChatGroq(
            api_key=GROQ_API_KEY,
            model="llama-3.3-70b-versatile",
        )
        return groq_model   
    except Exception as e:
        raise RuntimeError(f"Failed to initialize Groq model: {str(e)}")