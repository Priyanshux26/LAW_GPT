import streamlit as st
import numpy as np
import faiss
import os
from sentence_transformers import SentenceTransformer
from groq import Groq
import time

# Page configuration
st.set_page_config(
    page_title="LAW-GPT: Legal Research Assistant",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1E3A8A;
        margin-bottom: 1rem;
    }
    .sub-header {
        text-align: center;
        color: #64748B;
        margin-bottom: 2rem;
    }
    .disclaimer-box {
        background-color: #FEF3C7;
        border-left: 5px solid #F59E0B;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
    }
    .confidence-high {
        color: #059669;
        font-weight: bold;
    }
    .confidence-medium {
        color: #D97706;
        font-weight: bold;
    }
    .confidence-low {
        color: #DC2626;
        font-weight: bold;
    }
    .stButton>button {
        width: 100%;
        background-color: #1E3A8A;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
    }
    .analysis-section {
        background-color: #F8FAFC;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 1px solid #E2E8F0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'analysis_done' not in st.session_state:
    st.session_state.analysis_done = False
if 'response' not in st.session_state:
    st.session_state.response = None
if 'retrieved_chunks' not in st.session_state:
    st.session_state.retrieved_chunks = None

@st.cache_resource
def load_resources():
    """Load FAISS index, metadata, and embedding model"""
    try:
        EMB_DIR = "data/processed/embeddings"
        INDEX_PATH = "data/processed/faiss/sc_judgments.index"

        metadata = np.load(os.path.join(EMB_DIR, "metadata.npy"), allow_pickle=True)
        index = faiss.read_index(INDEX_PATH)
        embed_model = SentenceTransformer("all-MiniLM-L6-v2")

        return metadata, index, embed_model
    except Exception as e:
        st.error(f"Error loading resources: {str(e)}")
        st.info("Please ensure the data files are in the correct directory structure.")
        return None, None, None

def retrieve_chunks(query, metadata, index, embed_model, top_k=3):
    """Retrieve relevant legal chunks using FAISS similarity search"""
    CHUNK_DIR = "data/processed/chunks"

    query_emb = embed_model.encode([query])
    D, I = index.search(query_emb, top_k)

    results = []
    for dist, idx in zip(D[0], I[0]):
        conf = float(1 / (1 + dist))
        fname = metadata[idx]

        try:
            with open(os.path.join(CHUNK_DIR, fname), "r", encoding="utf-8") as f:
                chunk_text = f.read()
            results.append((chunk_text, conf, fname))
        except Exception as e:
            st.warning(f"Could not read chunk {fname}")

    return results

def build_legal_prompt(user_case, retrieved_chunks):
    """Build structured legal prompt with retrieved context"""
    context = ""
    for txt, conf, fname in retrieved_chunks:
        context += f"\n[Confidence={round(conf,2)}]\n{txt[:500]}...\n"

    prompt = f"""
You are a legal research assistant trained on Indian Supreme Court judgments.
You DO NOT provide legal advice. You ONLY summarize patterns.

User Case Description:
{user_case}

Relevant Judgment Extracts:
{context}

Now respond in EXACTLY this structure:

1. Key Legal Issues Raised
2. Possible Applicable Acts / IPC / CrPC / Labour Codes
3. How Supreme Court Has Handled Similar Cases
4. General Strategic Considerations (Non-advisory)
5. Potential Risks / Limitations
6. Documentation Commonly Required in Such Matters
7. Strong Disclaimer (Not Legal Advice)

Start now:
"""
    return prompt

def generate_response(prompt, api_key, model="llama-3.3-70b-versatile", max_tokens=1500, temperature=0.2):
    """Generate response using Groq LLM - FIXED VERSION"""
    try:
        # Initialize Groq client with ONLY api_key parameter
        client = Groq(api_key=api_key)

        # Create chat completion
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a legal research assistant. You DO NOT give legal advice. You only summarize patterns from judgments."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=temperature
        )
        return completion.choices[0].message.content

    except Exception as e:
        error_msg = str(e)
        if "api_key" in error_msg.lower():
            return "❌ Invalid API Key. Please check your Groq API key in the sidebar."
        elif "rate" in error_msg.lower():
            return "❌ Rate limit exceeded. Please wait a moment and try again."
        else:
            return f"❌ Error generating response: {error_msg}"

def main():
    # Header
    st.markdown('<p class="main-header">⚖️ LAW-GPT</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Retrieval-Augmented Legal Analysis System for Indian Law</p>', unsafe_allow_html=True)

    # Disclaimer
    st.markdown("""
    <style>
    .disclaimer-box {
        color: black;
    }
    </style>
    <div class="disclaimer-box">
        <strong>⚠️ IMPORTANT DISCLAIMER:</strong><br>
        This system is designed for <strong>educational and research purposes only</strong>. 
        It does NOT provide legal advice. Always consult a qualified legal professional for 
        legal matters. The information provided is based on pattern analysis of Supreme Court judgments.
    </div>
""", unsafe_allow_html=True)    

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")

        # API Key input
        api_key = st.text_input(
            "Groq API Key",
            type="password",
            help="Enter your Groq API key. Get one from https://console.groq.com"
        )

        # Model selection
        model = st.selectbox(
            "Select Model",
            ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "llama-3.1-70b-versatile"],
            help="Choose the LLM model for analysis"
        )

        # Advanced settings
        with st.expander("🔧 Advanced Settings"):
            num_chunks = st.slider("Number of precedents to retrieve", 1, 10, 3)
            max_tokens = st.slider("Maximum response tokens", 500, 2000, 1500)
            temperature = st.slider("Temperature", 0.0, 1.0, 0.2, 0.1)

        st.divider()

        # About section
        st.header("📚 About")
        st.markdown("""
        **LAW-GPT** uses:
        - 🗂️ **FAISS** for semantic search
        - 🤖 **SentenceTransformer** for embeddings
        - 🧠 **Groq LLM** for synthesis
        - ⚖️ **Supreme Court judgments** (2023-2024)

        **Architecture:**
        RAG-based system combining retrieval 
        and generation for grounded legal analysis.
        """)

        st.divider()

        # Stats
        st.header("📊 System Stats")
        metadata, index, embed_model = load_resources()
        if metadata is not None:
            st.metric("Total Judgment Chunks", len(metadata))
            st.metric("Embedding Dimension", 384)

    # Main content
    col1, col2 = st.columns([2, 1])

    with col1:
        st.header("📝 Case Description")
        user_case = st.text_area(
            "Describe your legal scenario",
            placeholder="Example: I was terminated from my private IT job without any prior notice or reason. I was working as a Senior Software Engineer for 3 years...",
            height=150,
            help="Provide a detailed description of your legal situation"
        )

        analyze_button = st.button("🔍 Analyze Case", type="primary")

    with col2:
        st.header("💡 Quick Examples")
        if st.button("📄 Employment Termination"):
            user_case = "I was terminated from a private job without notice."
            st.session_state.example_case = user_case
        if st.button("⚖️ Contract Breach"):
            user_case = "The vendor failed to deliver goods as per contract terms."
            st.session_state.example_case = user_case
        if st.button("🏢 Property Dispute"):
            user_case = "Boundary dispute with neighbor over property line."
            st.session_state.example_case = user_case

        if 'example_case' in st.session_state:
            user_case = st.session_state.example_case
            del st.session_state.example_case
            st.rerun()

    # Analysis logic
    if analyze_button:
        if not api_key:
            st.error("⚠️ Please enter your Groq API key in the sidebar")
        elif not user_case.strip():
            st.error("⚠️ Please enter a case description")
        else:
            metadata, index, embed_model = load_resources()

            if metadata is None:
                st.error("❌ Failed to load system resources. Please check data files.")
            else:
                with st.spinner("🔍 Analyzing case and retrieving relevant precedents..."):
                    # Retrieve relevant chunks
                    retrieved = retrieve_chunks(user_case, metadata, index, embed_model, top_k=num_chunks)
                    st.session_state.retrieved_chunks = retrieved

                    # Build prompt
                    prompt = build_legal_prompt(user_case, retrieved)

                    # Generate response
                    progress_bar = st.progress(0)
                    for i in range(100):
                        time.sleep(0.01)
                        progress_bar.progress(i + 1)

                    response = generate_response(prompt, api_key, model, max_tokens, temperature)
                    st.session_state.response = response
                    st.session_state.analysis_done = True
                    progress_bar.empty()

    # Display results
    if st.session_state.analysis_done and st.session_state.response:
        st.divider()
        st.header("📋 Legal Analysis Report")

        # Retrieved Precedents
        with st.expander("📚 Retrieved Supreme Court Precedents", expanded=False):
            for i, (chunk, conf, fname) in enumerate(st.session_state.retrieved_chunks, 1):
                conf_class = "confidence-high" if conf > 0.6 else "confidence-medium" if conf > 0.4 else "confidence-low"
                st.markdown(f"**Precedent {i}** | Confidence: <span class='{conf_class}'>{conf:.2%}</span> | Source: `{fname}`", unsafe_allow_html=True)
                st.text_area(f"precedent_{i}", chunk[:500] + "...", height=150, key=f"chunk_{i}", label_visibility="collapsed")
                st.divider()

        # Main Analysis
        st.markdown('<div class="analysis-section">', unsafe_allow_html=True)
        st.markdown(st.session_state.response)
        st.markdown('</div>', unsafe_allow_html=True)

        # Download button
        st.download_button(
            label="📥 Download Analysis Report",
            data=f"CASE DESCRIPTION:\n{user_case}\n\n{'='*50}\n\nANALYSIS:\n{st.session_state.response}",
            file_name="legal_analysis_report.txt",
            mime="text/plain"
        )

        # Reset button
        if st.button("🔄 New Analysis"):
            st.session_state.analysis_done = False
            st.session_state.response = None
            st.session_state.retrieved_chunks = None
            st.rerun()

if __name__ == "__main__":
    main()
