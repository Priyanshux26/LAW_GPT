#!/usr/bin/env python3
"""
LAW-GPT Setup Script
Automates the initial setup process
"""

import os
import sys
import subprocess

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def run_command(command, description):
    print(f"\n🔄 {description}...")
    try:
        subprocess.run(command, check=True, shell=True)
        print(f"✅ {description} completed!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        return False

def check_directories():
    """Check and create required directories"""
    print_header("Checking Directory Structure")

    dirs = [
        "data/raw/zips",
        "data/raw/sc_last_2_years",
        "data/processed/texts",
        "data/processed/clean_texts",
        "data/processed/chunks",
        "data/processed/embeddings",
        "data/processed/faiss"
    ]

    for dir_path in dirs:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            print(f"📁 Created: {dir_path}")
        else:
            print(f"✓ Exists: {dir_path}")

def install_dependencies():
    """Install Python dependencies"""
    print_header("Installing Dependencies")

    if not os.path.exists("requirements.txt"):
        print("❌ requirements.txt not found!")
        return False

    return run_command(
        f"{sys.executable} -m pip install -r requirements.txt",
        "Installing packages from requirements.txt"
    )

def download_nltk_data():
    """Download required NLTK data"""
    print_header("Downloading NLTK Data")

    try:
        import nltk
        nltk.download('punkt', quiet=True)
        nltk.download('punkt_tab', quiet=True)
        print("✅ NLTK data downloaded!")
        return True
    except Exception as e:
        print(f"❌ NLTK download failed: {e}")
        return False

def check_data_files():
    """Check if processed data files exist"""
    print_header("Checking Data Files")

    required_files = [
        "data/processed/embeddings/embeddings.npy",
        "data/processed/embeddings/metadata.npy",
        "data/processed/faiss/sc_judgments.index"
    ]

    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✓ Found: {file_path}")
        else:
            print(f"❌ Missing: {file_path}")
            all_exist = False

    if not all_exist:
        print("\n⚠️  WARNING: Some data files are missing!")
        print("   Please run the data processing pipeline in main.ipynb")
        print("   or ensure the processed data files are in the correct location.")

    return all_exist

def create_env_file():
    """Create .env file from template if it doesn't exist"""
    print_header("Setting Up Environment")

    if os.path.exists(".env"):
        print("✓ .env file already exists")
        return True

    if not os.path.exists(".env.example"):
        print("❌ .env.example not found!")
        return False

    try:
        with open(".env.example", "r") as src, open(".env", "w") as dst:
            dst.write(src.read())
        print("✅ Created .env file from template")
        print("⚠️  Please edit .env and add your Groq API key!")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env: {e}")
        return False

def main():
    print("""
    ╔═══════════════════════════════════════════════════════╗
    ║                                                       ║
    ║           ⚖️  LAW-GPT Setup Script  ⚖️               ║
    ║                                                       ║
    ║       Retrieval-Augmented Legal Analysis System      ║
    ║                                                       ║
    ╚═══════════════════════════════════════════════════════╝
    """)

    print("This script will help you set up LAW-GPT on your system.\n")

    # Step 1: Check directories
    check_directories()

    # Step 2: Install dependencies
    if not install_dependencies():
        print("\n⚠️  Installation failed. Please install dependencies manually.")
        sys.exit(1)

    # Step 3: Download NLTK data
    download_nltk_data()

    # Step 4: Check data files
    data_ready = check_data_files()

    # Step 5: Create .env file
    create_env_file()

    # Final summary
    print_header("Setup Summary")

    if data_ready:
        print("""
✅ Setup completed successfully!

🚀 Next Steps:
   1. Edit .env file and add your Groq API key
   2. Run: streamlit run streamlit_app.py
   3. Open browser at http://localhost:8501

📚 Documentation: See README.md for more details
        """)
    else:
        print("""
⚠️  Setup partially completed!

📋 Action Required:
   1. Run the data processing pipeline in main.ipynb to:
      - Download Supreme Court judgments
      - Process and chunk the text
      - Generate embeddings
      - Build FAISS index

   2. After processing, run this setup script again

   3. Edit .env and add your Groq API key

   4. Run: streamlit run streamlit_app.py

📚 See README.md for detailed instructions
        """)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Setup failed with error: {e}")
        sys.exit(1)
