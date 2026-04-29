import os
from pathlib import Path
from typing import List
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Directory where individual PDF files are located
BASE_DIR = Path(__file__).resolve().parent.parent
PDF_DIR = BASE_DIR / "data" / "pdfs"

def load_and_split_pdfs() -> List:
    """
    Loads all PDF files from the PDF_DIR, splits their content into chunks,
    and returns a list of LangChain document chunks.
    """
    # 1. Error handling: if the folder does not exist, create it.
    if not PDF_DIR.exists():
        print(f"Directory {PDF_DIR} does not exist. Creating it now.")
        PDF_DIR.mkdir(parents=True, exist_ok=True)

    # 2. Get list of PDF files
    pdf_files = list(PDF_DIR.glob("*.pdf"))
    total_found = len(pdf_files)
    print(f"[PDF_LOADER] Found {total_found} PDF(s) in {PDF_DIR}")

    # 3. Handle case where no PDFs are found
    if total_found == 0:
        print("Warning: No PDF files found to load.")
        return []

    # 4. Load PDFs
    documents = []
    loaded_count = 0
    for pdf_path in pdf_files:
        try:
            loader = PyPDFLoader(str(pdf_path))
            docs = loader.load()
            documents.extend(docs)
            loaded_count += 1
        except Exception as e:
            # 5. Skip individual failures
            print(f"Error: Failed to load {pdf_path.name}: {e}")
            continue

    print(f"Success: Successfully loaded {loaded_count}/{total_found} PDF(s)")

    # 6. Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        add_start_index=True
    )
    
    chunks = text_splitter.split_documents(documents)
    print(f"Total chunks created: {len(chunks)}")

    return chunks

# Test block
if __name__ == "__main__":
    print("-" * 30)
    print("Testing PDF Loader and Splitter Pipeline...")
    all_chunks = load_and_split_pdfs()
    
    if all_chunks:
        print("\n--- Preview of First 2 Chunks ---")
        for i, chunk in enumerate(all_chunks[:2]):
            print(f"\n[Chunk {i+1}]")
            # Preview text only
            print(chunk.page_content[:200].replace("\n", " ").strip() + "...")
        print("-" * 30)
    else:
        print("No chunks were produced for testing.")
