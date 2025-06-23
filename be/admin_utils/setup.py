import os
import asyncio

from create_database import create_database
from populate_data import populate_data
from download_data import download_pdfs
from gen_policy_docs import generate_faq, generate_returns_policy, generate_shipping_policy
from ingest_pdfs import main as ingest_pdfs_main

PDF_DIR = os.path.join(os.path.dirname(__file__), "..", "pdfs")


def ensure_pdfs_dir():
    if not os.path.exists(PDF_DIR):
        os.makedirs(PDF_DIR)
        print(f"Created directory: '{PDF_DIR}'")


def main():
    print("=== Step 1: Creating database ===")
    create_database()
    print("\n=== Step 2: Populating database with mock data ===")
    populate_data()
    print("\n=== Step 3: Downloading PDF manuals and generating policy docs ===")
    ensure_pdfs_dir()
    download_pdfs()
    print("Generating policy documents...")
    generate_returns_policy(PDF_DIR)
    generate_shipping_policy(PDF_DIR)
    generate_faq(PDF_DIR)
    print("All policy documents generated successfully.")
    print("\n=== Step 4: Ingesting PDFs into vector database ===")
    asyncio.run(ingest_pdfs_main())
    print("\nSetup complete.")


if __name__ == "__main__":
    main()
