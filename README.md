# LAW-GPT: Retrieval-Augmented Legal Analysis System

<div align="center">

⚖️ **Legal Research Assistant for Indian Supreme Court Judgments**

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.29.0-FF4B4B.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

</div>

## 🎯 Project Overview

LAW-GPT is a **Retrieval-Augmented Generation (RAG)** system designed for legal research and analysis in the Indian legal context. It combines:

- 🔍 **Semantic Search** using FAISS and SentenceTransformers
- 🧠 **LLM-based Synthesis** using Groq (Llama 3.3)
- ⚖️ **Supreme Court Judgments** as authoritative sources

### Key Features

✅ Semantic retrieval of relevant legal precedents  
✅ Structured legal analysis with 7-point framework  
✅ Confidence scoring for retrieved judgments  
✅ Non-advisory, research-focused responses  
✅ Professional web interface with Streamlit  

---

## 🏗️ System Architecture

```
┌─────────────────┐
│  User Query     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Embedding      │ (SentenceTransformer)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  FAISS Search   │ (Vector Similarity)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Retrieved       │
│ Precedents      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Prompt         │
│  Builder        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  LLM            │ (Groq/Llama)
│  Generation     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Structured     │
│  Legal Analysis │
└─────────────────┘
```

---

## 📦 Installation

### Prerequisites

- Python 3.8+
- pip package manager
- Git

### Step 1: Clone Repository

```bash
git clone <your-repo-url>
cd lawGPT
```

### Step 2: Create Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Download NLTK Data

```python
python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab')"
```

### Step 5: Prepare Data Files

Ensure your directory structure looks like this:

```
lawGPT/
├── streamlit_app.py
├── requirements.txt
├── data/
│   ├── raw/
│   │   └── sc_last_2_years/
│   └── processed/
│       ├── chunks/
│       ├── embeddings/
│       │   ├── embeddings.npy
│       │   └── metadata.npy
│       └── faiss/
│           └── sc_judgments.index
```

**Note:** If you haven't processed the data yet, run the cells in `main.ipynb` to:
1. Download Supreme Court judgments
2. Extract and clean text
3. Create chunks
4. Generate embeddings
5. Build FAISS index

---

## 🚀 Running the Application

### Local Deployment

```bash
streamlit run streamlit_app.py
```

The app will open at `http://localhost:8501`

### Get Groq API Key

1. Visit [Groq Console](https://console.groq.com)
2. Sign up for a free account
3. Generate an API key
4. Enter it in the sidebar of the app

---

## 🌐 Cloud Deployment

### Option 1: Streamlit Cloud (Recommended)

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud:**
   - Go to [streamlit.io/cloud](https://streamlit.io/cloud)
   - Connect your GitHub repository
   - Select `streamlit_app.py` as main file
   - Add Groq API key in Secrets management
   - Deploy!

3. **Secrets Configuration:**
   In Streamlit Cloud settings, add:
   ```toml
   GROQ_API_KEY = "your_api_key_here"
   ```

### Option 2: Heroku

```bash
# Install Heroku CLI
heroku login
heroku create lawgpt-app

# Add files
echo "web: streamlit run streamlit_app.py --server.port=$PORT" > Procfile
echo "python-3.11.0" > runtime.txt

# Deploy
git push heroku main
```

### Option 3: AWS EC2

```bash
# Launch EC2 instance (Ubuntu 22.04)
# SSH into instance
sudo apt update
sudo apt install python3-pip
pip3 install -r requirements.txt

# Run with nohup
nohup streamlit run streamlit_app.py --server.port=8501 &
```

### Option 4: Railway.app

1. Go to [railway.app](https://railway.app)
2. Connect GitHub repo
3. Add environment variable: `GROQ_API_KEY`
4. Deploy automatically

---

## 📚 Usage Guide

### Basic Usage

1. **Enter Case Description:**
   - Describe your legal scenario in detail
   - Include relevant facts and context

2. **Configure Settings:**
   - Select LLM model (llama-3.3-70b-versatile recommended)
   - Adjust number of precedents (3-5 optimal)
   - Set temperature (0.2 for consistency)

3. **Analyze:**
   - Click "Analyze Case"
   - Wait for retrieval and generation
   - Review structured analysis

4. **Review Results:**
   - Check confidence scores of retrieved precedents
   - Read the 7-point legal analysis
   - Download report if needed

### Advanced Features

- **Custom Chunk Retrieval:** Adjust `num_chunks` for more/fewer precedents
- **Temperature Control:** Lower for consistent, higher for creative responses
- **Model Selection:** Choose between speed (8B) vs quality (70B)

---

## 📊 Dataset Information

- **Source:** Indian Supreme Court Judgments
- **Years:** 2023-2024
- **Format:** PDF → Text → Chunks (500 words)
- **Total Chunks:** ~27,551
- **Embedding Model:** all-MiniLM-L6-v2 (384 dimensions)

---

## 🔬 Technical Details

### Components

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Frontend** | Streamlit | Web interface |
| **Embeddings** | SentenceTransformer | Semantic encoding |
| **Vector DB** | FAISS | Similarity search |
| **LLM** | Groq (Llama 3.3) | Text generation |
| **Data Processing** | PDFPlumber, NLTK | Text extraction |

### RAG Pipeline

1. **Query Encoding:** User query → Dense vector (384d)
2. **Similarity Search:** FAISS finds top-K similar chunks
3. **Context Building:** Retrieved chunks + query → Structured prompt
4. **Generation:** LLM synthesizes legal analysis
5. **Output:** 7-point structured response

---

## ⚠️ Important Disclaimers

🔴 **This system is NOT a substitute for legal advice**

- For educational and research purposes only
- Always consult qualified legal professionals
- No attorney-client relationship is created
- Not responsible for decisions based on output

---

## 🎓 Academic Context

This project is suitable for:

- ✅ Final year B.Tech/M.Tech projects
- ✅ AI/ML research in legal domain
- ✅ NLP and RAG system demonstrations
- ✅ Legal tech innovation showcases

### Alignment with Outcomes

- **CO1:** Problem analysis in legal AI
- **CO2:** Design of RAG-based solutions
- **CO3:** Implementation using modern tools
- **CO4:** Evaluation through retrieval metrics

---

## 🛠️ Troubleshooting

### Common Issues

**1. FAISS Index Not Found**
```bash
# Ensure you've run the data processing pipeline
# Check data/processed/faiss/sc_judgments.index exists
```

**2. Memory Issues**
```bash
# Use faiss-cpu instead of faiss-gpu if no GPU
# Reduce batch_size in embedding generation
```

**3. API Rate Limits**
```bash
# Groq free tier: 30 requests/minute
# Add retry logic or upgrade plan
```

**4. Streamlit Port Already in Use**
```bash
streamlit run streamlit_app.py --server.port=8502
```

---

## 📈 Future Enhancements

- [ ] Multi-language support (Hindi, regional languages)
- [ ] Citation tracking and case law network
- [ ] Advanced filters (date range, court level)
- [ ] User authentication and history
- [ ] Feedback loop for model improvement
- [ ] Integration with legal databases (SCC, Manupatra)

---

## 👥 Contributors

- **Your Name** - Project Developer
- **Ramaiah Institute of Technology** - Academic Institution

---

## 📄 License

This project is licensed under the MIT License.

---

## 📞 Contact

For questions or support:
- 📧 Email: your.email@example.com
- 🔗 LinkedIn: [Your Profile]
- 🐱 GitHub: [@yourusername]

---

<div align="center">

**⚖️ Built with ❤️ for Legal Research**

[⭐ Star this repo](https://github.com/yourusername/lawgpt) | [🐛 Report Bug](https://github.com/yourusername/lawgpt/issues) | [💡 Request Feature](https://github.com/yourusername/lawgpt/issues)

</div>
