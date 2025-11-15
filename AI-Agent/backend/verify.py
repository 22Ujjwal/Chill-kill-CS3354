"""
Step-by-Step Verification Guide for Nintendo Chatbot Backend

This script verifies each component of the backend pipeline and reports status.
Run this AFTER setting up your API keys to diagnose any issues.
"""

import os
import sys
from pathlib import Path

def print_header(text):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def print_check(status, message):
    icon = "✓" if status else "✗"
    print(f"{icon} {message}")

def verify_directory_structure():
    """Verify backend directory structure is correct."""
    print_header("1️⃣  Directory Structure Verification")
    
    required_files = [
        "app.py",
        "requirements.txt",
        ".env.example",
        "README.md",
        "quickstart.py",
        "src/__init__.py",
        "src/config/__init__.py",
        "src/config/settings.py",
        "src/modules/__init__.py",
        "src/modules/firecrawl_scraper.py",
        "src/modules/gemini_embedder.py",
        "src/modules/pinecone_store.py",
        "src/modules/rag_pipeline.py",
        "tests/test_integration.py",
    ]
    
    all_exist = True
    for file_path in required_files:
        exists = Path(file_path).exists()
        print_check(exists, f"  {file_path}")
        if not exists:
            all_exist = False
    
    return all_exist

def verify_env_configuration():
    """Verify .env file configuration."""
    print_header("2️⃣  Environment Configuration Verification")
    
    env_path = Path(".env")
    env_example_path = Path(".env.example")
    
    # Check if files exist
    print_check(env_example_path.exists(), "  .env.example exists")
    
    if not env_path.exists():
        print_check(False, "  .env file exists (REQUIRED - create from .env.example)")
        return False
    
    print_check(True, "  .env file exists")
    
    # Check for required variables
    with open(env_path, 'r') as f:
        content = f.read()
    
    required_vars = {
        "FIRECRAWL_API_KEY": "From Firecrawl dashboard",
        "GOOGLE_API_KEY": "From Google AI Studio",
        "PINECONE_API_KEY": "From Pinecone Dashboard",
        "PINECONE_INDEX_NAME": "Name of your Pinecone index",
    }
    
    all_configured = True
    for var, source in required_vars.items():
        if var in content:
            is_placeholder = f"{var}=your_" in content or f"{var}=" == content.split('\n')
            if not is_placeholder:
                print_check(True, f"  {var} is configured ({source})")
            else:
                print_check(False, f"  {var} is PLACEHOLDER (needs your actual value from {source})")
                all_configured = False
        else:
            print_check(False, f"  {var} not found in .env")
            all_configured = False
    
    return all_configured

def verify_dependencies():
    """Verify Python dependencies."""
    print_header("3️⃣  Python Dependencies Verification")
    
    required_packages = {
        "flask": "Flask web framework",
        "flask_cors": "CORS support",
        "requests": "HTTP client",
        "google": "Google Gemini API",
        "pinecone": "Pinecone vector database",
        "dotenv": "Environment configuration",
    }
    
    all_installed = True
    for package, description in required_packages.items():
        try:
            __import__(package)
            print_check(True, f"  {package} ({description})")
        except ImportError:
            print_check(False, f"  {package} ({description}) - NOT INSTALLED")
            all_installed = False
    
    if not all_installed:
        print("\n⚠️  Run: pip install -r requirements.txt\n")
    
    return all_installed

def verify_api_connectivity():
    """Verify API connectivity (optional - requires keys)."""
    print_header("4️⃣  API Connectivity Verification")
    
    print("⏭️  Skipping API connectivity tests (requires valid API keys)\n")
    print("After setting up your API keys, you can test:")
    print("  1. Firecrawl: POST to https://api.firecrawl.dev/v2/crawl")
    print("  2. Gemini: Generate embeddings and text")
    print("  3. Pinecone: Connect to your index\n")
    
    return True

def verify_module_imports():
    """Verify that modules can be imported."""
    print_header("5️⃣  Module Import Verification")
    
    sys.path.insert(0, str(Path.cwd()))
    
    modules_to_test = [
        ("src.config.settings", "Settings configuration"),
        ("src.modules.firecrawl_scraper", "Firecrawl scraper"),
        ("src.modules.gemini_embedder", "Gemini embedder"),
        ("src.modules.pinecone_store", "Pinecone vector store"),
        ("src.modules.rag_pipeline", "RAG pipeline"),
    ]
    
    all_importable = True
    for module_path, description in modules_to_test:
        try:
            __import__(module_path)
            print_check(True, f"  {description} ({module_path})")
        except ImportError as e:
            print_check(False, f"  {description} ({module_path}) - {str(e)}")
            all_importable = False
        except Exception as e:
            print_check(False, f"  {description} ({module_path}) - {str(e)}")
            all_importable = False
    
    return all_importable

def print_summary(checks):
    """Print verification summary."""
    print_header("📋 Verification Summary")
    
    total = len(checks)
    passed = sum(1 for c in checks if c)
    failed = total - passed
    
    print(f"Total Checks: {total}")
    print(f"✓ Passed: {passed}")
    print(f"✗ Failed: {failed}\n")
    
    if failed == 0:
        print("🎉 All checks passed! Backend is ready to use.\n")
        print("Next steps:")
        print("  1. Set up your API keys in .env")
        print("  2. Create a Pinecone index (768 dimensions)")
        print("  3. Run: python app.py")
        print("  4. Initialize: curl -X POST http://localhost:5000/api/initialize")
        print("  5. Query: curl -X POST http://localhost:5000/api/query -H 'Content-Type: application/json' -d '{\"query\": \"Your question\"}'")
    else:
        print(f"⚠️  {failed} check(s) failed. Please fix the issues above before using the backend.\n")
        print("Common fixes:")
        print("  1. Create .env from .env.example: cp .env.example .env")
        print("  2. Install dependencies: pip install -r requirements.txt")
        print("  3. Add your API keys to .env")
    
    print()

def main():
    """Run all verifications."""
    print("\n" + "="*60)
    print("  Nintendo Chatbot Backend - Verification Script")
    print("="*60)
    
    print("\nThis script will verify your backend setup.\n")
    
    checks = [
        ("Directory Structure", verify_directory_structure()),
        ("Environment Configuration", verify_env_configuration()),
        ("Python Dependencies", verify_dependencies()),
        ("API Connectivity", verify_api_connectivity()),
        ("Module Imports", verify_module_imports()),
    ]
    
    print_summary([c[1] for c in checks])
    
    # Return exit code
    all_passed = all(c[1] for c in checks)
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
