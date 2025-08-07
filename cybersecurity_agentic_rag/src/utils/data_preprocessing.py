import logging
import re
import pandas as pd
from langchain_core.documents import Document

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def clean_text(text: str) -> str:
    """
    Cleans text by removing special characters, extra whitespace, and converting to lowercase.

    Args:
        text (str): The input string.

    Returns:
        str: The cleaned string.
    """
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space
    text = re.sub(r'[^\w\s\.\-]', '', text) # Remove special characters except for . and -
    return text.strip()

def load_documents_from_csv(filepath: str, content_column: str) -> list[Document]:
    """
    Loads data from a CSV file and converts it into a list of LangChain Document objects.

    Args:
        filepath (str): The path to the CSV file.
        content_column (str): The name of the column containing the text content.

    Returns:
        list[Document]: A list of Document objects.
    """
    logging.info(f"Loading documents from {filepath}")
    try:
        df = pd.read_csv(filepath)
        if content_column not in df.columns:
            raise ValueError(f"Content column '{content_column}' not found in the CSV file.")

        documents = [Document(page_content=row[content_column]) for index, row in df.iterrows()]
        logging.info(f"Successfully loaded {len(documents)} documents.")
        return documents
    except FileNotFoundError:
        logging.error(f"File not found: {filepath}")
        return []
    except Exception as e:
        logging.error(f"An error occurred while loading from CSV: {e}")
        return []

def extract_features_from_log(log_entry: str) -> dict:
    """
    Extracts structured features from a raw log entry using regex.
    This is a simplified example. A real system would use more robust parsing.

    Args:
        log_entry (str): A single log line.

    Returns:
        dict: A dictionary of extracted features.
    """
    # Example log format: "TIMESTAMP [LEVEL] IP_ADDRESS - Message"
    pattern = r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z) \[(\w+)\] ([\d\.]+) - (.*)"
    match = re.match(pattern, log_entry)

    if match:
        return {
            "timestamp": match.group(1),
            "level": match.group(2),
            "ip_address": match.group(3),
            "message": match.group(4)
        }
    return None

if __name__ == '__main__':
    # --- Example Usage ---

    # 1. Text Cleaning
    raw_text = "  This is a sample text!! It has extra spaces & special characters.  "
    cleaned_text = clean_text(raw_text)
    print(f"Raw text: '{raw_text}'")
    print(f"Cleaned text: '{cleaned_text}'")

    # 2. Feature Extraction from a log
    log_line = "2025-08-07T12:30:00Z [WARNING] 192.168.1.101 - Failed login attempt."
    features = extract_features_from_log(log_line)
    print(f"\nLog line: '{log_line}'")
    print(f"Extracted features: {features}")

    # 3. Loading from CSV (demonstration with a dummy file)
    dummy_csv_data = {
        'report_id': [1, 2],
        'threat_description': [
            'Incident involving CVE-2023-1234.',
            'Suspicious activity detected from a known malicious IP.'
        ]
    }
    dummy_df = pd.DataFrame(dummy_csv_data)
    dummy_csv_path = "dummy_reports.csv"
    dummy_df.to_csv(dummy_csv_path, index=False)

    print(f"\nLoading documents from '{dummy_csv_path}'...")
    docs = load_documents_from_csv(dummy_csv_path, content_column='threat_description')
    for i, doc in enumerate(docs):
        print(f"  Document {i+1}: '{doc.page_content}'")

    # Clean up the dummy file
    import os
    os.remove(dummy_csv_path)
