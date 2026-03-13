import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from models.embeddings import get_embedding_model



def load_pdfs_from_folder(folder_path="data"):
    """Load all PDFs from the data folder"""
    try:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        folder_path = os.path.join(base_dir, folder_path)

        all_docs = []
        pdf_files = [f for f in os.listdir(folder_path) if f.endswith(".pdf")]

        if not pdf_files:
            print(f"No PDFs found in {folder_path}")
            return []
        
        for pdf_file in pdf_files:
            pdf_path = os.path.join(folder_path, pdf_file)
            loader = PyPDFLoader(pdf_path)
            docs = loader.load()
            all_docs.extend(docs)
            print(f"Loaded: {pdf_file} ({len(docs)} pages)")
        
        return all_docs
    except Exception as e:
        raise RuntimeError(f"Failed to load PDFs: {str(e)}")


def split_documents(docs):
    """Split documents into smaller chunks"""
    try:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
        )
        chunks = splitter.split_documents(docs)
        print(f"Total chunks created: {len(chunks)}")
        return chunks
    except Exception as e:
        raise RuntimeError(f"Failed to split documents: {str(e)}")


def create_vector_store(chunks):
    """Create FAISS vector store from chunks"""
    try:
        embedding_model = get_embedding_model()
        vector_store = FAISS.from_documents(chunks, embedding_model)
        print("Vector store created successfully")
        return vector_store
    except Exception as e:
        raise RuntimeError(f"Failed to create vector store: {str(e)}")


def retrieve_relevant_chunks(vector_store, query, k=4):
    """Retrieve top k relevant chunks for a query"""
    try:
        results = vector_store.similarity_search(query, k=k)
        context = "\n\n".join([doc.page_content for doc in results])
        return context
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve chunks: {str(e)}")


def build_rag_pipeline(folder_path="data"):
    """Full pipeline: load → split → embed → store"""
    try:
        docs = load_pdfs_from_folder(folder_path)
        if not docs:
            return None
        chunks = split_documents(docs)
        vector_store = create_vector_store(chunks)
        return vector_store
    except Exception as e:
        raise RuntimeError(f"RAG pipeline failed: {str(e)}")