# 🏛️ Indian Legal RAG Chatbot (Supreme Court Case Retrieval)

A Retrieval-Augmented Generation (RAG) chatbot built for **Indian Supreme Court legal research**, summarizing patterns from case law.  
The system does **not provide legal advice** — it retrieves relevant judgments and generates structured legal summaries.

---

## 🚀 Features

- 📂 Upload / load Indian Supreme Court PDFs  
- 🔍 Extract text from judgments  
- ✂️ Sentence-based text chunking  
- 📊 Vector embeddings (Sentence Transformers)  
- ⚡ FAISS similarity search  
- 🤖 LLM response generation (OpenAI API currently)  
- 🏛 Large-context legal prompting template  
- 🎯 Outputs:
  - Key Legal Issues
  - Applicable Acts
  - Judicial Trends
  - General Strategy Notes
  - Risks & Documents
  - Disclaimer

---

## 📁 Project Structure
project/
│
├── data/ # Your Supreme Court PDFs
├── cleaned/ # Extracted text after preprocessing
├── chunks/ # Sentence-level chunks for FAISS
├── vectors/ # FAISS index files
│
├── notebook.ipynb # Main Notebook
├── retriever.py # Chunk + FAISS helper code (optional)
├── README.md
└── requirements.txt

---

## 🔧 Installation

```bash
git clone <repo-url>
cd project
pip install -r requirements.txt
