"""StudyBuddy RAG Assistant - AI-powered study companion"""

__version__ = "1.0.0"
__author__ = "Thao Minh Le"

from .main import create_app
from .config import settings

__all__ = ["create_app", "settings"]
