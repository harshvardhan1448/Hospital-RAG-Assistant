"""
Test script for the Hospital RAG Assistant API
Run this after starting the FastAPI backend
"""

import requests
import json
from typing import Optional
import time

API_BASE_URL = "http://localhost:8000"

# ANSI color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    BOLD = '\033[1m'
    END = '\033[0m'


def print_header(text: str):
    """Print a formatted header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}")
    print(f"{text:^60}")
    print(f"{'='*60}{Colors.END}\n")


def print_success(text: str):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")


def print_error(text: str):
    """Print error message"""
    print(f"{Colors.RED}✗ {text}{Colors.END}")


def print_info(text: str):
    """Print info message"""
    print(f"{Colors.YELLOW}ℹ {text}{Colors.END}")


def test_health_check():
    """Test API health"""
    print_header("Testing API Health")
    try:
        response = requests.get(f"{API_BASE_URL}/")
        if response.status_code == 200:
            data = response.json()
            print_success(f"API is running: {data['message']}")
            return True
        else:
            print_error(f"API returned status {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Failed to connect to API: {str(e)}")
        print_info(f"Make sure FastAPI backend is running at {API_BASE_URL}")
        return False


def test_upload_pdf(pdf_path: str):
    """Test PDF upload"""
    print_header("Testing PDF Upload")
    try:
        with open(pdf_path, "rb") as f:
            files = {"file": f}
            response = requests.post(f"{API_BASE_URL}/upload", files=files, timeout=120)
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Document uploaded: {data['filename']}")
            print_info(f"Pages: {data['pages']}, Chunks: {data['chunks']}")
            return True
        else:
            print_error(f"Upload failed: {response.status_code}")
            print(response.json())
            return False
    except FileNotFoundError:
        print_error(f"PDF file not found: {pdf_path}")
        return False
    except Exception as e:
        print_error(f"Error uploading document: {str(e)}")
        return False


def test_query(question: str, test_name: Optional[str] = None):
    """Test query endpoint"""
    display_name = test_name or question[:40]
    print(f"\n{Colors.BOLD}Testing Query:{Colors.END} {display_name}")
    
    try:
        payload = {"question": question}
        response = requests.post(f"{API_BASE_URL}/query", json=payload, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            if data["status"] == "success":
                print_success(f"Query processed successfully")
                print(f"\n{Colors.BOLD}Question:{Colors.END} {question}")
                print(f"\n{Colors.BOLD}Answer:{Colors.END}\n{data['answer']}")
                if data.get("sources"):
                    print(f"\n{Colors.BOLD}Sources:{Colors.END} {', '.join(data['sources'])}")
                print(f"{Colors.YELLOW}Chunks retrieved: {data['chunks_found']}{Colors.END}")
                return True
            else:
                print_error(f"Query failed: {data.get('answer', 'Unknown error')}")
                return False
        else:
            print_error(f"API returned status {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error executing query: {str(e)}")
        return False


def test_get_documents():
    """Test retrieving documents"""
    print_header("Testing Get Documents")
    try:
        response = requests.get(f"{API_BASE_URL}/documents")
        if response.status_code == 200:
            documents = response.json()
            if documents:
                print_success(f"Retrieved {len(documents)} document chunks")
                # Group by filename
                files = {}
                for doc in documents:
                    filename = doc.get("filename", "Unknown")
                    files[filename] = files.get(filename, 0) + 1
                
                for filename, count in files.items():
                    print_info(f"{filename}: {count} chunks")
                return True
            else:
                print_info("No documents stored yet")
                return True
        else:
            print_error(f"API returned status {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error retrieving documents: {str(e)}")
        return False


def run_test_suite(pdf_path: Optional[str] = None):
    """Run complete test suite"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}")
    print("""
    ╔═════════════════════════════════════════════════════════╗
    ║     Hospital RAG Assistant - API Test Suite            ║
    ╚═════════════════════════════════════════════════════════╝
    """)
    print(f"{Colors.END}")
    
    results = {}
    
    # Test 1: Health Check
    results["health_check"] = test_health_check()
    if not results["health_check"]:
        print_error("Cannot continue without API connection")
        return results
    
    # Test 2: Get Documents
    results["get_documents"] = test_get_documents()
    
    # Test 3: Upload PDF (if provided)
    if pdf_path:
        results["upload_pdf"] = test_upload_pdf(pdf_path)
        time.sleep(2)  # Wait for processing
    else:
        print_header("PDF Upload Test Skipped")
        print_info("Provide a PDF file path to test upload: python test_api.py <pdf_path>")
    
    # Test 4: Test Queries
    print_header("Testing Query Functionality")
    
    test_queries = [
        ("What are OPD timings?", "OPD Timings"),
        ("Who is the cardiologist?", "Cardiologist"),
        ("What is the cost of MRI?", "MRI Cost"),
        ("Can I cancel appointment within 24 hours?", "Cancellation Policy"),
        ("What is ICU cost per day?", "ICU Cost"),
        ("Emergency number?", "Emergency Contact"),
    ]
    
    query_results = []
    for question, name in test_queries:
        result = test_query(question, name)
        query_results.append(result)
        time.sleep(1)  # Rate limiting
    
    results["queries"] = all(query_results) if query_results else False
    
    # Summary
    print_header("Test Summary")
    print(f"Health Check: {Colors.GREEN if results.get('health_check') else Colors.RED}{'PASS' if results.get('health_check') else 'FAIL'}{Colors.END}")
    print(f"Get Documents: {Colors.GREEN if results.get('get_documents') else Colors.RED}{'PASS' if results.get('get_documents') else 'FAIL'}{Colors.END}")
    if pdf_path:
        print(f"Upload PDF: {Colors.GREEN if results.get('upload_pdf') else Colors.RED}{'PASS' if results.get('upload_pdf') else 'FAIL'}{Colors.END}")
    print(f"Query Tests: {Colors.GREEN if results.get('queries') else Colors.RED}{'PASS' if results.get('queries') else 'FAIL'}{Colors.END}")
    
    print("\n")


if __name__ == "__main__":
    import sys
    
    pdf_path = None
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
    
    run_test_suite(pdf_path)
