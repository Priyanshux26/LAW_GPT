#!/usr/bin/env python3
"""
Test if .env file is properly configured
"""

from dotenv import load_dotenv
import os

print("╔═══════════════════════════════════════════════════════╗")
print("║                                                       ║")
print("║         🧪 LAW-GPT Environment Test 🧪              ║")
print("║                                                       ║")
print("╚═══════════════════════════════════════════════════════╝")
print()

# Check if .env exists
if os.path.exists('.env'):
    print("✅ .env file found")
else:
    print("❌ .env file not found")
    print("   Run: cp .env.example .env")
    exit(1)

# Load environment variables
load_dotenv()

# Check API key
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    print("❌ GROQ_API_KEY not found in .env")
    print("   Edit .env and add your API key")
    exit(1)
elif api_key == "your_groq_api_key_here":
    print("⚠️  GROQ_API_KEY is still the placeholder")
    print("   Edit .env and replace with your actual API key")
    print("   Get one from: https://console.groq.com")
    exit(1)
elif not api_key.startswith("gsk_"):
    print("⚠️  GROQ_API_KEY doesn't look valid (should start with 'gsk_')")
    print(f"   Current value starts with: {api_key[:4]}...")
    exit(1)
else:
    print(f"✅ GROQ_API_KEY configured: {api_key[:10]}...{api_key[-4:]}")

# Test Groq import
try:
    from groq import Groq
    print("✅ Groq package installed")
except ImportError:
    print("❌ Groq package not installed")
    print("   Run: pip install groq")
    exit(1)

# Test Groq client creation
try:
    client = Groq(api_key=api_key)
    print("✅ Groq client created successfully")
except Exception as e:
    print(f"❌ Failed to create Groq client: {e}")
    exit(1)

print()
print("╔═══════════════════════════════════════════════════════╗")
print("║                                                       ║")
print("║          ✨ Environment Setup Complete! ✨          ║")
print("║                                                       ║")
print("║         Run: streamlit run streamlit_app.py         ║")
print("║                                                       ║")
print("╚═══════════════════════════════════════════════════════╝")
