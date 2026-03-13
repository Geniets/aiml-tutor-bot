import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from langchain_community.embeddings import HuggingFaceEmbeddings


def get_embedding_model():
    """Initialize and return the embedding model"""
    try:
        embedding_model = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2",
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True}
        )
        return embedding_model
    except Exception as e:
        raise RuntimeError(f"Failed to initialize embedding model: {str(e)}")