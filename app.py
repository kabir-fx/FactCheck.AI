import streamlit as st
import pandas as pd
from src.extraction import extract_claims
from src.retrieval import index_facts, retrieve_facts
from src.llm import verify_claim
from src.utils import save_feedback
import os

# Page Config
st.set_page_config(
    page_title="FactCheck.AI",
    page_icon="assets/icon.png",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
    }
    .verdict-true {
        color: #4CAF50;
        font-weight: bold;
        font-size: 1.2rem;
    }
    .verdict-false {
        color: #F44336;
        font-weight: bold;
        font-size: 1.2rem;
    }
    .verdict-unverifiable {
        color: #FFC107;
        font-weight: bold;
        font-size: 1.2rem;
    }
    .confidence-high {
        color: #4CAF50;
        font-weight: bold;
    }
    .confidence-medium {
        color: #FFC107;
        font-weight: bold;
    }
    .confidence-low {
        color: #F44336;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# Title and Header
col_logo, col_title = st.columns([1, 10])
with col_logo:
    st.image("assets/icon.png", width=80)
with col_title:
    st.title("FactCheck.AI")
    st.markdown("### AI-Powered Fact Checking System")
    st.markdown("Enter a news snippet or claim below to verify it against our trusted knowledge base.")

# Initialize Knowledge Base
if 'indexed' not in st.session_state:
    with st.spinner("Initializing Knowledge Base..."):
        index_facts()
        st.session_state['indexed'] = True
    st.success("Knowledge Base Ready!")

# Input Section
input_text = st.text_area("Enter Text to Verify:", height=150, placeholder="e.g., The Indian government has announced free electricity to all farmers starting July 2025.")

if st.button("Verify Claims"):
    if not input_text:
        st.warning("Please enter some text to verify.")
    else:
        with st.spinner("Analyzing..."):
            # 1. Extract Claims
            extraction_result = extract_claims(input_text)
            st.session_state['results'] = extraction_result
            st.session_state['verified_claims'] = []
            
            # Process claims and store in session state
            for claim in extraction_result['claims']:
                evidence = retrieve_facts(claim)
                verification = verify_claim(claim, evidence)
                st.session_state['verified_claims'].append({
                    'claim': claim,
                    'evidence': evidence,
                    'verification': verification
                })

# Display Results from Session State
if 'results' in st.session_state:
    st.subheader("🔍 Analysis Results")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("#### Extracted Claims & Verification")
        claims = st.session_state['results']['claims']
        
        if not claims:
            st.info("No specific claims detected. Try rephrasing.")
        
        # Use the stored verified claims
        if 'verified_claims' in st.session_state:
            for i, item in enumerate(st.session_state['verified_claims']):
                claim = item['claim']
                evidence = item['evidence']
                verification = item['verification']
                
                with st.expander(f"Claim {i+1}: {claim}", expanded=True):
                    verdict = verification.get("verdict", "Unverifiable")
                    reasoning = verification.get("reasoning", "No reasoning provided.")
                    confidence = verification.get("confidence", 0)
                    
                    # Display Verdict
                    if verdict.lower() == "true":
                        st.markdown(f"<p class='verdict-true'>✅ Verdict: True</p>", unsafe_allow_html=True)
                    elif verdict.lower() == "false":
                        st.markdown(f"<p class='verdict-false'>❌ Verdict: False</p>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<p class='verdict-unverifiable'>🤷 Verdict: Unverifiable</p>", unsafe_allow_html=True)
                    
                    # Display Confidence
                    conf_class = "confidence-low"
                    if confidence > 80:
                        conf_class = "confidence-high"
                    elif confidence > 50:
                        conf_class = "confidence-medium"
                    
                    st.markdown(f"**Confidence:** <span class='{conf_class}'>{confidence}%</span>", unsafe_allow_html=True)
                    st.markdown(f"**Reasoning:** {reasoning}")
                    
                    st.markdown("**Evidence Used:**")
                    for e in evidence:
                        st.markdown(f"- {e['text']} *(Source: {e['source']}, {e['date']})*")
                    
                    # Feedback Toggle
                    st.markdown("---")
                    st.write("Was this helpful?")
                    c1, c2 = st.columns([1, 10])
                    with c1:
                        if st.button("👍", key=f"up_{i}"):
                            save_feedback(claim, verdict, reasoning, "positive")
                            st.toast("Thanks for your feedback! (Saved)")
                    with c2:
                        if st.button("👎", key=f"down_{i}"):
                            save_feedback(claim, verdict, reasoning, "negative")
                            st.toast("Thanks for your feedback! (Saved)")

    with col2:
        st.markdown("#### Detected Entities")
        entities = st.session_state['results']['entities']
        if entities:
            df_entities = pd.DataFrame(entities, columns=["Entity", "Label"])
            st.dataframe(df_entities, hide_index=True)
        else:
            st.info("No named entities detected.")

# Sidebar
with st.sidebar:
    st.header("About")
    st.info(
        """
        This system uses a RAG (Retrieval-Augmented Generation) pipeline to verify claims.
        
        **Pipeline:**
        1. **Extraction:** spaCy
        2. **Retrieval:** SentenceTransformers + ChromaDB
        3. **Verification:** Google Gemini
        """
    )
