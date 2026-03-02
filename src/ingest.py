import os
from pathlib import Path
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
#from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_postgres import PGVector
from langchain_core.documents import Document

def ingest_pdf():
    """carrega o PDF, gera embeddings e grava no PGVector."""
    load_dotenv()

    for key in (
        "PDF_PATH",
        "HF_EMBEDDING_MODEL",
        "DATABASE_URL",
        "PG_VECTOR_COLLECTION_NAME",
    ):
        if key not in os.environ:
            raise RuntimeError(f"{key} não está definido em variáveis de ambiente")        
    
    current_dir = Path(__file__).parent.parent
    pdf_path = current_dir / os.getenv("PDF_PATH", "document.pdf")    

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF não encontrado: {pdf_path}")    

    docs = PyPDFLoader(str(pdf_path)).load()

    splits = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=150, 
        add_start_index=False
    ).split_documents(docs)
    if not splits:
        raise SystemExit(0)

    enriched = [
        Document(
            page_content=d.page_content,
            metadata={k: v for k, v in d.metadata.items() if v not in ("", None)},
        )
        for d in splits
    ]

    ids = [f"doc-{i}" for i in range(len(enriched))]

    #embeddings = GoogleGenerativeAIEmbeddings(
    #    model=os.getenv("GOOGLE_EMBEDDING_MODEL", "models/gemini-embedding-001")
    #)
    
    embeddings = HuggingFaceEmbeddings(
        model_name=os.getenv("HF_EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2"),         
        model_kwargs={'device': 'cpu'}
    )

    store = PGVector(        
        embeddings=embeddings,
        collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"),
        connection=os.getenv("DATABASE_URL"),
        use_jsonb=True,
    )

    store.add_documents(documents=enriched, ids=ids)

    print(f"✅ Ingestão concluída! {len(enriched)} chunks adicionados ao banco.")

if __name__ == "__main__":
    ingest_pdf()