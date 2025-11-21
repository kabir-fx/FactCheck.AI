import spacy

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Downloading language model...")
    from spacy.cli import download
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

def extract_claims(text):
    """
    Extracts key claims or entities from the input text.
    For this simple implementation, we'll extract noun chunks and named entities
    as a proxy for "claims" to be verified.
    """
    doc = nlp(text)
    claims = []
    
    # Extract sentences as base claims
    for sent in doc.sents:
        claims.append(sent.text.strip())
        
    # Extract named entities for context
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    
    return {
        "claims": claims,
        "entities": entities
    }

if __name__ == "__main__":
    text = "The Indian government has announced free electricity to all farmers starting July 2025."
    print(extract_claims(text))
