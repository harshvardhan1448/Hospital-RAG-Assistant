import io
import re
import PyPDF2
from typing import List, Tuple
from langchain_text_splitters import RecursiveCharacterTextSplitter
from embeddings import embed_texts   # <-- use shared module
import config


async def extract_text_from_pdf(pdf_file) -> Tuple[str, int]:
    try:
        file_content = await pdf_file.read()
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
        text = ""
        num_pages = len(pdf_reader.pages)
        for page_num, page in enumerate(pdf_reader.pages):
            page_text = page.extract_text() or ""
            text += f"\n[PAGE {page_num + 1}]\n{page_text}\n"
        return text.strip(), num_pages
    except Exception as e:
        raise Exception(f"Error extracting PDF: {str(e)}")


def chunk_text(text: str) -> List[str]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP,
        separators=["\n\n", "\n", " ", ""]
    )
    return splitter.split_text(text)


def prepare_documents_for_storage(text: str, filename: str) -> List[dict]:
    chunks = chunk_text(text)
    embeddings = embed_texts(chunks)   # <-- shared

    documents = []
    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        page_num = "1"
        matches = list(re.finditer(r'\[PAGE (\d+)\]', chunk))
        if matches:
            page_num = matches[-1].group(1)

        documents.append({
            "filename": filename,
            "chunk_index": i,
            "content": chunk,
            "embedding": embedding,
            "page": page_num,
            "metadata": {"source": filename, "chunk_id": i, "page": page_num}
        })

    return documents


async def ingest_document(pdf_file) -> dict:
    try:
        text, page_count = await extract_text_from_pdf(pdf_file)
        if not text:
            raise Exception("No text extracted from PDF")
        documents = prepare_documents_for_storage(text, pdf_file.filename)
        return {
            "status": "success",
            "filename": pdf_file.filename,
            "pages": page_count,
            "chunks": len(documents),
            "documents": documents
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}