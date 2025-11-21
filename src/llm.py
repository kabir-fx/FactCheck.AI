import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

def verify_claim(claim, evidence_list, model_name="gemini-2.0-flash"):
    """
    Verifies a claim against a list of evidence using Google Gemini.
    """
    evidence_text = "\n".join([f"- {e['text']} (Source: {e['source']}, Date: {e['date']})" for e in evidence_list])
    
    prompt = f"""
    You are a fact-checking assistant. Your task is to verify the following claim based ONLY on the provided evidence.
    
    Claim: "{claim}"
    
    Evidence:
    {evidence_text}
    
    Instructions:
    1. Compare the claim with the evidence.
    2. Determine if the claim is "True", "False", or "Unverifiable".
    3. Provide a brief reasoning.
    4. Assign a confidence score (0-100%) based on how well the evidence supports the claim.
    
    Output Format (JSON):
    {{
        "verdict": "True" | "False" | "Unverifiable",
        "reasoning": "Your reasoning here.",
        "confidence": 85
    }}
    """
    
    if api_key:
        try:
            model = genai.GenerativeModel(model_name, generation_config={"response_mime_type": "application/json"})
            response = model.generate_content(prompt)
            return json.loads(response.text)
        except Exception as e:
            return {
                "verdict": "Unverifiable",
                "reasoning": f"Error calling Gemini: {str(e)}"
            }
    else:
        return {
            "verdict": "Unverifiable",
            "reasoning": "Gemini API key not found. Please set the GEMINI_API_KEY environment variable.",
            "confidence": 0
        }

if __name__ == "__main__":
    # Test
    claim = "The Indian government has announced free electricity to all farmers starting July 2025."
    evidence = [
        {"text": "The Indian government has launched the PM Surya Ghar: Muft Bijli Yojana to provide free electricity to 1 crore households.", "source": "PIB", "date": "2024-02-15"},
        {"text": "The Pradhan Mantri Kisan Samman Nidhi (PM-KISAN) scheme provides Rs. 6000 per year to eligible farmer families.", "source": "PM-KISAN Portal", "date": "2019-02-24"}
    ]
    print(verify_claim(claim, evidence))
