import csv
import os
from datetime import datetime

FEEDBACK_FILE = "data/feedback.csv"

def save_feedback(claim, verdict, reasoning, feedback_type):
    """
    Saves user feedback to a CSV file.
    
    Args:
        claim (str): The claim being verified.
        verdict (str): The verdict provided by the system.
        reasoning (str): The reasoning provided by the system.
        feedback_type (str): 'positive' (👍) or 'negative' (👎).
    """
    file_exists = os.path.isfile(FEEDBACK_FILE)
    
    with open(FEEDBACK_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Write header if file is new
        if not file_exists:
            writer.writerow(["Timestamp", "Claim", "Verdict", "Reasoning", "Feedback"])
            
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            claim,
            verdict,
            reasoning,
            feedback_type
        ])
