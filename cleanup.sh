#!/bin/bash
# LAW-GPT Project Cleanup Script

echo "╔═══════════════════════════════════════════════════════╗"
echo "║                                                       ║"
echo "║         🧹 LAW-GPT Project Cleanup 🧹               ║"
echo "║                                                       ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo ""

echo "🗑️  Removing unnecessary files..."

# Remove duplicate/old requirements files
rm -f "requirements (1).txt"
rm -f requirements_fixed.txt
rm -f requirements_minimal.txt
rm -f requirements_working.txt

# Remove fix scripts (no longer needed)
rm -f fix_dependencies.py
rm -f ultimate_fix.sh
rm -f definitive_fix.sh
rm -f fix_groq_package.sh
rm -f install_alternative.sh
rm -f install_smart.py
rm -f setup_env.sh

# Remove old gitignore (should be .gitignore)
rm -f gitignore

# Remove test outputs
rm -f legal_analysis_report.txt

# Keep only essential docs
rm -f QUICKSTART.md
rm -f TROUBLESHOOTING.md
rm -f VERSION_FIX.md
rm -f FIX_PIP_ERROR.md
rm -f GROQ_SETUP.md
rm -f GROQ_FIX_GUIDE.md
rm -f ONE_COMMAND_FIX.txt
rm -f QUICK_START_ENV.md
rm -f FINAL_SETUP_SUMMARY.md

echo "✅ Cleanup complete!"
echo ""
echo "📁 Remaining structure:"
ls -la

echo ""
echo "📦 Essential files kept:"
echo "   ✅ streamlit_app.py"
echo "   ✅ requirements.txt (will be regenerated)"
echo "   ✅ .env (your config)"
echo "   ✅ .env.example"
echo "   ✅ .gitignore"
echo "   ✅ README.md"
echo "   ✅ ENV_SETUP_GUIDE.md"
echo "   ✅ main.ipynb"
echo "   ✅ test_env.py"
echo "   ✅ data/"
echo "   ✅ .streamlit/"
