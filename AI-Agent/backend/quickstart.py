#!/usr/bin/env python3
"""
Quick Start Script for Nintendo Chatbot Backend
Run this to set up and initialize the backend for the first time.
"""

import os
import sys
import subprocess
from pathlib import Path

def print_section(title):
    """Print a formatted section header."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def check_dependencies():
    """Check if Python dependencies are installed."""
    print("📦 Checking dependencies...")
    
    try:
        import flask
        import requests
        import google
        import pinecone
        print("✓ All required packages are installed\n")
        return True
    except ImportError as e:
        print(f"✗ Missing package: {e}")
        print("\nRun: pip install -r requirements.txt\n")
        return False

def check_env_file():
    """Check if .env file exists and is configured."""
    print("🔑 Checking environment configuration...")
    
    env_path = Path(".env")
    env_example_path = Path(".env.example")
    
    if not env_path.exists():
        if env_example_path.exists():
            print("Creating .env from .env.example...")
            with open(env_example_path, 'r') as f:
                content = f.read()
            with open(env_path, 'w') as f:
                f.write(content)
            print("✓ Created .env file")
            print("\n⚠️  Please update .env with your API keys:")
            print("   - GOOGLE_API_KEY")
            print("   - PINECONE_API_KEY")
            return False
        else:
            print("✗ .env file not found and no .env.example available\n")
            return False
    
    # Check required variables
    with open(env_path, 'r') as f:
        content = f.read()
    
    required = ["GOOGLE_API_KEY", "PINECONE_API_KEY"]
    missing = []
    
    for var in required:
        if f"{var}=your_" in content or f"{var}=" not in content:
            missing.append(var)
    
    if missing:
        print(f"✗ Missing/unconfigured variables: {', '.join(missing)}\n")
        print("Please update .env with your API keys\n")
        return False
    
    print("✓ Environment configured correctly\n")
    return True

def install_dependencies():
    """Install Python dependencies."""
    print("📥 Installing Python dependencies...")
    
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
            check=True,
            capture_output=True
        )
        print("✓ Dependencies installed\n")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install dependencies: {e}\n")
        return False

def start_server():
    """Start the Flask development server."""
    print_section("🚀 Starting Backend Server")
    
    try:
        print("Starting on http://localhost:5000")
        print("\nAPI Endpoints:")
        print("  POST   /api/initialize     - Initialize backend & scrape website")
        print("  POST   /api/query          - Query the chatbot")
        print("  GET    /api/history        - Get conversation history")
        print("  POST   /api/reset          - Reset conversation")
        print("  GET    /api/health         - Health check")
        print("  GET    /api/stats          - Vector store stats")
        print("\nPress Ctrl+C to stop the server\n")
        
        subprocess.run([sys.executable, "app.py"], check=True)
    except KeyboardInterrupt:
        print("\n\nServer stopped.")
    except Exception as e:
        print(f"✗ Error starting server: {e}")
        return False
    
    return True

def main():
    """Main setup workflow."""
    print_section("Nintendo Chatbot Backend - Quick Start")
    
    # Check current directory
    if not Path("app.py").exists():
        print("✗ app.py not found. Please run this script from the backend directory.\n")
        sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        print("Installing dependencies...")
        if not install_dependencies():
            sys.exit(1)
    
    # Check environment configuration
    if not check_env_file():
        print("⚠️  Please configure .env file and run this script again.\n")
        sys.exit(1)
    
    # Offer to start server
    print_section("Setup Complete")
    print("✓ Backend is ready to use!\n")
    
    response = input("Start the backend server now? (y/n): ").strip().lower()
    if response == 'y':
        if not start_server():
            sys.exit(1)
    else:
        print("\nTo start the server later, run:")
        print("  python app.py\n")
        print("Then in another terminal, initialize the backend:")
        print("  curl -X POST http://localhost:5000/api/initialize\n")

if __name__ == "__main__":
    main()
