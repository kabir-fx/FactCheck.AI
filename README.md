# FactCheck.AI

A lightweight system that analyzes news posts or social media statements, extracts key claims, and verifies them against a trusted knowledge base using a RAG pipeline.

## Features
- **Claim Extraction**: Uses spaCy to identify key claims and entities.
- **RAG Pipeline**: Retrieves relevant facts from a local knowledge base using SentenceTransformers and ChromaDB.
- **LLM Verification**: Uses Google Gemini to verify claims against retrieved evidence.
- **Streamlit UI**: A simple, user-friendly interface for fact-checking.

## Setup

1. **Clone the repository**
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```
3. **Set up Environment**:
   - Create a `.env` file and add your Gemini API Key:
   - `GEMINI_API_KEY=your_key_here`

## Usage

### Running the App
```bash
streamlit run app.py
```

### How it Works
1. Enter a claim in the text box (e.g., "The Indian government has announced free electricity to all farmers starting July 2025.").
2. Click "Verify Claims".
3. The system will:
   - Extract claims from your text.
   - Search the knowledge base (`data/facts.csv`) for relevant evidence.
   - Use the LLM (Gemini) to compare the claim with the evidence.
   - Display a verdict (True/False/Unverifiable) with reasoning.
   - Store the user's results, if feedback is provided.

## Project Structure
- `app.py`: Main Streamlit application.
- `src/`:
  - `extraction.py`: NLP logic for claim extraction.
  - `retrieval.py`: Vector DB and retrieval logic.
  - `llm.py`: LLM interaction logic.
  - `utils.py`: User feedback storage
- `data/facts.csv`: Trusted knowledge base.
