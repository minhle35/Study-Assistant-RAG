import uuid
import time
from typing import List, Dict, Any
from pathlib import Path

import openai
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

from ..config import settings
from ..models.responses import SourceDocument, DocumentInfo


class StudyBuddyRAG:
    """RAG engine for StudyBuddy"""

    def __init__(self):
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")

        self.openai_client = openai.AsyncOpenAI(api_key=settings.openai_api_key)
        self.embeddings = OpenAIEmbeddings(api_key=settings.openai_api_key)
        self.llm = ChatOpenAI(
            api_key=settings.openai_api_key,
            model=settings.openai_model,
            temperature=settings.openai_temperature,
        )
        self.vector_store = None
        self.documents_metadata = {}

    async def initialize(self):
        """Initialize the RAG system"""
        print("🚀 Initializing StudyBuddy RAG...")

        # Ensure directories exist
        settings.documents_dir.mkdir(exist_ok=True)
        settings.vector_db_dir.mkdir(exist_ok=True)

        # Initialize ChromaDB
        self.vector_store = Chroma(
            persist_directory=str(settings.vector_db_dir),
            embedding_function=self.embeddings,
        )

        # Process all documents in documents/ folder
        await self._process_documents_directory()
        print("✅ StudyBuddy RAG initialized!")

    async def _process_documents_directory(self):
        """Process all documents in the documents directory"""
        for file_path in settings.documents_dir.iterdir():
            if file_path.suffix.lower() in settings.supported_extensions:
                if str(file_path) not in self.documents_metadata:
                    print(f"📄 Processing: {file_path.name}")
                    await self._process_single_document(file_path)

    async def _process_single_document(self, file_path: Path):
        """Process a single document"""
        try:
            # Load document
            if file_path.suffix.lower() == ".pdf":
                loader = PyPDFLoader(str(file_path))
            else:
                loader = TextLoader(str(file_path), encoding="utf-8")

            documents = loader.load()

            # Split into chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=settings.chunk_size,
                chunk_overlap=settings.chunk_overlap,
                separators=["\n\n", "\n", ". ", " ", ""],
            )
            chunks = text_splitter.split_documents(documents)

            # Add metadata to chunks
            doc_id = str(uuid.uuid4())
            for i, chunk in enumerate(chunks):
                chunk.metadata.update(
                    {
                        "document_id": doc_id,
                        "filename": file_path.name,
                        "chunk_index": i,
                        "subject": "general",
                    }
                )

            # Add to vector store
            self.vector_store.add_documents(chunks)

            # Save metadata
            self.documents_metadata[str(file_path)] = {
                "filename": file_path.name,
                "chunk_count": len(chunks),
                "subject": "general",
            }

            print(f"✅ Processed {file_path.name}: {len(chunks)} chunks")

        except Exception as e:
            print(f"❌ Error processing {file_path.name}: {e}")
            raise

    async def answer_question(
        self, question: str, max_sources: int = None
    ) -> Dict[str, Any]:
        """Answer a question using RAG"""
        start_time = time.time()
        max_sources = max_sources or settings.max_sources

        try:
            # Create retriever
            retriever = self.vector_store.as_retriever(search_kwargs={"k": max_sources})

            # Custom prompt for study assistance
            prompt_template = """You are StudyBuddy, an AI tutor helping students learn.

Based on the study materials provided, answer the question clearly and helpfully.

Guidelines:
- Provide clear, accurate explanations
- Include examples when helpful
- Keep responses focused and educational
- If you don't know something from the materials, say so

Study Materials Context:
{context}

Student Question: {question}

StudyBuddy's Answer:"""

            prompt = PromptTemplate(
                template=prompt_template, input_variables=["context", "question"]
            )

            # Create QA chain
            qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=retriever,
                chain_type_kwargs={"prompt": prompt},
                return_source_documents=True,
            )

            # Get answer
            result = qa_chain({"query": question})

            # Format sources
            sources = []
            if result.get("source_documents"):
                for doc in result["source_documents"]:
                    sources.append(
                        SourceDocument(
                            filename=doc.metadata.get("filename", "unknown"),
                            content_snippet=doc.page_content[:200] + "...",
                            relevance_score=0.8,
                        )
                    )

            # Generate study tips
            study_tips = await self._generate_study_tips(question, result["result"])

            response_time = time.time() - start_time

            return {
                "answer": result["result"],
                "sources": sources,
                "study_tips": study_tips,
                "response_time": response_time,
            }

        except Exception as e:
            print(f"❌ Error answering question: {e}")
            raise

    async def _generate_study_tips(self, question: str, answer: str) -> List[str]:
        """Generate study tips"""
        try:
            response = await self.openai_client.chat.completions.create(
                model=settings.openai_model,
                messages=[
                    {
                        "role": "system",
                        "content": "Generate 2-3 concise study tips based on the question and answer. Each tip should be practical and actionable.",
                    },
                    {
                        "role": "user",
                        "content": f"Question: {question}\nAnswer: {answer}\n\nStudy tips:",
                    },
                ],
                max_tokens=150,
                temperature=0.7,
            )

            tips_text = response.choices[0].message.content
            tips = [
                tip.strip().lstrip("•-123456789. ")
                for tip in tips_text.split("\n")
                if tip.strip()
            ]
            return tips[:3]

        except Exception as e:
            print(f"⚠️ Could not generate study tips: {e}")
            return [
                "Review the material regularly",
                "Practice with examples",
                "Connect concepts together",
            ]

    def get_documents_info(self) -> List[DocumentInfo]:
        """Get information about processed documents"""
        return [
            DocumentInfo(**doc_info) for doc_info in self.documents_metadata.values()
        ]

    async def cleanup(self):
        """Cleanup resources"""
        # Add cleanup logic if needed
        pass
